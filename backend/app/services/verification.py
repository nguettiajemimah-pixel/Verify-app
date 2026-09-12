"""Verification service for deterministic product comparison."""

import json
import re
from typing import Optional

from app.models.product import Product
from app.schemas.enums import VerificationStatus
from app.schemas.verification import VerificationResult


class VerificationService:
    """Service for deterministic product verification against registry."""

    def __init__(self, registry_version: str = "demo-v1"):
        self.registry_version = registry_version

    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison by removing extra whitespace and standardizing case."""
        if not text:
            return ""
        # Remove extra whitespace and convert to uppercase for comparison
        return " ".join(text.strip().upper().split())

    def normalize_identifier(self, identifier: str) -> str:
        """Normalize registration numbers and similar identifiers."""
        if not identifier:
            return ""
        # Remove common separators and whitespace, keep case-sensitive for IDs
        return re.sub(r"[\s\-_\.]", "", identifier.strip())

    def compare_field(
        self,
        submitted: Optional[str],
        registry: Optional[str],
        field_name: str,
        is_identifier: bool = False,
    ) -> tuple[bool, str]:
        """
        Compare a single field between submitted and registry data.
        
        Returns (matches, normalized_registry_value)
        """
        if not submitted and not registry:
            return True, ""
        
        if not submitted or not registry:
            return False, registry or ""

        if is_identifier:
            # Strict comparison for identifiers
            return self.normalize_identifier(submitted) == self.normalize_identifier(registry), registry
        else:
            # Flexible comparison for text fields
            return self.normalize_text(submitted) == self.normalize_text(registry), registry

    def verify_product(
        self,
        registration_number: str,
        product_name: Optional[str] = None,
        manufacturer: Optional[str] = None,
    ) -> VerificationResult:
        """
        Verify product information against registry.
        
        Returns a VerificationResult with status, matched/mismatched fields, and explanation.
        """
        from app.database.connection import SessionLocal
        
        db = SessionLocal()
        try:
            # Look up product by registration number
            product = db.query(Product).filter(
                Product.registration_number == self.normalize_identifier(registration_number)
            ).first()
            
            if not product:
                return VerificationResult(
                    status=VerificationStatus.NOT_FOUND,
                    product_id=None,
                    registry_version=self.registry_version,
                    matched_fields=[],
                    mismatched_fields=[],
                    unavailable_fields=["registration_number", "product_name", "manufacturer"],
                    explanation=(
                        "No corresponding record was found in the available registry dataset. "
                        "This does not prove that the product is fake. Further verification through "
                        "the relevant authority may be appropriate."
                    ),
                )
            
            # Compare fields
            matched_fields = []
            mismatched_fields = []
            unavailable_fields = []
            
            # Compare registration number
            reg_matches, _ = self.compare_field(
                registration_number, product.registration_number, "registration_number", is_identifier=True
            )
            if reg_matches:
                matched_fields.append("registration_number")
            else:
                mismatched_fields.append("registration_number")
            
            # Compare product name if provided
            if product_name:
                name_matches, _ = self.compare_field(
                    product_name, product.name, "product_name", is_identifier=False
                )
                if name_matches:
                    matched_fields.append("product_name")
                else:
                    mismatched_fields.append("product_name")
            else:
                unavailable_fields.append("product_name")
            
            # Compare manufacturer if provided
            if manufacturer:
                mfg_matches, _ = self.compare_field(
                    manufacturer, product.manufacturer, "manufacturer", is_identifier=False
                )
                if mfg_matches:
                    matched_fields.append("manufacturer")
                else:
                    mismatched_fields.append("manufacturer")
            else:
                unavailable_fields.append("manufacturer")
            
            # Determine overall status
            if not mismatched_fields and not unavailable_fields:
                status = VerificationStatus.MATCH
                explanation = "The information you entered matches the available registry record for所有 checked fields."
            elif mismatched_fields:
                status = VerificationStatus.DOES_NOT_MATCH
                explanation = self._build_mismatch_explanation(mismatched_fields)
            else:
                status = VerificationStatus.PARTIAL_MATCH
                explanation = f"Some information matches the registry record, but {', '.join(unavailable_fields)} were not provided for comparison."
            
            return VerificationResult(
                status=status,
                product_id=product.id,
                registry_version=self.registry_version,
                matched_fields=matched_fields,
                mismatched_fields=mismatched_fields,
                unavailable_fields=unavailable_fields,
                explanation=explanation,
            )
        finally:
            db.close()

    def _build_mismatch_explanation(self, mismatched_fields: list[str]) -> str:
        """Build a human-readable explanation for mismatched fields."""
        field_descriptions = {
            "registration_number": "Registration number",
            "product_name": "Product name",
            "manufacturer": "Manufacturer information",
        }
        
        if len(mismatched_fields) == 1:
            field = mismatched_fields[0]
            return f"{field_descriptions.get(field, field)} differs from the available registry record."
        else:
            described = [field_descriptions.get(f, f) for f in mismatched_fields]
            return f"{', '.join(described[:-1])} and {described[-1]} differ from the available registry record."


# Singleton instance
verification_service = VerificationService()

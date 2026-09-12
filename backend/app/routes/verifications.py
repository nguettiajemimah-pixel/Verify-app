"""Verification routes for VERIFY GH."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.verification import Verification
from app.schemas.verification import VerificationCreate, VerificationRead
from app.services.verification import verification_service

router = APIRouter(prefix="/verifications", tags=["verifications"])


@router.post("/", response_model=VerificationRead)
def create_verification(
    verification_data: VerificationCreate,
    db: Session = Depends(get_db),
):
    """Create a new verification by comparing product info with registry."""
    # Perform verification
    result = verification_service.verify_product(
        registration_number=verification_data.registration_number,
        product_name=verification_data.product_name,
        manufacturer=verification_data.manufacturer,
    )
    
    # Store verification record
    user_input_dict = verification_data.model_dump()
    import json
    user_input_json = json.dumps(user_input_dict)
    
    db_verification = Verification(
        user_input=user_input_json,
        product_id=result.product_id,
        match_status=result.status,
        matched_fields=",".join(result.matched_fields),
        mismatched_fields=",".join(result.mismatched_fields),
        unavailable_fields=",".join(result.unavailable_fields),
        registry_version=result.registry_version,
        explanation=result.explanation,
    )
    
    db.add(db_verification)
    db.commit()
    db.refresh(db_verification)
    
    return db_verification


@router.get("/{verification_id}", response_model=VerificationRead)
def get_verification(verification_id: int, db: Session = Depends(get_db)):
    """Get a verification by ID."""
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    return verification

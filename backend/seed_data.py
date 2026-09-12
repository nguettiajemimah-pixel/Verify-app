"""Seed demo data for VERIFY GH."""

import hashlib

from app.database.connection import Base, engine, SessionLocal
from app.models.audit import AuditLog
from app.models.product import Product
from app.models.user import User
from app.schemas.enums import UserRole


def simple_hash(password: str) -> str:
    """Simple hash for demo purposes (not production-safe)."""
    return hashlib.sha256(password.encode()).hexdigest()


def seed_products():
    """Seed demo registry products."""
    db = SessionLocal()
    
    # Check if products already exist
    existing = db.query(Product).first()
    if existing:
        print("Products already seeded. Skipping.")
        return
    
    demo_products = [
        # Demo 1 - MATCH scenario
        Product(
            name="Demo Product Alpha",
            category="Medicine",
            registration_number="GH-DEMO-001",
            manufacturer="Demo Pharma Ltd",
            status="Active",
            source_version="demo-v1",
        ),
        # Additional demo products for search
        Product(
            name="Ghana Pain Relief",
            category="Medicine",
            registration_number="GH-FDA-2024-001",
            manufacturer="Accra Pharmaceuticals Ltd",
            status="Active",
            source_version="demo-v1",
        ),
        Product(
            name="Malaria Prevention Tablets",
            category="Medicine",
            registration_number="GH-FDA-2024-002",
            manufacturer="Kumasi Drug Works",
            status="Active",
            source_version="demo-v1",
        ),
        Product(
            name="Skin Care Cream",
            category="Cosmetics",
            registration_number="GH-FDA-2024-003",
            manufacturer="Tamale Beauty Products",
            status="Active",
            source_version="demo-v1",
        ),
        Product(
            name="Vitamin C Supplement",
            category="Supplements",
            registration_number="GH-FDA-2024-004",
            manufacturer="Cape Coast Nutritionals",
            status="Active",
            source_version="demo-v1",
        ),
        # Product for PARTIAL MATCH scenario
        Product(
            name="Antibiotic Capsules",
            category="Medicine",
            registration_number="GH-DEMO-002",
            manufacturer="Health Ghana Corp",
            status="Active",
            source_version="demo-v1",
        ),
    ]
    
    db.add_all(demo_products)
    db.commit()
    print(f"Seeded {len(demo_products)} demo products")


def seed_users():
    """Seed demo users including regulator account."""
    db = SessionLocal()
    
    # Check if users already exist
    existing = db.query(User).first()
    if existing:
        print("Users already seeded. Skipping.")
        return
    
    # Demo regulator account
    regulator = User(
        email="regulator@verifygh.demo",
        password_hash=simple_hash("demo123"),
        role=UserRole.REGULATOR,
        account_status="active",
    )
    
    # Demo admin account
    admin = User(
        email="admin@verifygh.demo",
        password_hash=simple_hash("demo123"),
        role=UserRole.ADMIN,
        account_status="active",
    )
    
    db.add_all([regulator, admin])
    db.commit()
    print("Seeded demo regulator and admin accounts")
    print("Regulator credentials: regulator@verifygh.demo / demo123")
    print("Admin credentials: admin@verifygh.demo / demo123")


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created")


def main():
    """Main seeding function."""
    print("Seeding VERIFY GH demo data...")
    create_tables()
    seed_products()
    seed_users()
    print("Seeding complete!")


if __name__ == "__main__":
    main()

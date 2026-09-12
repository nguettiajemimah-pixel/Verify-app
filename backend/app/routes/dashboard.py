"""Dashboard routes for VERIFY GH."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth.dependencies import require_regulator_or_admin
from app.database.connection import get_db
from app.models.report import Report
from app.models.verification import Verification
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_regulator_or_admin),
):
    """Get dashboard summary statistics."""
    total_reports = db.query(Report).count()
    new_reports = db.query(Report).filter(Report.status == "SUBMITTED").count()
    under_review = db.query(Report).filter(Report.status == "UNDER_REVIEW").count()
    resolved = db.query(Report).filter(Report.status == "RESOLVED").count()
    
    # Verification statistics
    match_count = db.query(Verification).filter(Verification.match_status == "MATCH").count()
    partial_match_count = db.query(Verification).filter(Verification.match_status == "PARTIAL_MATCH").count()
    does_not_match_count = db.query(Verification).filter(Verification.match_status == "DOES_NOT_MATCH").count()
    not_found_count = db.query(Verification).filter(Verification.match_status == "NOT_FOUND").count()
    
    return {
        "reports": {
            "total": total_reports,
            "new": new_reports,
            "under_review": under_review,
            "resolved": resolved,
        },
        "verifications": {
            "match": match_count,
            "partial_match": partial_match_count,
            "does_not_match": does_not_match_count,
            "not_found": not_found_count,
        },
    }


@router.get("/recent-reports")
def get_recent_reports(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_regulator_or_admin),
):
    """Get recent reports for dashboard."""
    reports = db.query(Report).order_by(Report.created_at.desc()).limit(limit).all()
    
    return [
        {
            "report_id": r.report_id,
            "product_name": r.product_name,
            "issue_type": r.issue_type,
            "location": r.location,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
        }
        for r in reports
    ]

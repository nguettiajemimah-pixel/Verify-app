"""Report routes for VERIFY GH."""

from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_regulator_or_admin
from app.database.connection import get_db
from app.models.report import Report
from app.models.user import User
from app.schemas.report import ReportCreate, ReportRead, ReportStatusUpdate

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=ReportRead)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
):
    """Create a new inconsistency report."""
    # Generate report ID
    report_id = f"VG-{uuid.uuid4().hex[:8].upper()}"
    
    db_report = Report(
        report_id=report_id,
        **report_data.model_dump(),
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report


@router.get("/", response_model=List[ReportRead])
def list_reports(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_regulator_or_admin),
):
    """List all reports (regulator/admin only)."""
    query = db.query(Report)
    
    if status:
        query = query.filter(Report.status == status)
    
    reports = query.order_by(Report.created_at.desc()).limit(100).all()
    return reports


@router.get("/{report_id}", response_model=ReportRead)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_regulator_or_admin),
):
    """Get a report by ID (regulator/admin only)."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.patch("/{report_id}", response_model=ReportRead)
def update_report_status(
    report_id: str,
    update_data: ReportStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_regulator_or_admin),
):
    """Update report status and add internal note (regulator/admin only)."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.status = update_data.status
    
    if update_data.internal_note:
        import json
        notes = json.loads(report.internal_notes) if report.internal_notes else []
        notes.append({
            "author": current_user.email,
            "note": update_data.internal_note,
            "timestamp": report.updated_at.isoformat(),
        })
        report.internal_notes = json.dumps(notes)
    
    db.commit()
    db.refresh(report)
    
    return report

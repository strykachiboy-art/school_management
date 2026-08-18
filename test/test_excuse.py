from datetime import date
import pytest

from App.enums.attendance import AttendanceStatus
from App.enums.excuse import ExcuseStatus
from App.models.attendance import Attendance
from App.models.excuses import Excuse


def test_approve_excuse_workflow(client, db_session, sample_absent_attendance, sample_teacher):
    """
    Test full approval flow:
    Absent -> Submit Excuse (Pending) -> Approve -> Status becomes EXCUSED and APPROVED
    """
    # 1. Create Excuse
    create_res = client.post("/excuses", json={
        "attendance_id": sample_absent_attendance.id,
        "reason": "Severe fever and Doctor note attached."
    })
    assert create_res.status_code == 201
    excuse_id = create_res.json["id"]
    assert create_res.json["status"] == "pending"

    # 2. Approve Excuse
    approve_res = client.post(f"/excuses/{excuse_id}/approve", json={
        "reviewer_id": sample_teacher.id
    })
    assert approve_res.status_code == 200
    assert approve_res.json["status"] == "approved"
    assert approve_res.json["reviewed_by"] == sample_teacher.id

    # 3. Verify Attendance status changed automatically
    attendance = db_session.get(Attendance, sample_absent_attendance.id)
    assert attendance.status == AttendanceStatus.EXCUSED


def test_reject_excuse_workflow(client, db_session, sample_absent_attendance, sample_teacher):
    """
    Test full rejection flow:
    Absent -> Submit Excuse -> Reject -> Attendance remains ABSENT
    """
    excuse = Excuse(
        attendance_id=sample_absent_attendance.id,
        reason="Went to family event",
        status=ExcuseStatus.PENDING
    )
    db_session.add(excuse)
    db_session.commit()

    reject_res = client.post(f"/excuses/{excuse.id}/reject", json={
        "reviewer_id": sample_teacher.id
    })
    assert reject_res.status_code == 200
    assert reject_res.json["status"] == "rejected"

    attendance = db_session.get(Attendance, sample_absent_attendance.id)
    assert attendance.status == AttendanceStatus.ABSENT


def test_cannot_create_excuse_for_present_student(client, sample_present_attendance):
    """
    Cannot submit an excuse for a student who was marked PRESENT.
    """
    res = client.post("/excuses", json={
        "attendance_id": sample_present_attendance.id,
        "reason": "Invalid excuse"
    })
    assert res.status_code == 400
    assert "ABSENT" in res.json["description"]


def test_cannot_update_approved_excuse(client, db_session, sample_absent_attendance, sample_teacher):
    """
    Cannot modify reason after excuse has been approved.
    """
    excuse = Excuse(
        attendance_id=sample_absent_attendance.id,
        reason="Initial reason",
        status=ExcuseStatus.APPROVED,
        reviewed_by=sample_teacher.id
    )
    db_session.add(excuse)
    db_session.commit()

    res = client.patch(f"/excuses/{excuse.id}", json={
        "reason": "Updated reason attempt"
    })
    assert res.status_code == 400
    assert "Only PENDING excuses can be modified" in res.json["description"]
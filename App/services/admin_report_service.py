from App.services.admin_report_service import get_admin_report


def test_get_admin_report_counts(app, teacher, student, subject, classroom):
    report = get_admin_report()

    assert report["total_students"] == 1
    assert report["total_teachers"] == 1
    assert report["total_subjects"] == 1
    assert report["total_classrooms"] == 1


def test_get_admin_report_empty(app):
    report = get_admin_report()

    assert report["total_students"] == 0
    assert report["total_teachers"] == 0
    assert report["total_subjects"] == 0
    assert report["total_classrooms"] == 0
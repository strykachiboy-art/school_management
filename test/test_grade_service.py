import pytest
from App.models.result import Result
from App.services.grade_service import (
    calculate_total,
    calculate_average,
    calculate_grade,
    calculate_remark,
    calculate_student_grade,
)


# ======================= calculate_total =======================
def test_calculate_total_sums_marks():
    results = [Result(marks_obtained=80), Result(marks_obtained=65), Result(marks_obtained=90)]
    assert calculate_total(results) == 235


def test_calculate_total_empty_list_is_zero():
    assert calculate_total([]) == 0


# ======================= calculate_average =======================
def test_calculate_average_normal():
    assert calculate_average(200, 4) == 50


def test_calculate_average_zero_subjects_returns_zero():
    # guards against ZeroDivisionError
    assert calculate_average(0, 0) == 0


# ======================= calculate_grade boundaries =======================
@pytest.mark.parametrize("average,expected_grade", [
    (100, "A"),
    (70, "A"),
    (69.99, "B"),
    (60, "B"),
    (59.99, "C"),
    (50, "C"),
    (49.99, "D"),
    (45, "D"),
    (44.99, "E"),
    (40, "E"),
    (39.99, "F"),
    (0, "F"),
])
def test_calculate_grade_boundaries(average, expected_grade):
    assert calculate_grade(average) == expected_grade


# ======================= calculate_remark =======================
@pytest.mark.parametrize("grade,expected_remark", [
    ("A", "Excelent"),
    ("B", "Very Good"),
    ("C", "Good"),
    ("D", "Pass"),
    ("E", "Weak Pass"),
    ("F", "Fail"),
])
def test_calculate_remark_known_grades(grade, expected_remark):
    assert calculate_remark(grade) == expected_remark


def test_calculate_remark_unknown_grade_falls_back():
    assert calculate_remark("Z") == "unknown"


# ======================= calculate_student_grade (integration) =======================
def test_calculate_student_grade_typical_case():
    results = [Result(marks_obtained=80), Result(marks_obtained=60), Result(marks_obtained=70)]

    payload = calculate_student_grade(results)

    assert payload["total"] == 210
    assert payload["average"] == 70
    assert payload["grade"] == "A"
    assert payload["remark"] == "Excelent"


def test_calculate_student_grade_no_results_defaults_to_fail():
    payload = calculate_student_grade([])

    assert payload["total"] == 0
    assert payload["average"] == 0
    assert payload["grade"] == "F"
    assert payload["remark"] == "Fail"
from App.models.result import Result

# =========================== calculate Total =================================
def calculate_total(results):
    return sum(result.marks_obtained for result in results)



# =========================== calculate Average =================================
def calculate_average(total, number_of_subjects):
    if number_of_subjects == 0:
        return 0
    
    return total / number_of_subjects



# ============================= calculate grade ==================================
GRADE_SCALE = (
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (45, "D"),
    (40, "E"),
    (0, "F")
)

def calculate_grade(average):
    for minimum, grade in GRADE_SCALE:
        if average >= minimum:
            return grade
    
    return "F"


# ====================== Grade Remarks ===========================
GRADE_REMARK = {
    "A": "Excelent",
    "B": "Very Good",
    "C": "Good",
    "D": "Pass",
    "E": "Weak Pass",
    "F": "Fail"
}


def calculate_remark(grade):
    return GRADE_REMARK.get(grade, "unknown")


# ===================== calculate student_grade =======================
def calculate_student_grade(results):
    total = calculate_total(results)
    number_of_subjects = len(results)
    
    average = calculate_average(total, number_of_subjects)
    grade = calculate_grade(average)
    remark = calculate_remark(grade)
    
    return {
        "total" : total,
        "average" : average,
        "grade" : grade,
        "remark" : remark
    }
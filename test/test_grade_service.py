def test_calculate_total(app, make_result, make_exam, student):
    from App.services.grade_service import calculate_total
    
    with app.app_context():
        # Create two different exams for the student's results
        exam1 = make_exam("1")
        exam2 = make_exam("2")
        
        r1 = make_result(student_obj=student, exam_obj=exam1, marks=75.0)
        r2 = make_result(student_obj=student, exam_obj=exam2, marks=85.0)
        
        # Test your total calculation logic here...

def test_calculate_average():
    from App.services.grade_service import calculate_average
    
    assert calculate_average(160.0, 2) == 80.0
    assert calculate_average(0.0, 0) == 0.0  # Division by zero safety check

def test_calculate_grade():
    from App.services.grade_service import calculate_grade
    
    assert calculate_grade(75.0) == "A"
    assert calculate_grade(62.0) == "B"
    assert calculate_grade(55.0) == "C"
    assert calculate_grade(45.0) == "D"
    assert calculate_grade(30.0) == "F"

def test_calculate_remark():
    from App.services.grade_service import calculate_remark
    
    assert calculate_remark("A") == "Excelent"
    assert calculate_remark("B") == "Very Good"
    assert calculate_remark("C") == "Good"
    assert calculate_remark("D") == "Pass"
    assert calculate_remark("F") == "Fail"
    assert calculate_remark("UNKNOWN") == "unknown"

def test_calculate_student_grade_service(app, make_result, make_exam, student):
    from App.services.grade_service import calculate_student_grade
    
    with app.app_context():
        exam1 = make_exam("1")
        exam2 = make_exam("2")
        
        r1 = make_result(student_obj=student, exam_obj=exam1, marks=70.0)
        r2 = make_result(student_obj=student, exam_obj=exam2, marks=80.0)
        

def test_get_student_grade_route(client, admin_headers, make_result, make_exam, student):
    with client.application.app_context():
        exam1 = make_exam("1")
        exam2 = make_exam("2")
        
        make_result(student_obj=student, exam_obj=exam1, marks=80.0)
        make_result(student_obj=student, exam_obj=exam2, marks=60.0)
        
        # Rest of your assertions...
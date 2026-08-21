from App.models import *
from App.models.classroom import Classroom
from App.models.student import Student
from App.models.teacher import Teacher
from App.models.user import User
from App.models.subject import Subject
from App.models.association import student_subjects, teacher_subjects, classroom_subjects
from App.models.exam import Exam
from App.models.result import Result
from App.models.password_reset_token import PasswordResetToken
from App.models.academic_session import AcademicSession
from App.models.term import Term
from App.models.attendance import Attendance
from App.models.promotion_history import PromotionHistory
from App.models.excuses import Excuse
from App.models.password_reset_token import PasswordResetToken
from App.models.timetable import Timetable
from App.models.parent_guardian import ParentGuardian, ParentGuardianStudent
from App.models.teacher_permission import TeacherPermission
from App.models.notification import Notification
from App.models.audit_log import AuditLog

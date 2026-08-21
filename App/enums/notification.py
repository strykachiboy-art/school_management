from enum import Enum

class NotificationType(str, Enum):
    GENERAL = "general"
    ATTENDANCE = "attendance"
    EXCUSE = "excuse"
    RESULT = "result"
    EXAM = "exam"
    TIMETABLE = "timetable"
    PROMOTION = "promotion"
    SCHOOL_FEES = "school_fess"
    SYSTEM = "system"
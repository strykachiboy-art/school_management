from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class ClassroomForm(FlaskForm):
    name = StringField("Classroom Name", validators=[DataRequired(), Length(max=100)])
    capacity = IntegerField("Capacity", validators=[Optional()])
    location = StringField("Location", validators=[Optional(), Length(max=100)])
    teacher_id = IntegerField("Teacher ID", validators=[Optional()])
    submit = SubmitField("Create Classroom")
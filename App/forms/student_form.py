from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class StudentForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    admission_number = StringField("Admission Number", validators=[Optional(), Length(max=50)])
    classroom_id = IntegerField("Classroom ID", validators=[Optional()])
    password = PasswordField("Password", validators=[Optional(), Length(min=6, max=255)])
    submit = SubmitField("Create Student")
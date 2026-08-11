from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class TeacherForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    subject = StringField("Subject", validators=[Optional(), Length(max=100)])
    password = PasswordField("Password", validators=[Optional(), Length(min=6, max=255)])
    submit = SubmitField("Create Teacher")
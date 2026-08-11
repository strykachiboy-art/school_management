from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class SubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=100)])
    code = StringField("Code", validators=[DataRequired(), Length(max=20)])
    description = StringField("Description", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Create Subject")
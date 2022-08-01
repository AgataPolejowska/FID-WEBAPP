from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    nickname = StringField("Enter the nickname you want to be identified with", validators=[DataRequired(), Length(min=2, max=15)], render_kw={"placeholder": "Nickname"})
    register = SubmitField("REGISTER")

class VerificationForm(FlaskForm):
    nickname = StringField("Enter the nickname you are identified as", validators=[DataRequired(), Length(min=2, max=15)], render_kw={"placeholder": "Nickname"})
    verify = SubmitField("VERIFY")
    
class IdentificationForm(FlaskForm):
    identify = SubmitField("UPLOAD AND IDENTIFY")



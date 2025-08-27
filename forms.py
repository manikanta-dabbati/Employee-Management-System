from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class EmployeeForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=120)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField('Phone', validators=[Optional(), Length(max=40)])
    position = StringField('Position', validators=[Optional(), Length(max=150)])
    department = StringField('Department', validators=[Optional(), Length(max=120)])
    salary = FloatField('Salary', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import Company
from datetime import date

class RegistrationForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    industry = SelectField('Industry', choices=[
        ('', 'Select Industry'),
        ('agriculture', 'Agriculture'),
        ('manufacturing', 'Manufacturing'),
        ('services', 'Services'),
        ('technology', 'Technology'),
        ('energy', 'Energy'),
        ('transportation', 'Transportation'),
        ('retail', 'Retail'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('other', 'Other')
    ])
    size = SelectField('Company Size', choices=[
        ('', 'Select Size'),
        ('small', 'Small (1-50 employees)'),
        ('medium', 'Medium (51-500 employees)'),
        ('large', 'Large (500+ employees)')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ActivityForm(FlaskForm):
    title = StringField('Activity Title', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('energy', 'Energy Consumption'),
        ('transportation', 'Transportation'),
        ('manufacturing', 'Manufacturing Process'),
        ('business_travel', 'Business Travel'),
        ('waste', 'Waste Management'),
        ('water', 'Water Usage'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    emission_value = FloatField('Emission Value', validators=[DataRequired()])
    emission_unit = SelectField('Unit', choices=[
        ('kg', 'Kilograms (kg CO2e)'),
        ('tonnes', 'Tonnes (t CO2e)')
    ], default='kg')
    submit = SubmitField('Submit Activity')

class EmissionTargetForm(FlaskForm):
    target_value = FloatField('Target Emission Value', validators=[DataRequired()])
    target_unit = SelectField('Unit', choices=[
        ('kg', 'Kilograms (kg CO2e)'),
        ('tonnes', 'Tonnes (t CO2e)')
    ], default='kg')
    target_date = DateField('Target Date', validators=[DataRequired()])
    category = SelectField('Category (Optional)', choices=[
        ('overall', 'Overall Emissions'),
        ('energy', 'Energy Consumption'),
        ('transportation', 'Transportation'),
        ('manufacturing', 'Manufacturing Process'),
        ('business_travel', 'Business Travel'),
        ('waste', 'Waste Management'),
        ('water', 'Water Usage'),
        ('other', 'Other')
    ], default='overall')
    submit = SubmitField('Set Target')

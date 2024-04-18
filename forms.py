from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, DateField
from wtforms.validators import InputRequired, Optional

class AddUserForm(FlaskForm):
    """Form for signing up a user"""
    username = StringField('Username',
                            validators=[InputRequired()])
    
    password = PasswordField('Password',
                             validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                           validators=[InputRequired()])
    
# Trip forms 
    
class AddTripForm(FlaskForm):
    name = StringField('Trip Name',
                       validators=[InputRequired()])
    
    location = StringField('Location',
                           validators=[InputRequired()])
    
    start_date = DateField('Start Date',
                           validators=[InputRequired()])
    
    end_date = DateField('End Date',
                         validators=[InputRequired()])

    mileage = FloatField('Total Mileage')

    notes = StringField('Trip Notes')

class EditTripForm(FlaskForm):
    name = StringField('Trip Name',
                       validators=[InputRequired()])
    
    location = StringField('Location',
                           validators=[InputRequired()])
    
    start_date = DateField('Start Date',
                           validators=[InputRequired()])
    
    end_date = DateField('End Date',
                         validators=[InputRequired()])

    mileage = FloatField('Total Mileage')

    notes = StringField('Trip Notes')

# Pack Forms

class AddPackForm(FlaskForm):
    name = StringField('Pack Name',
                       validators=[InputRequired()])
    
    notes = StringField('Notes')

class EditPackForm(FlaskForm):
    name = StringField('Pack Name',
                       validators=[InputRequired()])
    
    notes = StringField('Notes')


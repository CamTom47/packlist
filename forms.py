from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, DateField, EmailField, SelectField, RadioField, BooleanField
from wtforms.validators import InputRequired, Optional

class AddUserForm(FlaskForm):
    """Form for signing up a user"""
    
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    
    last_name = StringField('Last Name',
                             validators=[InputRequired()])
    
    username = StringField('Username',
                            validators=[InputRequired()])
    
    password = PasswordField('Password',
                             validators=[InputRequired()])
    


class EditUserForm(FlaskForm):
    """Form for signing up a user"""
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    
    last_name = StringField('Last Name',
                             validators=[InputRequired()])
    
    username = StringField('Username')
    
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

class AddItemForm(FlaskForm):
    name = StringField('Item Name',
                       validators=[InputRequired()])
    category = SelectField('Item Category',
                           validators=[InputRequired()],
                           choices=[("Clothing","Clothing"),("Cooking","Cooking"),("Gear","Gear"),("Hygiene","Hygiene"),("Miscellaneous","Miscellaneous"),("Navigation","Navigation"),("Pet","Pet"),("Safety","Safety"),("Sleeping","Sleeping")])
    essential = RadioField("essential",
                        choices=[(True,"Yes"),(False,"No")])
    rain_precautionary = RadioField("rain_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    cold_precautionary = RadioField("cold_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    heat_precautionary = RadioField("heat_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    emergency_precautionary = RadioField("emergency_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    
class EditItemForm(FlaskForm):
    name = StringField('Item Name',
                       validators=[InputRequired()])
    category = SelectField('Item Category',
                           validators=[InputRequired()],
                           choices=[("Clothing","Clothing"),("Cooking","Cooking"),("Gear","Gear"),("Hygiene","Hygiene"),("Miscellaneous","Miscellaneous"),("Navigation","Navigation"),("Pet","Pet"),("Safety","Safety"),("Sleeping","Sleeping")])
    essential = RadioField("essential",
                        choices=[(True,"Yes"),(False,"No")])
    rain_precautionary = RadioField("rain_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    cold_precautionary = RadioField("cold_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    heat_precautionary = RadioField("heat_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
    emergency_precautionary = RadioField("emergency_precautionary",
                        choices=[(True,"Yes"),(False,"No")])
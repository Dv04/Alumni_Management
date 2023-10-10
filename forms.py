import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_ckeditor import CKEditorField

# Load college data from 'clg.json' file
with open('clg.json', 'r') as file:
    colleges = json.load(file)
    
# Create a list of college choices for the SelectField
listclg = [(i, colleges.get(i)) for i in colleges]

class RegisterForm(FlaskForm):
    """Form for user registration."""
    
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    college = SelectField("College", choices=listclg, validators=[DataRequired()])
    pass_year = IntegerField("Graduation Year", validators=[DataRequired(), NumberRange(min=1960, message="Year must be 1960 or later.")], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    furthereducation = StringField("Further Education", validators=[DataRequired(), Length(min=2, message="Please enter a valid education.")])
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')], validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be atleast 8 characters long.")])
    submit = SubmitField("Register")

class UniForm(FlaskForm):
    """Form for university registration."""
    
    uni_name = StringField("University Name", validators=[DataRequired(), Length(min=2, message="Please enter a valid name.")])
    uni_addr = TextAreaField("University Address", validators=[DataRequired(), Length(min=10, message="Please enter a valid address.")])
    uni_email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    uni_password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    submit = SubmitField("Register")

class DirectorateForm(FlaskForm):
    """Form for directorate registration."""
    
    dir_name = StringField("Director Name", validators=[DataRequired(), Length(min=2)])
    dir_college = SelectField("College Name", choices=listclg, validators=[DataRequired()])
    dir_email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    dir_password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be atleast 8 characters long.")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    """Form for user login."""
    
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message="Password must be atleast 8 characters long."),
    ])
    type = RadioField('Login As', choices=[('users', 'Alumni'), ('directorate', 'Directorate'), ('universities', 'University')])
    submit = SubmitField("Login")

class UpdateForm(FlaskForm):
    """Form for updating user information."""
    
    startup = TextAreaField('Startup Details', validators=[Length(max=500)])
    work = TextAreaField('Work Details', validators=[Length(max=500)])
    submit = SubmitField("Update")

class SearchForm(FlaskForm):
    """Form for searching user profiles."""

    college = SelectField("College", choices=listclg)
    pass_year_from = IntegerField("Graduation Year From", validators=[DataRequired(), NumberRange(min=1960, message="Year must be 1960 or later.")], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    pass_year_to = IntegerField("Graduation Year To", validators=[DataRequired(), NumberRange(min=1960, message="Year must be 1960 or later.")], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')])
    furthereducation = SelectField("Further Education", choices=[('none','None'), ('masters', 'Masters')])
    search = SubmitField("Search")

class ChatForm(FlaskForm):
    """Form for sending chat messages."""
    
    chat_msg = CKEditorField("", validators=[DataRequired()])
    submit = SubmitField("Send Message")

class PasswordForm(FlaskForm):
    """Form for updating user passwords."""

    old_pass = PasswordField("Old Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    new_pass = PasswordField("New Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    rep_new_pass = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    reset = SubmitField("Change Password")

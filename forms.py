import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

# Load college data from 'clg.json' file
with open('clg.json', 'r') as file:
    colleges = json.load(file)
    
# Create a list of college choices for the SelectField
listclg = [(i, colleges.get(i)) for i in colleges]

class RegisterForm(FlaskForm):
    """Form for user registration."""
    
    name = StringField("Name", validators=[DataRequired()])
    college = SelectField("College", choices=listclg)
    pass_year = IntegerField("Graduation Year", validators=[DataRequired()], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    furthereducation = StringField("Further Education", validators=[DataRequired()])
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')], validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class UniForm(FlaskForm):
    """Form for university registration."""
    
    uni_name = StringField("University Name", validators=[DataRequired()])
    # college = SelectField("College", choices=listclg)
    # pass_year = IntegerField("Graduation Year", validators=[DataRequired()], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    uni_addr = TextAreaField("University Address", validators=[DataRequired()])
    # occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')], validators=[DataRequired()])
    uni_email = StringField("Email", validators=[DataRequired()])
    uni_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class DirectorateForm(FlaskForm):
    """Form for directorate registration."""
    
    dir_name = StringField("Director Name", validators=[DataRequired()])
    dir_college = SelectField("College Name", choices=listclg)
    # pass_year = IntegerField("Graduation Year", validators=[DataRequired()], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    # furthereducation = StringField("Further Education", validators=[DataRequired()])
    # occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')], validators=[DataRequired()])
    dir_email = StringField("Email", validators=[DataRequired()])
    dir_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    """Form for user login."""
    
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    type = RadioField('Login As', choices=[('users', 'Alumni'), ('directorate', 'Directorate'), ('universities', 'University')])
    submit = SubmitField("Login")

class UpdateForm(FlaskForm):
    """Form for updating user information."""
    
    startup = TextAreaField('Startup Details')
    work = TextAreaField('Work Details')
    submit = SubmitField("Update")
    
class SearchForm(FlaskForm):
    """Form for searching user profiles."""

    college = SelectField("College", choices=listclg)
    pass_year_from = IntegerField("Graduation Year From", render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)}, default=int(datetime.datetime.now().year - 63))
    pass_year_to = IntegerField("Graduation Year To", render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)}, default=int(datetime.datetime.now().year))
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')])
    furthereducation = SelectField("Further Education", choices=[('none','None'), ('masters', 'Masters')])
    search = SubmitField("Search")

class ChatForm(FlaskForm):
    """Form for sending chat messages."""
    
    chat_msg = CKEditorField("", validators=[DataRequired()])
    submit = SubmitField("Send Message")

class PasswordForm(FlaskForm):
    """Form for updating user passwords."""

    old_pass = PasswordField("Old Password", validators=[DataRequired()])
    new_pass = PasswordField("New Password", validators=[DataRequired()])
    rep_new_pass = PasswordField("Repeat New Password", validators=[DataRequired()])
    reset = SubmitField("Update Password")
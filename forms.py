import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

with open('clg.json', 'r') as file:
    colleges = json.load(file)

listclg = [(i, colleges.get(i)) for i in colleges]

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    college = SelectField("College", choices=listclg)
    pass_year = IntegerField("Graduation Year", validators=[DataRequired()], render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)})
    furthereducation = StringField("Further Education", validators=[DataRequired()])
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')], validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    college = SelectField("College", choices=listclg)
    pass_year_from = IntegerField("Graduation Year From", render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)}, default=int(datetime.datetime.now().year - 63))
    pass_year_to = IntegerField("Graduation Year To", render_kw={"min": int(datetime.datetime.now().year) - 63, "max": int(datetime.datetime.now().year)}, default=int(datetime.datetime.now().year))
    occupation = SelectField("Occupation", choices=[('work','Work'), ('startup', 'Start Up')])
    furthereducation = SelectField("Further Education", choices=[('none','None'), ('masters', 'Masters')])
    search = SubmitField("Search")

class ChatForm(FlaskForm):
    chat_msg = CKEditorField("", validators=[DataRequired()])
    submit = SubmitField("Send Message")

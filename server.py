from functools import wraps
import json
from firebase import firebase
from firebase_admin import db
from forms import RegisterForm, LoginForm, SearchForm, ChatForm, UniForm, DirectorateForm, UpdateForm, PasswordForm
from flask import abort, Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__, static_folder='static')
Bootstrap(app=app)
app.app_context().push()
app.secret_key = "secret-tunnel"

ckeditor = CKEditor(app=app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

global logged_in
logged_in = False

firebase = firebase.FirebaseApplication('https://virthack-a728b-default-rtdb.firebaseio.com/', None)

users = firebase.get('/users', None)
for key, value in users.items():
    print(value)
class User(UserMixin):
    is_active = False
    email = ""
    password = ""
    college = ""
    name = ""
    grad_year = ""
    further_ed = ""
    occupation = ""
    addr=""
    startup_details=""
    work_details=""
    priv = "alumni"

log_user = User()

def usr_priv(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if log_user.priv == "alumni" and request.path != "/user":
            return redirect(url_for('user_page', user=log_user))
        elif log_user.priv == "university" and request.path != "/university":
            return redirect(url_for('university_page', user=log_user))
        elif log_user.priv == "directorate" and request.path != "/directorate":
            return redirect(url_for('directorate_page', user=log_user))
        else:
            return function(*args, **kwargs)
    return decorated_function

def logged_in(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if log_user.is_active:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))
            
    return decorated_function

@app.route('/')
def home_page():
    global logged_in
    print(logged_in)
    return render_template('Index.html', user=log_user)

@app.route('/university')
@logged_in
@usr_priv
def university_page():
    return render_template('University.html', user=log_user)

@app.route('/change-password', methods=["GET", "POST"])
@logged_in
def change_password():
    pass_form = PasswordForm()
    if log_user.priv == "university":
        page = "universities"
    elif log_user.priv == "directorate":
        page = "directorate"
    else:
        page="users"
    print("start")
    if pass_form.validate_on_submit():
        print("validate")
        if check_password_hash(pwhash=log_user.password, password=pass_form.old_pass.data):
            print("match")
            new_pass = pass_form.new_pass.data
            if new_pass == pass_form.rep_new_pass.data:
                print("match2")
                users = firebase.get(f'/{page}', None)
                for key, value in users.items():
                    if value["email"] == log_user.email:
                        print("updating")
                        usr_name = log_user.name
                        usr_email = log_user.email
                        usr_password = generate_password_hash(
                            new_pass,
                            method='pbkdf2:sha256',
                            salt_length=8
                        )
                        usr_college = log_user.college
                        usr_further_ed = log_user.further_ed
                        usr_occup = log_user.occupation
                        usr_grad_year = log_user.grad_year
                        data = {"college": usr_college,"email": usr_email,"furthereducation": usr_further_ed, "name": usr_name, "occupation":usr_occup, "pass_year": usr_grad_year, "password": usr_password, "priv": log_user.priv}
                        print("posting")
                        result = firebase.put(f'/{page}', name=key, data=data)
                        print("posted")
                        return redirect(url_for('logout_page'))
    return render_template('Password.html', user=log_user, form=pass_form)

@app.route('/update', methods=["GET", "POST"])
@logged_in
def update_page():
    update_form = UpdateForm()
    pass_form = PasswordForm()
    print("yes")
    if update_form.validate_on_submit():
        startup_details = update_form.startup.data
        work_details = update_form.work.data
        data = {"email": log_user.email, "startup": startup_details, "work": work_details}
        print("yes2")
        firebase.post(f'/details', data)
        return redirect(url_for('user_page', user=log_user))
    return render_template('Update.html', user=log_user, update_form=update_form, pass_form=pass_form)

@app.route('/directorate')
@logged_in
@usr_priv
def directorate_page():
    with open('clg.json', 'r') as file:
        clg_data = json.load(file)
    return render_template('Director.html', user=log_user, usr_clg=clg_data.get(log_user.college))

@app.route('/result/contact', methods=["GET", "POST"])
def contact_page():
    return render_template('Contact.html', user=log_user)


# Define the route for the chat page
@app.route('/chat', methods=["GET", "POST"])
@logged_in
def chat():
    chat_form = ChatForm()
    with open('clg.json', 'r') as file:
        clg_data = json.load(file)
    if log_user.is_active and chat_form.validate_on_submit():
        usr_msg = chat_form.chat_msg.data
        msg = {"group": clg_data.get(log_user.college), "name": log_user.name, "msg": usr_msg}
        firebase.post(f'/chats', msg)
    if not log_user:
        return redirect(url_for('home_page'))
    chat_result = firebase.get('/chats', None)
    return render_template('Chat.html', user=log_user, chat=chat_form, prev_chat=chat_result, usr_clg=clg_data.get(log_user.college))

@app.route('/user')
@logged_in
@usr_priv
def user_page():
    return render_template('User.html', user=log_user)

@app.route('/search', methods=["GET", "POST"])
def search_page():
    search_form=SearchForm()
    if search_form.validate_on_submit():
        college_name = search_form.college.data
        grad_year_from = search_form.pass_year_from.data
        grad_year_to = search_form.pass_year_to.data
        occup = search_form.occupation.data
        further_ed = search_form.furthereducation.data
        return redirect(url_for('result_page', college=college_name, grad_year_from=grad_year_from, grad_year_to=grad_year_to, occup=occup, further_ed=further_ed, user=log_user))
    return render_template('Search.html', form=search_form, user=log_user)


@app.route('/result/', methods=["GET", "POST"])
def result_page():
    result_data = []
    with open('details.json', 'r') as file:
        data = json.load(file)
    with open('clg.json', 'r') as file:
        clg_data = json.load(file)

    college = clg_data.get(request.args.get('college'))
    print(college)
    grad_year_from = request.args.get('grad_year_from')
    grad_year_to = request.args.get('grad_year_to')
    occup = ["startup", "work"]
    occup = [request.args.get('occup')]
    further_ed = ["Masters","None"]
    further_ed = [request.args.get('further_ed')]

    for i in data:
        
        if grad_year_from < i.get("year") < grad_year_to:
            match = True
            
            if college and i.get("college")[0] != college:
                match = False

            if occup and i.get("occupation")[0] != occup[0]:
                match = False

            if further_ed and i.get("Further_Education")[0] != further_ed[0]:
                match = False
            
            if match == True:
                result_data.append(i)
                
    print(result_data)
    return render_template('Result.html', result_data=result_data, user=log_user)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    reg_form = RegisterForm()
    uni_form = UniForm()
    dir_form = DirectorateForm()
    if reg_form.validate_on_submit():
        usr_name=reg_form.name.data
        college_name = reg_form.college.data
        grad_year = str(reg_form.pass_year.data)
        further_ed = reg_form.furthereducation.data
        occup = reg_form.occupation.data
        usr_email=reg_form.email.data
        hash_and_salted_password = generate_password_hash(
            reg_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        data = {"college": college_name,"email": usr_email,"furthereducation": further_ed, "name": usr_name, "occupation":occup, "pass_year": grad_year, "password": hash_and_salted_password, "priv": "alumni"}
        firebase.post(f'/users', data)
        log_user.is_active = True
        log_user.name = usr_name
        log_user.email = usr_email
        log_user.password = hash_and_salted_password
        log_user.college = college_name
        log_user.further_ed = further_ed
        log_user.occupation = occup
        log_user.grad_year = grad_year
        return redirect(url_for('user_page', user=log_user))
    elif uni_form.validate_on_submit():
        uni_name=uni_form.uni_name.data
        uni_addr=uni_form.uni_addr.data
        uni_email=uni_form.uni_email.data
        hash_and_salted_password = generate_password_hash(
            uni_form.uni_password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        data = {"university": uni_name,"email": uni_email, "password": hash_and_salted_password, "priv": "university"}
        firebase.post(f'/universities', data)
        log_user.is_active = True
        log_user.name = uni_name
        log_user.email = uni_email
        log_user.password = hash_and_salted_password
        log_user.addr = uni_addr
        log_user.priv = "university"
        return redirect(url_for('university_page', user=log_user))
    elif dir_form.validate_on_submit():
        dir_name=dir_form.dir_name.data
        dir_college = dir_form.dir_college.data
        dir_email=dir_form.dir_email.data
        hash_and_salted_password = generate_password_hash(
            dir_form.dir_password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        data = {"college": dir_college,"email": dir_email, "name": dir_name, "password": hash_and_salted_password, "priv": "directorate"}
        firebase.post(f'/directorate', data)
        log_user.is_active = True
        log_user.name = dir_name
        log_user.email = dir_email
        log_user.password = hash_and_salted_password
        log_user.college = dir_college
        log_user.priv = "directorate"
        return redirect(url_for('directorate_page', user=log_user))
    return render_template('Register.html', reg_form=reg_form, uni_form=uni_form, dir_form=dir_form, user=log_user)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        usr_email=login_form.email.data
        acc_type = login_form.type.data
        print("Type "+acc_type)
        result = firebase.get(f'/{acc_type}', None)
        result_filt = [(result.get(i).get('email'), result.get(i).get('password'), i) for i in result]
        for credentials in result_filt:
            if credentials[0] == usr_email:
                if check_password_hash(pwhash=credentials[1], password=login_form.password.data):
                    for key, value in result.items():
                        if credentials[0] == value['email']:
                            try:
                                result = result[key]
                            except:
                                continue
                    log_user.is_active = True
                    log_user.name = result.get('name')
                    log_user.email = result.get('email')
                    log_user.password = result.get('password')
                    log_user.college = result.get('college')
                    log_user.further_ed = result.get('furthereducation')
                    log_user.occupation = result.get('occupation')
                    log_user.grad_year = result.get('pass_year')
                    if acc_type == "universities":
                        log_user.priv = "university"
                        page = "university"
                    elif acc_type == "directorate":
                        log_user.priv = "directorate"
                        page = "directorate"
                    else:
                        log_user.priv = "alumni"
                        page = "user"
                    return redirect(url_for(f'{page}_page', user=log_user))
    return render_template('Login.html', form=login_form, user=log_user)

@app.route('/logout')
def logout_page():
    log_user.is_active = False
    log_user.name = ""
    log_user.email = ""
    log_user.password = ""
    log_user.college = ""
    log_user.further_ed = ""
    log_user.occupation = ""
    log_user.grad_year = ""
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    # We will run this on all addresses and accessible through port 5000 so that we can check for the comments too
    app.run(debug=True, host='0.0.0.0', port=5001)

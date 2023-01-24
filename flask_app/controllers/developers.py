from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.developer import Developer
from flask_app.models.skill import Skill
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/devs/register')
def devRegisterPage():
    # if 'user_id' in session:
    #     return redirect('/dashboard')
    return render_template('devRegisterPage.html')

@app.route('/create_developer', methods=['POST'])
def create_developer():
    if 'developer_id' in session:
        return redirect('/devs/register')

    if not Developer.validate_developer(request.form):
        flash('Something went wrong!', 'devSignUp')
        return redirect(request.referrer)

    if Developer.get_developer_by_email(request.form):
        flash('This email already exists!', 'emailSignUp')
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'bio': None
    }
    Developer.create_developer(data)
    flash('Succesfull Registration!', 'devSignUpSuccessful')
    return redirect(request.referrer)

@app.route('/enter_developerDashboard', methods=['POST'])
def devsDashboard():
    if 'developer_id' in session:
        return redirect('/devs/login')

    data = {
        'email': request.form['email']
    }

    if len(request.form['email'])<1:
        flash('*Email is required to login!', 'emailLogIn')
        return redirect(request.referrer)

    if not Developer.get_developer_by_email(data):
        flash('*This email does not exist!', 'emailLogIn')
        return redirect(request.referrer)

    developer = Developer.get_developer_by_email(data)

    if not bcrypt.check_password_hash(developer['password'], request.form['password']):
        flash("*Invalid Password!", 'passwordLogIn')
        return redirect(request.referrer)

    session['developer_id'] = developer['id']
    return redirect('/devs/dashboard')

@app.route('/devs/dashboard')
def devDashboard():
    if 'developer_id' in session:
        data = {
            'developer_id': session['developer_id']
        }
        developer = Developer.get_developer_by_id(data)
        skills = Skill.getAllSkills()
        dev_skills = Skill.getDevSkills(data)
        progress = len(dev_skills)*20
        return render_template('devDashboard.html', loggedDeveloper = developer, skills = skills, dev_skills = dev_skills, progress = progress)
    return redirect('/devs/logout')

@app.route('/devs/login')
def devLoginPage():
    if 'developer_id' in session:
        return redirect('/devs/dashboard')
    return render_template('devLoginPage.html')

@app.route('/devs/logout')
def devLogout():
    session.clear()
    return redirect('/devs/login')


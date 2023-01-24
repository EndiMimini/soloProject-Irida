from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.organization import Organization
from flask_app.models.position import Position
from flask_app.models.developer import Developer
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/orgs/register')
def orgRegisterPage():
    if 'organization_id' in session:
        return redirect('/orgs/dashboard')
    return render_template('orgRegisterPage.html')

@app.route('/create_organization', methods=['POST'])
def create_organisation():
    if 'organization_id' in session:
        return redirect('/orgs/register')

    if not Organization.validate_organization(request.form):
        flash('Something went wrong!', 'orgSignUp')
        return redirect(request.referrer)

    if Organization.get_organization_by_email(request.form):
        flash('This email already exists!', 'emailSignUp')
        return redirect(request.referrer)

    data = {
        'orgName': request.form['orgName'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'orgAddress': request.form['orgAddress'],
        'orgCity': request.form['orgCity'],
        'state' : request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    Organization.create_organization(data)
    flash('Succesfull Registration!', 'orgSignUpSuccessful')
    return redirect(request.referrer)

@app.route('/enter_organization', methods=['POST'])
def orgsDashboard():
    if 'organization_id' in session:
        return redirect('/orgs/login')

    data = {
        'email': request.form['email']
    }

    if len(request.form['email'])<1:
        flash('*Email is required to login!', 'emailLogIn')
        return redirect(request.referrer)

    if not Organization.get_organization_by_email(data):
        flash('*This email does not exist!', 'emailLogIn')
        return redirect(request.referrer)

    organization = Organization.get_organization_by_email(data)

    if not bcrypt.check_password_hash(organization['password'], request.form['password']):
        flash("*Invalid Password!", 'passwordLogIn')
        return redirect(request.referrer)

    session['organization_id'] = organization['id']
    return redirect('/orgs/dashboard')

@app.route('/orgs/dashboard')
def dashboard():
    if 'organization_id' in session:
        data = {
            'organization_id': session['organization_id'],
            
        }
        organization = Organization.get_organization_by_id(data)
        allPositions = Position.getAllPositions(data)
        allDevelopers = Developer.getAllDevelopers()
        return render_template('orgDashboard.html', loggedOrganization = organization, orgPositions = allPositions, devs = allDevelopers)
    return redirect('/logout')

@app.route('/orgs/login')
def orgLoginPage():
    if 'organization_id' in session:
        return redirect('/orgs/dashboard')
    return render_template('orgLoginPage.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/orgs/login')
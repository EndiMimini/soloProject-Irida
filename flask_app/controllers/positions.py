from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.position import Position
from flask_app.models.organization import Organization
from flask_app.models.skill import Skill
from flask import flash

@app.route("/orgs/jobs/new")
def fill_position_form():
    if 'organization_id' not in session:
        return redirect("/logout")
    skills = Skill.getAllSkills()
    return render_template("newPosition.html", skills = skills)

@app.route('/create_position', methods=['POST'])
def createPosition():
    if 'organization_id' not in session:
        return redirect('/logout')

    if not Position.validate_position(request.form):
        flash('Something went wrong!', 'newPosition')
        return redirect(request.referrer)

    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'organization_id' : session['organization_id']
    }
    Position.create_position(data)
    return redirect('/orgs/dashboard')

@app.route('/orgs/jobs/<int:id>')
def display_each_position(id):
    if 'organization_id' not in session:
        return redirect('/logout')
    data = {
        'position_id' : id,
        'organization_id' : session['organization_id']
    }
    position = Position.get_position_by_id(data)
    organization = Organization.get_organization_by_id(data)
    skills = Skill.getAllSkills()
    position_id = session.get('position_id', None)
    return render_template("posDashboard.html", positions = position, loggedOrganization = organization, skills = skills)



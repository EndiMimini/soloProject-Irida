from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.skill import Skill
from flask import flash

@app.route('/add_dev_skill/<int:id>')
def addDevSkill(id):
    if 'developer_id' not in session:
        return redirect('/devs/logout')
    data = {
        'developer_id': session['developer_id'],
        'skill_id': id
    }
    dev_skills = Skill.getDevSkills(data)
    for row in dev_skills:
        if data['skill_id'] == row['id']:
            flash('*You have selected this skill once!', 'selectedSkill')
            return redirect('/devs/dashboard')
    if len(dev_skills) >= 5:
        flash('*You can select only 5 skills!', 'skillErr')
        return redirect('/devs/dashboard')
    Skill.add_dev_skill(data)
    return redirect('/devs/dashboard')

@app.route('/add_pos_skill/<int:id>')
def addPosSkill(id):
    if 'organization_id' not in session:
        return redirect('/logout')
    data = {
        'position_id': session['position_id'],
        'skill_id': id
    }
    pos_skills = Position.getPosSkills(data)
    for row in pos_skills:
        if data['skill_id'] == row['id']:
            flash('*You have selected this skill once!', 'selectedSkill')
            return redirect('/devs/dashboard')
    if len(dev_skills) >= 5:
        flash('*You can select only 5 skills!', 'skillErr')
        return redirect('/devs/dashboard')
    Skill.add_pos_skill(data)
    return redirect('/orgs/dashboard')
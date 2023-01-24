from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Skill:
    db_name='devsOnDeck'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name']

    @classmethod
    def getAllSkills(cls):
        query= 'SELECT * FROM skills;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        skills= []
        if results:
            for row in results:
                skills.append(row)
            return skills
        return skills

    @classmethod
    def getDevSkills(cls,data):
        query= 'SELECT skills.id, skills.name FROM skills LEFT JOIN dev_skills ON dev_skills.skill_id = skills.id WHERE developer_id = %(developer_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        skills= []
        if results:
            for row in results:
                skills.append(row)
            return skills
        return skills

    @classmethod
    def add_dev_skill(cls,data):
        query = 'INSERT INTO dev_skills (developer_id, skill_id) VALUES ( %(developer_id)s, %(skill_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def add_pos_skill(cls,data):
        query = 'INSERT INTO pos_skills (name, description, organization_id) VALUES ( %(name)s, %(description)s, %(organization_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getPosSkills(cls,data):
        query= 'SELECT skills.id, skills.name FROM skills LEFT JOIN pos_skills ON pos_skills.skill_id = skills.id WHERE position_id = %(position_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        skills= []
        if results:
            for row in results:
                skills.append(row)
            return skills
        return skills

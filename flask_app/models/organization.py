from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Organization:
    db_name='devsOnDeck'
    def __init__(self,data):
        self.id = data['id'],
        self.orgName = data['orgName'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.orgAddress = data['orgAddress'],
        self.orgCity = data['orgCity'],
        self.state = data['state'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def create_organization(cls,data):
        query = 'INSERT INTO organizations (orgName, first_name, last_name, email, orgAddress, orgCity, state, password) VALUES ( %(orgName)s, %(first_name)s, %(last_name)s, %(email)s, %(orgAddress)s, %(orgCity)s, %(state)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_organization_by_email(cls, data):
        query= 'SELECT * FROM organizations WHERE organizations.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def get_organization_by_id(cls, data):
        query= 'SELECT * FROM organizations WHERE organizations.id = %(organization_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    @staticmethod
    def validate_organization(organization):
        is_valid = True
        if not EMAIL_REGEX.match(organization['email']): 
            flash("*Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(organization['orgName']) < 2:
            flash("*Organization name must be at least 2 characters!", 'orgName')
            is_valid = False
        if len(organization['first_name']) < 2:
            flash("*Name must be at least 2 characters!", 'name')
            is_valid = False
        if len(organization['last_name']) < 2:
            flash("*Surname must be at least 2 characters!", 'surname')
            is_valid = False
        if organization['orgAddress'] == '':
            flash("*Organization address is required!", 'orgAddress')
            is_valid = False
        if organization['orgCity'] == '':
            flash("*City is required!", 'orgCity')
            is_valid = False
        if organization['state'] == 'Select State':
            flash("*Organization state is required!", 'state')
            is_valid = False   
        if len(organization['password']) < 8:
            flash("*Password must be at least 8 characters!", 'passwordSignUp')
            is_valid = False
        if organization['confirm_password'] != organization['password']:
            flash("*Password does not match!", 'passwordConfirm')
            is_valid = False
        return is_valid


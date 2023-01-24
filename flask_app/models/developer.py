from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Developer:
    db_name='devsOnDeck'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.address = data['address'],
        self.city = data['city'],
        self.state = data['state'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
        

    @classmethod
    def create_developer(cls,data):
        query = 'INSERT INTO developers (first_name, last_name, email, address, city, state, password) VALUES ( %(first_name)s, %(last_name)s,  %(email)s, %(address)s, %(city)s, %(state)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_developer_by_email(cls, data):
        query= 'SELECT * FROM developers WHERE developers.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def get_developer_by_id(cls, data):
        query= 'SELECT * FROM developers WHERE developers.id = %(developer_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]
    
    @classmethod
    def getAllDevelopers(cls):
        query= 'SELECT developers.first_name, developers.last_name, GROUP_CONCAT(name) AS skills FROM dev_skills LEFT JOIN developers ON dev_skills.developer_id = developers.id LEFT JOIN skills ON dev_skills.skill_id = skills.id GROUP BY developers.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        developers= []
        if results:
            for row in results:
                developers.append(row)
            return developers
        return developers

    @classmethod
    def add_profile_photo(cls, data):
        query = 'UPDATE developers SET profile_photo = %(file_path)s WHERE id = %(developer_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def getDeveloperSkills(cls):
        developers = []
        query = 'SELECT * FROM developers;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        for row in results:
            skills = []
            idja = str(row['id'])
            query2 = 'SELECT GROUP_CONCAT(name) FROM dev_skills LEFT JOIN developers ON dev_skills.developer_id = developers.id LEFT JOIN skills ON dev_skills.skill_id = skills.id WHERE developers.id = 1;'
        

    @staticmethod
    def validate_developer(developer):
        is_valid = True
        if not EMAIL_REGEX.match(developer['email']): 
            flash("*Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(developer['first_name']) < 3:
            flash("*Name must be at least 3 characters!", 'name')
            is_valid = False
        if len(developer['last_name']) < 3:
            flash("*Last name must be at least 3 characters!", 'surname')
            is_valid = False
        if developer['address'] == '':
            flash("*Address is required!", 'address')
            is_valid = False
        if developer['city'] == '':
            flash("*City is required!", 'city')
            is_valid = False
        if developer['state'] == 'Select State':
            flash("*State is required!", 'state')
            is_valid = False   
        if len(developer['password']) < 8:
            flash("*Password must be at least 8 characters!", 'passwordSignUp')
            is_valid = False
        if developer['confirm_password'] != developer['password']:
            flash("*Password does not match!", 'passwordConfirm')
            is_valid = False
        return is_valid
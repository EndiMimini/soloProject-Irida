from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Position:
    db_name='devsOnDeck'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.description = data['description'],
        self.organization_id = data['organization_id'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def create_position(cls,data):
        query = 'INSERT INTO positions (name, description, organization_id) VALUES ( %(name)s, %(description)s, %(organization_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAllPositions(cls,data):
        query= 'SELECT positions.id, positions.name FROM positions JOIN organizations ON positions.organization_id = organizations.id WHERE organizations.id = %(organization_id)s ;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        positions= []
        if results:
            for row in results:
                positions.append(row)
            return positions
        return positions

    @classmethod
    def get_position_by_id(cls, data):
        query= 'SELECT * FROM positions WHERE positions.id = %(position_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    @staticmethod
    def validate_position(position):
        is_valid = True
        if len(position['name']) < 2:
            flash("*Position name must be at least 2 characters!", 'posName')
            is_valid = False
        if len(position['description']) < 3:
            flash("*Description must be at least 3 characters!", 'description')
            is_valid = False
        return is_valid

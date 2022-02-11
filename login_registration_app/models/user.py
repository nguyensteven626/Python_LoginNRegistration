from login_registration_app.config.mysqlconnection import connectToMySQL
from login_registration_app import DB
from flask import flash
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#-----create-------#
    @classmethod 
    def create(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        #---returnid----#
        return connectToMySQL(DB).query_db(query, data)


#------retrieve------#
    @classmethod
    def retrieve_one(cls, data):
        query = 'SELECT * FROM users WHERE id=%(id)s;'
        results = connectToMySQL(DB).query_db(query, data)
        # if results:
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


#------validation-----#

    # Registration
    @staticmethod
    def validate_register(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters.')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False            
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid


    # I recommend not validating user login in your model 
    # @staticmethod
    # def validate_login(data):
    #     if not EMAIL_REGEX.match(data['email']): 
    #         flash("Invalid email address!")
    #         is_valid = False            
    #     if len(data['password']) < 8:
    #         flash("Password must be at least 8 characters.")
    #         is_valid = False
    #     if data['password'] != data['confirm_password']:
    #         flash("Passwords do not match.")
    #         is_valid = False
    #     return is_valid
        

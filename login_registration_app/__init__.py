from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = 'supersecretkey'
bcrypt = Bcrypt(app)

DB = 'login_registration_schema'
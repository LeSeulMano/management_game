from flask import Flask
app = Flask(__name__, template_folder="../routes/templates", static_folder="../static")
app.config['SECRET_KEY'] = 'TOKEN'
app.config['SESSION_TYPE'] = 'filesystem'

from routes import users
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import csv
import json

from flask import Flask

app = Flask(__name__, template_folder='../templates')

app.secret_key = 'some_secure_random_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rootroot@127.0.0.1/postgres'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
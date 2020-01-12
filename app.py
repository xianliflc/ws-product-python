# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from libs.rate_limiter import rate_limiter
from routes.routes import init_routes

# web app
app = Flask(__name__)
api = init_routes(app)
CORS(app)

@app.route('/')
@rate_limiter(100)
def index():
    return 'Welcome to EQ Works 😎'

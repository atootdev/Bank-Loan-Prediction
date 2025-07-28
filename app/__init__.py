import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from . import db

def create_app(test_config=None):
  # creates and configures the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'bank.sqlite'),
  )
  
  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)
  
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  # Define a route for the home page
  @app.get('/')
  def home():
    return "Welcome to the Prediction Loan API!"
  
  db.init_app(app)
  
  from . import auth
  app.register_blueprint(auth.bp)
  
  return app
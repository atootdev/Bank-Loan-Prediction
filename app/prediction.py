from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('prediction', __name__)

bp.route('/')
def index():
  db = get_db()
  predicitions = db.execute(
    'SELECT p.id, customer_id, created, prediction'
    ' ORDER BY created DESC'
  ).fetchall()
  return render_template('prediction/index.html', predictions=predicitions)

bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    age = request.form['age']
    experience = request.form['experience']
    income = request.form['income']
    zip_code = request.form['zip_code']
    family = request.form['family']
    cc_avg = request.form['cc_avg']
    education = request.form['education']
    mortgage = request.form['mortgage']
    securities_account = request.form['securities_account']
    cd_account = request.form['cd_account']
    online = request.form['online']
    credit_card = request.form['credit_card']
    error = None
    
    if not age:
      error = 'Age is required.'
      
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO customer (age, experience, income, zip_code, family, cc_avg, education, mortgage, securities_account, cd_account, online, credit_card)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (age, experience, income, zip_code, family, cc_avg, education, mortgage, securities_account, cd_account, online, credit_card)
      )
      db.commit()
      
      customer_id = db.lastrowid
      
      input_data = db.execute(
        'SELECT * FROM customer WHERE customer_id = ?', (customer_id,)
      ).fetchone()
      
      prediction = model.predict()
      
      return redirect(url_for('prediction.index'))
  
  return render_template('prediction/create.html')
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db, app
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

bp = Blueprint('destination', __name__, url_prefix='/destinations')

@bp.route('/<id>')
def show(id):
    destination = Destination.query.filter_by(id=id).first()
    cform = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=cform)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    db_file_path=check_upload_file(form)
    destination=Destination(name=form.name.data,description=form.description.data, 
    image=db_file_path,currency=form.currency.data)
    db.session.add(destination)
    db.session.commit()
    print('Successfully created new travel destination', 'success')
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  fp=form.image.data
  filename=fp.filename
  BASE_PATH=os.path.dirname(__file__)
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  db_upload_path='/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<destination>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(destination):  
    form = CommentForm()  
    destination_obj = Destination.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data,  
                        destination=destination_obj,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 

      print('Your comment has been added', 'success') 
    return redirect(url_for('destination.show', id=destination))
    
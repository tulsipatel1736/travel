from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
app=Flask(__name__)

def create_app():
    
    bootstrap = Bootstrap(app)

    app.secret_key='somerandomvalue'

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///travel123.sqlite'
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    return app

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html")


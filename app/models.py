from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
##import jwt
from app import db, login_manager


ROLE_USER = 0
ROLE_ADMIN = 1

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(250), index = True, unique = True)
	password = db.Column(db.String(250), nullable=False)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)

	def __repr__(self):
		return '<User %r>' % (self.nickname)
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)


@login_manager.user_loader
def load_user(id):
	#return None
    return Users.query.get(int(id))



class PageItemsList (db.Model):
	id					= db.Column(db.Integer, primary_key = True)
	persistent_id		= db.Column(db.Integer)
	parent				= db.Column(db.Integer)
	name				= db.Column(db.String(250),  )
	path				= db.Column(db.String(1024),  )
	icon				= db.Column(db.String(1024),  )
	roles				= db.Column(db.String(1024),  )





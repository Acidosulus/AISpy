from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
##import jwt
from app import app, db, login


ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

@login.user_loader
def load_user(id):
	return db.session.get(User, int(id))


class PageItemsList (db.Model):
	id					= db.Column(db.Integer, primary_key = True)
	persistent_id		= db.Column(db.Integer)
	parent				= db.Column(db.Integer)
	name				= db.Column(db.String(250),  unique = True)
	path				= db.Column(db.String(1024),  unique = True)
	icon				= db.Column(db.String(1024),  )
	roles				= db.Column(db.String(1024),  )





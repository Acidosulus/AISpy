from datetime import datetime, timezone
from hashlib import md5
from time import time
from sqlalchemy import ForeignKey, Column, String, Table, Integer, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
##import jwt
from common import app, db, login_manager


ROLE_USER = 0
ROLE_ADMIN = 1

class Users(db.Model):
	__tablename__ = 'Users'
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
	note				= db.Column(db.String(1024))





class UserObject (db.Model):
	__tablename__ = 'user_objects'

	id					=	db.Column(db.Integer, primary_key = True)
	user_id				=	db.Column(db.Integer)
	dt					=	db.Column(db.DateTime)
	name				=	db.Column(db.String)
	parameters			=	db.Column(db.String)
	data				=	db.Column(db.String)
	data_01				=	db.Column(db.String)




class UserMessage(db.Model):
    __tablename__ = 'user_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    dt = Column(TIMESTAMP, nullable=True, server_default='now()')
    text = Column(String, nullable=False)
    link = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    style = Column(String, nullable=True)


def Add_Message_for_User(user_id, text, link, icon, style):
	if user_id<=0:
		return
	message = UserMessage(	user_id = user_id,
					   		text = text,
							link = link,
							icon = icon,
							style = style)
	db.session.add(message)
	db.session.commit()
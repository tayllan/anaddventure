from models.DAO import DAO
from pprint import pprint
import re, hashlib

class User(DAO):

	def __init__(self, name, username, email, password, signup_date, biography, is_email_visible = False):
		self.name = name
		self.username = username
		self.email = email
		self.password = password
		self.signup_date = signup_date
		self.biography = biography
		self.is_email_visible = is_email_visible

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.system_user (
				system_user_name,
				system_user_username,
				system_user_email,
				system_user_password,
				system_user_signup_date,
				system_user_biography,
				system_user_is_email_visible
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			''',
			(
				self.name,
				self.username,
				self.email,
				hashlib.sha256(self.password.encode('utf-8')).hexdigest(),
				self.signup_date,
				self.biography,
				self.is_email_visible
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_user_objects(users_array):
		return [
			{
				'id': id,
				'name': name,
				'username': username,
				'email': email,
				'password': password,
				'signup_date': signup_date,
				'biography': biography,
				'is_email_visible': is_email_visible,
				'is_valid_account': is_valid_account
			}
			for
				id, name, username, email, password,
				signup_date, biography, is_email_visible, is_valid_account
			in
				users_array
		]

	@staticmethod
	def delete_account(user_id):
		DAO.delete(
			"DELETE FROM anaddventure.system_user WHERE system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def update_profile(user_id, name, email, biography, is_email_visible):
		DAO.update(
			"""
			UPDATE anaddventure.system_user SET
				system_user_name = (%s),
				system_user_email = (%s),
				system_user_biography = (%s),
				system_user_is_email_visible = (%s)
				WHERE system_user_id = (%s)
			""",
			(name, email, biography, is_email_visible, user_id)
		)

	@staticmethod
	def update_password(user_id, password):
		DAO.update(
			"UPDATE anaddventure.system_user SET system_user_password = (%s) WHERE system_user_id = (%s)",
			(hashlib.sha256(password.encode('utf-8')).hexdigest(), user_id)
		)

	@staticmethod
	def activate_account(user_id):
		DAO.update(
			"UPDATE anaddventure.system_user SET system_user_is_valid_account = True WHERE system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def select_by_id(user_id, rows = None):
		return User._construct_user_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.system_user WHERE system_user_id = (%s)",
				(user_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_username(username = '', rows = None):
		return User._construct_user_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.system_user WHERE system_user_username ILIKE (%s)",
				('%' + username + '%', ),
				rows
			)
		)

	@staticmethod
	def select_count_by_username(username = '', rows = None):
		return DAO.select_by(
			"SELECT COUNT(system_user_id) FROM anaddventure.system_user WHERE system_user_username ILIKE (%s)",
			('%' + username + '%', ),
			rows
		)

	@staticmethod
	def select_by_full_username(username = '', rows = None):
		return User._construct_user_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.system_user WHERE system_user_username ILIKE (%s)",
				(username, ),
				rows
			)
		)

	@staticmethod
	def select_by_email(email = '', rows = None):
		return User._construct_user_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.system_user WHERE system_user_email LIKE (%s)",
				(email, ),
				rows
			)
		)

	@staticmethod
	def select_count_all(rows = None):
		return DAO.select_by(
			"SELECT COUNT(*) FROM anaddventure.system_user",
			(),
			rows
		)

	@staticmethod
	def is_valid_user(username, password):
		user = User.select_by_full_username(username, 1)

		if len(user) is not 1:
			user = User.select_by_email(username, 1)

			if len(user) is not 1:
				return None

		if hashlib.sha256(password.encode('utf-8')).hexdigest() == user[0]['password'] and user[0]['is_valid_account']:
			return user[0]['id']
		else:
			return None

	@staticmethod
	def is_name_valid(name):
		return 3 <= len(name) <= 50

	@staticmethod
	def is_username_valid(username):
		return 3 <= len(username) <= 50

	@staticmethod
	def is_username_available(username):
		return len(User.select_by_full_username(username, 1)) is 0

	@staticmethod
	def is_email_valid(email):
		if re.search(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', email) and len(email) <= 50:
			return True
		else:
			return False

	@staticmethod
	def is_email_available(email):
		return len(User.select_by_email(email, 1)) is 0

	@staticmethod
	def is_password_valid(password):
		return len(password) >= 6

	@staticmethod
	def is_biography_valid(biography):
		return len(biography) <= 500
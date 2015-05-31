from models.DAO import DAO
from datetime import datetime, timedelta
import random, hashlib

class Password_Change_Requests(DAO):

	def __init__(self, user_id):
		self.user_id = user_id
		self.id = Password_Change_Requests._generate_random_token()
		self.datetime = datetime.now()

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.password_change_requests (
				password_change_requests_system_user_id,
				password_change_requests_id,
				password_change_requests_datetime
			)
			VALUES (%s, %s, %s)
			''',
			(
				self.user_id,
				hashlib.sha256(self.id.encode('utf-8')).hexdigest(),
				self.datetime
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_password_change_request_objects(password_change_requests_array):
		return [
			{
				'user_id': user_id,
				'id': id,
				'datetime': date
			}
			for
				user_id, id, date
			in
				password_change_requests_array
		]

	@staticmethod
	def delete(user_id):
		DAO.delete(
			"DELETE FROM anaddventure.password_change_requests WHERE password_change_requests_system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def select_by_id(id, rows = None):
		print(hashlib.sha256(id.encode('utf-8')).hexdigest())

		return Password_Change_Requests._construct_password_change_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.password_change_requests WHERE password_change_requests_id LIKE (%s)",
				(hashlib.sha256(id.encode('utf-8')).hexdigest(), ),
				rows
			)
		)

	@staticmethod
	def _generate_random_token(amount_of_characters = 150):
		available_characters = [
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
			'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
			'u', 'v', 'w', 'x', 'y', 'z'
		];

		while True:
			random_token = ''

			for i in range(0, amount_of_characters):
				random_token += random.choice(available_characters)

			if Password_Change_Requests.is_random_token_available(random_token):
				return random_token

	@staticmethod
	def is_random_token_available(random_token):
		return len(Password_Change_Requests.select_by_id(random_token, 1)) is 0

	@staticmethod
	def is_valid_random_token(time):
		return (
			(datetime.now() - time) <= timedelta(hours = 2)
		)
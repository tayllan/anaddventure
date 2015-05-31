from models.DAO import DAO
import random, hashlib

class Signup_Queue(DAO):

	def __init__(self, user_id):
		self.user_id = user_id
		self.id = Signup_Queue._generate_random_token()

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.signup_queue (
				signup_queue_system_user_id,
				signup_queue_id
			)
			VALUES (%s, %s)
			''',
			(
				self.user_id,
				hashlib.sha256(self.id.encode('utf-8')).hexdigest()
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_signup_queue_objects(signup_queues_array):
		return [
			{
				'user_id': user_id,
				'id': id
			}
			for
				user_id, id
			in
				signup_queues_array
		]

	@staticmethod
	def delete(user_id):
		DAO.delete(
			"DELETE FROM anaddventure.signup_queue WHERE signup_queue_system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def select_by_id(id, rows = None):
		return Signup_Queue._construct_signup_queue_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.signup_queue WHERE signup_queue_id LIKE (%s)",
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

			if Signup_Queue.is_random_token_available(random_token):
				return random_token

	@staticmethod
	def is_random_token_available(random_token):
		return len(Signup_Queue.select_by_id(random_token, 1)) is 0
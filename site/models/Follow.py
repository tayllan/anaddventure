from models.DAO import DAO

class Follow(DAO):

	def __init__(self, user_id, tale_id):
		self.user_id = user_id
		self.tale_id = tale_id

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.follow (
				follow_system_user_id,
				follow_tale_id
			)
			VALUES (%s, %s)
			''',
			(
				self.user_id,
				self.tale_id
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def delete_by_user_id(user_id):
		return DAO.delete(
			"DELETE FROM anaddventure.follow WHERE follow_system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.follow WHERE follow_tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def select_by_user_id(user_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.follow WHERE follow_system_user_id = (%s)",
			(user_id, ),
			rows
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.follow WHERE follow_tale_id = (%s)",
			(tale_id, ),
			rows
		)

	@staticmethod
	def select_by_user_id_and_tale_id(user_id, tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.follow WHERE follow_system_user_id = (%s) AND follow_tale_id = (%s)",
			(user_id, tale_id),
			rows
		)
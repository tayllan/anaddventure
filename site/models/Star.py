from models.DAO import DAO

class Star(DAO):

	def __init__(self, user_id, tale_id, date):
		self.user_id = user_id
		self.tale_id = tale_id
		self.date = date

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.star (
				star_system_user_id,
				star_tale_id,
				star_datetime
			)
			VALUES (%s, %s, %s)
			''',
			(
				self.user_id,
				self.tale_id,
				self.date
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def delete_by_user_id(user_id):
		return DAO.delete(
			"DELETE FROM anaddventure.star WHERE star_system_user_id = (%s)",
			(user_id, )
		)

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.star WHERE star_tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def select_by_user_id(user_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.star WHERE star_system_user_id = (%s)",
			(user_id, ),
			rows
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.star WHERE star_tale_id = (%s)",
			(tale_id, ),
			rows
		)

	@staticmethod
	def select_by_user_id_and_tale_id(user_id, tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.star WHERE star_system_user_id = (%s) AND star_tale_id = (%s)",
			(user_id, tale_id),
			rows
		)
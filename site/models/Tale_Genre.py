from models.DAO import DAO

class Tale_Genre(DAO):

	def __init__(self, tale_id, genre_id):
		self.tale_id = tale_id
		self.genre_id = genre_id

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.tale_genre (
				tale_genre_tale_id,
				tale_genre_genre_id
			)
			VALUES (%s, %s)
			''',
			(
				self.tale_id,
				self.genre_id
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.tale_genre WHERE tale_genre_tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.tale_genre WHERE tale_genre_tale_id = (%s)",
			(tale_id, ),
			rows
		)

	@staticmethod
	def select_by_genre_id(genre_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.tale_genre WHERE tale_genre_genre_id = (%s)",
			(genre_id, ),
			rows
		)

	@staticmethod
	def select_by_tale_id_and_genre_id(tale_id, genre_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.tale_genre WHERE tale_genre_tale_id = (%s) AND tale_genre_genre_id = (%s)",
			(tale_id, genre_id),
			rows
		)
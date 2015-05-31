from models.DAO import DAO

class Genre(DAO):

	def __init__(self, category):
		self.category = category

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.genre (
				genre_type
			)
			VALUES (%s)
			''',
			(
				self.category
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_genre_objects(genres_array):
		return [
			{
				'id': id,
				'type': type,
				'tale_count': tale_count
			}
			for
				id, type, tale_count
			in
				genres_array
		]

	@staticmethod
	def select_by_id(genre_id, rows = None):
		return Genre._construct_genre_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.genre WHERE genre_id = (%s)",
				(genre_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_type(category, rows = None):
		return Genre._construct_genre_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.genre WHERE genre_type ILIKE (%s)",
				('%' + category + '%', ),
				rows
			)
		)

	@staticmethod
	def select_all(rows = None):
		return Genre._construct_genre_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.genre",
				(),
				rows
			)
		)

	@staticmethod
	def select_top_ten(rows = None):
		return Genre._construct_genre_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.genre ORDER BY genre_tale_count DESC, genre_type ASC LIMIT 10",
				(),
				rows
			)
		)

	@staticmethod
	def is_genre_id_valid(genre_id):
		return len(Genre.select_by_id(genre_id, 1)) is not 0
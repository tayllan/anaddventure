from models.DAO import DAO
from config import cache

class Chapter(DAO):

	def __init__(self, user_id, tale_id, number, title, content, date, previous_chapter_id = None):
		self.user_id = user_id
		self.tale_id = tale_id
		self.number = number
		self.title = title
		self.content = content
		self.date = date
		self.previous_chapter_id = previous_chapter_id

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.chapter (
				chapter_system_user_id,
				chapter_tale_id,
				chapter_number,
				chapter_title,
				chapter_content,
				chapter_datetime,
				chapter_previous_chapter
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			''',
			(
				self.user_id,
				self.tale_id,
				self.number,
				self.title,
				self.content,
				self.date,
				self.previous_chapter_id
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_chapter_objects(chapters_array):
		return [
			{
				'id': id,
				'user_id': user_id,
				'tale_id': tale_id,
				'number': number,
				'title': title,
				'content': content,
				'date': date,
				'downloads': downloads,
				'previous_chapter_id': previous_chapter_id
			}
			for
				id, user_id, tale_id, number, title,
				content, date, downloads, previous_chapter_id
			in
				chapters_array
		]

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.chapter WHERE chapter_tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def update_title_and_content(chapter_id, title, content):
		return DAO.update(
			"UPDATE anaddventure.chapter SET chapter_title = (%s), chapter_content = (%s) WHERE chapter_id = (%s)",
			(title, content, chapter_id)
		)

	@staticmethod
	def update_download_count(chapter_id):
		return DAO.update(
			"UPDATE anaddventure.chapter SET chapter_download_count = chapter_download_count + 1 WHERE chapter_id = (%s)",
			(chapter_id, )
		)

	@staticmethod
	def select_by_id(chapter_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_id = (%s)",
				(chapter_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_user_id(user_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_system_user_id = (%s)",
				(user_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_tale_id = (%s)",
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_tale_id_order_by_date(tale_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_tale_id = (%s) ORDER BY chapter_datetime DESC",
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_number(number, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_number = (%s)",
				(number, ),
				rows
			)
		)

	@staticmethod
	def select_by_title(title, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_title ILIKE (%s)",
				('%' + title + '%', ),
				rows
			)
		)

	@staticmethod
	def select_by_date(date, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_datetime = (%s)",
				(date, ),
				rows
			)
		)

	@staticmethod
	def select_by_previous_chapter_id(previous_chapter_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_previous_chapter = (%s)",
				(previous_chapter_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_tale_id_and_previous_chapter_id(tale_id, previous_chapter_id, rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter WHERE chapter_tale_id = (%s) AND chapter_previous_chapter = (%s)",
				(tale_id, previous_chapter_id),
				rows
			)
		)

	@staticmethod
	@cache.cached(timeout = 86400)
	def select_all(rows = None):
		return Chapter._construct_chapter_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.chapter",
				(),
				rows
			)
		)

	@staticmethod
	def is_editable_chapter(chapter_id):
		return DAO.select_by(
			"SELECT COUNT(chapter_id) FROM anaddventure.chapter WHERE chapter_previous_chapter = (%s)",
			(chapter_id, )
		)[0][0]
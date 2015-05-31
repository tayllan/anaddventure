from models.DAO import DAO

class Contribution_Request(DAO):

	def __init__(
			self, user_id, tale_id,
			number, title, content,
			date, previous_chapter_id = None, was_accepted = False,
			was_closed = False
	):
		self.user_id = user_id
		self.tale_id = tale_id
		self.number = number
		self.title = title
		self.content = content
		self.date = date
		self.previous_chapter_id = previous_chapter_id
		self.was_accepted = was_accepted
		self.was_closed = was_closed

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.contribution_request (
				contribution_request_system_user_id,
				contribution_request_tale_id,
				contribution_request_number,
				contribution_request_title,
				contribution_request_content,
				contribution_request_datetime,
				contribution_request_previous_chapter,
				contribution_request_was_accepted,
				contribution_request_was_closed
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
			''',
			(
				self.user_id,
				self.tale_id,
				self.number,
				self.title,
				self.content,
				self.date,
				self.previous_chapter_id,
				self.was_accepted,
				self.was_closed
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_contribution_request_objects(contribution_requests_array):
		return [
			{
				'id': id,
				'user_id': user_id,
				'tale_id': tale_id,
				'number': number,
				'title': title,
				'content': content,
				'datetime': date,
				'previous_chapter_id': previous_chapter_id,
				'was_accepted': was_accepted,
				'was_closed': was_closed,
			}
			for
				id, user_id, tale_id, number, title, content,
				date, previous_chapter_id, was_accepted, was_closed
			in
				contribution_requests_array
		]

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.contribution_request WHERE contribution_request_tale_id = (%s)",
			(tale_id, )
		)

	# accepted or refused, the contribution_request is automatically closed
	@staticmethod
	def update_was_accepted(contribution_request_id, was_accepted):
		return DAO.update(
			'''
			UPDATE anaddventure.contribution_request
				SET contribution_request_was_accepted = (%s),
					contribution_request_was_closed = True
				WHERE contribution_request_id = (%s)
			''',
			(was_accepted, contribution_request_id)
		)

	@staticmethod
	def select_by_id(contribution_request_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.contribution_request WHERE contribution_request_id = (%s)",
				(contribution_request_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_user_id(user_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.contribution_request WHERE contribution_request_system_user_id = (%s)",
				(user_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.contribution_request WHERE contribution_request_tale_id = (%s)",
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_tale_id_order_by_datetime(tale_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				'''
				SELECT * FROM anaddventure.contribution_request
					WHERE contribution_request_tale_id = (%s)
					ORDER BY contribution_request_datetime DESC
				''',
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_open_by_tale_id_order_by_datetime(tale_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				'''
				SELECT * FROM anaddventure.contribution_request
					WHERE contribution_request_tale_id = (%s) AND
					contribution_request_was_closed = False
					ORDER BY contribution_request_datetime DESC;
				''',
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_closed_by_tale_id_order_by_datetime(tale_id, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				'''
				SELECT * FROM anaddventure.contribution_request
					WHERE contribution_request_tale_id = (%s) AND
					contribution_request_was_closed = True
					ORDER BY contribution_request_datetime DESC;
				''',
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_was_accepted(was_accepted, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.contribution_request WHERE contribution_request_was_accepted = (%s)",
				(was_accepted, ),
				rows
			)
		)

	@staticmethod
	def select_by_was_closed(was_closed, rows = None):
		return Contribution_Request._construct_contribution_request_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.contribution_request WHERE contribution_request_was_closed = (%s)",
				(was_closed, ),
				rows
			)
		)

	@staticmethod
	def is_title_valid(title):
		return 1 <= len(title) <= 500

	@staticmethod
	def is_content_valid(content):
		return len(content) > 0
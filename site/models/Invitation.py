from models.DAO import DAO

class Invitation(DAO):

	def __init__(self, creator_id, invited_id, tale_id):
		self.creator_id = creator_id
		self.invited_id = invited_id
		self.tale_id = tale_id

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.invitation (
				invitation_creator,
				invitation_invited,
				invitation_tale_id
			)
			VALUES (%s, %s, %s)
			''',
			(
				self.creator_id,
				self.invited_id,
				self.tale_id
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def delete_by_tale_id(tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.invitation WHERE invitation_tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def delete_by_invited_id_and_tale_id(invited_id, tale_id):
		return DAO.delete(
			"DELETE FROM anaddventure.invitation WHERE invitation_invited = (%s) AND invitation_tale_id = (%s)",
			(invited_id, tale_id)
		)

	@staticmethod
	def select_by_creator_id(creator_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.invitation WHERE invitation_creator = (%s)",
			(creator_id, ),
			rows
		)

	@staticmethod
	def select_by_invited_id(invited_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.invitation WHERE invitation_invited = (%s)",
			(invited_id, ),
			rows
		)

	@staticmethod
	def select_by_tale_id(tale_id, rows = None):
		return DAO.select_by(
			"SELECT * FROM anaddventure.invitation WHERE invitation_tale_id = (%s)",
			(tale_id, ),
			rows
		)
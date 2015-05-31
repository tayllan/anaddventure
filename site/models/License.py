from models.DAO import DAO

class License(DAO):

	def __init__(self, name, url):
		self.name = name
		self.url = url

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.license (
				license_name,
				license_url
			)
			VALUES (%s, %s)
			''',
			(
				self.name,
				self.url
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_license_objects(licenses_array):
		return [
			{
				'id': id,
				'name': name,
				'url': url
			}
			for
				id, name, url
			in
				licenses_array
		]

	@staticmethod
	def select_by_id(id, rows = None):
		return License._construct_license_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.license WHERE license_id = (%s)",
				(id, ),
				rows
			)
		)

	@staticmethod
	def select_by_name(name, rows = None):
		return License._construct_license_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.license WHERE license_name ILIKE (%s)",
				('%' + name + '%', ),
				rows
			)
		)

	@staticmethod
	def select_all(rows = None):
		return License._construct_license_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.license",
				(),
				rows
			)
		)

	@staticmethod
	def is_license_id_valid(license_id):
		return len(License.select_by_id(license_id, 1)) is not 0
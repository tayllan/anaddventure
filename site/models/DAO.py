import psycopg2

class DAO:

	connection_string = "host='localhost' dbname='tales' user='anaddventure' password='dozeDolares'"
	connection = psycopg2.connect(connection_string)

	@staticmethod
	def delete(delete_string, parameters):
		cursor = DAO.connection.cursor()
		cursor.execute(delete_string, parameters)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def update(update_string, parameters):
		cursor = DAO.connection.cursor()
		cursor.execute(update_string, parameters)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def select_by(select_string, parameters, rows = None):
		cursor = DAO.connection.cursor()
		cursor.execute(select_string, parameters)
		return_object = []

		if rows is None:
			return_object = cursor.fetchall()
		else:
			return_object = cursor.fetchmany(rows)

		DAO.connection.commit()
		cursor.close()

		return return_object

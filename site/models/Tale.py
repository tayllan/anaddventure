from models.DAO import DAO
from config import cache

class Tale(DAO):

	def __init__(self, title, description, category, creator_id, license_id, creation_datetime):
		self.title = title
		self.description = description
		self.category = category
		self.creator_id = creator_id
		self.license_id = license_id
		self.creation_datetime = creation_datetime

	def insert(self):
		cursor = DAO.connection.cursor()
		cursor.execute(
			'''
			INSERT INTO anaddventure.tale (
				tale_title,
				tale_description,
				tale_category,
				tale_creator,
				tale_license,
				tale_creation_datetime
			)
			VALUES (%s, %s, %s, %s, %s, %s)
			''',
			(
				self.title,
				self.description,
				self.category,
				self.creator_id,
				self.license_id,
				self.creation_datetime
			)
		)
		DAO.connection.commit()
		cursor.close()

	@staticmethod
	def _construct_tale_objects(tales_array):
		return [
			{
				'id': id,
				'title': title,
				'description': description,
				'category': category,
				'creator_id': creator_id,
				'license_id': license_id,
				'stars': star_count,
				'followers': follow_count,
				'contribution_requests': contribution_request_count,
				'creation_datetime': creation_datetime
			}
			for
				id, title, description, category, creator_id, license_id,
				star_count, follow_count, contribution_request_count, creation_datetime
			in
				tales_array
		]

	@staticmethod
	def delete(tale_id):
		DAO.delete(
			"DELETE FROM anaddventure.tale WHERE tale_id = (%s)",
			(tale_id, )
		)

	@staticmethod
	def update_all(tale_id, title, description, category, license_id):
		DAO.update(
			'''
			UPDATE anaddventure.tale
				SET tale_title = (%s),
					tale_description = (%s),
					tale_category = (%s),
					tale_license = (%s)
				WHERE tale_id = (%s)
			''',
			(title, description, category, license_id, tale_id)
		)

	@staticmethod
	def update_star_count(tale_id, value):
		DAO.update(
			'''
			UPDATE anaddventure.tale
				SET tale_star_count = tale_star_count + (%s)
				WHERE tale_id = (%s)
			''',
			(value, tale_id)
		)

	@staticmethod
	def update_follow_count(tale_id, value):
		DAO.update(
			'''
			UPDATE anaddventure.tale
				SET tale_follow_count = tale_follow_count + (%s)
				WHERE tale_id = (%s)
			''',
			(value, tale_id)
		)

	@staticmethod
	def update_contribution_request_count(tale_id, value):
		DAO.update(
			'''
			UPDATE anaddventure.tale
				SET tale_contribution_request_count = tale_contribution_request_count + (%s)
				WHERE tale_id = (%s)
			''',
			(value, tale_id)
		)

	@staticmethod
	def select_by_id(tale_id, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_id = (%s)",
				(tale_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_title(title = '', rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_title ILIKE (%s)",
				('%' + title + '%', ),
				rows
			)
		)

	@staticmethod
	def select_by_full_title(title = '', rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_title ILIKE (%s)",
				(title, ),
				rows
			)
		)

	@staticmethod
	def select_count_by_title(title = '', rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT COUNT(tale_id) FROM anaddventure.tale WHERE tale_title ILIKE (%s)",
				('%' + title + '%', ),
				rows
			)
		)

	@staticmethod
	def select_by_category(category = '', rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_category = (%s)",
				(category, ),
				rows
			)
		)

	@staticmethod
	def select_by_creator_id(creator_id, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_creator = (%s)",
				(creator_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_license_id(license_id, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_license = (%s)",
				(license_id, ),
				rows
			)
		)

	@staticmethod
	def select_by_creator_id_and_full_title(creator_id, title, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_creator = (%s) AND tale_title ILIKE (%s)",
				(creator_id, title),
				rows
			)
		)

	@staticmethod
	@cache.cached(timeout = 86400)
	def select_all(rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale",
				(),
				rows
			)
		)

	# the name says top 10, but it's actually top 5 (too much work to refactor it)
	@staticmethod
	def select_top_ten_order_by_star_count():
		return Tale._construct_tale_objects(
			DAO.select_by(
				"SELECT * FROM anaddventure.tale WHERE tale_category = 1 ORDER BY tale_star_count DESC LIMIT 5",
				()
			)
		)

	# the name says top 10, but it's actually top 5 (too much work to refactor it)
	@staticmethod
	def select_top_ten_order_by_star_count_today():
		tales_aux =  DAO.select_by(
			'''
			SELECT *, (
				SELECT COUNT(*) AS star_count_today FROM anaddventure.star
					WHERE star_tale_id = tale_id AND
					star_datetime >= CURRENT_DATE + interval '1 second'
			) FROM anaddventure.tale
				WHERE tale_category = 1
				ORDER BY star_count_today DESC LIMIT 5
			''',
			()
		)

		tales = Tale._construct_tale_objects([tale[:10] for tale in tales_aux])

		for i in range(0, len(tales)):
			tales[i]['stars_today'] = tales_aux[i][10]

		return tales

	@staticmethod
	def select_tales_other_creator(user_id, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				'''
				SELECT DISTINCT
					tale_id, tale_title, tale_description,
					tale_category, tale_creator, tale_license,
					tale_star_count, tale_follow_count,
					tale_contribution_request_count, tale_creation_datetime
					FROM anaddventure.chapter INNER JOIN anaddventure.tale ON
					chapter_system_user_id = (%s) AND
					tale_creator != chapter_system_user_id AND
					tale_id = chapter_tale_id;
				''',
				(user_id, ),
				rows
			)
		)

	@staticmethod
	def select_tales_other_creator_by_title_with_offset_and_limit(
			user_id, viewer_id, title, offset, limit = 5, rows = None
		):
		return Tale._construct_tale_objects(
			DAO.select_by(
				'''
				SELECT DISTINCT
					tale_id, tale_title, tale_description,
					tale_category, tale_creator, tale_license,
					tale_star_count, tale_follow_count,
					tale_contribution_request_count, tale_creation_datetime
					FROM anaddventure.tale INNER JOIN anaddventure.contribution_request ON
					contribution_request_system_user_id = (%s) AND
					tale_creator != contribution_request_system_user_id AND
					tale_id = contribution_request_tale_id AND
					(
						tale_category = 1 OR
						(
							(
								SELECT COUNT(*) FROM anaddventure.invitation WHERE
									invitation_creator = tale_creator AND
									invitation_invited = contribution_request_system_user_id
							) > 0 AND
							(
								SELECT COUNT(*) FROM anaddventure.invitation WHERE
									invitation_creator = tale_creator AND
									invitation_invited = (%s)
							) > 0
						)
					) AND
					tale_title ILIKE (%s)
					ORDER BY tale_star_count DESC OFFSET (%s) LIMIT (%s)
				''',
				(user_id, viewer_id, '%' + title + '%', offset, limit),
				rows
			)
		)

	@staticmethod
	def select_by_title_and_genre_id(title, genre_id, rows = None):
		return DAO.select_by(
			'''
			SELECT * FROM anaddventure.tale INNER JOIN anaddventure.tale_genre ON
				tale_genre_genre_id = (%s) AND
				tale_id = tale_genre_tale_id AND
				tale_title ILIKE (%s)
			''',
			(genre_id, '%' + title + '%'),
			rows
		)

	@staticmethod
	def select_viewable_by_creator_id_and_viewer_id_and_title_with_offset_and_limit(
			creator_id, viewer_id, title, offset, limit = 5, rows = None
		):
		return Tale._construct_tale_objects(
			DAO.select_by(
				'''
				SELECT DISTINCT
					tale_id, tale_title, tale_description,
					tale_category, tale_creator, tale_license,
					tale_star_count, tale_follow_count,
					tale_contribution_request_count, tale_creation_datetime
					FROM anaddventure.tale INNER JOIN anaddventure.invitation ON
					tale_creator = (%s) AND
					(
						tale_category = 1 OR
						(
							invitation_creator = tale_creator AND
							invitation_invited = (%s) AND
							invitation_tale_id = tale_id
						) OR
						tale_creator = (%s)
					) AND
					tale_title ILIKE (%s)
					ORDER BY tale_star_count DESC OFFSET (%s) LIMIT (%s)
				''',
				(creator_id, viewer_id, viewer_id, '%' + title + '%', offset, limit),
				rows
			)
		)

	@staticmethod
	def select_viewable_by_title_and_creator_id(title, creator_id, rows = None):
		return Tale._construct_tale_objects(
			DAO.select_by(
				'''
				SELECT * FROM anaddventure.tale
					WHERE tale_title ILIKE (%s) AND
					(
						tale_category = 1 OR
						tale_creator = (%s)
					)
				''',
				('%' + title + '%', creator_id),
				rows
			)
		)

	@staticmethod
	def select_viewable_by_title_creator_id_and_genre_id(title, creator_id, genre_id, rows = None):
		tales_aux = DAO.select_by(
			'''
			SELECT * FROM anaddventure.tale INNER JOIN anaddventure.tale_genre ON
				tale_genre_genre_id = (%s) AND
				tale_id = tale_genre_tale_id AND
				tale_title ILIKE (%s) AND
				(tale_category = 1 OR tale_creator = (%s))
			''',
			(genre_id, '%' + title + '%', creator_id),
			rows
		)

		return Tale._construct_tale_objects([tale[:10] for tale in tales_aux])

	@staticmethod
	def select_count_viewable_by_title_and_creator_id(title, creator_id, rows = None):
		return DAO.select_by(
			'''
			SELECT COUNT(tale_id) FROM anaddventure.tale
				WHERE tale_title ILIKE (%s) AND (tale_category = 1 OR tale_creator = (%s))
			''',
			('%' + title + '%', creator_id),
			rows
		)

	@staticmethod
	def select_contributors_id(tale_id, rows = None):
		return DAO.select_by(
			'''
			SELECT DISTINCT chapter_system_user_id
				FROM anaddventure.tale INNER JOIN anaddventure.chapter ON
				tale_id = (%s) AND
				tale_id = chapter_tale_id
			''',
			(tale_id, ),
			rows
		)

	@staticmethod
	def select_last_update(tale_id, rows = None):
		return DAO.select_by(
			'''
			 SELECT MAX(chapter_datetime)
			 	FROM anaddventure.chapter INNER JOIN anaddventure.tale ON
			 	tale_id = (%s) AND
			 	chapter_tale_id = tale_id
			''',
			(tale_id, ),
			rows
		)

	@staticmethod
	@cache.memoize()
	def select_chapters_count(tale_id, rows = None):
		return DAO.select_by(
			"SELECT COUNT(*) FROM anaddventure.chapter WHERE chapter_tale_id = (%s)",
			(tale_id, ),
			rows
		)

	@staticmethod
	def is_title_valid(title):
		return len(title) > 2

	@staticmethod
	def is_title_available(creator_id, title):
		return len(Tale.select_by_creator_id_and_full_title(creator_id, title, 1)) is 0

	@staticmethod
	def is_description_valid(description):
		return True
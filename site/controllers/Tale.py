from flask import request, session, render_template, redirect, jsonify, make_response
from languages import strings
from models.Chapter import Chapter
from models.Contribution_Request import Contribution_Request
from models.Follow import Follow
from models.Genre import Genre
from models.Invitation import Invitation
from models.License import License
from models.Star import Star
from models.Tale import Tale
from models.Tale_Genre import Tale_Genre
from models.User import User
from controllers import aux
from config import www, pt, app

# BEGIN Tale Controller
@www.route('/tale/<int:tale_id>/<int:chapter_id>/')
@pt.route('/tale/<int:tale_id>/<int:chapter_id>/')
@www.route('/tale/<int:tale_id>/<int:chapter_id>/fullscreen')
@pt.route('/tale/<int:tale_id>/<int:chapter_id>/fullscreen')
def tale(tale_id, chapter_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		if chapter_id is 0:
			chapter = Chapter.select_by_tale_id_and_previous_chapter_id(tale['id'], -1, 1)
		else:
			chapter = Chapter.select_by_id(chapter_id, 1)

		# no chapter with this ID
		if len(chapter) is 0:
			if chapter_id is 0:
				chapter = None
			else:
				return redirect('/404')
		else:
			chapter = chapter[0]
			next_chapters = Chapter.select_by_tale_id_and_previous_chapter_id(tale['id'], chapter['id'])

			chapter['datetime'] = aux.beautify_datetime(chapter['date'])
			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			chapter['next_chapters'] = next_chapters
			chapter['is_editable'] = tale['creator_id'] is session.get('user_logged_id', None)

		tale['chapter'] = chapter

		return aux.return_rendered_tale_template(tale, 'tale.html')
	else:
		return redirect('/404')

@www.route('/tale/add/')
@pt.route('/tale/add/')
def tale_add_get():
	if 'user_logged_id' in session:
		return render_template('tale_add.html', genres = Genre.select_all(), licenses = License.select_all())
	else:
		return redirect('/404')

@www.route('/tale/add/', methods = ['POST'])
@pt.route('/tale/add/', methods = ['POST'])
def tale_add_post():
	if request.is_xhr and 'user_logged_id' in session:
		title = request.form.get('tale-add-title', '')
		description = request.form.get('tale-add-description', '')
		category = 2 if int(request.form.get('tale-add-type', 1)) is  not 1 else 1
		genres = request.form.getlist('tale-add-genres')
		license_id = request.form.get('tale-add-license', -1)
		creator_id = session['user_logged_id']
		language = session.get('language', 'en')

		error_list = list()

		if Tale.is_title_available(creator_id, title):
			if not Tale.is_title_valid(title):
				error_list.append(strings.STRINGS[language]['INVALID_TITLE'])
		else:
			error_list.append(strings.STRINGS[language]['TITLE_TAKEN'])

		if not Tale.is_description_valid(description):
			error_list.append(strings.STRINGS[language]['INVALID_DESCRIPTION'])

		if not License.is_license_id_valid(license_id):
			error_list.append(strings.STRINGS[language]['INVALID_LICENSE'])

		if len(genres) is not 0:
			for genre_id in genres:
				if not Genre.is_genre_id_valid(genre_id):
					error_list.append(strings.STRINGS[language]['INVALID_GENRE'])
					break
		else:
			error_list.append(strings.STRINGS[language]['NO_GENRES'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			new_tale = Tale(title, description, category, creator_id, license_id, aux.get_current_datetime_as_string())
			new_tale.insert()

			tale_id = Tale.select_by_creator_id_and_full_title(creator_id, title, 1)[0]['id']

			for genre_id in genres:
				new_tale_genre = Tale_Genre(tale_id, genre_id)
				new_tale_genre.insert()

			if category is 2:
				invitation = Invitation(creator_id, creator_id, tale_id)
				invitation.insert()

			return jsonify(url = '/tale/' + str(tale_id) + '/0')
	else:
		return redirect('/404')

@www.route('/tale/edit/<int:tale_id>/')
@pt.route('/tale/edit/<int:tale_id>/')
def tale_edit_get(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		tale = tale[0]

		tale_genres = Tale_Genre.select_by_tale_id(tale_id)
		tale_genres_ids_set = set()

		for tale_genre in tale_genres:
			tale_genres_ids_set.add(tale_genre[1])

		genres = Genre.select_all()
		genres_list = list()

		for genre in genres:
			genre['checked'] = True if genre['id'] in tale_genres_ids_set else False
			genres_list.append(genre)

		licenses = License.select_all()
		licenses_list = list()

		for license in licenses:
			license['selected'] = True if tale['license_id'] is license['id'] else False
			licenses_list.append(license)

		return aux.return_rendered_tale_template(
			tale,
			'tale_edit.html',
			genres_list = genres_list,
			licenses_list = licenses_list
		)
	else:
		return redirect('/404')

@www.route('/tale/edit/<int:tale_id>/', methods = ['POST'])
@pt.route('/tale/edit/<int:tale_id>/', methods = ['POST'])
def tale_edit_post(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if request.is_xhr and len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		tale = tale[0]
		title = request.form.get('tale-edit-title', '')
		description = request.form.get('tale-edit-description', '')
		category = 2 if int(request.form.get('tale-edit-type', 1)) is not 1 else 1
		genres = request.form.getlist('tale-edit-genres')
		license_id = request.form.get('tale-edit-license', -1)
		creator_id = session['user_logged_id']
		language = session.get('language', 'en')

		error_list = list()

		if tale['title'] == title or Tale.is_title_available(creator_id, title):
			if not Tale.is_title_valid(title):
				error_list.append(strings.STRINGS[language]['INVALID_TITLE'])
		else:
			error_list.append(strings.STRINGS[language]['TITLE_TAKEN'])

		if not Tale.is_description_valid(description):
			error_list.append(strings.STRINGS[language]['INVALID_DESCRIPTION'])

		if not License.is_license_id_valid(license_id):
			error_list.append(strings.STRINGS[language]['INVALID_LICENSE'])

		if len(genres) is not 0:
			for genre_id in genres:
				if not Genre.is_genre_id_valid(genre_id):
					error_list.append(strings.STRINGS[language]['INVALID_GENRE'])
					break
		else:
			error_list.append(strings.STRINGS[language]['NO_GENRES'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			tale_last_category = int(tale['category'])

			if tale_last_category is not category:
				if tale_last_category is 1:
					contributors = Tale.select_contributors_id(tale_id)

					for contributor_id in contributors:
						new_invitation = Invitation(creator_id, contributor_id, tale_id)
						new_invitation.insert()
				else:
					Invitation.delete_by_tale_id(tale_id)

			Tale.update_all(tale_id, title, description, category, license_id)
			Tale_Genre.delete_by_tale_id(tale_id)

			for genre_id in genres:
				new_tale_genre = Tale_Genre(tale_id, genre_id)
				new_tale_genre.insert()

			return jsonify(url = '/tale/' + str(tale_id) + '/0')
	else:
		return redirect('/404')

@www.route('/tale/delete/<int:tale_id>/', methods = ['POST'])
@pt.route('/tale/delete/<int:tale_id>/', methods = ['POST'])
def tale_delete(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if request.is_xhr and len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		tale = tale[0]
		creator = User.select_by_id(tale['creator_id'], 1)[0]

		email_object = strings.construct_delete_tale_email_object(
			session.get('language', 'en'),
			tale,
			creator,
			app.config['SITE_NAME']
		)

		aux.send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

		Chapter.delete_by_tale_id(tale['id'])
		Contribution_Request.delete_by_tale_id(tale['id'])
		Follow.delete_by_tale_id(tale['id'])
		Invitation.delete_by_tale_id(tale['id'])
		Star.delete_by_tale_id(tale['id'])
		Tale_Genre.delete_by_tale_id(tale['id'])
		Tale.delete(tale['id'])

		return jsonify(url = '/profile/' + creator['username'])
	else:
		redirect('/404')

@www.route('/tale/collaborations/<int:tale_id>/')
@pt.route('/tale/collaborations/<int:tale_id>/')
def collaborations(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		chapters = Chapter.select_by_tale_id_order_by_date(tale_id)
		chapters_dict = dict()

		for chapter in chapters:
			date = aux.beautify_datetime(chapter['date'])

			if date not in chapters_dict:
				chapters_dict[date] = list()

			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			chapters_dict[date].append(chapter)

		keys = list(chapters_dict.keys())
		keys.sort(reverse = True)

		return aux.return_rendered_tale_template(
			tale,
			'collaborations.html',
			contributions_object = {
				'keys': keys,
				'content': chapters_dict
			}
		)
	else:
		return redirect('/404')

@www.route('/tale/branches/<int:tale_id>/')
@pt.route('/tale/branches/<int:tale_id>/')
def branches(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		chapters = Chapter.select_by_tale_id(tale_id)
		number_bundle = dict()

		for chapter in chapters:
			number = chapter['number']

			if number not in number_bundle:
				number_bundle[number] = {'number': number, 'contributions': list()}

			chapter['date'] = aux.beautify_datetime(chapter['date'])
			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			number_bundle[number]['contributions'].append(chapter)

		return aux.return_rendered_tale_template(tale, 'branches.html', branches_object = number_bundle)
	else:
		return redirect('/404')

@www.route('/tale/contributors/<int:tale_id>/')
@pt.route('/tale/contributors/<int:tale_id>/')
def contributors(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		contributors = Chapter.select_by_tale_id(tale_id)
		contributors_dict = dict()

		creator = User.select_by_id(tale['creator_id'], 1)[0]
		contributors_dict[creator['id']] = {'username': creator['username'], 'count': 0}

		for c in contributors:
			contributor = User.select_by_id(c['user_id'], 1)[0]

			if contributor['id'] not in contributors_dict:
				contributors_dict[contributor['id']] = {'username': contributor['username'], 'count': 0}

			contributors_dict[contributor['id']]['count'] += 1

		return aux.return_rendered_tale_template(
			tale, 'contributors.html', contributors_object = contributors_dict
		)
	else:
		return redirect('/404')
# END Tale Controller

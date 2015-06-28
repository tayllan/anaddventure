from flask import request, session, render_template, redirect, jsonify, make_response
from languages import strings
from models.Chapter import Chapter
from models.Contribution_Request import Contribution_Request
from models.Tale import Tale
from models.User import User
from controllers import aux
from config import www, pt, app

# BEGIN Collaboration Controller
@www.route('/collaboration/<int:contribution_request_id>/')
@pt.route('/collaboration/<int:contribution_request_id>/')
def collaboration(contribution_request_id):
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]
		tale = aux.is_visible_tale(contribution_request['tale_id'], session.get('user_logged_id', None))

		if tale:
			contribution_request['user_username'] = User.select_by_id(
				contribution_request['user_id'],
				1
			)[0]['username']
			contribution_request['datetime'] = aux.beautify_datetime(contribution_request['datetime'])

			return aux.return_rendered_tale_template(tale, 'collaboration.html', contribution = contribution_request)
		else:
			return redirect('/404')
	else:
		return redirect('/404')

@www.route('/collaboration/add/<int:tale_id>/<int:chapter_id>/')
@pt.route('/collaboration/add/<int:tale_id>/<int:chapter_id>/')
def collaboration_add_get(tale_id, chapter_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))
	chapter = Chapter.select_by_id(chapter_id, 1)

	if tale and 'user_logged_id' in session and (
		((len(chapter) is not 0 and int(chapter[0]['tale_id']) is tale_id)) or
		(chapter_id is 0 and len(Chapter.select_by_tale_id_and_previous_chapter_id(tale_id, -1)) is 0)):

		return render_template('collaboration_add.html', tale_id = tale_id, chapter_id = chapter_id)
	elif 'user_logged_id' not in session:
		return redirect('/join?redirect=/collaboration/add/' + str(tale_id) + '/' + str(chapter_id))
	else:
		return redirect('/404')

@www.route('/collaboration/add/<int:tale_id>/<int:chapter_id>/', methods = ['POST'])
@pt.route('/collaboration/add/<int:tale_id>/<int:chapter_id>/', methods = ['POST'])
def collaboration_add_post(tale_id, chapter_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))
	chapter = Chapter.select_by_id(chapter_id, 1)

	if request.is_xhr and tale and 'user_logged_id' in session and (
		((len(chapter) is not 0 and int(chapter[0]['tale_id']) is tale_id)) or
		(chapter_id is 0 and len(Chapter.select_by_tale_id_and_previous_chapter_id(tale_id, -1)) is 0)):

		creator = tale['creator_id']
		user_id = session['user_logged_id']
		title = request.form.get('collaboration-add-title', '')
		content = request.form.get('collaboration-add-content', '')
		language = session.get('language', 'en')

		error_list = list()

		if not Contribution_Request.is_title_valid(title):
			error_list.append(strings.STRINGS[language]['INVALID_TITLE'])

		if not Contribution_Request.is_content_valid(content):
			error_list.append(strings.STRINGS[language]['INVALID_CONTENT'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			email_object = {}
			creator_username = User.select_by_id(user_id, 1)[0]['username']

			if creator is user_id:
				if chapter_id is 0:
					new_chapter = Chapter(
						user_id,
						tale_id,
						1,
						title,
						content,
						aux.get_current_datetime_as_string(),
						-1
					)
					new_chapter.insert()

					email_object = strings.construct_new_chapter_email_object(
						language,
						tale,
						creator_username,
						1,
						app.config['SITE_NAME'],
						app.config['SITE_URL'],
						0
					)
				else:
					chapter = Chapter.select_by_id(chapter_id, 1)[0]
					date = aux.get_current_datetime_as_string()
					new_chapter = Chapter(
						user_id,
						tale_id,
						chapter['number'] + 1,
						title,
						content,
						date,
						chapter['id']
					)
					new_chapter.insert()
					new_chapter_id = Chapter.select_by_date(date, 1)[0]['id']

					email_object = strings.construct_new_chapter_email_object(
						language,
						tale,
						creator_username,
						chapter['number'] + 1,
						app.config['SITE_NAME'],
						app.config['SITE_URL'],
						new_chapter_id
					)
			else:
				chapter = Chapter.select_by_id(chapter_id, 1)[0]
				new_contribution_request = Contribution_Request(
					user_id,
					tale_id,
					chapter['number'] + 1,
					title,
					content,
					aux.get_current_datetime_as_string(),
					chapter['id']
				)
				new_contribution_request.insert()
				Tale.update_contribution_request_count(tale_id, 1)

				email_object = strings.construct_new_contribution_request_email_object(
					language,
					tale,
					creator_username,
					app.config['SITE_NAME'],
					app.config['SITE_URL']
				)

			aux.send_email_to_followers(tale_id, email_object['title'], email_object['body'])

			return jsonify(url = '/tale/' + str(tale_id) + '/' + str(chapter_id))
	else:
		return redirect('/404')

@www.route('/collaboration/edit/<int:contribution_request_id>/')
@pt.route('/collaboration/edit/<int:contribution_request_id>/')
def collaboration_edit_get(contribution_request_id):
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if (len(contribution_request) is not 0 and
			session.get('user_logged_id', None) is contribution_request[0]['user_id'] and
			not contribution_request[0]['was_closed']):
		return render_template('collaboration_edit.html', contribution_request = contribution_request[0])
	else:
		return redirect('/404')

@www.route('/collaboration/edit/<int:contribution_request_id>/', methods = ['POST'])
@pt.route('/collaboration/edit/<int:contribution_request_id>/', methods = ['POST'])
def collaboration_edit_post(contribution_request_id):
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if (request.is_xhr and len(contribution_request) is not 0 and
			session.get('user_logged_id', None) is contribution_request[0]['user_id'] and
			not contribution_request[0]['was_closed']):
		contribution_request = contribution_request[0]
		title = request.form.get('collaboration-edit-title', '')
		content = request.form.get('collaboration-edit-content', '')
		language = session.get('language', 'en')

		error_list = list()

		if not Contribution_Request.is_title_valid(title):
			error_list.append(strings.STRINGS[language]['INVALID_TITLE'])

		if not Contribution_Request.is_content_valid(content):
			error_list.append(strings.STRINGS[language]['INVALID_CONTENT'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			Contribution_Request.update_title_and_content(contribution_request_id, title, content)

			return jsonify(url = '/collaboration/' + str(contribution_request_id))
	else:
		return redirect('/404')
# END Collaboration Controller

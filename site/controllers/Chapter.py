from flask import request, session, render_template, redirect, jsonify, make_response
from languages import strings
from models.Chapter import Chapter
from models.Contribution_Request import Contribution_Request
from models.Tale import Tale
from models.User import User
from controllers import aux
from config import www, pt, app

# BEGIN Chapter Controller
@www.route('/chapter/edit/<int:chapter_id>/')
@pt.route('/chapter/edit/<int:chapter_id>/')
def chapter_edit_get(chapter_id):
	chapter = Chapter.select_by_id(chapter_id, 1)

	if len(chapter) is not 0 and session.get('user_logged_id', None) is chapter[0]['user_id']:
		return render_template('chapter_edit.html', chapter = chapter[0])
	else:
		return redirect('/404')

@www.route('/chapter/edit/<int:chapter_id>/', methods = ['POST'])
@pt.route('/chapter/edit/<int:chapter_id>/', methods = ['POST'])
def chapter_edit_post(chapter_id):
	chapter = Chapter.select_by_id(chapter_id, 1)
	creator_id = session.get('user_logged_id', None)

	if request.is_xhr and len(chapter) is not 0 and creator_id is chapter[0]['user_id']:
		chapter = chapter[0]
		title = request.form.get('chapter-edit-title', '')
		content = request.form.get('chapter-edit-content', '')
		language = session.get('language', 'en')

		error_list = list()

		if not Contribution_Request.is_title_valid(title):
			error_list.append(strings.STRINGS[language]['INVALID_TITLE'])

		if not Contribution_Request.is_content_valid(content):
			error_list.append(strings.STRINGS[language]['INVALID_CONTENT'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			Chapter.update_title_and_content(chapter_id, title, content)
			tale = Tale.select_by_id(chapter['tale_id'], 1)[0]

			email_object = strings.construct_updated_chapter_email_object(
				language,
				tale,
				User.select_by_id(creator_id, 1)[0]['username'],
				chapter['number'],
				chapter['id']
			)

			aux.send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

			return jsonify(url = '/tale/' + str(chapter['tale_id']) + '/' + str(chapter_id))
	else:
		return redirect('/404')

@www.route('/chapter/download/<int:chapter_id>/', methods = ['GET', 'POST'])
@pt.route('/chapter/download/<int:chapter_id>/', methods = ['GET', 'POST'])
def chapter_download(chapter_id):
	chapter = Chapter.select_by_id(chapter_id, 1)

	if len(chapter) is not 0:
		chapter = chapter[0]
		chapter['datetime'] = aux.beautify_datetime(chapter['date'])
		chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']

		if request.method == 'POST':
			Chapter.update_download_count(chapter_id)

		return render_template('fragment/downloadable_chapter.html', chapter = chapter)
	else:
		return redirect('/404')

@www.route('/chapter/download_all/<int:chapter_id>/', methods = ['GET', 'POST'])
@pt.route('/chapter/download_all/<int:chapter_id>/', methods = ['GET', 'POST'])
def chapter_download_all(chapter_id):
	chapter = Chapter.select_by_id(chapter_id, 1)

	if len(chapter) is not 0:
		chapter = chapter[0]
		chapter_list = list()
		chapters_ids_list = list()
		previous_chapter_id = chapter_id
		tale = Tale.select_by_id(chapter['tale_id'], 1)[0]

		while previous_chapter_id is not -1:
			chapters_ids_list.append(previous_chapter_id)
			chapter = Chapter.select_by_id(previous_chapter_id, 1)[0]
			previous_chapter_id = chapter['previous_chapter_id']

		for chapter_id in reversed(chapters_ids_list):
			chapter = Chapter.select_by_id(chapter_id, 1)[0]

			if request.method == 'POST':
				Chapter.update_download_count(chapter_id)

			chapter['datetime'] = aux.beautify_datetime(chapter['date'])
			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			chapter_list.append(chapter)

		return render_template('fragment/downloadable_all.html', tale = tale, chapters = chapter_list)
	else:
		return redirect('/404')
# END Chapter Controller

from flask import Flask, request, session, render_template, redirect, jsonify, make_response, flash, abort, send_file
from flask_mail import Mail, Message
from languages import strings
from models.Chapter import Chapter
from models.Contribution_Request import Contribution_Request
from models.License import License
from models.Follow import Follow
from models.Genre import Genre
from models.Invitation import Invitation
from models.Password_Change_Requests import Password_Change_Requests
from models.Signup_Queue import Signup_Queue
from models.Star import Star
from models.Tale import Tale
from models.Tale_Genre import Tale_Genre
from models.User import User
from datetime import datetime, timedelta
from threading import Thread
import os, hashlib, random, re

# BEGIN app configuration
app = Flask(__name__)

app.config.update(
	# FLASK SETTINGS
	DEBUG = True,
	SECRET_KEY = '\xe1{\xb3\x96\xbac\x1ds\xad\x04\x92@\x0e\x8d\xaf`|\x95P\x84;\xa7\x0b\x98\xbcX\x9d\xeaV\x7f',
	MAX_CONTENT_LENGTH = 1024 * 1024,

	# PERSONAL SETTINGS
	SITE_NAME = 'An Addventure',
	SITE_URL = 'https://www.anaddventure.com',
	CONF_PRODUCTION = True,

	# EMAIL SETTINGS
	MAIL_SERVER = 'smtp-mail.outlook.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS = True,
	MAIL_DEFAULT_SENDER = 'anaddventure@outlook.com',
	MAIL_USERNAME = 'anaddventure@outlook.com',
	MAIL_PASSWORD = 'autoescola19',
)

mail = Mail(app)
# END app configuration

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MONTHS_DICTIONARY = {
	1: 'Jan',
	2: 'Feb',
	3: 'Mar',
	4: 'Apr',
	5: 'May',
	6: 'Jun',
	7: 'Jul',
	8: 'Aug',
	9: 'Sep',
	10: 'Oct',
	11: 'Nov',
	12: 'Dec'
}
PAGINATION_LIMIT = 5

# BEGIN auxiliary functions
def generate_random_token(amount_of_characters = 50):
	available_characters = [
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
		'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
		'u', 'v', 'w', 'x', 'y', 'z'
	];

	random_token = ''

	for i in range(0, amount_of_characters):
		random_token += random.choice(available_characters)

	return random_token

def get_number_with_two_digits(number):
	temp = str(number)

	if len(temp) > 1:
		return temp
	else:
		return '00' if len(temp) is 0 else '0' + temp

def beautify_datetime(d, withHour = False, timezone_offset = 0):
	d = d - timedelta(minutes = timezone_offset)
	if withHour:
		return str(d.day) + ' ' + MONTHS_DICTIONARY[d.month] + ', ' + str(d.year) + ' ' + get_number_with_two_digits(d.hour) + ':' + get_number_with_two_digits(d.minute)
	else:
		return str(d.day) + ' ' + MONTHS_DICTIONARY[d.month] + ', ' + str(d.year)

def send_email_to_followers(tale_id, message_title, message_body):
	followers = Follow.select_by_tale_id(tale_id);

	for follower in followers:
		id = follower[0]
		email = User.select_by_id(id, 1)[0]['email']
		send_email(message_title, email, message_body)

def return_rendered_tale_template(
		tale, template, contributions_object = None,
		branches_object = None, contributors_object = None,
		genres_list = None, licenses_list = None,
		open_contribution_requests_list = None,
		closed_contribution_requests_list = None, contribution = None
	):
	this_user_gave_star = did_the_logged_user_give_star(tale['id'])
	this_user_is_following = did_the_logged_user_follow(tale['id'])

	return render_template(
		template,
		creator = User.select_by_id(tale['creator_id'], 1)[0],
		tale = tale,
		license = License.select_by_id(tale['license_id'], 1)[0],
		contributions = contributions_object,
		branches = branches_object,
		contributors = contributors_object,
		this_user_gave_star = this_user_gave_star,
		this_user_is_following = this_user_is_following,
		genres = genres_list,
		licenses = licenses_list,
		open_contribution_requests = open_contribution_requests_list,
		closed_contribution_requests = closed_contribution_requests_list,
		contribution = contribution
	).encode('utf-8')

def did_the_logged_user_give_star(tale_id):
	if 'user_logged_id' in session:
		star_aux = Star.select_by_user_id_and_tale_id(session['user_logged_id'], tale_id, 1)

		return len(star_aux) is not 0
	else:
		return False

def did_the_logged_user_follow(tale_id):
	if 'user_logged_id' in session:
		follow_aux = Follow.select_by_user_id_and_tale_id(session['user_logged_id'], tale_id, 1)

		return len(follow_aux) is not 0
	else:
		return False

def get_file_extension(filename):
	filename = filename.lower()

	if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
		return filename.rsplit('.', 1)[1]
	else:
		return None

def get_current_datetime_as_string(format = '%Y-%m-%d %H:%M:%S'):
	return datetime.utcnow().strftime(format)

def send_async_email(message):
	with app.app_context():
		mail.send(message)

def send_email(message_title, recipient, message_body):
	message = Message(message_title, recipients = [recipient])
	message.body = message_body

	thread = Thread(target = send_async_email, args = [message])
	thread.start()

@app.context_processor
def inject_data():
	language_url = 'https://www.anaddventure.com'
	if not request.is_xhr and request.method != 'POST':
		matches = re.findall(r'(https?://)(\w+)(\.anaddventure\.com.*)', request.base_url)[0]

		if matches[1] == 'pt':
			language = 'pt'
			language_url = matches[0] + 'www'
		else:
			language = 'en'
			language_url = matches[0] + 'pt'

		language_url += matches[2] + '?' + ''.join(list(map(
			lambda key: key + '=' + request.args.get(key) + '&', request.args
		)))
		language_url = language_url[:len(language_url) - 1]

		if session.get('language', None) != language:
			session['language'] = language

	language = session.get('language', 'en')

	def generate_csrf_token():
		if '_csrf_token' not in session:
			session['_csrf_token'] = generate_random_token()

		return session['_csrf_token']

	if 'user_logged_id' in session:
		user_is_logged = True
		user_logged_id = session['user_logged_id']
		user_logged_username = User.select_by_id(user_logged_id, 1)[0]['username']
	else:
		user_is_logged = None
		user_logged_id = None
		user_logged_username = None

	return {
		'language': language,
		'_csrf_token': generate_csrf_token,
		'user_logged_id': user_logged_id,
		'user_is_logged': user_is_logged,
		'user_logged_username': user_logged_username,
		'_': lambda token: strings.STRINGS[language][token],
		'conf_production': app.config['CONF_PRODUCTION'],
		'language_url': language_url,
	}
# END auxiliary functions

@app.before_request
def csrf_protect():
	if request.method == 'POST':
		token = session.get('_csrf_token', None)

		if not token or token != request.form.get('_csrf_token', None):
			print('CSRF TOKEN WRONG')
			print(token)
			print(request.form.get('_csrf_token'))
			abort(400)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html')

@app.route('/')
def index():
	return render_template('index.html', genres = Genre.select_top_ten())

@app.route('/tale/delete/<int:tale_id>/', methods = ['POST'])
def tale_delete(tale_id):
	if request.is_xhr:
		user_logged_id = session.get('user_logged_id', None)
		tale = Tale.select_by_id(tale_id, 1)

		if len(tale) is not 0 and tale[0]['creator_id'] is user_logged_id:
			tale = tale[0]
			creator = User.select_by_id(tale['creator_id'], 1)[0]

			email_object = strings.construct_delete_tale_email_object(
				session.get('language', 'en'),
				tale,
				creator,
				app.config['SITE_NAME']
			)

			send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

			Chapter.delete_by_tale_id(tale['id'])
			Contribution_Request.delete_by_tale_id(tale['id'])
			Follow.delete_by_tale_id(tale['id'])
			Invitation.delete_by_tale_id(tale['id'])
			Star.delete_by_tale_id(tale['id'])
			Tale_Genre.delete_by_tale_id(tale['id'])
			Tale.delete(tale['id'])

			username = User.select_by_id(user_logged_id, 1)[0]['username']

			return jsonify(url = '/profile/' + username)
		else:
			return redirect('/404')
	else:
		redirect('/404')

@app.route('/create/')
def create_tale_get():
	if 'user_logged_id' in session:
		return render_template(
			'create.html',
			genres = Genre.select_all(),
			licenses = License.select_all()
		)
	else:
		return redirect('/404')

@app.route('/create/', methods = ['POST'])
def create_tale_post():
	if request.is_xhr and 'user_logged_id' in session:
		title = request.form.get('create-title', '')
		description = request.form.get('create-description', '')
		category = 2 if int(request.form.get('create-type', 1)) is  not 1 else 1
		genres = request.form.getlist('create-genres')
		license_id = request.form.get('create-license', -1)
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
			new_tale = Tale(title, description, category, creator_id, license_id, get_current_datetime_as_string())
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

@app.route('/tale/<int:tale_id>/<int:chapter_id>/')
@app.route('/tale/<int:tale_id>/<int:chapter_id>/fullscreen')
def tale(tale_id, chapter_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		tale = tale[0]

		# Private tale
		if tale['category'] is 2:
			invitations = Invitation.select_by_tale_id(tale['id'])
			allowed_users_id = set([tale['creator_id']])

			for invitation in invitations:
				allowed_users_id.add(invitation[2])

			if session.get('user_logged_id', None) not in allowed_users_id:
				return redirect('/404')

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

			chapter['datetime'] = beautify_datetime(chapter['date'])
			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			chapter['next_chapters'] = next_chapters

		tale['chapter'] = chapter

		tale_genres = Tale_Genre.select_by_tale_id(tale['id'])
		tale_genres_list = list()

		for tale_genre in tale_genres:
			genre = Genre.select_by_id(tale_genre[1], 1)[0]
			tale_genres_list.append(genre)

		tale['genres'] = tale_genres_list

		return return_rendered_tale_template(tale, 'tale.html')
	else:
		return redirect('/404')

@app.route('/settings/<int:tale_id>/')
def settings(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		return return_rendered_tale_template(tale[0], 'settings.html')
	else:
		return redirect('/404')

@app.route('/invite/<int:tale_id>/')
def invite_get(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		return return_rendered_tale_template(tale[0], 'invite.html')
	else:
		return redirect('/404')

@app.route('/invite/<int:tale_id>/', methods = ['POST'])
def invite_post(tale_id):
	username = request.form.get('invite-username', '')
	user = User.select_by_email(username, 1)

	if len(user) is 0:
		user = User.select_by_full_username(username, 1)

	if len(user) is not 0:
		user = user[0]
		new_invitation = Invitation(session['user_logged_id'], user['id'], tale_id)
		new_invitation.insert()

		tale = Tale.select_by_id(tale_id, 1)[0]
		creator = User.select_by_id(tale['creator_id'], 1)[0]

		email_object = strings.construct_tale_invitation_email_object(
			session.get('language', 'en'),
			user,
			tale,
			creator,
			app.config['SITE_NAME'],
			app.config['SITE_URL']
		)

		send_email(email_object['title'], user['email'], email_object['body'])

	return redirect('/tale/' + str(tale_id) + '/0')

@app.route('/update_tale/<int:tale_id>/')
def update_tale_get(tale_id):
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

		return return_rendered_tale_template(
			tale,
			'update_tale.html',
			genres_list = genres_list,
			licenses_list = licenses_list
		)
	else:
		return redirect('/404')

@app.route('/update_tale/<int:tale_id>/', methods = ['POST'])
def update_tale_post(tale_id):
	if request.is_xhr:
		title = request.form.get('update-tale-title', '')
		description = request.form.get('update-tale-description', '')
		category = 2 if int(request.form.get('update-tale-type', 1)) is not 1 else 1
		genres = request.form.getlist('update-tale-genres')
		license_id = request.form.get('update-tale-license', -1)
		creator_id = session['user_logged_id']
		language = session.get('language', 'en')

		tale = Tale.select_by_id(tale_id, 1)[0]
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

@app.route('/contribute/<int:tale_id>/<int:chapter_id>/')
def contribute_get(tale_id, chapter_id):
	if 'user_logged_id' in session:
		return render_template(
			'contribute.html',
			tale_id = tale_id,
			chapter_id = chapter_id
		)
	else:
		return redirect('/join?redirect=/tale/' + str(tale_id) + '/' + str(chapter_id))

@app.route('/contribute/<int:tale_id>/<int:chapter_id>/', methods = ['POST'])
def contribute_post(tale_id, chapter_id):
	if request.is_xhr:
		tale = Tale.select_by_id(tale_id, 1)

		if len(tale) is not 0:
			tale = tale[0]
			creator = tale['creator_id']
			user_id = session['user_logged_id']
			title = request.form.get('contribute-title', '')
			content = request.form.get('contribute-content', '')
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
							get_current_datetime_as_string(),
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
						date = get_current_datetime_as_string()
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
						get_current_datetime_as_string(),
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

				send_email_to_followers(tale_id, email_object['title'], email_object['body'])

				return jsonify(url = '/tale/' + str(tale_id) + '/' + str(chapter_id))
		else:
			return redirect('/404')
	else:
		return redirect('/404')

@app.route('/contributions/<int:tale_id>/')
def contributions(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		tale = tale[0]

		chapters = Chapter.select_by_tale_id_order_by_date(tale_id)
		chapters_dict = dict()

		for chapter in chapters:
			date = beautify_datetime(chapter['date'])

			if date not in chapters_dict:
				chapters_dict[date] = list()

			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			chapters_dict[date].append(chapter)

		keys = list(chapters_dict.keys())
		keys.sort(reverse = True)

		return return_rendered_tale_template(
			tale,
			'contributions.html',
			contributions_object = {
				'keys': keys,
				'content': chapters_dict
			}
		)
	else:
		return redirect('/404')

@app.route('/branches/<int:tale_id>/')
def branches(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		tale = tale[0]

		chapters = Chapter.select_by_tale_id(tale_id)
		number_bundle = dict()

		for chapter in chapters:
			number = chapter['number']

			if number not in number_bundle:
				number_bundle[number] = {'number': number, 'contributions': list()}

			chapter['date'] = beautify_datetime(chapter['date'])
			chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
			number_bundle[number]['contributions'].append(chapter)

		return return_rendered_tale_template(
			tale, 'branches.html', branches_object = number_bundle
		)
	else:
		return redirect('/404')

@app.route('/contributors/<int:tale_id>/')
def contributors(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		tale = tale[0]

		contributors = Chapter.select_by_tale_id(tale_id)
		contributors_dict = dict()

		creator = User.select_by_id(tale['creator_id'], 1)[0]
		contributors_dict[creator['id']] = {'username': creator['username'], 'count': 0}

		for c in contributors:
			contributor = User.select_by_id(c['user_id'], 1)[0]

			if contributor['id'] not in contributors_dict:
				contributors_dict[contributor['id']] = {'username': contributor['username'], 'count': 0}

			contributors_dict[contributor['id']]['count'] += 1

		return return_rendered_tale_template(
			tale, 'contributors.html', contributors_object = contributors_dict
		)
	else:
		return redirect('/404')

@app.route('/contribution_requests/<int:tale_id>/')
def contribution_requests(tale_id):
	tale = Tale.select_by_id(tale_id, 1)[0]

	return return_rendered_tale_template(tale, 'contribution_requests.html')

@app.route('/contribution_requests/accept/', methods = ['POST'])
def contribution_requests_accept():
	contribution_request_id = request.form.get('contribution_request_id', -1)
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]

		Contribution_Request.update_was_accepted(contribution_request['id'], True)
		Tale.update_contribution_request_count(contribution_request['tale_id'], -1)

		new_chapter = Chapter(
			contribution_request['user_id'],
			contribution_request['tale_id'],
			contribution_request['number'],
			contribution_request['title'],
			contribution_request['content'],
			contribution_request['datetime'],
			contribution_request['previous_chapter_id'],
		)
		new_chapter.insert()

		tale = Tale.select_by_id(contribution_request['tale_id'], 1)[0]
		creator = User.select_by_id(tale['creator_id'], 1)[0]
		contributor = User.select_by_id(contribution_request['user_id'], 1)[0]

		email_object = strings.construct_contribution_request_accepted_email_object(
			session.get('language', 'en'),
			tale,
			creator,
			contributor,
			contribution_request['id'],
			app.config['SITE_NAME'],
			app.config['SITE_URL']
		)

		send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

		return redirect('/tale/' + str(tale['id']) + '/0')
	else:
		return redirect('/404')

@app.route('/contribution_requests/refuse/', methods = ['POST'])
def contribution_requests_refuse():
	contribution_request_id = request.form.get('contribution_request_id', -1)
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]

		Contribution_Request.update_was_accepted(contribution_request['id'], False)
		Tale.update_contribution_request_count(contribution_request['tale_id'], -1)

		tale = Tale.select_by_id(contribution_request['tale_id'], 1)[0]
		creator = User.select_by_id(tale['creator_id'], 1)[0]
		contributor = User.select_by_id(contribution_request['user_id'], 1)[0]

		email_object = strings.construct_contribution_request_refused_email_object(
			session.get('language', 'en'),
			tale,
			creator,
			contributor,
			contribution_request['id'],
			app.config['SITE_NAME'],
			app.config['SITE_URL']
		)

		send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

		return redirect('/tale/' + str(contribution_request['tale_id']) + '/0')
	else:
		return redirect('/404')

@app.route('/contribution_request/<int:contribution_request_id>/')
def contribution_request(contribution_request_id):
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]
		tale = Tale.select_by_id(contribution_request['tale_id'], 1)[0]

		contribution_request['user_username'] = User.select_by_id(contribution_request['user_id'], 1)[0]['username']
		contribution_request['datetime'] = beautify_datetime(contribution_request['datetime'])

		return return_rendered_tale_template(
			tale,
			'contribution_request.html',
			contribution = contribution_request
		)
	else:
		return redirect('/404')

@app.route('/download_chapter/<int:chapter_id>/', methods = ['GET', 'POST'])
def download_chapter(chapter_id):
	chapter = Chapter.select_by_id(chapter_id, 1)[0]
	chapter['datetime'] = beautify_datetime(chapter['date'])
	chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']

	if request.method == 'POST':
		Chapter.update_download_count(chapter_id)

	return render_template('fragment/downloadable_chapter.html', chapter = chapter)

@app.route('/download_all/<int:chapter_id>/', methods = ['GET', 'POST'])
def download_all(chapter_id):
	chapter_list = list()
	chapters_ids_list = list()
	previous_chapter_id = chapter_id
	tale = Tale.select_by_id(
		Chapter.select_by_id(chapter_id, 1)[0]['tale_id'], 1
	)[0]

	while previous_chapter_id is not -1:
		chapters_ids_list.append(previous_chapter_id)
		chapter = Chapter.select_by_id(previous_chapter_id, 1)[0]
		previous_chapter_id = chapter['previous_chapter_id']

	for chapter_id in reversed(chapters_ids_list):
		chapter = Chapter.select_by_id(chapter_id, 1)[0]

		if request.method == 'POST':
			Chapter.update_download_count(chapter_id)

		chapter['datetime'] = beautify_datetime(chapter['date'])
		chapter['contributor_username'] = User.select_by_id(chapter['user_id'], 1)[0]['username']
		chapter_list.append(chapter)

	return render_template(
		'fragment/downloadable_all.html',
		tale = tale,
		chapters = chapter_list
	)

@app.route('/profile/<username>/')
def profile(username):
	user = User.select_by_full_username(username, 1)

	if len(user) is not 0 and user[0]['is_valid_account']:
		user = user[0]
		user['signup_date'] = beautify_datetime(user['signup_date'])
		user['is_email_visible'] = user['is_email_visible'] or session.get('user_logged_id', None) is user['id']

		return render_template(
			'profile.html',
			user = user
		)
	else:
		return redirect('/404')

@app.route('/avatars/<int:user_id>/')
def avatars(user_id):
	for extension in ALLOWED_EXTENSIONS:
		if os.path.exists('anaddventure/site/static/avatars/' + str(user_id) + '.' + extension):
			return send_file(
				'static/avatars/' + str(user_id) + '.' + extension,
				mimetype = 'image/' + extension
			)

	return send_file(
		'static/avatars/identicons/' + str(user_id % 60) + '.png',
		mimetype = 'image/png'
	)

@app.route('/update/<int:user_id>/')
def update(user_id):
	user = User.select_by_id(user_id, 1)

	if len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		user['signup_date'] = beautify_datetime(user['signup_date'])
		user['is_email_visible'] = True

		return render_template(
			'update.html',
			user = user
		)
	else:
		return redirect('/404')

@app.route('/update_profile/<int:user_id>/', methods = ['POST'])
def update_profile(user_id):
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id') is user[0]['id']:
		user = user[0]
		uploaded_file = request.files['update-avatar']
		name = request.form.get('update-name', '')
		email = request.form.get('update-email', '')
		is_email_visible = True if request.form.get('update-email-visibility', False) == 'true' else False
		biography = request.form.get('update-biography', '')
		language = session.get('language', 'en')

		error_list = list()

		if uploaded_file:
			uploaded_file_extension = get_file_extension(uploaded_file.filename)

			if uploaded_file_extension is not None:
				try:
					os.remove('anaddventure/site/static/avatars/' + str(user['id']) + '-temp.' + uploaded_file_extension)
				except:
					print('Could not remove ' + str(user['id']) + '-temp.' + uploaded_file_extension + ' file BEFORE saving the new image.')
					pass

				uploaded_file.save(
					os.path.join('anaddventure/site/static/avatars/', str(user['id']) + '-temp.' + uploaded_file_extension)
				)
				os.chdir('anaddventure/site/static/avatars/')
				os.system(
					'/usr/bin/convert -resize 300x -quality 80 -strip ' +
					str(user['id']) + '-temp.' + uploaded_file_extension + ' ' +
					str(user['id']) + '.' + uploaded_file_extension
				)

				try:
					os.remove(str(user['id']) + '-temp.' + uploaded_file_extension)
				except:
					print('Could not remove ' + str(user['id']) + '-temp.' + uploaded_file_extension + ' file AFTER saving the new image.')
					pass
			else:
				error_list.append(strings.STRINGS[language]['INVALID_FILE'])

		if not User.is_name_valid(name):
			error_list.append(strings.STRINGS[language]['INVALID_NAME'])

		if email == user['email'] or User.is_email_available(email):
			if not User.is_email_valid(email):
				error_list.append(strings.STRINGS[language]['INVALID_EMAIL'])
		else:
			error_list.append(strings.STRINGS[language]['EMAIL_TAKEN'])

		if not User.is_biography_valid(biography):
			error_list.append(strings.STRINGS[language]['INVALID_BIOGRAPHY'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			biography = biography.replace("<", "&lt;").replace(">", "&gt;").replace("\r\n", "<br>")

			User.update_profile(user['id'], name, email, biography, is_email_visible)

			return jsonify(url = '/profile/' + user['username'])
	else:
		return redirect('/404')

@app.route('/update_password/<int:user_id>/', methods = ['POST'])
def update_password(user_id):
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		old_password = request.form.get('update-old-password', '')
		new_password = request.form.get('update-new-password', '')
		confirm_new_password = request.form.get('update-confirm-new-password', '')
		language = session.get('language', 'en')

		error_list = list()

		if not User.is_password_valid(new_password):
			error_list.append(strings.STRINGS[language]['INVALID_PASSWORD'])

		if new_password != confirm_new_password:
			error_list.append(strings.STRINGS[language]['PASSWORD_NO_MATCH'])

		if hashlib.sha256(old_password.encode('utf-8')).hexdigest() != user['password']:
			error_list.append(strings.STRINGS[language]['WRONG_OLD_PASSWORD'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			User.update_password(user_id, new_password)

			return jsonify(url = '/profile/' + user['username'])
	else:
		return redirect('/404')

@app.route('/join/')
def join():
	if 'user_logged_id' in session:
		user = User.select_by_id(session['user_logged_id'], 1)[0]

		return redirect('/profile/' + user['username'])
	else:
		return render_template(
			'join.html',
			redirect_url = request.args.get('redirect', '')
		)

@app.route('/signup/', methods = ['POST'])
def signup():
	if request.is_xhr:
		username = request.form.get('signup-username', '')
		email = request.form.get('signup-email', '')
		password = request.form.get('signup-password', '')
		repeat_password = request.form.get('signup-repeat-password', '')
		language = session.get('language', 'en')

		error_list = list()

		if User.is_username_available(username):
			if not User.is_username_valid(username):
				error_list.append(strings.STRINGS[language]['INVALID_USERNAME'])
		else:
			error_list.append(strings.STRINGS[language]['USERNAME_TAKEN'])

		if User.is_email_available(email):
			if not User.is_email_valid(email):
				error_list.append(strings.STRINGS[language]['INVALID_EMAIL'])
		else:
			error_list.append(strings.STRINGS[language]['EMAIL_TAKEN'])

		if not User.is_password_valid(password):
			error_list.append(strings.STRINGS[language]['INVALID_PASSWORD'])

		if password != repeat_password:
			error_list.append(strings.STRINGS[language]['PASSWORD_NO_MATCH'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			new_user = User(username, username, email, password, get_current_datetime_as_string(), '')
			new_user.insert()

			user_id = User.select_by_full_username(username, 1)[0]['id']

			signup_queue = Signup_Queue(user_id)
			signup_queue.insert()

			email_object = strings.construct_signup_email_object(
				language,
				signup_queue.id,
				app.config['SITE_NAME'],
				app.config['SITE_URL']
			)

			send_email(email_object['title'], email, email_object['body'])

			return jsonify(message = strings.STRINGS[language]['SIGN_UP_MESSAGE'] + ' ' + email + '.')
	else:
		return redirect('/404')

@app.route('/login/', methods = ['POST'])
def login():
	if request.is_xhr:
		username = request.form.get('login-username', '')
		password = request.form.get('login-password', '')
		user_id = User.is_valid_user(username, password)

		if user_id is not None:
			session['user_logged_id'] = user_id
			username = User.select_by_id(user_id, 1)[0]['username']

			return jsonify(url = request.args.get('redirect', '/profile/' + username))
		else:
			return make_response(jsonify(error_list = (['invalid user'])), 400)
	else:
		return redirect('/404')

@app.route('/logout/')
def logout():
	del session['user_logged_id']

	return redirect('/')

@app.route('/activate_account/<random_token>/')
def activate_account(random_token):
	signup_queue = Signup_Queue.select_by_id(random_token, 1)

	if len(signup_queue) is not 0:
		signup_queue = signup_queue[0]
		Signup_Queue.delete(signup_queue['user_id'])
		User.activate_account(signup_queue['user_id'])

		flash('The Account was activated successfully.')

		return redirect('/join')
	else:
		return redirect('/404')

@app.route('/delete_account/<random_token>/')
def delete_account(random_token):
	signup_queue = Signup_Queue.select_by_id(random_token, 1)

	if len(signup_queue) is not 0:
		signup_queue = signup_queue[0]
		Signup_Queue.delete(signup_queue['user_id'])
		User.delete_account(signup_queue['user_id'])

		return redirect('/')
	else:
		return redirect('/404')

@app.route('/password_reset/')
def password_reset_get():
	return render_template('password_reset.html')

@app.route('/password_reset/', methods = ['POST'])
def password_reset_post():
	if request.is_xhr:
		email = request.form.get('password-reset-email', '')
		user = User.select_by_email(email, 1)

		if len(user) is not 0 and User.is_email_valid(email):
			user = user[0]
			language = session.get('language', 'en')
			Password_Change_Requests.delete(user['id'])
			p_c_r = Password_Change_Requests(user['id'])
			p_c_r.insert()

			email_object = strings.construct_password_reset_email_object(
				language,
				p_c_r.id,
				app.config['SITE_NAME'],
				app.config['SITE_URL']
			)

			send_email(email_object['title'], email, email_object['body'])

		return jsonify(message = strings.STRINGS[language]['RESET_PASSWORD_MESSAGE'] + ' ' + email)
	else:
		return redirect('/404')

@app.route('/change_password/<random_token>/')
def change_password_get(random_token):
	p_c_r = Password_Change_Requests.select_by_id(random_token, 1)

	if len(p_c_r) is not 0:
		if Password_Change_Requests.is_valid_random_token(p_c_r[0]['datetime']):
			return render_template(
				'change_password.html',
				random_token = random_token
			)
		else:
			Password_Change_Requests.delete(p_c_r[0]['user_id'])
			return redirect('/404')
	else:
		return redirect('/404')

@app.route('/change_password/', methods = ['POST'])
def change_password_post():
	if request.is_xhr:
		random_token = request.form.get('change-password-random-token', '')
		new_password = request.form.get('change-password-new-password', '')
		confirm_new_password = request.form.get('change-password-confirm-new-password', '')
		language = session.get('language', 'en')

		error_list = list()

		if not User.is_password_valid(new_password):
			error_list.append(strings.STRINGS[language]['INVALID_PASSWORD'])

		if new_password != confirm_new_password:
			error_list.append(strings.STRINGS[language]['PASSWORD_NO_MATCH'])

		if len(error_list) is not 0:
			return make_response(jsonify(error_list = error_list), 400)
		else:
			p_c_r = Password_Change_Requests.select_by_id(random_token, 1)

			if len(p_c_r) is not 0:
				p_c_r = p_c_r[0]
				User.update_password(p_c_r['user_id'], new_password)
				Password_Change_Requests.delete(p_c_r['user_id'])

				session['user_logged_id'] = p_c_r['user_id']

				username = User.select_by_id(p_c_r['user_id'], 1)[0]['username']

				return jsonify(url = '/profile/' + username)
			else:
				return jsonify(url = '/')
	else:
		return redirect('/404')

@app.route('/search_users/')
def search_users():
	content = request.args.get('c', '')
	sort_value = int(request.args.get('s', 1))

	if len(content) < 3:
		return render_template('bad_search.html', search_page = 'users')

	users = User.select_by_username(content)
	users_list = list()

	for user in users:
		users_list.append({
			'id': user['id'],
			'username': user['username'],
			'signup_date': beautify_datetime(user['signup_date']),
			'ugly_signup_date': user['signup_date'],
		})

	if sort_value is 2:
		users_list = sorted(users_list, key = lambda user: user['ugly_signup_date'], reverse = True)
	elif sort_value is 3:
		users_list = sorted(users_list, key = lambda user: user['ugly_signup_date'])

	return render_template(
		'search_users.html',
		content = content,
		users = users_list,
		amount_of_users = len(users_list),
		sort_value = sort_value,
	)

@app.route('/search_tales/')
def search_tales():
	content = request.args.get('c', '')
	genre_id = int(request.args.get('g', -1))

	if len(content) < 3 and genre_id is -1:
		return render_template('bad_search.html', search_page = 'tales')

	sort_value = int(request.args.get('s', 1))
	user_logged_id = session.get('user_logged_id', None)
	tales = Tale.select_viewable_by_title_and_creator_id(
		content, user_logged_id
	) if genre_id is -1 else Tale.select_viewable_by_title_creator_id_and_genre_id(
		content, user_logged_id, genre_id
	)
	tales_per_genre = dict()
	tales_list = list()

	for tale in tales:
		tale_genres = Tale_Genre.select_by_tale_id(tale['id'])
		tale_genres_list = list()

		for tale_genre in tale_genres:
			genre = Genre.select_by_id(tale_genre[1], 1)[0]
			tale_genres_list.append(genre)

			if genre['type'] in tales_per_genre:
				tales_per_genre[genre['type']]['count'] += 1
			else:
				tales_per_genre[genre['type']] = {'count': 1, 'id': genre['id']}

		last_update = Tale.select_last_update(tale['id'], 1)[0][0]
		tale['genres'] = tale_genres_list
		tale['creator_username'] = User.select_by_id(tale['creator_id'], 1)[0]['username']
		tale['last_update'] = False if last_update is None else beautify_datetime(last_update)
		tale['ugly_last_update'] = datetime(1, 1, 1, 15, 11) if last_update is None else last_update
		tales_list.append(tale)

	if sort_value is 2:
		tales_list = sorted(tales_list, key = lambda tale: tale['stars'], reverse = True)
	elif sort_value is 3:
		tales_list = sorted(tales_list, key = lambda tale: tale['stars'])
	elif sort_value is 4:
		tales_list = sorted(tales_list, key = lambda tale: tale['ugly_last_update'], reverse = True)
	elif sort_value is 5:
		tales_list = sorted(tales_list, key = lambda tale: tale['ugly_last_update'])

	return render_template(
		'search_tales.html',
		content = content,
		tales = tales_list,
		amount_of_tales = len(tales_list),
		tales_per_genre = tales_per_genre,
		sort_value = sort_value,
		genre_id = genre_id,
	)

@app.route('/contact')
def contact_get():
	return render_template('contact.html')

@app.route('/contact', methods = ['POST'])
def contact_post():
	if request.is_xhr:
		name = request.form.get('contact-name', '')
		email = request.form.get('contact-email', '')
		message = request.form.get('contact-message', '') + '\nReply to: <' + email + '>'
		language = session.get('language', 'en')

		send_email('Contact: ' + name, app.config['MAIL_USERNAME'], message)
		return strings.STRINGS[language]['CONTACT_MESSAGE_RECEIVED']
	else:
		return redirect('/404')

@app.route('/about')
def about():
	return render_template(
		'about.html',
		total_users = User.select_count_all()[0][0]
	)

@app.route('/faq')
def faq():
	return render_template('faq.html')

# Ajax
@app.route('/get_user_info/')
def get_user_info():
	user_id = int(request.args.get('user_id', -1))
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		user['biography'] = user['biography'].replace("<br>", "\r\n")

		return render_template(
			'fragment/update_profile_form.html',
			user = user
		)
	else:
		return redirect('/404')

@app.route('/get_update_password_form')
def get_update_password_form():
	return render_template(
		'fragment/update_password_form.html',
		user_id = int(request.args.get('user_id', -1))
	)

@app.route('/follow/<int:tale_id>/', methods = ['POST'])
def follow(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		if 'user_logged_id' in session:
			new_follow = Follow(session['user_logged_id'], tale_id)
			new_follow.insert()

			return jsonify({'followers': tale[0]['followers']})
		else:
			return jsonify({'error' : '/join/?redirect=/tale/' + str(tale_id) + '/0'})
	else:
		abort(404)

@app.route('/unfollow/<int:tale_id>/', methods = ['POST'])
def unfollow(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		Follow.delete_by_user_id(session['user_logged_id'])

		return jsonify({'followers': tale[0]['followers']})
	else:
		abort(404)

@app.route('/star/<int:tale_id>/', methods = ['POST'])
def star(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		if 'user_logged_id' in session:
			new_star = Star(session['user_logged_id'], tale_id, get_current_datetime_as_string())
			new_star.insert()

			return jsonify({'stars': tale[0]['stars']})
		else:
			return jsonify({'error' : '/join/?redirect=/tale/' + str(tale_id) + '/0'})
	else:
		abort(404)

@app.route('/unstar/<int:tale_id>/', methods = ['POST'])
def unstar(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		Star.delete_by_user_id(session['user_logged_id'])

		return jsonify({'stars': Tale.select_by_id(tale_id, 1)[0]['stars']})
	else:
		abort(404)

@app.route('/get_open_contribution_requests/')
def get_open_contribution_requests():
	tale_id = int(request.args.get('tale_id', 0))
	contribution_requests = Contribution_Request.select_open_by_tale_id_order_by_datetime(tale_id)

	for contribution_request in contribution_requests:
		contribution_request['user_username'] = User.select_by_id(contribution_request['user_id'], 1)[0]['username']
		contribution_request['datetime'] = beautify_datetime(contribution_request['datetime'])

	return return_rendered_tale_template(
		Tale.select_by_id(tale_id, 1)[0],
		'fragment/open_contribution_requests.html',
		open_contribution_requests_list = contribution_requests
	)

@app.route('/get_closed_contribution_requests/')
def get_closed_contribution_requests():
	tale_id = int(request.args.get('tale_id', 0))
	contribution_requests = Contribution_Request.select_closed_by_tale_id_order_by_datetime(tale_id)

	for contribution_request in contribution_requests:
		contribution_request['user_username'] = User.select_by_id(contribution_request['user_id'], 1)[0]['username']
		contribution_request['datetime'] = beautify_datetime(contribution_request['datetime'])

	return return_rendered_tale_template(
		Tale.select_by_id(tale_id, 1)[0],
		'fragment/closed_contribution_requests.html',
		closed_contribution_requests_list = contribution_requests
	)

@app.route('/get_rendered_own_tales/')
def get_rendered_own_tales():
	username = request.args.get('username')
	offset = int(request.args.get('offset'))
	search_string = request.args.get('search_string', '')
	user_logged_id = session.get('user_logged_id', None)
	user_id = User.select_by_full_username(username, 1)[0]['id']

	tales = Tale.select_viewable_by_creator_id_and_viewer_id_and_title_with_offset_and_limit(
		user_id, user_logged_id, search_string, offset, PAGINATION_LIMIT + 1
	)

	return jsonify({
		'template': render_template('fragment/own_tales.html', tales = tales[:PAGINATION_LIMIT]),
		'previous_offset': 0 if (offset - PAGINATION_LIMIT < 0) else (offset - PAGINATION_LIMIT),
		'next_offset': offset if len(tales) <= PAGINATION_LIMIT else (offset + PAGINATION_LIMIT)
	})

@app.route('/get_rendered_participated_tales/')
def get_rendered_participated_tales():
	username = request.args.get('username')
	offset = int(request.args.get('offset'))
	search_string = request.args.get('search_string', '')
	user_logged_id = session.get('user_logged_id', None)
	user_id = User.select_by_full_username(username, 1)[0]['id']

	tales = Tale.select_tales_other_creator_by_title_with_offset_and_limit(
		user_id, user_logged_id, search_string, offset, PAGINATION_LIMIT + 1
	)

	for tale in tales:
		tale['creator'] = User.select_by_id(tale['creator_id'], 1)[0]

	return jsonify({
		'template': render_template('fragment/participated_tales.html', tales = tales[:PAGINATION_LIMIT]),
		'previous_offset': 0 if (offset - PAGINATION_LIMIT < 0) else (offset - PAGINATION_LIMIT),
		'next_offset': offset if len(tales) <= PAGINATION_LIMIT else (offset + PAGINATION_LIMIT)
	})

@app.route('/get_ten_best_tales/')
def get_ten_best_tales():
	tales = Tale.select_top_ten_order_by_star_count()
	tales_list = list()

	for tale in tales:
		creator = User.select_by_id(tale['creator_id'])
		last_update = Tale.select_last_update(tale['id'])[0][0]

		tale['creator'] = creator[0]
		tale['last_update'] = False if last_update is None else beautify_datetime(
			last_update,
			True,
			int(request.args.get('timezone_offset', 0))
		)
		tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
		tale['creation_datetime'] = beautify_datetime(tale['creation_datetime'])

		tales_list.append(tale)

	return render_template(
		'fragment/top10_tales.html',
		tales = tales_list
	)

@app.route('/get_ten_best_daily_tales/')
def get_ten_best_daily_tales():
	tales = Tale.select_top_ten_order_by_star_count_today()
	tales_list = list()

	for tale in tales:
		creator = User.select_by_id(tale['creator_id'])
		last_update = Tale.select_last_update(tale['id'])[0][0]

		tale['creator'] = creator[0]
		tale['last_update'] = False if last_update is None else beautify_datetime(
			last_update,
			True,
			int(request.args.get('timezone_offset', 0))
		)
		tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
		tale['creation_datetime'] = beautify_datetime(tale['creation_datetime'])

		tales_list.append(tale)

	return render_template(
		'fragment/top10_tales_today.html',
		tales = tales_list
	)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5000)

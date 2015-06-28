from flask import request, session, render_template, redirect, jsonify, make_response, flash, abort, send_file
from languages import strings
from models.Chapter import Chapter
from models.Contribution_Request import Contribution_Request
from models.Follow import Follow
from models.Genre import Genre
from models.Invitation import Invitation
from models.Password_Change_Requests import Password_Change_Requests
from models.Signup_Queue import Signup_Queue
from models.Star import Star
from models.Tale import Tale
from models.Tale_Genre import Tale_Genre
from models.User import User
from datetime import datetime
from controllers import aux
from config import www, pt, app, cache
import os, re

@www.context_processor
@pt.context_processor
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
			session['_csrf_token'] = aux.generate_random_token()

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

@www.before_request
@pt.before_request
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

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html')

@www.route('/')
@pt.route('/')
def index():
	return render_template('index.html', genres = Genre.select_top_ten())

@www.route('/settings/<int:tale_id>/')
@pt.route('/settings/<int:tale_id>/')
def settings(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		return aux.return_rendered_tale_template(tale[0], 'settings.html')
	else:
		return redirect('/404')

@www.route('/invite/<int:tale_id>/')
@pt.route('/invite/<int:tale_id>/')
def invite_get(tale_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		return aux.return_rendered_tale_template(tale[0], 'invite.html')
	else:
		return redirect('/404')

@www.route('/invite/<int:tale_id>/', methods = ['POST'])
@pt.route('/invite/<int:tale_id>/', methods = ['POST'])
def invite_post(tale_id):
	username = request.form.get('invite-username', '')
	user = User.select_by_email(username, 1)
	tale = Tale.select_by_id(tale_id, 1)

	if len(user) is 0:
		user = User.select_by_full_username(username, 1)

	if len(user) is not 0 and len(tale) is not 0 and session.get('user_logged_id', None) is tale[0]['creator_id']:
		user = user[0]
		tale = tale[0]
		new_invitation = Invitation(session['user_logged_id'], user['id'], tale_id)
		new_invitation.insert()

		creator = User.select_by_id(tale['creator_id'], 1)[0]

		email_object = strings.construct_tale_invitation_email_object(
			session.get('language', 'en'),
			user,
			tale,
			creator,
			app.config['SITE_NAME'],
			app.config['SITE_URL']
		)

		aux.send_email(email_object['title'], user['email'], email_object['body'])

	return redirect('/tale/' + str(tale_id) + '/0')

@www.route('/contribution_requests/<int:tale_id>/')
@pt.route('/contribution_requests/<int:tale_id>/')
def contribution_requests(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		return aux.return_rendered_tale_template(tale, 'contribution_requests.html')
	else:
		return redirect('/404')

@www.route('/contribution_requests/accept/', methods = ['POST'])
@pt.route('/contribution_requests/accept/', methods = ['POST'])
def contribution_requests_accept():
	contribution_request_id = request.form.get('contribution_request_id', -1)
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]
		tale = Tale.select_by_id(contribution_request['tale_id'], 1)[0]

		if tale['creator_id'] is session.get('user_logged_id', None):
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

			aux.send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

			return redirect('/tale/' + str(tale['id']) + '/0')
		else:
			return redirect('/404')
	else:
		return redirect('/404')

@www.route('/contribution_requests/refuse/', methods = ['POST'])
@pt.route('/contribution_requests/refuse/', methods = ['POST'])
def contribution_requests_refuse():
	contribution_request_id = request.form.get('contribution_request_id', -1)
	contribution_request = Contribution_Request.select_by_id(contribution_request_id, 1)

	if len(contribution_request) is not 0:
		contribution_request = contribution_request[0]
		tale = Tale.select_by_id(contribution_request['tale_id'], 1)[0]

		if tale['creator_id'] is session.get('user_logged_id', None):
			Contribution_Request.update_was_accepted(contribution_request['id'], False)
			Tale.update_contribution_request_count(contribution_request['tale_id'], -1)

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

			aux.send_email_to_followers(tale['id'], email_object['title'], email_object['body'])

			return redirect('/tale/' + str(contribution_request['tale_id']) + '/0')
		else:
			return redirect('/404')
	else:
		return redirect('/404')

@www.route('/avatars/<int:user_id>/')
@pt.route('/avatars/<int:user_id>/')
def avatars(user_id):
	for extension in aux.ALLOWED_EXTENSIONS:
		if os.path.exists('anaddventure/site/static/avatars/' + str(user_id) + '.' + extension):
			return send_file('static/avatars/' + str(user_id) + '.' + extension, mimetype = 'image/' + extension)

	return send_file('static/avatars/identicons/' + str(user_id % 60) + '.png', mimetype = 'image/png')

@www.route('/join/')
@pt.route('/join/')
def join():
	if 'user_logged_id' in session:
		user = User.select_by_id(session['user_logged_id'], 1)[0]

		return redirect('/profile/' + user['username'])
	else:
		return render_template('join.html', redirect_url = request.args.get('redirect', ''))

@www.route('/login/', methods = ['POST'])
@pt.route('/login/', methods = ['POST'])
def login():
	if request.is_xhr and 'user_logged_id' not in session:
		username = request.form.get('login-username', '')
		password = request.form.get('login-password', '')
		user_id = User.is_valid_user(username, password)

		if user_id is not None:
			session['user_logged_id'] = user_id
			username = User.select_by_id(user_id, 1)[0]['username']

			return jsonify(url = request.args.get('redirect', '/profile/' + username))
		else:
			language = session.get('language', 'en')
			return make_response(
				jsonify(error_list = ([strings.STRINGS[language]['INVALID_USER']])),
				400
			)
	else:
		return redirect('/404')

@www.route('/logout/')
@pt.route('/logout/')
def logout():
	if 'user_logged_id' in session:
		del session['user_logged_id']

	return redirect('/')

@www.route('/activate_account/<random_token>/')
@pt.route('/activate_account/<random_token>/')
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

@www.route('/delete_account/<random_token>/')
@pt.route('/delete_account/<random_token>/')
def delete_account(random_token):
	signup_queue = Signup_Queue.select_by_id(random_token, 1)

	if len(signup_queue) is not 0:
		signup_queue = signup_queue[0]
		Signup_Queue.delete(signup_queue['user_id'])
		User.delete_account(signup_queue['user_id'])

		return redirect('/')
	else:
		return redirect('/404')

@www.route('/password_reset/')
@pt.route('/password_reset/')
def password_reset_get():
	return render_template('password_reset.html')

@www.route('/password_reset/', methods = ['POST'])
@pt.route('/password_reset/', methods = ['POST'])
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

			aux.send_email(email_object['title'], email, email_object['body'])

		return jsonify(message = strings.STRINGS[language]['RESET_PASSWORD_MESSAGE'] + ' ' + email)
	else:
		return redirect('/404')

@www.route('/change_password/<random_token>/')
@pt.route('/change_password/<random_token>/')
def change_password_get(random_token):
	p_c_r = Password_Change_Requests.select_by_id(random_token, 1)

	if len(p_c_r) is not 0:
		if Password_Change_Requests.is_valid_random_token(p_c_r[0]['datetime']):
			return render_template('change_password.html', random_token = random_token)
		else:
			Password_Change_Requests.delete(p_c_r[0]['user_id'])
			return redirect('/404')
	else:
		return redirect('/404')

@www.route('/change_password/', methods = ['POST'])
@pt.route('/change_password/', methods = ['POST'])
def change_password_post():
	random_token = request.form.get('change-password-random-token', '')
	p_c_r = Password_Change_Requests.select_by_id(random_token, 1)

	if request.is_xhr and len(p_c_r) is not 0 and Password_Change_Requests.is_valid_random_token(p_c_r[0]['datetime']):
		p_c_r = p_c_r[0]
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
			User.update_password(p_c_r['user_id'], new_password)
			Password_Change_Requests.delete(p_c_r['user_id'])

			session['user_logged_id'] = p_c_r['user_id']

			username = User.select_by_id(p_c_r['user_id'], 1)[0]['username']

			return jsonify(url = '/profile/' + username)
	else:
		return redirect('/404')

@www.route('/search_users/')
@pt.route('/search_users/')
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
			'signup_date': aux.beautify_datetime(user['signup_date']),
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

@www.route('/search_tales/')
@pt.route('/search_tales/')
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
		tale['last_update'] = False if last_update is None else aux.beautify_datetime(last_update)
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

@www.route('/contact')
@pt.route('/contact')
def contact_get():
	return render_template('contact.html')

@www.route('/contact', methods = ['POST'])
@pt.route('/contact', methods = ['POST'])
def contact_post():
	if request.is_xhr:
		name = request.form.get('contact-name')
		email = request.form.get('contact-email')
		message = request.form.get('contact-message')
		language = session.get('language', 'en')

		if name is not None and User.is_email_valid(email) and message is not None:
			aux.send_email('Contact: ' + name, app.config['MAIL_USERNAME'], message + '\nReply to: <' + email + '>')

		return strings.STRINGS[language]['CONTACT_MESSAGE_RECEIVED']
	else:
		return redirect('/404')

@www.route('/about')
@pt.route('/about')
def about():
	return render_template('about.html', total_users = User.select_count_all()[0][0])

@www.route('/faq')
@pt.route('/faq')
def faq():
	return render_template('faq.html')

# Ajax
@www.route('/get_user_info/')
@pt.route('/get_user_info/')
def get_user_info():
	user_id = int(request.args.get('user_id', -1))
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		user['biography'] = user['biography'].replace("<br>", "\r\n")

		return render_template('fragment/profile_edit_form.html', user = user)
	else:
		abort(404)

@www.route('/follow/<int:tale_id>/', methods = ['POST'])
@pt.route('/follow/<int:tale_id>/', methods = ['POST'])
def follow(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if request.is_xhr and tale and 'user_logged_id' in session:
		new_follow = Follow(session['user_logged_id'], tale_id)
		new_follow.insert()
		return jsonify({'followers': tale['followers'] + 1})
	elif 'user_logged_id' not in session:
		return jsonify({'error' : '/join/?redirect=/tale/' + str(tale_id) + '/0'})
	else:
		abort(404)

@www.route('/unfollow/<int:tale_id>/', methods = ['POST'])
@pt.route('/unfollow/<int:tale_id>/', methods = ['POST'])
def unfollow(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if request.is_xhr and tale and 'user_logged_id' in session:
		Follow.delete_by_user_id(session['user_logged_id'])
		return jsonify({'followers': tale['followers'] - 1})
	else:
		abort(404)

@www.route('/star/<int:tale_id>/', methods = ['POST'])
@pt.route('/star/<int:tale_id>/', methods = ['POST'])
def star(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if request.is_xhr and tale and 'user_logged_id' in session:
		new_star = Star(session['user_logged_id'], tale_id, aux.get_current_datetime_as_string())
		new_star.insert()
		return jsonify({'stars': tale['stars'] + 1})
	elif 'user_logged_id' not in session:
		return jsonify({'error' : '/join/?redirect=/tale/' + str(tale_id) + '/0'})
	else:
		abort(404)

@www.route('/unstar/<int:tale_id>/', methods = ['POST'])
@pt.route('/unstar/<int:tale_id>/', methods = ['POST'])
def unstar(tale_id):
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if request.is_xhr and tale and 'user_logged_id' in session:
		Star.delete_by_user_id(session['user_logged_id'])
		return jsonify({'stars': tale['stars'] - 1})
	else:
		abort(404)

@www.route('/get_open_contribution_requests/')
@pt.route('/get_open_contribution_requests/')
def get_open_contribution_requests():
	tale_id = int(request.args.get('tale_id', 0))
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		contribution_requests = Contribution_Request.select_open_by_tale_id_order_by_datetime(tale_id)

		for contribution_request in contribution_requests:
			contribution_request['user_username'] = User.select_by_id(contribution_request['user_id'], 1)[0]['username']
			contribution_request['datetime'] = aux.beautify_datetime(contribution_request['datetime'])

		return aux.return_rendered_tale_template(
			tale,
			'fragment/open_contribution_requests.html',
			open_contribution_requests_list = contribution_requests
		)
	else:
		abort(404)

@www.route('/get_closed_contribution_requests/')
@pt.route('/get_closed_contribution_requests/')
def get_closed_contribution_requests():
	tale_id = int(request.args.get('tale_id', 0))
	tale = aux.is_visible_tale(tale_id, session.get('user_logged_id', None))

	if tale:
		contribution_requests = Contribution_Request.select_closed_by_tale_id_order_by_datetime(tale_id)

		for contribution_request in contribution_requests:
			contribution_request['user_username'] = User.select_by_id(contribution_request['user_id'], 1)[0]['username']
			contribution_request['datetime'] = aux.beautify_datetime(contribution_request['datetime'])

		return aux.return_rendered_tale_template(
			tale,
			'fragment/closed_contribution_requests.html',
			closed_contribution_requests_list = contribution_requests
		)
	else:
		abort(404)

@www.route('/get_rendered_own_tales/')
@pt.route('/get_rendered_own_tales/')
def get_rendered_own_tales():
	username = request.args.get('username')
	offset = int(request.args.get('offset'))
	search_string = request.args.get('search_string', '')
	user_logged_id = session.get('user_logged_id', None)
	user_id = User.select_by_full_username(username, 1)[0]['id']

	tales = Tale.select_viewable_by_creator_id_and_viewer_id_and_title_with_offset_and_limit(
		user_id, user_logged_id, search_string, offset, aux.PAGINATION_LIMIT + 1
	)

	return jsonify({
		'template': render_template('fragment/own_tales.html', tales = tales[:aux.PAGINATION_LIMIT]),
		'previous_offset': 0 if (offset - aux.PAGINATION_LIMIT < 0) else (offset - aux.PAGINATION_LIMIT),
		'next_offset': offset if len(tales) <= aux.PAGINATION_LIMIT else (offset + aux.PAGINATION_LIMIT)
	})

@www.route('/get_rendered_participated_tales/')
@pt.route('/get_rendered_participated_tales/')
def get_rendered_participated_tales():
	username = request.args.get('username')
	offset = int(request.args.get('offset'))
	search_string = request.args.get('search_string', '')
	user_logged_id = session.get('user_logged_id', None)
	user_id = User.select_by_full_username(username, 1)[0]['id']

	tales = Tale.select_tales_other_creator_by_title_with_offset_and_limit(
		user_id, user_logged_id, search_string, offset, aux.PAGINATION_LIMIT + 1
	)

	for tale in tales:
		tale['creator'] = User.select_by_id(tale['creator_id'], 1)[0]

	return jsonify({
		'template': render_template('fragment/participated_tales.html', tales = tales[:aux.PAGINATION_LIMIT]),
		'previous_offset': 0 if (offset - aux.PAGINATION_LIMIT < 0) else (offset - aux.PAGINATION_LIMIT),
		'next_offset': offset if len(tales) <= aux.PAGINATION_LIMIT else (offset + aux.PAGINATION_LIMIT)
	})

@www.route('/get_ten_best_tales/')
@pt.route('/get_ten_best_tales/')
def get_ten_best_tales():

	@cache.memoize()
	def inner_get_ten_best_tales():
		tales = Tale.select_top_ten_order_by_star_count()
		tales_list = list()

		for tale in tales:
			creator = User.select_by_id(tale['creator_id'], 1)[0]
			last_update = Tale.select_last_update(tale['id'])[0][0]

			tale['creator'] = creator
			tale['last_update'] = False if last_update is None else aux.beautify_datetime(
				last_update,
				True,
				int(request.args.get('timezone_offset', 0))
			)
			tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
			tale['creation_datetime'] = aux.beautify_datetime(tale['creation_datetime'])
			tales_list.append(tale)

		return tales_list

	tales_list = inner_get_ten_best_tales()
	return render_template('fragment/top10_tales.html', tales = tales_list)

@www.route('/get_ten_best_daily_tales/')
@pt.route('/get_ten_best_daily_tales/')
def get_ten_best_daily_tales():

	@cache.memoize()
	def inner_get_ten_best_daily_tales():
		tales = Tale.select_top_ten_order_by_star_count_today()
		tales_list = list()

		for tale in tales:
			creator = User.select_by_id(tale['creator_id'], 1)[0]
			last_update = Tale.select_last_update(tale['id'])[0][0]

			tale['creator'] = creator
			tale['last_update'] = False if last_update is None else aux.beautify_datetime(
				last_update,
				True,
				int(request.args.get('timezone_offset', 0))
			)
			tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
			tale['creation_datetime'] = aux.beautify_datetime(tale['creation_datetime'])
			tales_list.append(tale)

		return tales_list

	tales_list = inner_get_ten_best_daily_tales()
	return render_template('fragment/top10_tales_today.html', tales = tales_list)

@www.route('/<path:no_match>/')
@pt.route('/<path:no_match>/')
def not_found2(no_match):
	return render_template('404.html')
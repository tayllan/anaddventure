from flask import request, session, render_template, redirect, jsonify, make_response
from languages import strings
from models.Signup_Queue import Signup_Queue
from models.User import User
from controllers import aux
from config import www, pt, app
import os, hashlib

# BEGIN User Controller
@www.route('/profile/<username>/')
@pt.route('/profile/<username>/')
def profile(username):
	user = User.select_by_full_username(username, 1)

	if len(user) is not 0 and user[0]['is_valid_account']:
		user = user[0]
		user['signup_date'] = aux.beautify_datetime(user['signup_date'])
		user['is_email_visible'] = user['is_email_visible'] or session.get('user_logged_id', None) is user['id']

		return render_template(
			'profile.html',
			user = user
		)
	else:
		return redirect('/404')

@www.route('/profile/add/', methods = ['POST'])
@pt.route('/profile/add/', methods = ['POST'])
def profile_add():
	if request.is_xhr and 'user_logged_id' not in session:
		username = request.form.get('profile-add-username', '')
		email = request.form.get('profile-add-email', '')
		password = request.form.get('profile-add-password', '')
		repeat_password = request.form.get('profile-add-repeat-password', '')
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
			new_user = User(username, username, email, password, aux.get_current_datetime_as_string(), '')
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

			aux.send_email(email_object['title'], email, email_object['body'])

			return jsonify(message = strings.STRINGS[language]['SIGN_UP_MESSAGE'] + ' ' + email + '.')
	else:
		return redirect('/404')

@www.route('/profile/edit/<int:user_id>/')
@pt.route('/profile/edit/<int:user_id>/')
def profile_edit_get(user_id):
	user = User.select_by_id(user_id, 1)

	if len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		user['signup_date'] = aux.beautify_datetime(user['signup_date'])
		user['biography'] = user['biography'].replace("<br>", "\r\n")
		user['is_email_visible'] = True

		return render_template('profile_edit.html', user = user)
	else:
		return redirect('/404')

@www.route('/profile/edit/<int:user_id>/', methods = ['POST'])
@pt.route('/profile/edit/<int:user_id>/', methods = ['POST'])
def profile_edit_post(user_id):
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id') is user[0]['id']:
		user = user[0]
		uploaded_file = request.files['profile-edit-avatar']
		name = request.form.get('profile-edit-name', '')
		email = request.form.get('profile-edit-email', '')
		is_email_visible = True if request.form.get('profile-edit-email-visibility', False) == 'true' else False
		biography = request.form.get('profile-edit-biography', '')
		language = session.get('language', 'en')

		error_list = list()

		if uploaded_file:
			uploaded_file_extension = aux.get_file_extension(uploaded_file.filename)

			if uploaded_file_extension is not None:
				user_id = str(user['id'])
				os.chdir('/home/user/apps/anaddventure/anaddventure/site/static/avatars/')
				try:
					os.remove(user_id + '-temp.' + uploaded_file_extension)
				except:
					print('Could not remove ' + user_id + '-temp.' + uploaded_file_extension + ' file BEFORE saving the new image.')
					pass

				uploaded_file.save(os.path.join(user_id + '-temp.' + uploaded_file_extension))
				os.system(
					'/usr/bin/convert -resize 300x -quality 80 -strip ' +
					user_id + '-temp.' + uploaded_file_extension + ' ' + user_id + '.' + uploaded_file_extension
				)

				try:
					os.remove(user_id + '-temp.' + uploaded_file_extension)
				except:
					print('Could not remove ' + user_id + '-temp.' + uploaded_file_extension + ' file AFTER saving the new image.')
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

@www.route('/profile/edit/password/<int:user_id>/', methods = ['POST'])
@pt.route('/profile/edit/password/<int:user_id>/', methods = ['POST'])
def profile_edit_password(user_id):
	user = User.select_by_id(user_id, 1)

	if request.is_xhr and len(user) is not 0 and session.get('user_logged_id', None) is user[0]['id']:
		user = user[0]
		old_password = request.form.get('profile-edit-password-old-password', '')
		new_password = request.form.get('profile-edit-password-new-password', '')
		confirm_new_password = request.form.get('profile-edit-password-confirm-new-password', '')
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
# END User Controller

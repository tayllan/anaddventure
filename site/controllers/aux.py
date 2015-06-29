from flask import render_template, session
from flask_mail import Message
from config import mail, app, cache
from models.License import License
from models.Follow import Follow
from models.Invitation import Invitation
from models.Star import Star
from models.Tale import Tale
from models.User import User
from datetime import datetime, timedelta
from threading import Thread
import random

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MONTHS_DICTIONARY = {
	'en': {
		1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
		7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
	},
	'pt': {
		1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
		7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
	}
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
		return str(d.day) + ' ' + MONTHS_DICTIONARY[session.get('language', 'en')][d.month] + ', ' + str(d.year) + ' ' + get_number_with_two_digits(d.hour) + ':' + get_number_with_two_digits(d.minute)
	else:
		return str(d.day) + ' ' + MONTHS_DICTIONARY[session.get('language', 'en')][d.month] + ', ' + str(d.year)

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

def is_visible_tale(tale_id, user_logged_id):
	tale = Tale.select_by_id(tale_id, 1)

	if len(tale) is not 0:
		tale = tale[0]
		# private tale
		if tale['category'] is 2:
			invitations = Invitation.select_by_tale_id(tale['id'])
			allowed_users_id = set([tale['creator_id']])

			for invitation in invitations:
				allowed_users_id.add(invitation[2])

			if user_logged_id not in allowed_users_id:
				return False
		return tale
	else:
		return False

@cache.memoize()
def get_ten_best_tales():
	tales = Tale.select_top_ten_order_by_star_count()
	tales_list = list()

	for tale in tales:
		last_update = Tale.select_last_update(tale['id'])[0][0]

		tale['creator'] = User.select_by_id(tale['creator_id'], 1)[0]
		tale['last_update'] = False if last_update is None else last_update
		tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
		tales_list.append(tale)

	return tales_list

@cache.memoize()
def get_ten_best_daily_tales():
	tales = Tale.select_top_ten_order_by_star_count_today()
	tales_list = list()

	for tale in tales:
		last_update = Tale.select_last_update(tale['id'])[0][0]

		tale['creator'] = User.select_by_id(tale['creator_id'], 1)[0]
		tale['last_update'] = False if last_update is None else last_update
		tale['chapters'] = Tale.select_chapters_count(tale['id'])[0][0]
		tales_list.append(tale)

	return tales_list
# END auxiliary functions

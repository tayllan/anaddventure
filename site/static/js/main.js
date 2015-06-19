$(document).ready(function() {
	'use strict';

	var language = $('[name="selected-language"]').val();

	if (language === 'en') {
		$('#language-pt')[0].href = window.location.protocol + '//pt.anaddventure.com.dev:5000' + window.location.pathname + window.location.search;
	}
	else {
		$('#language-en')[0].href = window.location.protocol + '//www.anaddventure.com.dev:5000' + window.location.pathname + window.location.search;
	}

	var path = window.location.pathname;

	var my_messages = {
		en: {
			NAME_MIN: 'Must have at least 3 characters',
			NAME_MAX: 'Can have at most 50 characters',
			USERNAME_MIN: 'Must have at least 3 characters',
			USERNAME_MAX: 'Can have at most 50 characters',
			EMAIL: 'This is not a valid email address',
			EMAIL_MAX: 'Can have at most 50 characters',
			PASSWORD_MIN: 'Must have at least 6 characters',
			BIOGRAPHY_MAX: 'Can have at most 500 characters',
			TITLE_MAX: 'Can have at most 500 characters',
			DESCRIPTION_MAX: 'Can have at most 500 characters',
			EMPTY: 'This field is required',
			CHECKED: 'This field is required',
			UNWATCH: 'Unwatch',
			WATCH: 'Watch',
			UNSTAR: 'Unstar',
			STAR: 'Star',
			MATCH: 'This field must match the field above',
			AVATAR_FORMAT: 'Unfortunately, we only support PNG, GIF, or JPG pictures',
			AVATAR_SIZE: 'Unfortunately, we only support pictures with up to 1 MB size',
			ADD_AVATAR: 'Upload new picture',
			TOO_WEAK: 'Too Weak',
			WEAK: 'Weak',
			GOOD: 'Good',
			STRONG: 'Strong',
			DELETE_MODAL_MESSAGE: 'Are you ABSOLUTELY sure?\nIf so, please type in the title of the tale to confirm.',
			DELETE_MODAL_WRONG_TITLE: 'Wrong tale title'
		},
		pt: {
			NAME_MIN: 'Deve conter ao menos 3 caracteres',
			NAME_MAX: 'Pode conter no máximo 50 caracters',
			USERNAME_MIN: 'Deve conter ao menos 3 caracteres',
			USERNAME_MAX: 'Pode conter no máximo 50 caracters',
			EMAIL: 'Este não é um email válido',
			EMAIL_MAX: 'Pode conter no máximo 50 caracters',
			PASSWORD_MIN: 'Deve conter ao menos 6 caracteres',
			BIOGRAPHY_MAX: 'Pode conter no máximo 500 caracteres',
			TITLE_MAX: 'Pode conter no máximo 500 caracteres',
			DESCRIPTION_MAX: 'Pode conter no máximo 500 caracteres',
			EMPTY: 'Este campo é obrigatório',
			CHECKED: 'Este campo é obrigatório',
			UNWATCH: 'Parar de Seguir',
			WATCH: 'Seguir',
			UNSTAR: 'Tirar Recomendação',
			STAR: 'Recomendar',
			MATCH: 'Este campo deve ser igual ao de cima',
			AVATAR_FORMAT: 'Infelizmente, suportamos apenas imagens em PGN, GIF ou JPG',
			AVATAR_SIZE: 'Infelizmente, suportamos apenas imagens com tamanho de até 1 MB',
			ADD_AVATAR: 'Enviar nova imagem',
			TOO_WEAK: 'Muito fraca',
			WEAK: 'Fraca',
			GOOD: 'Boa',
			STRONG: 'Forte',
			DELETE_MODAL_MESSAGE: 'Você tem certeza ABSOLUTA?\nSe sim, por favor digite o título do conto para confirmar.',
			DELETE_MODAL_WRONG_TITLE: 'Título do conto errado'
		}
	};

	var my_rules = {
		name: [
			{
				type: 'length[3]',
				prompt: my_messages[language]['NAME_MIN']
			},
			{
				type: 'maxLength[50]',
				prompt: my_messages[language]['NAME_MAX']
			}
		],
		username: [
			{
				type: 'length[3]',
				prompt: my_messages[language]['USERNAME_MIN']
			},
			{
				type: 'maxLength[50]',
				prompt: my_messages[language]['USERNAME_MAX']
			}
		],
		email: [
			{
				type: 'email',
				prompt: my_messages[language]['EMAIL']
			},
			{
				type: 'maxLength[50]',
				prompt: my_messages[language]['EMAIL_MAX']
			}
		],
		password: [{
			type: 'length[6]',
			prompt: my_messages[language]['PASSWORD_MIN']
		}],
		biography: [{
			type: 'maxLength[500]',
			prompt: my_messages[language]['BIOGRAPHY_MAX']
		}],
		title: [
			{
				type: 'empty',
				prompt: my_messages[language]['EMPTY']
			},
			{
				type: 'maxLength[500]',
				prompt: my_messages[language]['TITLE_MAX']
			}
		],
		description: [{
			type: 'maxLength[500]',
			prompt: my_messages[language]['DESCRIPTION_MAX']
		}],
		empty: [{
			type: 'empty',
			prompt: my_messages[language]['EMPTY']
		}],
		checked: [{
			type: 'checked',
			prompt: my_messages[language]['CHECKED']
		}],
		match: function(otherFieldIdentifier) {
			return [{
				type: 'match[' + otherFieldIdentifier + ']',
				prompt: my_messages[language]['MATCH']
			}];
		}
	};

	var calculate_password_strength = function(password) {
		if (password.length < 6) {
			return 0;
		}
		else if (password.length < 8) {
			return 1;
		}
		else {
			var amount_of_groups = 0;

			if (/[a-z]/.test(password)) {
				++amount_of_groups;
			}
			if (/[A-Z]/.test(password)) {
				++amount_of_groups;
			}
			if (/[0-9]/.test(password)) {
				++amount_of_groups;
			}
			if (/[@#$%&\*\(\)!\-\+]/.test(password)) {
				++amount_of_groups;
			}

			if (amount_of_groups == 1) {
				return 1;
			}
			else if (amount_of_groups == 2) {
				return 2;
			}
			else {
				return 3;
			}
		}
	};

	var append_messages_list = function(messages_list, element, positive) {
		var final_string = '<ul class="ui negative message" id="messages-list">';

		if (positive) {
			final_string = '<ul class="ui positive message" id="messages-list">';
		}

		for (var i = messages_list.length - 1; i >= 0; i--) {
			final_string += '<li>' + messages_list[i] + '</li>';
		}
		final_string += '</ul>';
		$('#messages-list').remove();
		element.after(final_string);
	};

	// BEGIN index.html js;
	if (path === '/') {
		var $top_all = $('#top-all');
		var $top_today = $('#top-today');
		var $top_tales = $('.top-tales');

		$top_all.on('click', function(event) {
			$top_today.removeClass('active');
			$top_all.addClass('active');

			$.ajax({
				type: 'get',
				url: '/get_ten_best_tales',
				data: {
					timezone_offset: (new Date()).getTimezoneOffset()
				},
				datatype: 'json',
				success: function(data) {
					$top_tales.find('div').remove();
					$top_tales.append(data);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});

		$top_today.on('click', function(event) {
			$top_all.removeClass('active');
			$top_today.addClass('active');

			$.ajax({
				type: 'get',
				url: '/get_ten_best_daily_tales',
				data: {
					timezone_offset: (new Date()).getTimezoneOffset()
				},
				datatype: 'json',
				success: function(data) {
					$top_tales.find('div').remove();
					$top_tales.append(data);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});

		$top_today.trigger('click');
	}
	// END index.html js

	// BEGIN join.html js
	if (path.indexOf('join') !== -1) {
		var $login = $('.login');
		var $signup = $('.signup');
		var $password_strength = $signup.find('.password-strength');

		$signup.find('input[name="signup-password"]').on('keyup', function(event) {
			var password = this.value;
			var strength = calculate_password_strength(password);

			$password_strength.removeClass();

			switch (strength) {
				case 0:
					$password_strength.addClass('ui yellow label').html(my_messages[language]['TOO_WEAK']);
					break;
				case 1:
					$password_strength.addClass('ui green label').html(my_messages[language]['WEAK']);
					break;
				case 2:
					$password_strength.addClass('ui blue label').html(my_messages[language]['GOOD']);
					break;
				default:
					$password_strength.addClass('ui red label').html(my_messages[language]['STRONG']);
			}
		});

		$login.find('form').form({
			username: {
				identifier: 'login-username',
				rules: my_rules.username
			},
			password: {
				identifier: 'login-password',
				rules: my_rules.password
			}
		},
		{
			inline: true,
			onSuccess: function() {
				var input_password = $(this).find('input[type="password"]')[0];
				var password = input_password.value;
				var hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

				input_password.value = hash;

				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						window.location = data.url;
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $login.find('h2'));
					}
				});

				return false;
			}
		});

		$signup.find('form').form({
			username: {
				identifier: 'signup-username',
				rules: my_rules.username
			},
			email: {
				identifier: 'signup-email',
				rules: my_rules.email
			},
			password: {
				identifier: 'signup-password',
				rules: my_rules.password
			},
			repeat_password: {
				identifier: 'signup-repeat-password',
				rules: my_rules.match('signup-password')
			}
		},
		{
			inline: true,
			onSuccess: function() {
				var input_password = $(this).find('input[name="signup-password"]')[0];
				var password = input_password.value;
				var hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

				input_password.value = hash;

				var input_password_repeat_password = $(this).find('input[name="signup-repeat-password"]')[0];
				password = input_password_repeat_password.value;
				hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

				input_password_repeat_password.value = hash;

				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						append_messages_list([data.message], $signup.find('h2'), true);
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $signup.find('h2'));
					}
				});

				return false;
			}
		});
	}
	// END join.html js

	// BEGIN password_reset.html js
	if (path.indexOf('password_reset') !== -1) {
		var $password_reset_form = $('.password-reset form');

		$password_reset_form.form({
			email: {
				identifier: 'password-reset-email',
				rules: my_rules.email
			}
		},
		{
			inline: true,
			onSuccess: function() {
				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						append_messages_list([data.message], $password_reset_form.find('h1'), true);
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $password_reset_form.find('h1'));
					}
				});

				return false;
			}
		});
	}
	// END password_reset.html js

	// BEGIN change_password.html js
	if (path.indexOf('change_password') !== -1) {
		var $change_password_form = $('.change-password form');

		$change_password_form.form({
			password: {
				identifier: 'change-password-new-password',
				rules: my_rules.password
			},
			repeat_password: {
				identifier: 'change-password-confirm-new-password',
				rules: my_rules.password
			}
		},
		{
			inline: true,
			onSuccess: function() {
				var input_password = $(this).find('input[name="change-password-new-password"]')[0];
				var password = input_password.value;
				var hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

				input_password.value = hash;

				var input_password_confirm_password = $(this).find('input[name="change-password-confirm-new-password"]')[0];
				password = input_password_confirm_password.value;
				hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

				input_password_confirm_password.value = hash;

				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						window.location = data.url;
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $change_password_form.find('h1'));
					}
				});

				return false;
			}
		});
	}
	// END change_password.html js

	// BEGIN profile.html js
	if (path.indexOf('profile') !== -1) {
		var username = /profile\/([^\/]+)/.exec(path)[1];
		var $own = $('.own');
		var $participated = $('.participated');

		var render_own_tales = function(offset, search_string, dont_focus) {
			$.ajax({
				type: 'get',
				url: '/get_rendered_own_tales',
				datatype: 'json',
				data: {
					username: username,
					offset: offset,
					search_string: search_string
				},
				success: function(data) {
					$own.empty().append(data);
					if (!dont_focus) {
						$own.find('input')[0].focus();
					}

					var $pagination_buttons = $own.find('#pagination-buttons button');

					$pagination_buttons.each(function() {
						if (parseInt(this.value, 10) === parseInt(offset, 10)) {
							$(this).addClass('disabled');
						}
						else {
							$(this).removeClass('disabled');
						}
					});
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		};

		var render_participated_tales = function(offset, search_string, dont_focus) {
			$.ajax({
				type: 'get',
				url: '/get_rendered_participated_tales',
				datatype: 'json',
				data: {
					username: username,
					offset: offset,
					search_string: search_string
				},
				success: function(data) {
					$participated.empty().append(data);
					if (!dont_focus) {
						$participated.find('input')[0].focus();
					}

					var $pagination_buttons = $participated.find('#pagination-buttons button');

					$pagination_buttons.each(function() {
						if (parseInt(this.value, 10) === parseInt(offset, 10)) {
							$(this).addClass('disabled');
						}
						else {
							$(this).removeClass('disabled');
						}
					});
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		};

		$own.on('click', '.own-pagination', function(event) {
			event.preventDefault();

			render_own_tales(this.value, $own.find('input')[0].value);

			return false;
		});

		$participated.on('click', '.participated-pagination', function(event) {
			event.preventDefault();

			render_participated_tales(this.value, $participated.find('input')[0].value);

			return false;
		});

		render_own_tales(0, '', true);
		render_participated_tales(0, '', true);

		$own.on('submit', 'form', function(event) {
			event.preventDefault();

			render_own_tales(0, $(this).find('input')[0].value);

			return false;
		});

		$participated.on('submit', 'form', function(event) {
			event.preventDefault();

			render_participated_tales(0, $(this).find('input')[0].value);

			return false;
		});
	}
	// END profile.html js

	// BEGIN update.html js
	var $profile = $('.profile');

	if (path.indexOf('update/') !== -1) {
		var $button_update_profile = $('.button-update-profile');

		$profile.on('change', 'input[name="update-avatar"]', function(event) {
			var file = this.files[0];

			if (file) {
				var $button_choose_file = $profile.find('.button-choose-file');
				var $label_choose_file = $profile.find('.label-choose-file');

				if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
					if (file.size < (1024 * 1024)) {
						$button_choose_file.addClass('green').html(file.name);
						$label_choose_file.removeClass('ui red label').html('');
					}
					else {
						this.value = '';
						this.files = [];
						$button_choose_file.removeClass('green').html(my_messages[language]['ADD_AVATAR']);
						$label_choose_file.addClass('ui red label').html(my_messages[language]['AVATAR_SIZE']);
					}
				}
				else {
					this.value = '';
					this.files = [];
					$button_choose_file.removeClass('green').html(my_messages[language]['ADD_AVATAR']);
					$label_choose_file.addClass('ui red label').html(my_messages[language]['AVATAR_FORMAT']);
				}
			}
		});

		$profile.on('click', '.button-choose-file', function(event) {
			event.preventDefault();

			$profile.find('input[name="update-avatar"]').trigger('click');

			return false;
		});

		$button_update_profile.on('click', function(event) {
			$.ajax({
				type: 'get',
				url: '/get_user_info',
				datatype: 'json',
				data: {
					user_id: this.value
				},
				success: function(data) {
					$profile.find('form').remove();
					$profile.append(data);

					$profile.find('form').form({
						name: {
							identifier: 'update-name',
							rules: my_rules.name
						},
						email: {
							identifier: 'update-email',
							rules: my_rules.email
						},
						email_visibility: {
							identifier: 'update-email-visibility',
							rules: my_rules.empty
						},
						biography: {
							identifier: 'update-biography',
							rules: my_rules.biography
						}
					},
					{
						inline: true,
						onSuccess: function() {
							$.ajax({
								type: this.method,
								url: this.action,
								data: new FormData(this),
								processData: false,
								contentType: false,
								success: function(data) {
									window.location = data.url;
								},
								error: function(xhr, status, error) {
									append_messages_list(xhr.responseJSON.error_list, $profile.find('h4'));
								}
							});

							return false;
						},
						onFailure: function() {
							return false;
						}
					});
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});

		$button_update_profile.trigger('click');

		$('.button-update-password').on('click', function(event) {
			$.ajax({
				type: 'get',
				url: '/get_update_password_form',
				datatype: 'json',
				data: {
					user_id: this.value
				},
				success: function(data) {
					$profile.find('form').remove();
					$profile.append(data);

					var $update_password_strength = $('.password-strength');

					$('input[name="update-new-password"]').on('keyup', function(event) {
						var password = this.value;
						var strength = calculate_password_strength(password);

						$update_password_strength.removeClass();

						switch (strength) {
							case 0:
								$update_password_strength.addClass('ui yellow label').html(my_messages[language]['TOO_WEAK']);
								break;
							case 1:
								$update_password_strength.addClass('ui green label').html(my_messages[language]['WEAK']);
								break;
							case 2:
								$update_password_strength.addClass('ui blue label').html(my_messages[language]['GOOD']);
								break;
							default:
								$update_password_strength.addClass('ui red label').html(my_messages[language]['STRONG']);
						}
					});

					$profile.find('form').form({
						old_password: {
							identifier: 'update-old-password',
							rules: my_rules.password
						},
						new_password: {
							identifier: 'update-new-password',
							rules: my_rules.password
						},
						confirm_new_password: {
							identifier: 'update-confirm-new-password',
							rules: my_rules.match('update-new-password')
						}
					},
					{
						inline: true,
						onSuccess: function() {
							var input_old_password = $(this).find('input[name="update-old-password"]')[0];
							var password = input_old_password.value;
							var hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

							input_old_password.value = hash;

							var input_new_password = $(this).find('input[name="update-new-password"]')[0];
							password = input_new_password.value;
							hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

							input_new_password.value = hash;

							var input_confirm_password = $(this).find('input[name="update-confirm-new-password"]')[0];
							password = input_confirm_password.value;
							hash = new jsSHA(password, 'TEXT').getHash('SHA-256', 'HEX');

							input_confirm_password.value = hash;

							$.ajax({
								type: this.method,
								url: this.action,
								data: new FormData(this),
								processData: false,
								contentType: false,
								success: function(data) {
									window.location = data.url;
								},
								error: function(xhr, status, error) {
									append_messages_list(xhr.responseJSON.error_list, $profile.find('h4'));
								}
							});

							return false;
						},
						onFailure: function() {
							return false;
						}
					});
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});
	}
	// END update.html js

	// BEGIN tale.html js
	var $upper_bar = $('.upper-bar');

	if ($upper_bar.length > 0) {
		var $to_fullscreen = $('#to-fullscreen');
		var $fullscreen = $('#fullscreen');

		$upper_bar.on('submit', '.form-unfollow', function(event) {
			event.preventDefault();

			var $form_unfollow = $('.form-unfollow');
			var action = $form_unfollow[0].action;

			$.ajax({
				type: 'post',
				url: action,
				datatype: 'json',
				data: new FormData(this),
				processData: false,
				contentType: false,
				success: function(data) {
					var $form_unfollow_button = $form_unfollow.find('button')[0];

					$form_unfollow_button.innerHTML = '<i class="unhide icon"></i>' +
						my_messages[language]['WATCH'] + ' ' + data.followers;

					$form_unfollow.attr(
						'action',
						action.replace('unfollow', 'follow')
					);

					$form_unfollow.attr(
						'class',
						'form-follow column'
					);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});

			return false;
		});

		$upper_bar.on('submit', '.form-follow', function(event) {
			event.preventDefault();

			var $form_follow = $('.form-follow');
			var action = $form_follow[0].action;

			$.ajax({
				type: 'post',
				url: action,
				datatype: 'json',
				data: new FormData(this),
				processData: false,
				contentType: false,
				success: function(data) {
					if (!data.error) {
						var $form_follow_button = $form_follow.find('button')[0];

						$form_follow_button.innerHTML = '<i class="unhide icon"></i>' +
							my_messages[language]['UNWATCH'] + ' ' + data.followers;

						$form_follow.attr(
							'action',
							action.replace('follow', 'unfollow')
						);

						$form_follow.attr(
							'class',
							'form-unfollow column'
						);
					}
					else {
						window.location = data.error;
					}
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});

			return false;
		});

		$upper_bar.on('submit', '.form-unstar', function(event) {
			event.preventDefault();

			var $form_unstar = $('.form-unstar');
			var action = $form_unstar[0].action;

			$.ajax({
				type: 'post',
				url: action,
				datatype: 'json',
				data: new FormData(this),
				processData: false,
				contentType: false,
				success: function(data) {
					var $form_unstar_button = $form_unstar.find('button')[0];

					$form_unstar_button.innerHTML = '<i class="star icon"></i>' +
						my_messages[language]['STAR'] + ' ' + data.stars;

					$form_unstar.attr(
						'action',
						action.replace('unstar', 'star')
					);

					$form_unstar.attr(
						'class',
						'form-star column'
					);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});

			return false;
		});

		$upper_bar.on('submit', '.form-star', function(event) {
			event.preventDefault();

			var $form_star = $('.form-star');
			var action = $form_star[0].action;

			$.ajax({
				type: 'post',
				url: action,
				datatype: 'json',
				data: new FormData(this),
				processData: false,
				contentType: false,
				success: function(data) {
					if (!data.error) {
						var $form_star_button = $form_star.find('button')[0];

						$form_star_button.innerHTML = '<i class="star icon"></i>' +
							my_messages[language]['UNSTAR'] + ' ' + data.stars;

						$form_star.attr(
							'action',
							action.replace('star', 'unstar')
						);

						$form_star.attr(
							'class',
							'form-unstar column'
						);
					}
					else {
						window.location = data.error;
					}
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});

			return false;
		});

		if (path.indexOf('/fullscreen') !== -1) {
			$fullscreen.modal('show');
		}

		$to_fullscreen.on('click', function(event) {
			$fullscreen.modal('show');
		});
	}
	// END tale.html js

	// BEGIN update_tale.html js
	if (path.indexOf('update_tale') !== -1) {
		var $main_form = $('.main form');
		$main_form.form({
			title: {
				identifier: 'update-tale-title',
				rules: my_rules.title
			},
			description: {
				identifier: 'update-tale-description',
				rules: my_rules.description
			},
			genres: {
				identifier: 'update-tale-genres',
				rules: [{
					type: 'empty_genres',
					prompt: my_messages[language]['EMPTY']
				}]
			},
			license: {
				identifier: 'update-tale-license',
				rules: my_rules.checked
			},
			type: {
				identifier: 'update-tale-type',
				rules: my_rules.checked
			}
		},
		{
			rules: {
				empty_genres: function() {
					return ($('[name="update-tale-genres"]')[0].children.length > 0);
				}
			},
			inline: true,
			onSuccess: function() {
				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						window.location = data.url;
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $main_form.find('h1'));
					}
				});

				return false;
			}
		});

		var $genres = $('#genres');
		var $update_tale_genres = $('select[name="update-tale-genres"]');
		var $available_genres = $('select[name="available-genres"]');

		$('#available-genres').on('keyup', function(event) {
			var string = this.value;
			var select = $available_genres[0];

			for (var i = 0; i < select.length; i++) {
				if (select[i].innerHTML.indexOf(string) < 0) {
					$(select[i]).attr('hidden', 'true');
				}
				else {
					$(select[i]).removeAttr('hidden');
				}
			}
		});

		$('#taken-genres').on('keyup', function(event) {
			var string = this.value;
			var select = $update_tale_genres[0];

			for (var i = 0; i < select.length; i++) {
				if (select[i].innerHTML.indexOf(string) < 0) {
					$(select[i]).attr('hidden', 'true');
				}
				else {
					$(select[i]).removeAttr('hidden');
				}
			}
		});

		$('#add').on('click', function(event) {
			var something = $available_genres.find('option:selected');

			for (var i = 0; i < something.length; i++) {
				$update_tale_genres.append(something[i]);
			}
		});

		$('#remove').on('click', function(event) {
			var something = $update_tale_genres.find('option:selected');

			for (var i = 0; i < something.length; i++) {
				$available_genres.append(something[i]);
			}
		});

		$genres.on('dblclick', 'select[name="update-tale-genres"] option', function(event) {
			$available_genres.append(this);

			$update_tale_genres.find('option').each(function() {
				$(this).attr('selected', 'selected');
			});
		});
		$genres.on('dblclick', 'select[name="available-genres"] option', function(event) {
			$update_tale_genres.append(this);
		});
	}
	// END update_tale.html js

	// BEGIN search.html js
	if (path.indexOf('/search') !== -1) {
		$('#layout-search-bar').empty();
		$('input[name="c"]').focus();
		$('#sort-bar').on('change', function(event) {
			window.location = window.location.href.replace(/\&?s=\d+\&?/, '') + '&s=' + $(this).find('option:selected').val();
		});
	}
	// END search.html js

	// BEGIN contribution_requests.html
	var $contribution_requests = $('.contribution-requests');

	if (path.indexOf('contribution_requests') !== -1) {
		var tale_id = /contribution_requests\/([0-9]+)/.exec(window.location)[1];

		var $o_c_r = $('.o-c-r');
		var $c_c_r = $('.c-c-r');

		$o_c_r.on('click', function(event) {
			if ($contribution_requests.find('.open-contribution-requests').length === 1) {
				return;
			}
			console.log('HERE');
			$o_c_r.addClass('active');
			$c_c_r.removeClass('active');

			$.ajax({
				type: 'get',
				url: '/get_open_contribution_requests',
				datatype: 'json',
				data: {
					tale_id: tale_id
				},
				success: function(data) {
					$contribution_requests.find('.closed-contribution-requests').remove();
					$contribution_requests.append(data);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});

		$o_c_r.trigger('click');

		$c_c_r.on('click', function(event) {
			if ($contribution_requests.find('.closed-contribution-requests').length === 1) {
				return;
			}
			$c_c_r.addClass('active');
			$o_c_r.removeClass('active');

			$.ajax({
				type: 'get',
				url: '/get_closed_contribution_requests',
				datatype: 'json',
				data: {
					tale_id: tale_id
				},
				success: function(data) {
					$contribution_requests.find('.open-contribution-requests').remove();
					$contribution_requests.append(data);
				},
				error: function(xhr, status, error) {
					console.log(xhr);
				}
			});
		});
	}
	// END contribution_requests.html

	// BEGIN create.html js
	if (path.indexOf('create') !== -1) {
		var $create_form = $('.create form');
		$create_form.form({
			title: {
				identifier: 'create-title',
				rules: my_rules.title
			},
			description: {
				identifier: 'create-description',
				rules: my_rules.description
			},
			genres: {
				identifier: 'create-genres',
				rules: [{
					type: 'empty_genres',
					prompt: my_messages[language]['EMPTY']
				}]
			},
			license: {
				identifier: 'create-license',
				rules: my_rules.checked
			},
			type: {
				identifier: 'create-type',
				rules: my_rules.checked
			}
		},
		{
			rules: {
				empty_genres: function() {
					return ($('[name="create-genres"]')[0].children.length > 0);
				}
			},
			inline: true,
			onSuccess: function() {
				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						window.location = data.url;
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $create_form.find('h1'));
					}
				});

				return false;
			}
		});

		var $genres = $('#genres');
		var $create_genres = $('select[name="create-genres"]');
		var $available_genres = $('select[name="available-genres"]');

		$('#available-genres').on('keyup', function(event) {
			var string = this.value;
			var select = $available_genres[0];

			for (var i = 0; i < select.length; i++) {
				if (select[i].innerHTML.indexOf(string) < 0) {
					$(select[i]).attr('hidden', 'true');
				}
				else {
					$(select[i]).removeAttr('hidden');
				}
			}
		});

		$('#taken-genres').on('keyup', function(event) {
			var string = this.value;
			var select = $create_genres[0];

			for (var i = 0; i < select.length; i++) {
				if (select[i].innerHTML.indexOf(string) < 0) {
					$(select[i]).attr('hidden', 'true');
				}
				else {
					$(select[i]).removeAttr('hidden');
				}
			}
		});

		$('#add').on('click', function(event) {
			var something = $available_genres.find('option:selected');

			for (var i = 0; i < something.length; i++) {
				$create_genres.append(something[i]);
			}
		});

		$('#remove').on('click', function(event) {
			var something = $create_genres.find('option:selected');

			for (var i = 0; i < something.length; i++) {
				$available_genres.append(something[i]);
			}
		});

		$genres.on('dblclick', 'select[name="create-genres"] option', function(event) {
			$available_genres.append(this);

			$create_genres.find('option').each(function() {
				$(this).attr('selected', 'selected');
			});
		});
		$genres.on('dblclick', 'select[name="available-genres"] option', function(event) {
			$create_genres.append(this);
		});
	}
	// END create.html js

	// BEGIN contribute.html js
	if (path.indexOf('contribute') !== -1) {
		var $contribute_form = $('.contribute-form');

		tinymce.init({
			selector: 'textarea[name="contribute-content"]'
		});

		$contribute_form.form({
			title: {
				identifier: 'contribute-title',
				rules: my_rules.title
			}
		},
		{
			inline: true,
			onSuccess: function() {
				$.ajax({
					type: this.method,
					url: this.action,
					data: {
						'contribute-title': $contribute_form.find('[name="contribute-title"]')[0].value,
						'contribute-content': tinymce.get('contribute-content').getContent(),
						'_csrf_token': $contribute_form.find('[name="_csrf_token"]')[0].value
					},
					success: function(data) {
						window.location = data.url;
					},
					error: function(xhr, status, error) {
						append_messages_list(xhr.responseJSON.error_list, $contribute_form.find('h1'));
					}
				});

				return false;
			}
		});
	}
	// END contribute.html js

	// BEGIN settings.html js;
	if (path.indexOf('settings') !== -1) {
		var $form_delete = $('#form-delete');

		$form_delete.on('submit', function(event) {
			event.preventDefault();

			var original_tale_title = $(this).find('button')[0].value;
			var delete_modal = prompt(my_messages[language]['DELETE_MODAL_MESSAGE']);

			if (delete_modal) {
				if (delete_modal === original_tale_title) {
					$.ajax({
						type: this.method,
						url: this.action,
						datatype: 'json',
						data: new FormData(this),
						processData: false,
						contentType: false,
						success: function(data) {
							window.location = data.url;
						},
						error: function(xhr, status, error) {
							console.log(xhr);
						}
					});
				}
				else {
					$(this).find('div').remove();
					$(this).append('<div class="ui red message">' + my_messages[language]['DELETE_MODAL_WRONG_TITLE'] + '</div>');
				}
			}

			return false;
		});
	}
	// END settings.html js

	// BEGIN contact.html js
	if (path.indexOf('contact') !== -1) {
		var $contact_form = $('.contact-form');

		$contact_form.form({
			name: {
				identifier: 'contact-name',
				rules: my_rules.name
			},
			email: {
				identifier: 'contact-email',
				rules: my_rules.email
			},
			message: {
				identifier: 'contact-message',
				rules: my_rules.empty
			}
		},
		{
			inline: true,
			onSuccess: function() {
				$.ajax({
					type: this.method,
					url: this.action,
					data: new FormData(this),
					processData: false,
					contentType: false,
					success: function(data) {
						var $received_message = $('#received-message');
						$received_message.html(data);
						$received_message.addClass('ui positive message');
					},
					error: function(xhr, status, error) {
						// TODO: see what exaclty this "append_messages_list" does.
						append_messages_list(xhr.responseJSON.error_list, $contact_form.find('h1'));
					}
				});

				return false;
			}
		});
	}
	// END contact.html js
});

/*
 A JavaScript implementation of the SHA family of hashes, as
 defined in FIPS PUB 180-2 as well as the corresponding HMAC implementation
 as defined in FIPS PUB 198a

 Copyright Brian Turek 2008-2015
 Distributed under the BSD License
 See http://caligatio.github.com/jsSHA/ for more information

 Several functions taken from Paul Johnston
*/
'use strict';(function(F){function u(a,b,d){var c=0,f=[0],h="",g=null,h=d||"UTF8";if("UTF8"!==h&&"UTF16BE"!==h&&"UTF16LE"!==h)throw"encoding must be UTF8, UTF16BE, or UTF16LE";if("HEX"===b){if(0!==a.length%2)throw"srcString of HEX type must be in byte increments";g=w(a);c=g.binLen;f=g.value}else if("TEXT"===b)g=x(a,h),c=g.binLen,f=g.value;else if("B64"===b)g=y(a),c=g.binLen,f=g.value;else if("BYTES"===b)g=z(a),c=g.binLen,f=g.value;else throw"inputFormat must be HEX, TEXT, B64, or BYTES";this.getHash=
function(a,b,d,h){var g=null,e=f.slice(),k=c,l;3===arguments.length?"number"!==typeof d&&(h=d,d=1):2===arguments.length&&(d=1);if(d!==parseInt(d,10)||1>d)throw"numRounds must a integer >= 1";switch(b){case "HEX":g=A;break;case "B64":g=B;break;case "BYTES":g=C;break;default:throw"format must be HEX, B64, or BYTES";}if("SHA-224"===a)for(l=0;l<d;l+=1)e=t(e,k,a),k=224;else if("SHA-256"===a)for(l=0;l<d;l+=1)e=t(e,k,a),k=256;else throw"Chosen SHA variant is not supported";return g(e,D(h))};this.getHMAC=
function(a,b,d,g,s){var e,k,l,n,p=[],E=[];e=null;switch(g){case "HEX":g=A;break;case "B64":g=B;break;case "BYTES":g=C;break;default:throw"outputFormat must be HEX, B64, or BYTES";}if("SHA-224"===d)k=64,n=224;else if("SHA-256"===d)k=64,n=256;else throw"Chosen SHA variant is not supported";if("HEX"===b)e=w(a),l=e.binLen,e=e.value;else if("TEXT"===b)e=x(a,h),l=e.binLen,e=e.value;else if("B64"===b)e=y(a),l=e.binLen,e=e.value;else if("BYTES"===b)e=z(a),l=e.binLen,e=e.value;else throw"inputFormat must be HEX, TEXT, B64, or BYTES";
a=8*k;b=k/4-1;if(k<l/8){for(e=t(e,l,d);e.length<=b;)e.push(0);e[b]&=4294967040}else if(k>l/8){for(;e.length<=b;)e.push(0);e[b]&=4294967040}for(k=0;k<=b;k+=1)p[k]=e[k]^909522486,E[k]=e[k]^1549556828;d=t(E.concat(t(p.concat(f),a+c,d)),a+n,d);return g(d,D(s))}}function x(a,b){var d=[],c,f=[],h=0,g,m,q;if("UTF8"===b)for(g=0;g<a.length;g+=1)for(c=a.charCodeAt(g),f=[],128>c?f.push(c):2048>c?(f.push(192|c>>>6),f.push(128|c&63)):55296>c||57344<=c?f.push(224|c>>>12,128|c>>>6&63,128|c&63):(g+=1,c=65536+((c&
1023)<<10|a.charCodeAt(g)&1023),f.push(240|c>>>18,128|c>>>12&63,128|c>>>6&63,128|c&63)),m=0;m<f.length;m+=1){for(q=h>>>2;d.length<=q;)d.push(0);d[q]|=f[m]<<24-h%4*8;h+=1}else if("UTF16BE"===b||"UTF16LE"===b)for(g=0;g<a.length;g+=1){c=a.charCodeAt(g);"UTF16LE"===b&&(m=c&255,c=m<<8|c>>8);for(q=h>>>2;d.length<=q;)d.push(0);d[q]|=c<<16-h%4*8;h+=2}return{value:d,binLen:8*h}}function w(a){var b=[],d=a.length,c,f,h;if(0!==d%2)throw"String of HEX type must be in byte increments";for(c=0;c<d;c+=2){f=parseInt(a.substr(c,
2),16);if(isNaN(f))throw"String of HEX type contains invalid characters";for(h=c>>>3;b.length<=h;)b.push(0);b[c>>>3]|=f<<24-c%8*4}return{value:b,binLen:4*d}}function z(a){var b=[],d,c,f;for(c=0;c<a.length;c+=1)d=a.charCodeAt(c),f=c>>>2,b.length<=f&&b.push(0),b[f]|=d<<24-c%4*8;return{value:b,binLen:8*a.length}}function y(a){var b=[],d=0,c,f,h,g,m;if(-1===a.search(/^[a-zA-Z0-9=+\/]+$/))throw"Invalid character in base-64 string";f=a.indexOf("=");a=a.replace(/\=/g,"");if(-1!==f&&f<a.length)throw"Invalid '=' found in base-64 string";
for(f=0;f<a.length;f+=4){m=a.substr(f,4);for(h=g=0;h<m.length;h+=1)c="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".indexOf(m[h]),g|=c<<18-6*h;for(h=0;h<m.length-1;h+=1){for(c=d>>>2;b.length<=c;)b.push(0);b[c]|=(g>>>16-8*h&255)<<24-d%4*8;d+=1}}return{value:b,binLen:8*d}}function A(a,b){var d="",c=4*a.length,f,h;for(f=0;f<c;f+=1)h=a[f>>>2]>>>8*(3-f%4),d+="0123456789abcdef".charAt(h>>>4&15)+"0123456789abcdef".charAt(h&15);return b.outputUpper?d.toUpperCase():d}function B(a,b){var d=
"",c=4*a.length,f,h,g;for(f=0;f<c;f+=3)for(g=f+1>>>2,h=a.length<=g?0:a[g],g=f+2>>>2,g=a.length<=g?0:a[g],g=(a[f>>>2]>>>8*(3-f%4)&255)<<16|(h>>>8*(3-(f+1)%4)&255)<<8|g>>>8*(3-(f+2)%4)&255,h=0;4>h;h+=1)d=8*f+6*h<=32*a.length?d+"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(g>>>6*(3-h)&63):d+b.b64Pad;return d}function C(a){var b="",d=4*a.length,c,f;for(c=0;c<d;c+=1)f=a[c>>>2]>>>8*(3-c%4)&255,b+=String.fromCharCode(f);return b}function D(a){var b={outputUpper:!1,b64Pad:"="};
try{a.hasOwnProperty("outputUpper")&&(b.outputUpper=a.outputUpper),a.hasOwnProperty("b64Pad")&&(b.b64Pad=a.b64Pad)}catch(d){}if("boolean"!==typeof b.outputUpper)throw"Invalid outputUpper formatting option";if("string"!==typeof b.b64Pad)throw"Invalid b64Pad formatting option";return b}function p(a,b){return a>>>b|a<<32-b}function I(a,b,d){return a&b^~a&d}function J(a,b,d){return a&b^a&d^b&d}function K(a){return p(a,2)^p(a,13)^p(a,22)}function L(a){return p(a,6)^p(a,11)^p(a,25)}function M(a){return p(a,
7)^p(a,18)^a>>>3}function N(a){return p(a,17)^p(a,19)^a>>>10}function O(a,b){var d=(a&65535)+(b&65535);return((a>>>16)+(b>>>16)+(d>>>16)&65535)<<16|d&65535}function P(a,b,d,c){var f=(a&65535)+(b&65535)+(d&65535)+(c&65535);return((a>>>16)+(b>>>16)+(d>>>16)+(c>>>16)+(f>>>16)&65535)<<16|f&65535}function Q(a,b,d,c,f){var h=(a&65535)+(b&65535)+(d&65535)+(c&65535)+(f&65535);return((a>>>16)+(b>>>16)+(d>>>16)+(c>>>16)+(f>>>16)+(h>>>16)&65535)<<16|h&65535}function t(a,b,d){var c,f,h,g,m,q,p,t,s,e,k,l,n,u,
E,r,w,x,y,z,A,B,C,D,G,v=[],H,F=[1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,
3516065817,3600352804,4094571909,275423344,430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,2361852424,2428436474,2756734187,3204031479,3329325298];e=[3238371032,914150663,812702999,4144912697,4290775857,1750603025,1694076839,3204075428];f=[1779033703,3144134277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225];if("SHA-224"===d||"SHA-256"===d)k=64,c=(b+65>>>9<<4)+15,u=16,E=1,G=Number,r=O,w=P,x=Q,y=M,z=N,A=K,B=L,D=J,
C=I,e="SHA-224"===d?e:f;else throw"Unexpected error in SHA-2 implementation";for(;a.length<=c;)a.push(0);a[b>>>5]|=128<<24-b%32;a[c]=b;H=a.length;for(l=0;l<H;l+=u){b=e[0];c=e[1];f=e[2];h=e[3];g=e[4];m=e[5];q=e[6];p=e[7];for(n=0;n<k;n+=1)16>n?(s=n*E+l,t=a.length<=s?0:a[s],s=a.length<=s+1?0:a[s+1],v[n]=new G(t,s)):v[n]=w(z(v[n-2]),v[n-7],y(v[n-15]),v[n-16]),t=x(p,B(g),C(g,m,q),F[n],v[n]),s=r(A(b),D(b,c,f)),p=q,q=m,m=g,g=r(h,t),h=f,f=c,c=b,b=r(t,s);e[0]=r(b,e[0]);e[1]=r(c,e[1]);e[2]=r(f,e[2]);e[3]=r(h,
e[3]);e[4]=r(g,e[4]);e[5]=r(m,e[5]);e[6]=r(q,e[6]);e[7]=r(p,e[7])}if("SHA-224"===d)a=[e[0],e[1],e[2],e[3],e[4],e[5],e[6]];else if("SHA-256"===d)a=e;else throw"Unexpected error in SHA-2 implementation";return a}"function"===typeof define&&define.amd?define(function(){return u}):"undefined"!==typeof exports?"undefined"!==typeof module&&module.exports?module.exports=exports=u:exports=u:F.jsSHA=u})(this);

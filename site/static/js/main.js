'use strict';

var language = $('[name="selected-language"]').val();
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
var MONTHS_DICTIONARY = {
	en: {
		1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
		7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
	},
	pt: {
		1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
		7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
	}
};
def construct_new_chapter_email_object(language, tale, creator_username, chapter_number, SITE_NAME, SITE_URL, new_chapter_id):
	if language == 'en':
		email_object = {
			'title': 'New Chapter on ' + tale['title'],
			'body': '"{0}" just added a version for the chapter {1} on the tale "{2}" on "{3}", which can be viewed on {4}/tale/{5}/{6}.'.format(
					creator_username,
					str(chapter_number),
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id']),
					str(new_chapter_id)
				)
		}
	else:
		email_object = {
			'title': 'Novo Capítulo em ' + tale['title'],
			'body': '"{0}" adicionou outra versão do capítulo {1} no conto "{2}" em "{3}", o qual pode ser visualizado em {4}/tale/{5}/{6}.'.format(
					creator_username,
					str(chapter_number),
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id']),
					str(new_chapter_id)
				)
		}

	return email_object

def construct_new_contribution_request_email_object(language, tale, creator_username, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': 'New Collaboration Request on ' + tale['title'],
			'body': '"{0}" just sent a collaboration request for the tale "{1}" on "{2}", which can be viewed on {3}/contribution_requests/{4}.'.format(
					creator_username,
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id'])
				)
		}
	else:
		email_object = {
			'title': 'Novo Pedido de Colaboração em ' + tale['title'],
			'body': '"{0}" enviou um pedido de colaboração para o conto "{1}" em "{2}", o qual pode ser visualizado em {3}/contribution_requests/{4}.'.format(
					creator_username,
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id'])
				)
		}

	return email_object

def construct_contribution_request_accepted_email_object(language, tale, creator, contributor, contribution_id, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': 'Collaboration Request Accepted on ' + tale['title'],
			'body': '"{0}" just accepted a collaboration request on the tale "{1}" on "{2}" sent from "{3}". The collaboration can be viewed on {4}/collaboration/{5}/.'.format(
					creator['username'],
					tale['title'],
					SITE_NAME,
					contributor['username'],
					SITE_URL,
					str(contribution_id)
				)
		}
	else:
		email_object = {
			'title': 'Pedido de Colaboração Aceito em ' + tale['title'],
			'body': '"{0}" aceitou um pedido de colaboração no conto "{1}" em "{2}" enviado por "{3}". A colaboração pode ser visualizada em {4}/collaboration/{5}/.'.format(
					creator['username'],
					tale['title'],
					SITE_NAME,
					contributor['username'],
					SITE_URL,
					str(contribution_id)
				)
		}

	return email_object

def construct_contribution_request_refused_email_object(language, tale, creator, contributor, contribution_id, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': 'Collaboration Request Refused on ' + tale['title'],
			'body': '"{0}" just refused a collaboration request on the tale "{1}" on "{2}" sent from "{3}". The collaboration can be viewed on {4}/collaboration/{5}/.'.format(
					creator['username'],
					tale['title'],
					SITE_NAME,
					contributor['username'],
					SITE_URL,
					str(contribution_id)
				)
		}
	else:
		email_object = {
			'title': 'Pedido de Colaboração Recusado em ' + tale['title'],
			'body': '"{0}" recusou um pedido de colaboração no conto "{1}" em "{2}" enviado por "{3}". A colaboração pode ser visualizada em {4}/collaboration/{5}/.'.format(
					creator['username'],
					tale['title'],
					SITE_NAME,
					contributor['username'],
					SITE_URL,
					str(contribution_id)
				)
		}

	return email_object

def construct_delete_tale_email_object(language, tale, creator, SITE_NAME):
	if language == 'en':
		email_object = {
			'title': 'Tale ' + tale['title'] + ' Deleted',
			'body': '"{0}" just deleted the tale "{1}" on "{2}".'.format(
					creator['username'],
					tale['title'],
					SITE_NAME
				)
		}
	else:
		email_object = {
			'title': 'Conto ' + tale['title'] + ' Deletado',
			'body': '"{0}" deletou o conto "{1}" em "{2}".'.format(
					creator['username'],
					tale['title'],
					SITE_NAME
				)
		}

	return email_object

def construct_tale_invitation_email_object(language, user, tale, creator, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': 'Private Tale Invitation',
			'body': '"{0}", you\'ve been invited to collaborate to the private tale "{1}" on "{2}" by "{3}". To see the tale, click on the following link: {4}/join?redirect=/tale/{5}/0.\nIf clicking the link above doesn\'t work, please copy and paste the URL in a new browser window instead.'.format(
					user['name'],
					tale['title'],
					SITE_NAME,
					creator['name'],
					SITE_URL,
					str(tale['id'])
				)
		}
	else:
		email_object = {
			'title': 'Convite para um Conto Privado',
			'body': '"{0}", você foi convidado a colaborar para o conto privado "{1}" em "{2}" por "{3}". Para visualizar o conto, clique no seguinte link: {4}/join?redirect=/tale/{5}/0.\nSe clicar no link acima não funcionar, por favor copie e cole a URL em uma nova aba do navegador.'.format(
					user['name'],
					tale['title'],
					SITE_NAME,
					creator['name'],
					SITE_URL,
					str(tale['id'])
				)
		}

	return email_object

def construct_signup_email_object(language, signup_queue_id, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': '' + SITE_NAME + ' Registration',
			'body': 'To fulfill the account registration process on "{0}" just click the following link: {1}/activate_account/{2}.\nIf clicking the link above doesn\'t work, please copy and paste the URL in a new browser window instead.\nIf you\'ve received this email in error, it\'s likely that another person entered your email address by mistake while trying to signup on "{0}", if that\'s the case, you can remove your email address from our database on the following link: {1}/delete_account/{2}.'.format(
					SITE_NAME,
					SITE_URL,
					str(signup_queue_id)
				)
		}
	else:
		email_object = {
			'title': '' + SITE_NAME + ' Registration',
			'body': 'Para completar o processo de cadastro da sua conta em "{0}" clique no seguinte link: {1}/activate_account/{2}.\nSe clicar no link acima não funcionar, por favor copie e cole a URL em uma nova aba do navegador.\nSe você recebeu esse email por engano, é provável que outra pessoa digitou seu email sem querer enquanto tentava se cadastrar em "{0}", se esse for o caso, você pode remover seu email do nosso banco de dados no seguinte link: {1}/delete_account/{2}.'.format(
					SITE_NAME,
					SITE_URL,
					str(signup_queue_id)
				)
		}

	return email_object

def construct_password_reset_email_object(language, p_c_r_id, SITE_NAME, SITE_URL):
	if language == 'en':
		email_object = {
			'title': 'Password Resetting',
			'body': 'To initiate the password reset process for your account on "{0}" click on the following link: {1}/change_password/{2}.\nIf clicking the link above doesn\'t work, please copy and paste the URL in a new browser window instead.\nIf you\'ve received this email in error, it\'s likely that another user entered your email address by mistake while trying to reset a password.\nIf you didn\'t initiate the request, you don\'t need to take any further action and can safely disregard this email.'.format(
					SITE_NAME,
					SITE_URL,
					str(p_c_r_id)
				)
		}
	else:
		email_object = {
			'title': 'Password Resetting',
			'body': 'Para iniciar o processo de recuperação de senhar para sua conta em "{0}" clique no seguinte link: {1}/change_password/{2}.\nSe clicar no link acima não funcionar, por favor copie e cole a URL em uma nova aba do navegador.\nSe você recebeu esse email por engano, é provável que outro usuário tenha digitado seu email sem querer enquanto tentava resetar a senha dele.\nSe você não iniciou esse requisição, você não precisa tomar nenhuma outra ação e pode seguramente desconsiderar esse email.'.format(
					SITE_NAME,
					SITE_URL,
					str(p_c_r_id)
				)
		}

	return email_object

def construct_updated_chapter_email_object(language, tale, creator_username, chapter_number, SITE_NAME, SITE_URL, chapter_id):
	if language == 'en':
		email_object = {
			'title': 'Chapter Updated on ' + tale['title'],
			'body': '"{0}" just updated the chapter {1} on the tale "{2}" on "{3}", which can be viewed on {4}/tale/{5}/{6}.'.format(
					creator_username,
					str(chapter_number),
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id']),
					str(chapter_id)
				)
		}
	else:
		email_object = {
			'title': 'Capítulo Atualizado em ' + tale['title'],
			'body': '"{0}" atualizou o capítulo {1} no conto "{2}" em "{3}", o qual pode ser visualizado em {4}/tale/{5}/{6}.'.format(
					creator_username,
					str(chapter_number),
					tale['title'],
					SITE_NAME,
					SITE_URL,
					str(tale['id']),
					str(chapter_id)
				)
		}

	return email_object

STRINGS = {
	'en': {
		'TOP_10_GENRES': 'Hot Genres',
		'MY_PROFILE': 'My Profile',
		'LOGOUT': 'Logout',
		'LOGIN': 'Login',
		'SIGN_UP': 'Sign Up',
		'SEARCH_BY_GENRES': 'Search by Genres',
		'TERMS': 'Terms',
		'PRIVACY': 'Privacy',
		'CONTACT': 'Contact me',
		'ABOUT': 'About',
		'TALE_AND_OR_USER': 'tale and user',
		'PASSWORD': 'Password',
		'REPEAT_PASSWORD': 'Repeat the Password',
		'FORGOT_PASSWORD': 'forgot your password',
		'OR': 'or',
		'ENTER_EMAIL': 'Enter your email address',
		'SUBMIT': 'Submit',
		'CHANGE_PASSWORD': 'Change Password',
		'NEW_PASSWORD': 'New Password',
		'CONFIRM_NEW_PASSWORD': 'Confirm new Password',
		'UPDATE_PASSWORD': 'Update Password',
		'JOIN': 'Join',
		'NOT_FOUND': 'Page Not Found',
		'CHAPTERS': 'Chapters',
		'NO_CHAPTERS_TALE': 'There are no chapters for this Tale',
		'FOR_CHAPTER': 'For Chapter',
		'PUBLISHED_BY': 'published by',
		'ON': 'on',
		'TALE': 'Tale',
		'CONTRIBUTE': 'Collaborate',
		'TITLE': 'Title',
		'BY': 'by',
		'CONTRIBUTION_REQUEST': 'Collaboration Request',
		'OPEN': 'Open',
		'CLOSED': 'Closed',
		'ACCEPTED': 'Accepted',
		'REFUSED': 'Refused',
		'CHAPTER': 'Chapter',
		'CONTRIBUTION_REQUESTS': 'Collaboration Requests',
		'OPEN_CONTRIBUTION_REQUESTS': 'Open Collaboration Requests',
		'CLOSED_CONTRIBUTION_REQUESTS': 'Closed Collaboration Requests',
		'CONTRIBUTIONS': 'collaborations',
		'NO_CONTRIBUTIONS_TALE': 'There are no collaborations for the Tale',
		'WRITERS': 'Writers',
		'NEW_TALE': 'New Tale',
		'DESCRIPTION': 'Description',
		'GENRES': 'Genres',
		'TALE_TYPE': 'Tale Type',
		'PUBLIC': 'Public',
		'PRIVATE': 'Private',
		'TALE_LICENSE': 'Tale License',
		'SPECIFICATION': 'specification',
		'CREATE': 'Create',
		'SITE_HEADER': 'How about going on an Addventure',
		'INVITE_FRIEND': 'Invite a Friend',
		'INVITE': 'Invited',
		'EMAIL_INVITED_USER': 'Username or Email of your friend',
		'CREATE_TALE': 'Create Tale',
		'EDIT_PROFILE': 'Edit Profile',
		'BIOGRAPHY': 'About me',
		'SEARCH': 'Search',
		'TALES': 'Tales',
		'USERS': 'Users',
		'OPTIONS': 'Options',
		'UPDATE_TALE_INFO': 'Update Tale Informations',
		'INVITE_FRIEND_TO_TALE': 'Invite a Friend to your Private Tale',
		'DOWNLOAD_CHAPTER': 'Download this Chapter',
		'DOWNLOAD_ALL': 'Download all up to this Chapter',
		'CONTINUE_CHAPTER': 'Continue this Chapter here',
		'NO_CHAPTER': 'The owner of this Tale still didn\'t add the First Chapter',
		'ADD_FIRST_CHAPTER': 'add the First Chapter',
		'HERE': 'here',
		'ACCOUNT_SETTINGS': 'Account Settings',
		'UPDATE_PROFILE': 'Update Profile',
		'TALE_SETTINGS': 'Tale Settings',
		'UPDATE_TALE': 'Update Tale',
		'UPDATE': 'Update',
		'NO_CLOSED_CONTRIBUTIONS_TALE': 'There are no Closed Collaborations Requests for this Tale',
		'NO_OPEN_CONTRIBUTIONS_TALE': 'There are no Open Collaborations Requests for this Tale',
		'SUBMITTED_ON': 'submitted on',
		'ACCEPT_CONTRIBUTION': 'Accept Collaboration',
		'REFUSE_CONTRIBUTION': 'Refuse Collaboration',
		'MY_TALES': 'My Tales',
		'TALES_CONTRIBUTED_TO': 'Tales Collaborated to',
		'JOINED_ON': 'Joined on',
		'SETTINGS': 'Settings',
		'CONTENT': 'Content',
		'LICENSE': 'License',
		'UNWATCH': 'Unwatch',
		'WATCH': 'Watch',
		'UNSTAR': 'Unstar',
		'STAR': 'Star',
		'STARS': 'Stars',
		'PUBLIC_PROFILE': 'Public Profile',
		'AVATAR_IMAGE': 'Avatar Image',
		'NAME': 'Name',
		'PUBLIC_EMAIL': 'Public Email',
		'SHOW': 'Yes, show it',
		'NO_SHOW': 'Don\'t show my email address',
		'TOP_10': 'Recommended tales',
		'TOP_10_TODAY': 'Today',
		'TOP_10_ALL': 'All-Time',
		'STARS_TODAY': 'stars today',
		'OLD_PASSWORD': 'Old Password',
		'FORGOT_MY_PASSWORD': 'I forgot my password',
		'WAS_FOUND': 'Was found',
		'WERE_FOUND': 'Were found',
		'RESULTS': 'matches',
		'RESULT': 'match',
		'LAST_UPDATED_ON': 'Last updated on',
		'PREVIOUS_CHAPTER': 'Previous Chapter',
		'ADD_AVATAR': 'Upload new picture',

		'INVALID_USER': 'Invalid User',
		'INVALID_NAME': 'NAME Must have between 3 and 50 characters.',
		'INVALID_USERNAME': 'USERNAME Must have between 3 and 50 characters.',
		'INVALID_EMAIL': 'Invalid Email Address.',
		'INVALID_PASSWORD': 'PASSWORD Must have at least 6 characters.',
		'INVALID_BIOGRAPHY': 'BIOGRAPHY Can have at most 500 characters.',
		'INVALID_TITLE': 'TITLE Can have at most 500 characters.',
		'INVALID_CONTENT': 'CONTENT Must have at least 1 character.',
		'INVALID_DESCRIPTION': 'DESCRIPTION Can have at most 500 characters.',
		'INVALID_FILE': 'Invalid Picture.',
		'INVALID_GENRE': 'Invalid Genre.',
		'INVALID_LICENSE': 'Invalid License',
		'USERNAME_TAKEN': 'This Username is not available.',
		'EMAIL_TAKEN': 'This Email is not available.',
		'TITLE_TAKEN': 'You already have a Tale with this Title.',
		'PASSWORD_NO_MATCH': 'Your passwords do not match.',
		'NO_GENRES': 'The Tale must have at least one Genre.',
		'WRONG_OLD_PASSWORD': 'The Old password is wrong.',

		'TOO_WEAK': 'Too Weak',

		'ACTION / ADVENTURE': 'Action / Adventure',
		'CHILDREN\'S TALES': 'Children\'s Tales',
		'CRIME / DETECTIVE': 'Crime / Detective',
		'FABLE / FOLKLORE': 'Fable / Folklore',
		'FAN FICTION': 'Fan Fiction',
		'FANTASY': 'Fantasy',
		'FEMINIST': 'Feminist',
		'FLASH FICTION': 'Flash Fiction',
		'FOREIGN LANGUAGE': 'Foreign Language',
		'GAY / LESBIAN': 'Gay / Lesbian',
		'HISTORICAL': 'Historical',
		'HORROR': 'Horror',
		'HUMOR': 'Humor',
		'JUST FOR FUN': 'Just for Fun',
		'LITERARY': 'Literary',
		'MATURE THEMES': 'Mature Themes',
		'MYSTERY / THRILLER': 'Mystery / Thriller',
		'MYTHOLOGY': 'Mythology',
		'POLITICS': 'Politics',
		'RELIGION / SPIRITUALITY': 'Religion / Spirituality',
		'ROMANCE': 'Romance',
		'SATIRE / PARODY': 'Satire / Parody',
		'SCIENCE FICTION': 'Science Fiction',
		'SPECIAL INTEREST': 'Special Interest',
		'SPORTS': 'Sports',
		'SUPERNATURAL': 'Supernatural',
		'TABOO': 'Taboo',
		'TEEN / YOUNG ADULT': 'Teen / Young Adult',
		'URBAN': 'Urban',
		'WESTERN': 'Western',

		'ADD': 'Add',
		'REMOVE': 'Remove',
		'CONTACT_MESSAGE': 'Any problem, complaint and/or sugestion, please send an email to:',
		'WAITING_FIRST_CHAPTER': 'Still waiting for the First Chapter',
		'SITE_PRESENTATION': 'Awesome site to write Collaborative Tales',
		'TALE_BY': 'tale by',
		'SITE_LOGO': 'An Addventure',
		'NOT_WRONG': 'No, it\'s not writen wrong.',
		'MORE_ABOUT': 'More about it',
		'FAQ': 'Frequently Asked Questions',
		'WHAT_IS': 'What is',
		'WHERE_IT_STARTED': 'Where it all started',
		'WHERE_IS_GOING': 'Where An Addventure is going',
		'AN_ADDVENTURE': 'An Addventure',
		'WHAT_IS_CONTENT': '''
			is a site for writing Collaborative Tales,
			in which every user can carry on everyone else's work.
			''',
		'CURRENTLY_HAS': 'The site currectly has',
		'REGISTERED_USERS': 'registered users',
		'WHERE_IT_STARTED_CONTENT': '''
			It all started with a similar, yet different, idea from my friend Joelton.
			With some research and some more ideas I addapted the original one to fit
			the writing model to which I felt more confortable with, the addventure model:
			''',
		'AN_ADDVENTURE_CONTENT': '''
			An addventure, as a writing model, is a type of online interactive fiction that
			combines aspects of round-robin stories and Choose Your Own Adventure-style tales.
			Like a round-robin story, an addventure is a form of collaborative fiction in
			which many authors contribute to a story, each writing discrete segments.
			However, like a gamebook, the resulting narrative is non-linear, allowing authors
			to branch out in different directions after each segment of the story.
			The result is a continually growing work of hypertext fiction.
			''',
		'WHERE_IS_GOING_CONTENT': '''
			<a href="/contact">I'm open to sugestions</a> as to what would be the next big thing for <strong>An Addventure</strong>.
			''',
		'WHAT_IS_AN_ADDVENTURE': 'What is an addventure',
		'WHAT_IS_COLLABORATIVE_TALE': 'What is a Collaborative Tale',
		'COLLABORATIVE_TALE_CONTENT': 'It\'s a tale to which more than one person can (and should) collaborate.',
		'SO_I_CAN_CONTRIBUTE': 'So I can collaborate to any tale I want',
		'SO_I_CAN_CONTRIBUTE_CONTENT': '''
			Well, you can send collaborations to every Public Tale, but the acceptance of
			your collaboration still depends on the personal opinion of the creator of the tale,
			that is, your collaboration will only be a part of a tale if the owner of
			the tale accepted it.
			''',
		'WHAT_IS_PUBLIC_TALE': 'What is a Public Tale',
		'WHAT_IS_PUBLIC_TALE_CONTENT': '''
			A Public Tale is one that can be seen by any user of the site (registered or not).
			And any registered user can send a collaboration to it (although, as previously stated,
				the acceptance of such collaboration still depends uppon the owner's opinion).
			''',
		'WHAT_IS_PRIVATE_TALE': 'And a Private one',
		'WHAT_IS_PRIVATE_TALE_CONTENT': '''
			A Private Tale, in contrast, can only be seen and collaborated to by its owner
			and whichever users the owner decides to invite (but the acceptance of the
				collaborations still depends on the owner of the Pivate Tale).
			''',
		'DELETE_TALE': 'Delete Tale',
		'DELETE_TALE_CONTENT': '''
			Once you delete a tale, there is no going back.<br>
			<strong>This action CANNOT be undone</strong>.<br>
			This will permanently delete the
			tale and remove all collaborations.<br>
			Please be certain.
			''',
		'DANGER_ZONE': 'Danger Zone',
		'SIGN_UP_MESSAGE': 'An email with the next step in the Account Registration process was sent to',
		'RESET_PASSWORD_MESSAGE': 'A recovering email has been sent to',
		'NO_RESULT_TALES': 'Unable to find any tale matching',
		'NO_RESULT_USERS': 'Unable to find any user matching',
		'SORT_BEST_MATCH': 'Sort: Best Match',
		'SORT_MOST_RECENTLY_JOINED': 'Sort: Most Recently Joined',
		'SORT_LEAST_RECENTLY_JOINED': 'Sort: Least Recently Joined',
		'SORT_MORE_STARS': 'Sort: More Stars',
		'SORT_FEWEST_STARS': 'Sort: Fewest Stars',
		'SORT_RECENTLY_UPDATED': 'Sort: Recently Updated',
		'SORT_LEAST_RECENTLY_UPDATED': 'Sort: Least Recently Updated',
		'FULLSCREEN': 'Fullscreen',
		'HELP_ME_OUT': 'Help Me Improve the Site',
		'MESSAGE': 'Message',
		'SEND': 'Send',
		'CONTACT_MESSAGE_2': 'or fill the form below:',
		'CONTACT_MESSAGE_RECEIVED': 'Your message was sent. We\'ll get back to you shortly.',
		'MIN_CHARACTERS': 'Type at least 3 characters!',
		'INTERNAL_ERROR': 'Internal Server Error',
		'INTERNAL_ERROR_MESSAGE': 'Sorry, something went wrong! People will get fired because of that!',
		'TALES_GENRES': 'Tale\'s Genres',
		'UPDATE_CHAPTER': 'Update Chapter',
		'UPDATE_CONTRIBUTION_REQUEST': 'Update Collaboration Request',
	},
	'pt': {
		'TOP_10_GENRES': 'Gêneros Mais Acessados',
		'MY_PROFILE': 'Meu Perfil',
		'LOGOUT': 'Sair',
		'LOGIN': 'Entrar',
		'SIGN_UP': 'Cadastre-se',
		'SEARCH_BY_GENRES': 'Procurar por Gêneros',
		'TERMS': 'Termos',
		'PRIVACY': 'Privacidade',
		'CONTACT': 'Contate-me',
		'ABOUT': 'Sobre',
		'TALE_AND_OR_USER': 'conto e usuário',
		'PASSWORD': 'Senha',
		'REPEAT_PASSWORD': 'Confirme a Senha',
		'FORGOT_PASSWORD': 'esqueceu sua senha',
		'OR': 'o',
		'ENTER_EMAIL': 'Digite seu email',
		'SUBMIT': 'Enviar',
		'CHANGE_PASSWORD': 'Alterar Senha',
		'NEW_PASSWORD': 'Nova Senha',
		'CONFIRM_NEW_PASSWORD': 'Confirme nova Senha',
		'UPDATE_PASSWORD': 'Atualizar Senha',
		'JOIN': 'Entrar',
		'NOT_FOUND': 'Página Não Encontrada',
		'CHAPTERS': 'Capítulos',
		'NO_CHAPTERS_TALE': 'Não há capítulos para este Contro',
		'FOR_CHAPTER': 'No Capítulo',
		'PUBLISHED_BY': 'publicado por',
		'ON': 'em',
		'TALE': 'Conto',
		'CONTRIBUTE': 'Colaborar',
		'TITLE': 'Título',
		'BY': 'por',
		'CONTRIBUTION_REQUEST': 'Pedido de Colaboração',
		'OPEN': 'Aberto',
		'CLOSED': 'Fechado',
		'ACCEPTED': 'Aceito',
		'REFUSED': 'Recusado',
		'CHAPTER': 'Capítulo',
		'CONTRIBUTION_REQUESTS': 'Pedidos de Colaborações',
		'OPEN_CONTRIBUTION_REQUESTS': 'Pedidos de Colaborações Abertos',
		'CLOSED_CONTRIBUTION_REQUESTS': 'Pedidos de Colaborações Fechados',
		'CONTRIBUTIONS': 'colaborações',
		'NO_CONTRIBUTIONS_TALE': 'Não há colaborações para este Conto',
		'WRITERS': 'Escritores',
		'NEW_TALE': 'Novo Conto',
		'DESCRIPTION': 'Descrição',
		'GENRES': 'Gêneros',
		'TALE_TYPE': 'Tipo do Conto',
		'PUBLIC': 'Público',
		'PRIVATE': 'Privado',
		'TALE_LICENSE': 'Licença do Conto',
		'SPECIFICATION': 'especificação',
		'CREATE': 'Criar',
		'SITE_HEADER': 'Que tal ir em uma Addventure',
		'INVITE_FRIEND': 'Convide um Amigo',
		'INVITE': 'Convidado',
		'EMAIL_INVITED_USER': 'Username ou Email do seu amigo',
		'CREATE_TALE': 'Criar Conto',
		'EDIT_PROFILE': 'Alterar Perfil',
		'BIOGRAPHY': 'Sobre mim',
		'SEARCH': 'Procurar',
		'TALES': 'Contos',
		'USERS': 'Usuários',
		'OPTIONS': 'Opções',
		'UPDATE_TALE_INFO': 'Alterar Informações do Conto',
		'INVITE_FRIEND_TO_TALE': 'Convidar um Amigo para seu Conto Privado',
		'DOWNLOAD_CHAPTER': 'Baixar este Capítulo',
		'DOWNLOAD_ALL': 'Baixar tudo até este Capítulo',
		'CONTINUE_CHAPTER': 'Continuar este Capítulo',
		'NO_CHAPTER': 'O Criador deste Conto ainda não adicionou o Primeiro Capítulo',
		'ADD_FIRST_CHAPTER': 'adicione o Primeiro Capítulo',
		'HERE': 'aqui',
		'ACCOUNT_SETTINGS': 'Configurações da Conta',
		'UPDATE_PROFILE': 'Atualizar Perfil',
		'TALE_SETTINGS': 'Configurações do Conto',
		'UPDATE_TALE': 'Atualizar Conto',
		'UPDATE': 'Atualizar',
		'NO_CLOSED_CONTRIBUTIONS_TALE': 'Não há Colaborações Fechadas neste Conto',
		'NO_OPEN_CONTRIBUTIONS_TALE': 'Não há Colaborações Abertas neste Conto',
		'SUBMITTED_ON': 'submetido em',
		'ACCEPT_CONTRIBUTION': 'Aceitar Colaboração',
		'REFUSE_CONTRIBUTION': 'Recusar Colaboração',
		'MY_TALES': 'Meus Contos',
		'TALES_CONTRIBUTED_TO': 'Contos para os quais colaborar',
		'JOINED_ON': 'Cadastrou-se em',
		'SETTINGS': 'Configurações',
		'CONTENT': 'Conteúdo',
		'LICENSE': 'Licença',
		'UNWATCH': 'Parar de Seguir',
		'WATCH': 'Seguir',
		'UNSTAR': 'Tirar Recomendação',
		'STAR': 'Recomendar',
		'STARS': 'Estrelas',
		'PUBLIC_PROFILE': 'Perfil Público',
		'AVATAR_IMAGE': 'Imagem de Perfil',
		'NAME': 'Nome',
		'PUBLIC_EMAIL': 'Email Público',
		'SHOW': 'Sim, exiba',
		'NO_SHOW': 'Não exiba meu email',
		'TOP_10': 'Contos recomendados',
		'TOP_10_TODAY': 'Hoje',
		'TOP_10_ALL': 'Sempre',
		'STARS_TODAY': 'estrelas hoje',
		'OLD_PASSWORD': 'Senha Antiga',
		'FORGOT_MY_PASSWORD': 'Eu esqueci minha senha',
		'WAS_FOUND': 'Foi encontrado',
		'WERE_FOUND': 'Foram encontrados',
		'RESULTS': 'resultados',
		'RESULT': 'resultado',
		'LAST_UPDATED_ON': 'Atualizado em',
		'PREVIOUS_CHAPTER': 'Capítulo Anterior',
		'ADD_AVATAR': 'Enviar nova imagem',

		'INVALID_USER': 'Usuário Inválido',
		'INVALID_NAME': 'NOME Deve conter entre 3 e 50 caracteres.',
		'INVALID_USERNAME': 'USERNAME Deve conter entre 3 e 50 caracteres.',
		'INVALID_EMAIL': 'Email Inválido.',
		'INVALID_PASSWORD': 'SENHA Deve conter pelo menos 6 caracters.',
		'INVALID_BIOGRAPHY': 'BIOGRAFIA Pode ter no máximo 500 caracteres.',
		'INVALID_TITLE': 'TÍTULO Pode ter no máximo 500 caracteres.',
		'INVALID_CONTENT': 'CONTEÚDO Deve conter pelo menos 1 caracter.',
		'INVALID_DESCRIPTION': 'DESCRIÇÃO Pode ter no máximo 500 caracteres.',
		'INVALID_FILE': 'Imagem Inválida.',
		'INVALID_GENRE': 'Gênero Inválido.',
		'INVALID_LICENSE': 'Licença Inválida',
		'USERNAME_TAKEN': 'Este Username não está disponível.',
		'EMAIL_TAKEN': 'Este Email não está disponível.',
		'TITLE_TAKEN': 'Você já possui um Conto com este Título.',
		'PASSWORD_NO_MATCH': 'As Senhas não são iguais.',
		'NO_GENRES': 'Um Conto deve ter ao menos um Gênero.',
		'WRONG_OLD_PASSWORD': 'A Senha antiga está errada.',
		'TOO_WEAK': 'Muito Fraca',

		'ACTION / ADVENTURE': 'Ação / Aventura',
		'CHILDREN\'S TALES': 'Contos Infantis',
		'CRIME / DETECTIVE': 'Crime / Detetive',
		'FABLE / FOLKLORE': 'Fábula / Folclore',
		'FAN FICTION': 'Fan Fiction',
		'FANTASY': 'Fantasia',
		'FEMINIST': 'Feminista',
		'FLASH FICTION': 'Flash Fiction',
		'FOREIGN LANGUAGE': 'Estrangeiro',
		'GAY / LESBIAN': 'Gay / Lesbica',
		'HISTORICAL': 'Histórico',
		'HORROR': 'Horror',
		'HUMOR': 'Humor',
		'JUST FOR FUN': 'Só de Zueira',
		'LITERARY': 'Literário',
		'MATURE THEMES': 'Temas Adultos',
		'MYSTERY / THRILLER': 'Mistério / Suspense',
		'MYTHOLOGY': 'Mitologia',
		'POLITICS': 'Política',
		'RELIGION / SPIRITUALITY': 'Religião / Espiritualidade',
		'ROMANCE': 'Romance',
		'SATIRE / PARODY': 'Sátira / Parodia',
		'SCIENCE FICTION': 'Ficção Científica',
		'SPECIAL INTEREST': 'Interesse Especial',
		'SPORTS': 'Esportes',
		'SUPERNATURAL': 'Supernatural',
		'TABOO': 'Tab',
		'TEEN / YOUNG ADULT': 'Adolescente / Jovem Adulto',
		'URBAN': 'Urbano',
		'WESTERN': 'Ocidental',

		'ADD': 'Add',
		'REMOVE': 'Remover',
		'CONTACT_MESSAGE': 'Qualquer problema, reclamação e/ou sugestão, por favor envie um email para:',
		'WAITING_FIRST_CHAPTER': 'Ainda aguardando o Primeiro Capítulo',
		'SITE_PRESENTATION': 'Site da hora para escrever Contos Colaborativos',
		'TALE_BY': 'conto de',
		'SITE_LOGO': 'An Addventure',
		'NOT_WRONG': 'Não, não está escrito errado.',
		'MORE_ABOUT': 'Mais sobre',
		'FAQ': 'Frequently Asked Questions',
		'WHAT_IS': 'O que é',
		'WHERE_IT_STARTED': 'Onde tudo começo',
		'WHERE_IS_GOING': 'Onde An Addventure está indo',
		'AN_ADDVENTURE': 'An Addventure',
		'WHAT_IS_CONTENT': '''
			é um site para a escrita de Contos Colaborativos,
			nos quais qualquer usuário pode continuar o trabalho de qualquer outro usuário.
			''',
		'CURRENTLY_HAS': 'Atualmente o site possui',
		'REGISTERED_USERS': 'usuários registrados',
		'WHERE_IT_STARTED_CONTENT': '''
			Tudo começou com uma ideia similar, porém diferente, do meu amigo Joelton.
			Com alguma pesquisa e outras ideias eu adaptei a ideia original para combinar
			melhor com o estilo de escrita que eu achei melhor, o estilo addventure:
			''',
		'AN_ADDVENTURE_CONTENT': '''
			Uma addventure é um tipo de ficção interativa online
			que combina aspectos de histórias round-robin e contos do estilo
			"Escolha Sua Própria Aventura". Como uma história round-robin, uma addventure
			é uma forma de ficção colaborativa na qual muitos autores contribuem para o conto,
			cada um escrevendo pequenos segmentos. No entanto, como um gamebook, o resultado
			é uma narrativa não linear, permitindo que os autores criem diferentes
			continuações para qualquer segmento da história.
			O resultado é uma ficção em hipertexto em contínuo crescimento.
			''',
		'WHERE_IS_GOING_CONTENT': '''
			<a href="/contact">Estou aberto a sugestões</a> sobre qual seria o próximo grande passo para <strong>An Addventure</strong>.
			''',
		'WHAT_IS_AN_ADDVENTURE': 'O que é uma addventure',
		'WHAT_IS_COLLABORATIVE_TALE': 'O que é um Conto Colaborativo',
		'COLLABORATIVE_TALE_CONTENT': 'É um conto no qual mais de uma pessoal pode (e deveria) colaborar.',
		'SO_I_CAN_CONTRIBUTE': 'Então eu posso colaborar para o conto que eu quiser',
		'SO_I_CAN_CONTRIBUTE_CONTENT': '''
			Bom, você pode enviar colaborações para qualquer Conto Público, mas a aceitação
			da sua colaboração vai depender da opinião pessoal do dono do conto,
			ou seja, sua colaboração só será parte do conto se o usuário que o criou aceitá-la.
			''',
		'WHAT_IS_PUBLIC_TALE': 'O que é um Conto Público',
		'WHAT_IS_PUBLIC_TALE_CONTENT': '''
			Um Conto Público é conto que pode ser visto por qualquer usuário do site (registrado ou não).
			E qualquer usuário registrado pode enviar colaborações para ele (embora, como dito
				anteriormente, a aceitação da colaboração ainda depende da opinião do dono).
			''',
		'WHAT_IS_PRIVATE_TALE': 'E um Conto Privado',
		'WHAT_IS_PRIVATE_TALE_CONTENT': '''
			Já um Conto Privado pode ser visualizado apenas pelo seu dono e quaisquer usuários
			que ele convide para o conto. O mesmo vale para colaborações: só podem enviá-las a
			um Conto Privado o dono do conto e os usuários convidados (mas a aceitação das
				colaborações ainda depende do dono do conto).
			''',
		'DELETE_TALE': 'Deletar Conto',
		'DELETE_TALE_CONTENT': '''
			Uma vez deletado o conto, não há volta.<br>
			<strong>Esta ação NÃO PODE ser desfeita.</strong><br>
			Isso vai deletar permanentemente o conto e remover todas as colaborações.<br>
			Por favor, tenhar certeza.
			''',
		'DANGER_ZONE': 'Zona de Perigo',
		'SIGN_UP_MESSAGE': 'Um email com o próximo passo no processo de Cadastro foi enviado para',
		'RESET_PASSWORD_MESSAGE': 'Um email de recuperação foi enviado para',
		'NO_RESULT_TALES': 'Não foi encontrado nenhum conto com',
		'NO_RESULT_USERS': 'Não foi encontrado nenhum usuário com',
		'SORT_BEST_MATCH': 'Ordenar: Mais parecido',
		'SORT_MOST_RECENTLY_JOINED': 'Ordenar: Recentemente Cadastrado',
		'SORT_LEAST_RECENTLY_JOINED': 'Ordenar: Menos Recentemente Cadastrado',
		'SORT_MORE_STARS': 'Ordenar: Mais Recomendações',
		'SORT_FEWEST_STARS': 'Ordenar: Menos Recomendações',
		'SORT_RECENTLY_UPDATED': 'Ordenar: Recentemente Atualizado',
		'SORT_LEAST_RECENTLY_UPDATED': 'Ordenar: Menos Recentemente Atualizado',
		'FULLSCREEN': 'Tela Cheia',
		'HELP_ME_OUT': 'Me Ajude a Melhorar o Site',
		'MESSAGE': 'Mensagem',
		'SEND': 'Enviar',
		'CONTACT_MESSAGE_2': 'ou preencha o formulário abaixo:',
		'CONTACT_MESSAGE_RECEIVED': 'Sua mensagem foi enviada. Vamos lhe retornar em pouco tempo.',
		'MIN_CHARACTERS': 'Digite ao menos 3 caracteres!',
		'INTERNAL_ERROR': 'Erro no Servidor',
		'INTERNAL_ERROR_MESSAGE': 'Nos desculpe, algo deu errado! Pessoas serão demitidas por causa disso!',
		'TALES_GENRES': 'Gêneros dos Contos',
		'UPDATE_CHAPTER': 'Atualizar Capítulo',
		'UPDATE_CONTRIBUTION_REQUEST': 'Atualizar Pedido de Colaboração',
	}
}
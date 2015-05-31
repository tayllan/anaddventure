CREATE TABLE system_user (
	system_user_id SERIAL PRIMARY KEY,
	system_user_name VARCHAR(50) NOT NULL,
	system_user_username VARCHAR(50) UNIQUE NOT NULL,
	system_user_email VARCHAR(50) UNIQUE NOT NULL,
	system_user_password VARCHAR(50) NOT NULL,
	system_user_signup_date TIMESTAMP NOT NULL,
	system_user_biography VARCHAR(500),
	system_user_is_email_visible BOOLEAN DEFAULT False,
	system_user_is_valid_account BOOLEAN DEFAULT False
);

CREATE TABLE genre (
	genre_id SERIAL PRIMARY KEY,
	genre_type VARCHAR(50) UNIQUE NOT NULL,
	genre_tale_count INT DEFAULT 0
);

CREATE TABLE signup_queue (
	signup_queue_system_user_id INTEGER PRIMARY KEY,
	signup_queue_id VARCHAR(150) NOT NULL
);

CREATE TABLE password_change_requests (
	password_change_requests_system_user_id INTEGER PRIMARY KEY,
	password_change_requests_id VARCHAR(150) NOT NULL,
	password_change_requests_datetime TIMESTAMP NOT NULL
);

CREATE TABLE license (
	license_id SERIAL PRIMARY KEY,
	license_name VARCHAR(50) NOT NULL,
	license_url VARCHAR(200) NOT NULL
);

CREATE TABLE tale (
	tale_id SERIAL PRIMARY KEY,
	tale_title VARCHAR(500) NOT NULL,
	tale_description VARCHAR(500),
	tale_category INTEGER NOT NULL,
	tale_creator INTEGER REFERENCES system_user NOT NULL,
	tale_license INTEGER REFERENCES license NOT NULL,
	tale_star_count INTEGER DEFAULT 0,
	tale_follow_count INTEGER DEFAULT 0,
	tale_contribution_request_count INTEGER DEFAULT 0,
	tale_creation_datetime TIMESTAMP NOT NULL
);

CREATE TABLE tale_genre (
	tale_genre_tale_id INTEGER REFERENCES tale,
	tale_genre_genre_id INTEGER REFERENCES genre,
	PRIMARY KEY(tale_genre_tale_id, tale_genre_genre_id)
);

CREATE TABLE star (
	star_system_user_id INTEGER REFERENCES system_user,
	star_tale_id INTEGER REFERENCES tale,
	star_datetime TIMESTAMP NOT NULL,
	PRIMARY KEY(star_system_user_id, star_tale_id)
);

CREATE TABLE follow (
	follow_system_user_id INTEGER REFERENCES system_user,
	follow_tale_id INTEGER REFERENCES tale,
	PRIMARY KEY(follow_system_user_id, follow_tale_id)
);

CREATE TABLE chapter (
	chapter_id SERIAL PRIMARY KEY,
	chapter_system_user_id INTEGER REFERENCES system_user NOT NULL,
	chapter_tale_id INTEGER REFERENCES tale NOT NULL,
	chapter_number INTEGER NOT NULL,
	chapter_title VARCHAR(500) NOT NULL,
	chapter_content VARCHAR(100000) NOT NULL,
	chapter_datetime TIMESTAMP NOT NULL,
	chapter_download_count INTEGER DEFAULT 0,
	chapter_previous_chapter INTEGER DEFAULT 0 REFERENCES chapter
);

CREATE TABLE contribution_request (
	contribution_request_id SERIAL PRIMARY KEY,
	contribution_request_system_user_id INTEGER REFERENCES system_user NOT NULL,
	contribution_request_tale_id INTEGER REFERENCES tale NOT NULL,
	contribution_request_number INTEGER NOT NULL,
	contribution_request_title VARCHAR(500) NOT NULL,
	contribution_request_content VARCHAR(100000) NOT NULL,
	contribution_request_datetime TIMESTAMP NOT NULL,
	contribution_request_previous_chapter INTEGER DEFAULT 0 REFERENCES chapter NOT NULL,
	contribution_request_was_accepted BOOLEAN DEFAULT False,
	contribution_request_was_closed BOOLEAN DEFAULT False
);

CREATE TABLE invitation (
	invitation_id SERIAL PRIMARY KEY,
	invitation_creator INTEGER REFERENCES system_user NOT NULL,
	invitation_invited INTEGER REFERENCES system_user NOT NULL,
	invitation_tale_id INTEGER REFERENCES tale NOT NULL
);

-- BEGIN star Functions and Triggers
CREATE OR REPLACE FUNCTION function_adds_star_count_on_tale()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE tale SET tale_star_count = tale_star_count + 1 WHERE tale_id = NEW.star_tale_id;
		RETURN NEW;
	END;
$function$;

CREATE TRIGGER trigger_adds_star_count_on_tale
	BEFORE INSERT ON star
	FOR EACH ROW EXECUTE PROCEDURE function_adds_star_count_on_tale();

CREATE OR REPLACE FUNCTION function_subtracts_star_count_on_tale()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE tale SET tale_star_count = tale_star_count - 1 WHERE tale_id = OLD.star_tale_id;
		RETURN OLD;
	END;
$function$;

CREATE TRIGGER trigger_subtracts_star_count_on_tale
	BEFORE DELETE ON star
	FOR EACH ROW EXECUTE PROCEDURE function_subtracts_star_count_on_tale();
-- END star Functions and Triggers
	
-- BEGIN follow Functions and Triggers
CREATE OR REPLACE FUNCTION function_adds_follow_count_on_tale()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE tale SET tale_follow_count = tale_follow_count + 1 WHERE tale_id = NEW.follow_tale_id;
		RETURN NEW;
	END;
$function$;

CREATE TRIGGER trigger_adds_follow_count_on_tale
	BEFORE INSERT ON follow
	FOR EACH ROW EXECUTE PROCEDURE function_adds_follow_count_on_tale();

CREATE OR REPLACE FUNCTION function_subtracts_follow_count_on_tale()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE tale SET tale_follow_count = tale_follow_count - 1 WHERE tale_id = OLD.follow_tale_id;
		RETURN OLD;
	END;
$function$;

CREATE TRIGGER trigger_subtracts_follow_count_on_tale
	BEFORE DELETE ON follow
	FOR EACH ROW EXECUTE PROCEDURE function_subtracts_follow_count_on_tale();
-- END follow Functions and Triggers

-- BEGIN tale_genre Functions and Triggers
CREATE OR REPLACE FUNCTION function_adds_genre_count_on_genre()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE genre SET genre_tale_count = genre_tale_count + 1 WHERE genre_id = NEW.tale_genre_genre_id;
		RETURN NEW;
	END;
$function$;

CREATE TRIGGER trigger_adds_genre_count_on_genre
	BEFORE INSERT ON tale_genre
	FOR EACH ROW EXECUTE PROCEDURE function_adds_genre_count_on_genre();

CREATE OR REPLACE FUNCTION function_subtracts_genre_count_on_genre()
	RETURNS trigger
	LANGUAGE plpgsql
AS $function$
	BEGIN
		UPDATE genre SET genre_tale_count = genre_tale_count - 1 WHERE genre_id = OLD.tale_genre_genre_id;
		RETURN OLD;
	END;
$function$;

CREATE TRIGGER trigger_subtracts_genre_count_on_genre
	BEFORE DELETE ON tale_genre
	FOR EACH ROW EXECUTE PROCEDURE function_subtracts_genre_count_on_genre();
-- END tale_genre Functions and Triggers

-- inserting genres
INSERT INTO genre (genre_type) VALUES ('ACTION / ADVENTURE');
INSERT INTO genre (genre_type) VALUES ('CHILDREN''S TALES');
INSERT INTO genre (genre_type) VALUES ('CRIME / DETECTIVE');
INSERT INTO genre (genre_type) VALUES ('FABLE / FOLKLORE');
INSERT INTO genre (genre_type) VALUES ('FAN FICTION');
INSERT INTO genre (genre_type) VALUES ('FANTASY');
INSERT INTO genre (genre_type) VALUES ('FEMINIST');
INSERT INTO genre (genre_type) VALUES ('FLASH FICTION');
INSERT INTO genre (genre_type) VALUES ('FOREIGN LANGUAGE');
INSERT INTO genre (genre_type) VALUES ('GAY / LESBIAN');
INSERT INTO genre (genre_type) VALUES ('HISTORICAL');
INSERT INTO genre (genre_type) VALUES ('HORROR');
INSERT INTO genre (genre_type) VALUES ('HUMOR');
INSERT INTO genre (genre_type) VALUES ('JUST FOR FUN');
INSERT INTO genre (genre_type) VALUES ('LITERARY');
INSERT INTO genre (genre_type) VALUES ('MATURE THEMES');
INSERT INTO genre (genre_type) VALUES ('MYSTERY / THRILLER');
INSERT INTO genre (genre_type) VALUES ('MYTHOLOGY');
INSERT INTO genre (genre_type) VALUES ('POLITICS');
INSERT INTO genre (genre_type) VALUES ('RELIGION / SPIRITUALITY');
INSERT INTO genre (genre_type) VALUES ('ROMANCE');
INSERT INTO genre (genre_type) VALUES ('SATIRE / PARODY');
INSERT INTO genre (genre_type) VALUES ('SCIENCE FICTION');
INSERT INTO genre (genre_type) VALUES ('SPECIAL INTEREST');
INSERT INTO genre (genre_type) VALUES ('SPORTS');
INSERT INTO genre (genre_type) VALUES ('SUPERNATURAL');
INSERT INTO genre (genre_type) VALUES ('TABOO');
INSERT INTO genre (genre_type) VALUES ('TEEN / YOUNG ADULT');
INSERT INTO genre (genre_type) VALUES ('URBAN');
INSERT INTO genre (genre_type) VALUES ('WESTERN');

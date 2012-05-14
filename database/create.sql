

# Accounts
CREATE TABLE IF NOT EXISTS users (
  id INT(11) UNSIGNED NOT NULL COMMENT 'Twitter id',
  status TINYINT(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Status of the user',
  signin_count MEDIUMINT(8) UNSIGNED DEFAULT 0 COMMENT 'Amount of times the user has signed in',
  recent_signin TIMESTAMP DEFAULT 0 COMMENT 'The most recent time the user signed in',
  name VARCHAR(255) COMMENT 'Users name',
  avatar_url VARCHAR(255) DEFAULT NULL COMMENT 'URL to avatar',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When the user was created',
  access_key VARCHAR(255) COMMENT 'Twitter access token',
  access_secret VARCHAR(255) COMMENT 'Twitter access token secret',
  handle VARCHAR(255) COMMENT 'Users handle',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Information about our users';


# Lunches
CREATE TABLE IF NOT EXISTS lunch (
  id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique lunch id',
  creator_id INT(11) UNSIGNED NOT NULL COMMENT 'Twitter id',
  food VARCHAR(255) COMMENT 'Food to eat',
  place VARCHAR(255) COMMENT 'Where to eat',
  lunch_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When to eat',
  slots INT(3) UNSIGNED NOT NULL COMMENT 'How many slots',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Information about lunches';


CREATE TABLE IF NOT EXISTS lunch_tags (
  id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique lunch id',
  lunch_id INT(11) UNSIGNED NOT NULL COMMENT 'Reference to lunch',
  tag VARCHAR(255) COMMENT 'Tag',
  PRIMARY KEY (id),
  KEY (lunch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tags for lunches';


CREATE TABLE IF NOT EXISTS lunch_participants (
  id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Relation id',
  lunch_id INT(11) UNSIGNED NOT NULL COMMENT 'Reference to lunch',
  user_id INT(11) UNSIGNED NOT NULL COMMENT 'Reference to user',
  PRIMARY KEY (id),
  UNIQUE KEY (lunch_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Pariticpants for lunches';

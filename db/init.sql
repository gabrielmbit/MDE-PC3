CREATE DATABASE IF NOT EXISTS pictures
	DEFAULT CHARACTER SET utf8mb4
	DEFAULT COLLATE utf8mb4_general_ci;

USE pictures;

CREATE TABLE IF NOT EXISTS pictures (
	id CHAR(36) NOT NULL,
	path VARCHAR(255) NOT NULL,
	date VARCHAR(19) NOT NULL,
	PRIMARY KEY (id),
	INDEX idx_pictures_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tags (
	tag VARCHAR(32) NOT NULL,
	picture_id CHAR(36) NOT NULL,
	confidence DOUBLE NOT NULL,
	date VARCHAR(19) NOT NULL,
	PRIMARY KEY (tag, picture_id),
	INDEX idx_tags_picture_id (picture_id),
	INDEX idx_tags_tag (tag),
	INDEX idx_tags_date (date),
	CONSTRAINT fk_tags_picture
		FOREIGN KEY (picture_id) REFERENCES pictures(id)
		ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

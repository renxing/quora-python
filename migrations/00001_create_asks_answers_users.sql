SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

CREATE DATABASE wenda;
use wenda;

DROP TABLE IF EXISTS `asks`;
CREATE TABLE asks (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(512) NOT NULL,
    body MEDIUMTEXT NOT NULL,
    summary VARCHAR(512) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    answers_count INT NOT NULL default 0,
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  bio VARCHAR(255),
  created_at DATETIME NOT NULL,
  updated_at TIMESTAMP NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `answers`;
CREATE TABLE `answers` (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ask_id INT NOT NULL,
  user_id INT,
  body MEDIUMTEXT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  KEY `idx_ask_id` (`ask_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


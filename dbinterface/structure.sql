--
-- 2018-04-10 10:20
--
-- Struttura database 'segnalazioni'
--

CREATE DATABASE IF NOT EXISTS `segnalazioni` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `segnalazioni`;

DROP TABLE IF EXISTS `images`;
CREATE TABLE IF NOT EXISTS `images` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `issue_id` int(10) UNSIGNED NOT NULL,
  `filename` text,
  `category` varchar(50) DEFAULT NULL,
  `classification_dict` text,
  PRIMARY KEY (`id`),
  KEY `issue_images` (`issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `issues`;
CREATE TABLE IF NOT EXISTS `issues` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(10) UNSIGNED NOT NULL,
  `msg_id` varchar(30) DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(10,8) DEFAULT NULL,
  `channel` varchar(20) DEFAULT '',
  `text` text,
  `category` varchar(50) DEFAULT '',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `classification_dict` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `issues_idx0` (`user_id`,`msg_id`,`channel`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` varchar(30) DEFAULT NULL,
  `channel` varchar(20) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_channels` (`user_id`,`channel`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE `images`
  ADD CONSTRAINT `issue_images` FOREIGN KEY (`issue_id`) REFERENCES `issues` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `issues`
  ADD CONSTRAINT `issue_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

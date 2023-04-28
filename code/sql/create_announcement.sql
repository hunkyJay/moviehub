CREATE TABLE `Announcement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `announcement_id` int NOT NULL,
  `content` varchar(255) NOT NULL,
  `create_time` timestamp NOT NULL,
  `update_time` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `announcement_id_UNIQUE` (`announcement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `Release` (
  `id` int NOT NULL AUTO_INCREMENT,
  `release_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `room_id` int NOT NULL,
  `price` float NOT NULL,
  `is_delete` int NOT NULL default 0,
  `release_time` timestamp NOT NULL,
  `create_time` timestamp NOT NULL,
  `update_time` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `release_id_UNIQUE` (`release_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8

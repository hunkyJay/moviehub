CREATE TABLE `Movie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `movie_id` int NOT NULL,
  `movie_name` varchar(40) NOT NULL,
  `poster` varchar(255) NOT NULL,
  `duration` int NOT NULL,
  `type` varchar(20) NOT NULL,
  `cast` varchar(100) DEFAULT NULL,
  `introduction` varchar(100) DEFAULT NULL,
  `create_time` timestamp NOT NULL,
  `update_time` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_id_UNIQUE` (`movie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8
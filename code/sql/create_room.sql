CREATE TABLE `Room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `row_size` int NOT NULL,
  `column_size` int NOT NULL,
  `create_time` timestamp NOT NULL,
  `update_time` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_id_UNIQUE` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8
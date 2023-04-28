CREATE TABLE `seat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `release_id` int NOT NULL,
  `room_id` int NOT NULL,
  `row_id` int NOT NULL,
  `column_id` int NOT NULL,
  `is_available` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb3;
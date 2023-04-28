CREATE TABLE `Staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `staff_id` int NOT NULL,
  `password_hash` varchar(100) NOT NULL,
  `password_salt` varchar(50) NOT NULL,
  `name` varchar(20) NOT NULL,
  `level` int(10) unsigned zerofill NOT NULL,
  `phone` bigint NOT NULL,
  `email` varchar(40) NOT NULL,
  `create_time` timestamp NOT NULL,
  `update_time` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_id_UNIQUE` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8
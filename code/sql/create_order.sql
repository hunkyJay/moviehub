CREATE TABLE `Order` (
          `id` int NOT NULL AUTO_INCREMENT,
          `order_id` int NOT NULL,
          `customer_username` varchar(20) NOT NULL,
          `room_id` int NOT NULL,
          `seat_content` varchar(255) NOT NULL,
          `seat_num` int NOT NULL,
          `release_id` int NOT NULL,
          `movie_name` varchar(40) NOT NULL,
          `price` float NOT NULL,
          `is_cancel` int NOT NULL DEFAULT '0',
          `release_time` timestamp NOT NULL,
          `create_time` timestamp NOT NULL,
          `update_time` timestamp NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `order_id_UNIQUE` (`order_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
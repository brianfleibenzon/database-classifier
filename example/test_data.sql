--
-- Schema creation `schema1`
--

DROP DATABASE IF EXISTS `schema1`;
CREATE DATABASE `schema1`;

USE schema1;
--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `credit_card` varchar(45) DEFAULT NULL,
  `total` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Schema creation `schema2`
--

DROP DATABASE IF EXISTS `schema2`;
CREATE DATABASE `schema2`;
USE schema2; 

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Mailbox` varchar(45) DEFAULT NULL,
  `Passphrase` varchar(45) DEFAULT NULL,
  `WorkPhone` varchar(45) DEFAULT NULL,
  `MobilePhone` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `CustomerId` int DEFAULT NULL,
  `CardType` varchar(45) DEFAULT NULL,
  `CardNumber` varchar(45) DEFAULT NULL,
  `Total` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
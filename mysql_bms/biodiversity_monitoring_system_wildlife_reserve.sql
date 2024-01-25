CREATE DATABASE  IF NOT EXISTS `biodiversity_monitoring_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `biodiversity_monitoring_system`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: biodiversity_monitoring_system
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `wildlife_reserve`
--

DROP TABLE IF EXISTS `wildlife_reserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wildlife_reserve` (
  `RESERVE_ID` int NOT NULL,
  `NAME` varchar(30) NOT NULL,
  `COORDINATES` varchar(30) DEFAULT NULL,
  `AREA` int DEFAULT NULL,
  `PINCODE` int DEFAULT NULL,
  `ICONIC_SPECIES` varchar(30) DEFAULT NULL,
  `ESTABLISHED_YEAR` year DEFAULT NULL,
  PRIMARY KEY (`RESERVE_ID`),
  KEY `PINCODE` (`PINCODE`),
  KEY `ICONIC_SPECIES` (`ICONIC_SPECIES`),
  CONSTRAINT `wildlife_reserve_ibfk_1` FOREIGN KEY (`PINCODE`) REFERENCES `location` (`PINCODE`),
  CONSTRAINT `wildlife_reserve_ibfk_2` FOREIGN KEY (`ICONIC_SPECIES`) REFERENCES `species` (`SCIENTIFIC_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wildlife_reserve`
--

LOCK TABLES `wildlife_reserve` WRITE;
/*!40000 ALTER TABLE `wildlife_reserve` DISABLE KEYS */;
INSERT INTO `wildlife_reserve` VALUES (1,'Desert National Park','26°N & 70.5°E',3162,345001,'Ardeotis Nigriceps',1981),(2,'Kaziranga National Park','26°40\'N & 93°21\'E',1090,785609,'Rhinoceros unicornis',1974);
/*!40000 ALTER TABLE `wildlife_reserve` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-25 13:45:59

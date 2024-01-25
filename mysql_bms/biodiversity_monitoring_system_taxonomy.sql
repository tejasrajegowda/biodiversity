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
-- Table structure for table `taxonomy`
--

DROP TABLE IF EXISTS `taxonomy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taxonomy` (
  `TAXONOMY_ID` varchar(10) NOT NULL,
  `SCIENTIFIC_NAME` varchar(30) DEFAULT NULL,
  `KINGDOM` varchar(10) DEFAULT NULL,
  `PHYLUM` varchar(10) DEFAULT NULL,
  `SP_CLASS` varchar(10) DEFAULT NULL,
  `ORDERS` varchar(20) DEFAULT NULL,
  `FAMILY` varchar(20) DEFAULT NULL,
  `GENUS` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`TAXONOMY_ID`),
  KEY `SCIENTIFIC_NAME` (`SCIENTIFIC_NAME`),
  CONSTRAINT `taxonomy_ibfk_1` FOREIGN KEY (`SCIENTIFIC_NAME`) REFERENCES `species` (`SCIENTIFIC_NAME`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taxonomy`
--

LOCK TABLES `taxonomy` WRITE;
/*!40000 ALTER TABLE `taxonomy` DISABLE KEYS */;
INSERT INTO `taxonomy` VALUES ('1','Ardeotis Nigriceps','ANIMALIA','CHORDATA','AVES','OTIDIFORMES','OTIDIDAE','ARDEOTIS'),('2','Rhinoceros unicornis','Animalia','Chordata','Mammalia','Perissodactyla','Rhinocerotidae','Rhinoceros');
/*!40000 ALTER TABLE `taxonomy` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-25 13:45:58

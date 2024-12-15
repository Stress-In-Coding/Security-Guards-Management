-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: security_guards_db
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `client_id` varchar(10) NOT NULL,
  `client_details` json NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES 
('C001', '{"name": "Client A", "contact": "123456789"}', 'active'),
('C002', '{"name": "Client B", "contact": "987654321"}', 'active'),
('C003', '{"name": "Client C", "contact": "234567890"}', 'inactive'),
('C004', '{"name": "Client D", "contact": "345678901"}', 'active'),
('C005', '{"name": "Client E", "contact": "456789012"}', 'inactive'),
('C006', '{"name": "Client F", "contact": "567890123"}', 'active'),
('C007', '{"name": "Client G", "contact": "678901234"}', 'inactive'),
('C008', '{"name": "Client H", "contact": "789012345"}', 'active'),
('C009', '{"name": "Client I", "contact": "890123456"}', 'inactive'),
('C010', '{"name": "Client J", "contact": "901234567"}', 'active'),
('C011', '{"name": "Client K", "contact": "012345678"}', 'inactive'),
('C012', '{"name": "Client L", "contact": "123456789"}', 'active'),
('C013', '{"name": "Client M", "contact": "234567890"}', 'inactive'),
('C014', '{"name": "Client N", "contact": "345678901"}', 'active'),
('C015', '{"name": "Client O", "contact": "456789012"}', 'inactive'),
('C016', '{"name": "Client P", "contact": "567890123"}', 'active'),
('C017', '{"name": "Client Q", "contact": "678901234"}', 'inactive'),
('C018', '{"name": "Client R", "contact": "789012345"}', 'active'),
('C019', '{"name": "Client S", "contact": "890123456"}', 'inactive'),
('C020', '{"name": "Client T", "contact": "901234567"}', 'active'),
('C021', '{"name": "Client U", "contact": "012345678"}', 'inactive'),
('C022', '{"name": "Client V", "contact": "123456789"}', 'active'),
('C023', '{"name": "Client W", "contact": "234567890"}', 'inactive'),
('C024', '{"name": "Client X", "contact": "345678901"}', 'active'),
('C025', '{"name": "Client Y", "contact": "456789012"}', 'inactive');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_assignments`
--

DROP TABLE IF EXISTS `employee_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_assignments` (
  `employee_id` varchar(10) NOT NULL,
  `client_id` varchar(10) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('active','completed','cancelled') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`,`client_id`,`start_date`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `employee_assignments_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),
  CONSTRAINT `employee_assignments_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_assignments`
--

LOCK TABLES `employee_assignments` WRITE;
/*!40000 ALTER TABLE `employee_assignments` DISABLE KEYS */;
INSERT INTO `employee_assignments` VALUES 
('E001', 'C001', '2023-01-01', '2023-06-01', 'completed', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('E002', 'C002', '2023-02-01', '2023-07-01', 'active', '2023-02-01 00:00:00', '2023-02-01 00:00:00'),
('E003', 'C003', '2023-03-01', '2023-08-01', 'cancelled', '2023-03-01 00:00:00', '2023-03-01 00:00:00'),
('E004', 'C004', '2023-04-01', '2023-09-01', 'active', '2023-04-01 00:00:00', '2023-04-01 00:00:00'),
('E005', 'C005', '2023-05-01', '2023-10-01', 'completed', '2023-05-01 00:00:00', '2023-05-01 00:00:00'),
('E006', 'C006', '2023-06-01', '2023-11-01', 'active', '2023-06-01 00:00:00', '2023-06-01 00:00:00'),
('E007', 'C007', '2023-07-01', '2023-12-01', 'cancelled', '2023-07-01 00:00:00', '2023-07-01 00:00:00'),
('E008', 'C008', '2023-08-01', '2024-01-01', 'active', '2023-08-01 00:00:00', '2023-08-01 00:00:00'),
('E009', 'C009', '2023-09-01', '2024-02-01', 'completed', '2023-09-01 00:00:00', '2023-09-01 00:00:00'),
('E010', 'C010', '2023-10-01', '2024-03-01', 'active', '2023-10-01 00:00:00', '2023-10-01 00:00:00'),
('E011', 'C011', '2023-11-01', '2024-04-01', 'cancelled', '2023-11-01 00:00:00', '2023-11-01 00:00:00'),
('E012', 'C012', '2023-12-01', '2024-05-01', 'active', '2023-12-01 00:00:00', '2023-12-01 00:00:00'),
('E013', 'C013', '2024-01-01', '2024-06-01', 'completed', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
('E014', 'C014', '2024-02-01', '2024-07-01', 'active', '2024-02-01 00:00:00', '2024-02-01 00:00:00'),
('E015', 'C015', '2024-03-01', '2024-08-01', 'cancelled', '2024-03-01 00:00:00', '2024-03-01 00:00:00'),
('E016', 'C016', '2024-04-01', '2024-09-01', 'active', '2024-04-01 00:00:00', '2024-04-01 00:00:00'),
('E017', 'C017', '2024-05-01', '2024-10-01', 'completed', '2024-05-01 00:00:00', '2024-05-01 00:00:00'),
('E018', 'C018', '2024-06-01', '2024-11-01', 'active', '2024-06-01 00:00:00', '2024-06-01 00:00:00'),
('E019', 'C019', '2024-07-01', '2024-12-01', 'cancelled', '2024-07-01 00:00:00', '2024-07-01 00:00:00'),
('E020', 'C020', '2024-08-01', '2025-01-01', 'active', '2024-08-01 00:00:00', '2024-08-01 00:00:00'),
('E021', 'C021', '2024-09-01', '2025-02-01', 'completed', '2024-09-01 00:00:00', '2024-09-01 00:00:00'),
('E022', 'C022', '2024-10-01', '2025-03-01', 'active', '2024-10-01 00:00:00', '2024-10-01 00:00:00'),
('E023', 'C023', '2024-11-01', '2025-04-01', 'cancelled', '2024-11-01 00:00:00', '2024-11-01 00:00:00'),
('E024', 'C024', '2024-12-01', '2025-05-01', 'active', '2024-12-01 00:00:00', '2024-12-01 00:00:00'),
('E025', 'C025', '2025-01-01', '2025-06-01', 'completed', '2025-01-01 00:00:00', '2025-01-01 00:00:00');
/*!40000 ALTER TABLE `employee_assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_category`
--

DROP TABLE IF EXISTS `employee_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_category` (
  `category_code` varchar(10) NOT NULL,
  `category_description` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_category`
--

LOCK TABLES `employee_category` WRITE;
/*!40000 ALTER TABLE `employee_category` DISABLE KEYS */;
INSERT INTO `employee_category` VALUES 
('CAT001', 'Security Guard', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('CAT002', 'Supervisor', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('CAT003', 'Manager', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('CAT004', 'Receptionist', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('CAT005', 'Technician', '2023-01-01 00:00:00', '2023-01-01 00:00:00');
/*!40000 ALTER TABLE `employee_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_training`
--

DROP TABLE IF EXISTS `employee_training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_training` (
  `employee_id` varchar(10) NOT NULL,
  `course_id` varchar(10) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('ongoing','completed','cancelled') DEFAULT 'ongoing',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`,`course_id`,`start_date`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `employee_training_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),
  CONSTRAINT `employee_training_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `training_courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_training`
--

LOCK TABLES `employee_training` WRITE;
/*!40000 ALTER TABLE `employee_training` DISABLE KEYS */;
INSERT INTO `employee_training` VALUES 
('E001', 'COURSE001', '2023-01-01', '2023-02-01', 'completed', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('E002', 'COURSE002', '2023-02-01', '2023-03-01', 'ongoing', '2023-02-01 00:00:00', '2023-02-01 00:00:00'),
('E003', 'COURSE003', '2023-03-01', '2023-04-01', 'cancelled', '2023-03-01 00:00:00', '2023-03-01 00:00:00'),
('E004', 'COURSE004', '2023-04-01', '2023-05-01', 'completed', '2023-04-01 00:00:00', '2023-04-01 00:00:00'),
('E005', 'COURSE005', '2023-05-01', '2023-06-01', 'ongoing', '2023-05-01 00:00:00', '2023-05-01 00:00:00'),
('E006', 'COURSE006', '2023-06-01', '2023-07-01', 'cancelled', '2023-06-01 00:00:00', '2023-06-01 00:00:00'),
('E007', 'COURSE007', '2023-07-01', '2023-08-01', 'completed', '2023-07-01 00:00:00', '2023-07-01 00:00:00'),
('E008', 'COURSE008', '2023-08-01', '2023-09-01', 'ongoing', '2023-08-01 00:00:00', '2023-08-01 00:00:00'),
('E009', 'COURSE009', '2023-09-01', '2023-10-01', 'cancelled', '2023-09-01 00:00:00', '2023-09-01 00:00:00'),
('E010', 'COURSE010', '2023-10-01', '2023-11-01', 'completed', '2023-10-01 00:00:00', '2023-10-01 00:00:00'),
('E011', 'COURSE011', '2023-11-01', '2023-12-01', 'ongoing', '2023-11-01 00:00:00', '2023-11-01 00:00:00'),
('E012', 'COURSE012', '2023-12-01', '2024-01-01', 'cancelled', '2023-12-01 00:00:00', '2023-12-01 00:00:00'),
('E013', 'COURSE013', '2024-01-01', '2024-02-01', 'completed', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
('E014', 'COURSE014', '2024-02-01', '2024-03-01', 'ongoing', '2024-02-01 00:00:00', '2024-02-01 00:00:00'),
('E015', 'COURSE015', '2024-03-01', '2024-04-01', 'cancelled', '2024-03-01 00:00:00', '2024-03-01 00:00:00'),
('E016', 'COURSE016', '2024-04-01', '2024-05-01', 'completed', '2024-04-01 00:00:00', '2024-04-01 00:00:00'),
('E017', 'COURSE017', '2024-05-01', '2024-06-01', 'ongoing', '2024-05-01 00:00:00', '2024-05-01 00:00:00'),
('E018', 'COURSE018', '2024-06-01', '2024-07-01', 'cancelled', '2024-06-01 00:00:00', '2024-06-01 00:00:00'),
('E019', 'COURSE019', '2024-07-01', '2024-08-01', 'completed', '2024-07-01 00:00:00', '2024-07-01 00:00:00'),
('E020', 'COURSE020', '2024-08-01', '2024-09-01', 'ongoing', '2024-08-01 00:00:00', '2024-08-01 00:00:00'),
('E021', 'COURSE021', '2024-09-01', '2024-10-01', 'cancelled', '2024-09-01 00:00:00', '2024-09-01 00:00:00'),
('E022', 'COURSE022', '2024-10-01', '2024-11-01', 'completed', '2024-10-01 00:00:00', '2024-10-01 00:00:00'),
('E023', 'COURSE023', '2024-11-01', '2024-12-01', 'ongoing', '2024-11-01 00:00:00', '2024-11-01 00:00:00'),
('E024', 'COURSE024', '2024-12-01', '2025-01-01', 'cancelled', '2024-12-01 00:00:00', '2024-12-01 00:00:00'),
('E025', 'COURSE025', '2025-01-01', '2025-02-01', 'completed', '2025-01-01 00:00:00', '2025-01-01 00:00:00');
/*!40000 ALTER TABLE `employee_training` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` varchar(10) NOT NULL,
  `category_code` varchar(10) DEFAULT NULL,
  `employee_details` json NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES 
('E001', 'CAT001', '{"first_name": "John", "last_name": "Doe"}', 'active'),
('E002', 'CAT002', '{"first_name": "Jane", "last_name": "Smith"}', 'active'),
('E003', 'CAT003', '{"first_name": "Jim", "last_name": "Beam"}', 'inactive'),
('E004', 'CAT004', '{"first_name": "Jack", "last_name": "Daniels"}', 'active'),
('E005', 'CAT005', '{"first_name": "Jill", "last_name": "Valentine"}', 'inactive'),
('E006', 'CAT001', '{"first_name": "Chris", "last_name": "Redfield"}', 'active'),
('E007', 'CAT002', '{"first_name": "Leon", "last_name": "Kennedy"}', 'inactive'),
('E008', 'CAT003', '{"first_name": "Claire", "last_name": "Redfield"}', 'active'),
('E009', 'CAT004', '{"first_name": "Ada", "last_name": "Wong"}', 'inactive'),
('E010', 'CAT005', '{"first_name": "Albert", "last_name": "Wesker"}', 'active'),
('E011', 'CAT001', '{"first_name": "Barry", "last_name": "Burton"}', 'inactive'),
('E012', 'CAT002', '{"first_name": "Rebecca", "last_name": "Chambers"}', 'active'),
('E013', 'CAT003', '{"first_name": "Carlos", "last_name": "Oliveira"}', 'inactive'),
('E014', 'CAT004', '{"first_name": "Hunk", "last_name": "Unknown"}', 'active'),
('E015', 'CAT005', '{"first_name": "Tyrant", "last_name": "T-103"}', 'inactive'),
('E016', 'CAT001', '{"first_name": "Nemesis", "last_name": "T-Type"}', 'active'),
('E017', 'CAT002', '{"first_name": "William", "last_name": "Birkin"}', 'inactive'),
('E018', 'CAT003', '{"first_name": "Sherry", "last_name": "Birkin"}', 'active'),
('E019', 'CAT004', '{"first_name": "Alexia", "last_name": "Ashford"}', 'inactive'),
('E020', 'CAT005', '{"first_name": "Alfred", "last_name": "Ashford"}', 'active'),
('E021', 'CAT001', '{"first_name": "Steve", "last_name": "Burnside"}', 'inactive'),
('E022', 'CAT002', '{"first_name": "Sheva", "last_name": "Alomar"}', 'active'),
('E023', 'CAT003', '{"first_name": "Piers", "last_name": "Nivans"}', 'inactive'),
('E024', 'CAT004', '{"first_name": "Helena", "last_name": "Harper"}', 'active'),
('E025', 'CAT005', '{"first_name": "Jake", "last_name": "Muller"}', 'inactive');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualifications`
--

DROP TABLE IF EXISTS `qualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualifications` (
  `qualification_id` varchar(10) NOT NULL,
  `qualification_details` json NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`qualification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualifications`
--

LOCK TABLES `qualifications` WRITE;
/*!40000 ALTER TABLE `qualifications` DISABLE KEYS */;
INSERT INTO `qualifications` VALUES 
('QUAL001', '{"name": "First Aid", "description": "Basic first aid training"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL002', '{"name": "Fire Safety", "description": "Fire safety and prevention"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL003', '{"name": "Conflict Resolution", "description": "Handling conflicts effectively"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL004', '{"name": "Security Management", "description": "Managing security operations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL005', '{"name": "Customer Service", "description": "Improving customer interactions"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL006', '{"name": "Leadership", "description": "Leadership skills for managers"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL007', '{"name": "Team Building", "description": "Building effective teams"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL008', '{"name": "Crisis Management", "description": "Handling crisis situations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL009', '{"name": "Negotiation", "description": "Effective negotiation techniques"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL010', '{"name": "Time Management", "description": "Managing time effectively"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL011', '{"name": "Project Management", "description": "Managing projects efficiently"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL012', '{"name": "Risk Assessment", "description": "Assessing risks in operations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL013', '{"name": "Communication Skills", "description": "Improving communication skills"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL014', '{"name": "Problem Solving", "description": "Solving problems effectively"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL015', '{"name": "Decision Making", "description": "Making informed decisions"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL016', '{"name": "Strategic Planning", "description": "Planning strategically"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL017', '{"name": "Budgeting", "description": "Managing budgets effectively"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL018', '{"name": "Data Analysis", "description": "Analyzing data for insights"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL019', '{"name": "Quality Control", "description": "Ensuring quality standards"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL020', '{"name": "Inventory Management", "description": "Managing inventory efficiently"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL021', '{"name": "Supply Chain Management", "description": "Managing supply chains"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL022', '{"name": "Logistics", "description": "Managing logistics operations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL023', '{"name": "Customer Relationship Management", "description": "Managing customer relationships"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL024', '{"name": "Sales Techniques", "description": "Effective sales techniques"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('QUAL025', '{"name": "Marketing Strategies", "description": "Developing marketing strategies"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00');
/*!40000 ALTER TABLE `qualifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_courses`
--

DROP TABLE IF EXISTS `training_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `training_courses` (
  `course_id` varchar(10) NOT NULL,
  `course_details` json NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_courses`
--

LOCK TABLES `training_courses` WRITE;
/*!40000 ALTER TABLE `training_courses` DISABLE KEYS */;
INSERT INTO `training_courses` VALUES 
('COURSE001', '{"title": "Basic Security", "description": "Introduction to security"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE002', '{"title": "Advanced Security", "description": "Advanced security techniques"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE003', '{"title": "Customer Service", "description": "Improving customer interactions"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE004', '{"title": "Leadership", "description": "Leadership skills for managers"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE005', '{"title": "Team Building", "description": "Building effective teams"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE006', '{"title": "Crisis Management", "description": "Handling crisis situations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE007', '{"title": "Negotiation", "description": "Effective negotiation techniques"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE008', '{"title": "Time Management", "description": "Managing time effectively"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE009', '{"title": "Project Management", "description": "Managing projects efficiently"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE010', '{"title": "Risk Assessment", "description": "Assessing risks in operations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE011', '{"title": "Communication Skills", "description": "Improving communication skills"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE012', '{"title": "Problem Solving", "description": "Solving problems effectively"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE013', '{"title": "Decision Making", "description": "Making informed decisions"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE014', '{"title": "Strategic Planning", "description": "Planning strategically"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE015', '{"title": "Budgeting", "description": "Managing budgets effectively"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE016', '{"title": "Data Analysis", "description": "Analyzing data for insights"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE017', '{"title": "Quality Control", "description": "Ensuring quality standards"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE018', '{"title": "Inventory Management", "description": "Managing inventory efficiently"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE019', '{"title": "Supply Chain Management", "description": "Managing supply chains"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE020', '{"title": "Logistics", "description": "Managing logistics operations"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE021', '{"title": "Customer Relationship Management", "description": "Managing customer relationships"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE022', '{"title": "Sales Techniques", "description": "Effective sales techniques"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE023', '{"title": "Marketing Strategies", "description": "Developing marketing strategies"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE024', '{"title": "Financial Management", "description": "Managing finances effectively"}', 'active', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
('COURSE025', '{"title": "Human Resources", "description": "Managing human resources"}', 'inactive', '2023-01-01 00:00:00', '2023-01-01 00:00:00');
/*!40000 ALTER TABLE `training_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','manager','user') DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES 
('d2e3ec3d-5df7-4535-ae21-cc96e52cda62', 'user1', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda63', 'user2', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda64', 'user3', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda65', 'user4', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda66', 'user5', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda67', 'user6', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda68', 'user7', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda69', 'user8', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda70', 'user9', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda71', 'user10', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda72', 'user11', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda73', 'user12', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda74', 'user13', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda75', 'user14', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda76', 'user15', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda77', 'user16', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda78', 'user17', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda79', 'user18', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda80', 'user19', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda81', 'user20', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda82', 'user21', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda83', 'user22', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda84', 'user23', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'manager', 'inactive'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda85', 'user24', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'admin', 'active'),
('d2e3ec3d-5df7-4535-ae21-cc96e52cda86', 'user25', 'scrypt:32768:8:1$BmQl8gjQrhhyFtlh$39e75ec6c64f64ce7f10b378ee245c170134207dcb673b15b98d00dc7f09e25ac9a30656b674b56baeae91ec7eeafa99d701a5cae50a962ec4a5514af3464245', 'user', 'inactive');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-15  0:54:36

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 24, 2025 at 08:23 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `services_particuliers`
--
CREATE DATABASE IF NOT EXISTS `services_particuliers` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `services_particuliers`;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id_categorie` int NOT NULL AUTO_INCREMENT,
  `nom_categorie` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id_categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id_categorie`, `nom_categorie`, `description`) VALUES
(1, 'Jardinage', 'Services de tonte de pelouse, entretien de jardin et taille de haies'),
(2, 'Informatique', 'Assistance pour installation de logiciels, dépannage PC et formation'),
(3, 'Ménage', 'Aide pour le nettoyage de maisons et appartements'),
(4, 'Cours particuliers', 'Aide aux devoirs et cours personnalisés à domicile'),
(5, 'Bricolage', 'Montage de meubles, réparations mineures et petits travaux'),
(6, 'Cuisine à domicile', 'Préparation de repas chez le client, chef à domicile'),
(7, 'Garde d\'animaux', 'Garde de chiens, promenades, nourrissage et soins'),
(8, 'Transport', 'Aide pour déménagement, livraison de petits colis et covoiturage'),
(9, 'Rickroll', 'Service pour rick-roller un ami.');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id_service` int NOT NULL AUTO_INCREMENT,
  `id_categorie` int NOT NULL,
  `titre` varchar(50) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `localisation` varchar(50) NOT NULL,
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  `actif` tinyint(1) DEFAULT '1',
  `cout` decimal(8,2) DEFAULT '0.00',
  `photo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_service`),
  KEY `id_categorie` (`id_categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id_service`, `id_categorie`, `titre`, `description`, `localisation`, `date_creation`, `actif`, `cout`, `photo`) VALUES
(1, 1, 'Tonte de pelouse', 'Je propose de tondre votre pelouse chaque semaine pour un jardin propre.', 'Québec', '2025-08-10 10:00:00', 1, 25.00, 'tonte.jpg'),
(2, 1, 'Entretien de haies', 'Taille professionnelle de haies pour un jardin impeccable.', 'Limoilou', '2025-08-15 09:30:00', 1, 40.00, 'haies.png'),
(3, 2, 'Réinstallation Windows', 'Réinstallation complète de Windows avec sauvegarde de vos données.', 'Sainte-Foy', '2025-08-20 14:00:00', 1, 80.00, 'windows.jpg'),
(4, 2, 'Montage PC', 'Montage complet de votre nouvel ordinateur et installation des pilotes.', 'Charlesbourg', '2025-08-22 16:45:00', 1, 100.00, NULL),
(5, 3, 'Ménage de printemps', 'Grand ménage complet de la maison, produits inclus.', 'Beauport', '2025-08-25 08:00:00', 1, 120.00, 'menage.jpg'),
(6, 4, 'Cours de mathématiques', 'Cours personnalisés de mathématiques pour secondaire et cégep.', 'Sillery', '2025-08-26 18:30:00', 1, 30.00, NULL),
(7, 4, 'Cours d’anglais', 'Aide en conversation et grammaire pour tous niveaux.', 'Québec', '2025-08-28 19:00:00', 1, 35.00, NULL),
(8, 5, 'Montage de meuble IKEA', 'Montage rapide et efficace de meubles IKEA.', 'Québec', '2025-08-29 15:00:00', 1, 50.00, 'ikea.jpg'),
(9, 6, 'Chef à domicile', 'Préparation de repas gastronomiques chez vous pour 2 à 6 personnes.', 'Sillery', '2025-09-01 20:00:00', NULL, 150.00, 'chef.jpg'),
(10, 7, 'Promenade de chien', 'Promenade quotidienne de votre chien, 30 minutes.', 'Limoilou', '2025-09-03 07:00:00', 1, 15.00, 'chien.jpg'),
(11, 8, 'Aide déménagement', 'Transport d’objets lourds avec camionnette, sur réservation.', 'Charlesbourg', '2025-09-05 09:00:00', 1, 200.00, 'camion.jpg'),
(20, 1, 'gfh', 'gfhfg', 'hgfh', '2025-09-16 12:39:04', 1, 888.00, NULL),
(21, 1, 'ffgf', 'ghgh', 'ghgh', '2025-09-16 13:02:52', 1, 55.00, 'rick.png'),
(22, 3, 'w', 'sssss', 'ss', '2025-09-17 19:44:21', 1, 0.00, 'rick.png'),
(23, 1, 'ffff', 'fftyyr', 'rrrrr', '2025-09-17 19:45:30', NULL, 0.00, 'rick.png'),
(27, 1, 'ghfghd', 'gfhgh', 'ghgfhd', '2025-09-18 11:58:43', 0, 0.00, ''),
(28, 9, 'Arrêtez Julien et ses rickroll', 'J\'ai besoin de quelqu\'un pour envoyer `` n rickroll séééé ``à``aàà``aà``aààAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'Québec', '2025-09-22 12:03:06', 1, 0.00, 'rick.png'),
(29, 7, 'fgdf', 'hghfggggggggggggggggggggggggg</pgggggggggggggggggggggggggggggggggggggggggggg', 'hghgfh', '2025-09-24 16:06:12', 1, 40.00, '');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`id_categorie`) REFERENCES `categories` (`id_categorie`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

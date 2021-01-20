-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 29, 2020 at 01:13 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `catalog`
--

-- --------------------------------------------------------

--
-- Table structure for table `deployedflow`
--

CREATE TABLE `deployedflow` (
  `flowId` int(11) NOT NULL,
  `outport` varchar(100) NOT NULL,
  `inport` varchar(100) NOT NULL,
  `nodename` varchar(100) NOT NULL,
  `intentid` int(11) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0,
  `rapiesponse` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Table structure for table `intent`
--

CREATE TABLE `intent` (
  `Intentid` int(11) NOT NULL,
  `servicename` varchar(100) NOT NULL,
  `QoSType` varchar(100) NOT NULL,
  `ClientNodeName` varchar(100) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Table structure for table `links`
--

CREATE TABLE `links` (
  `Linkid` int(11) NOT NULL,
  `outportFirstnode` varchar(100) NOT NULL,
  `inportSecondNode` varchar(100) NOT NULL,
  `FirstNodeName` varchar(100) NOT NULL,
  `SecondNodeName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `links`
--

INSERT INTO `links` (`Linkid`, `outportFirstnode`, `inportSecondNode`, `FirstNodeName`, `SecondNodeName`) VALUES
(1, '39', '39', 'P1-Seoul', 'P2-Daejeon'),
(2, '39', '39', 'P2-Daejeon', 'P1-Seoul'),
(3, '16', '18', 'P1-Seoul', 'P1-Chuncheon'),
(4, '18', '16', 'P1-Chuncheon', 'P1-Seoul'),
(5, '1', '1', 'P1-Seoul', 'P3-Suwon'),
(6, '1', '1', 'P3-Suwon', 'P1-Seoul'),
(7, '33', '33', 'P1-Seoul', 'P3-Pangyo'),
(8, '33', '33', 'P3-Pangyo', 'P1-Seoul'),
(9, '33', '39', 'P2-Daejeon', 'P3-Pangyo'),
(10, '39', '33', 'P3-Pangyo', 'P2-Daejeon'),
(11, '2', '2', 'P2-Daejeon', 'P3-Suwon'),
(12, '2', '2', 'P3-Suwon', 'P2-Daejeon'),
(13, '11', '1', 'P2-Daejeon', 'P4-Gwangju'),
(14, '1', '11', 'P4-Gwangju', 'P2-Daejeon'),
(15, '13', '1', 'P2-Daejeon', 'P5-Daegu'),
(16, '1', '13', 'P5-Daegu', 'P2-Daejeon'),
(17, '14', '1', 'P2-Daejeon', 'P5-Busan'),
(18, '1', '14', 'P5-Busan', 'P2-Daejeon'),
(19, '12', '17', 'P2-Daejeon', 'P2-Jeonju'),
(20, '17', '12', 'P2-Jeonju', 'P2-Daejeon'),
(21, '18', '18', 'P4-Gwangju', 'P4-Jeju'),
(22, '18', '18', 'P4-Jeju', 'P4-Gwangju');

-- --------------------------------------------------------

--
-- Table structure for table `nodes`
--

CREATE TABLE `nodes` (
  `NodeName` varchar(100) NOT NULL,
  `switchID` varchar(100) NOT NULL,
  `ControllerIP` varchar(100) NOT NULL,
  `ControllerName` varchar(100) NOT NULL,
  `HostPort` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `nodes`
--

INSERT INTO `nodes` (`NodeName`, `switchID`, `ControllerIP`, `ControllerName`, `HostPort`) VALUES
('P1-Chuncheon', '0xda7b', '203.255.250.11', 'Seoul-Chuncheon', '46'),
('P1-Seoul', '0xda7a', '203.255.250.11', 'Seoul-Chuncheon', '36'),
('P2-Daejeon', '0xda7a', '203.255.250.21', 'Daejeon-Jeonju', '16'),
('P2-Jeonju', '0xda7b', '203.255.250.21', 'Daejeon-Jeonju', '6'),
('P3-Pangyo', '0xda7d', '203.255.250.33', 'Pangyo-Suwon', '46'),
('P3-Suwon', '0xda7c', '203.255.250.33', 'Pangyo-Suwon', '46'),
('P4-Gwangju', '0xda7a', '203.255.250.41', 'Gwangju-Jeju', '6'),
('P4-Jeju', '0xda7b', '203.255.250.41', 'Gwangju-Jeju', '6'),
('P5-Busan', '0xda7b', '203.255.250.51', 'Daegu-Busan', '6'),
('P5-Daegu', '0xda7a', '203.255.250.51', 'Daegu-Busan', '6');

-- --------------------------------------------------------

--
-- Table structure for table `qos`
--

CREATE TABLE `qos` (
  `QoSType` varchar(100) NOT NULL,
  `priority` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `qos`
--

INSERT INTO `qos` (`QoSType`, `priority`) VALUES
('Bandwidth', 3);

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE `service` (
  `servicename` varchar(100) NOT NULL,
  `ProviderNodeName` varchar(100) NOT NULL,
  `vLANid` int(11) NOT NULL,
  `status` int(100) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`servicename`, `ProviderNodeName`, `vLANid`, `status`) VALUES
('1K Video Service-3', 'P3-Pangyo', 3, 0),
('4k Video Service-2', 'P3-Suwon', 2, 1),
('8k Video Service-1', 'P3-Pangyo', 1, 1),
('Low-Quality Video Service-5', 'P3-Pangyo', 5, 1),
('Medium-Quality Video Service-4', 'P3-Suwon', 4, 0);

-- --------------------------------------------------------

--
-- Table structure for table `vlans`
--

CREATE TABLE `vlans` (
  `vLANid` int(11) NOT NULL,
  `vLAN` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vlans`
--

INSERT INTO `vlans` (`vLANid`, `vLAN`) VALUES
(1, '1611'),
(2, '1612'),
(3, '1613'),
(4, '1614'),
(5, '1615');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `deployedflow`
--
ALTER TABLE `deployedflow`
  ADD PRIMARY KEY (`flowId`),
  ADD KEY `fk_nodename` (`nodename`),
  ADD KEY `fk_intentid` (`intentid`);

--
-- Indexes for table `intent`
--
ALTER TABLE `intent`
  ADD PRIMARY KEY (`Intentid`),
  ADD KEY `servicename` (`servicename`),
  ADD KEY `QoSType` (`QoSType`),
  ADD KEY `ClientNodeName` (`ClientNodeName`);

--
-- Indexes for table `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`Linkid`),
  ADD KEY `FirstNodeName` (`FirstNodeName`),
  ADD KEY `SecondNodeName` (`SecondNodeName`);

--
-- Indexes for table `nodes`
--
ALTER TABLE `nodes`
  ADD PRIMARY KEY (`NodeName`);

--
-- Indexes for table `qos`
--
ALTER TABLE `qos`
  ADD PRIMARY KEY (`QoSType`);

--
-- Indexes for table `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`servicename`),
  ADD KEY `ProviderNodeName` (`ProviderNodeName`),
  ADD KEY `vLANid` (`vLANid`);

--
-- Indexes for table `vlans`
--
ALTER TABLE `vlans`
  ADD PRIMARY KEY (`vLANid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `deployedflow`
--
ALTER TABLE `deployedflow`
  MODIFY `flowId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=733;

--
-- AUTO_INCREMENT for table `intent`
--
ALTER TABLE `intent`
  MODIFY `Intentid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT for table `links`
--
ALTER TABLE `links`
  MODIFY `Linkid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `deployedflow`
--
ALTER TABLE `deployedflow`
  ADD CONSTRAINT `fk_intentid` FOREIGN KEY (`intentid`) REFERENCES `intent` (`Intentid`),
  ADD CONSTRAINT `fk_nodename` FOREIGN KEY (`nodename`) REFERENCES `nodes` (`NodeName`);

--
-- Constraints for table `intent`
--
ALTER TABLE `intent`
  ADD CONSTRAINT `intent_ibfk_1` FOREIGN KEY (`servicename`) REFERENCES `service` (`servicename`),
  ADD CONSTRAINT `intent_ibfk_2` FOREIGN KEY (`QoSType`) REFERENCES `qos` (`QoSType`),
  ADD CONSTRAINT `intent_ibfk_3` FOREIGN KEY (`ClientNodeName`) REFERENCES `nodes` (`NodeName`);

--
-- Constraints for table `links`
--
ALTER TABLE `links`
  ADD CONSTRAINT `links_ibfk_1` FOREIGN KEY (`FirstNodeName`) REFERENCES `nodes` (`NodeName`),
  ADD CONSTRAINT `links_ibfk_2` FOREIGN KEY (`SecondNodeName`) REFERENCES `nodes` (`NodeName`);

--
-- Constraints for table `service`
--
ALTER TABLE `service`
  ADD CONSTRAINT `service_ibfk_1` FOREIGN KEY (`ProviderNodeName`) REFERENCES `nodes` (`NodeName`),
  ADD CONSTRAINT `service_ibfk_2` FOREIGN KEY (`vLANid`) REFERENCES `vlans` (`vLANid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;




CREATE TABLE `Server Nodes` (
  `id` int(11) NOT NULL,
  `ServerNodeName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `service`
--
CREATE TABLE `servicename`(
  `ServiceId` int(11) NOT NULL,
  `servicename` varchar(100) NOT NULL,

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `service` (
  `servicepk` int(11) NOT NULL,
  `ServiceId` int(11) NOT NULL,
  `ServerNodeID` int(11) NOT NULL,
  `vLANid` int(11) NOT NULL,
  `status` int(100) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vlans`
--

CREATE TABLE `vlans` (
  `vLANid` int(11) NOT NULL,
  `vLAN` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vlans`
--


CREATE DATABASE trab_final_sd

-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 22-Jun-2019 às 23:58
-- Versão do servidor: 10.3.16-MariaDB
-- versão do PHP: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `trab_final_sd`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `nodes`
--

CREATE TABLE `nodes` (
  `id` int(11) NOT NULL,
  `node_name` varchar(500) NOT NULL,
  `processing_time` int(11) NOT NULL,
  `pinged_back` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `nodes`
--

INSERT INTO `nodes` (`id`, `node_name`, `processing_time`, `pinged_back`) VALUES
(4, 'q1', 1, 1),
(5, 'q2', 1, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `node_connections`
--

CREATE TABLE `node_connections` (
  `node_id_1` int(11) NOT NULL,
  `node_id_2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `node_connections`
--

INSERT INTO `node_connections` (`node_id_1`, `node_id_2`) VALUES
(5, 4),
(4, 5);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `nodes`
--
ALTER TABLE `nodes`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `node_connections`
--
ALTER TABLE `node_connections`
  ADD KEY `fk_node_id_1` (`node_id_1`),
  ADD KEY `fk_node_id_2` (`node_id_2`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `nodes`
--
ALTER TABLE `nodes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `node_connections`
--
ALTER TABLE `node_connections`
  ADD CONSTRAINT `fk_node_id_1` FOREIGN KEY (`node_id_1`) REFERENCES `nodes` (`id`),
  ADD CONSTRAINT `fk_node_id_2` FOREIGN KEY (`node_id_2`) REFERENCES `nodes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

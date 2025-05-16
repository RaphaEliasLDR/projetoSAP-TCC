-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`cozinha`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`cozinha` (
  `id_cozinha` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_cozinha`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`gerente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`gerente` (
  `id_gerente` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_gerente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`garcom`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`garcom` (
  `id_garcom` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_garcom`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome completo` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(10) NOT NULL,
  `CPF` VARCHAR(12) NOT NULL,
  `cozinha_id_cozinha` INT NOT NULL,
  `gerente_id_gerente` INT NOT NULL,
  `garcom_id_garcom` INT NOT NULL,
  PRIMARY KEY (`id_usuario`, `cozinha_id_cozinha`, `gerente_id_gerente`, `garcom_id_garcom`),
  INDEX `fk_usuario_cozinha1_idx` (`cozinha_id_cozinha` ASC) VISIBLE,
  INDEX `fk_usuario_gerente1_idx` (`gerente_id_gerente` ASC) VISIBLE,
  INDEX `fk_usuario_garcom1_idx` (`garcom_id_garcom` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_cozinha1`
    FOREIGN KEY (`cozinha_id_cozinha`)
    REFERENCES `mydb`.`cozinha` (`id_cozinha`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_gerente1`
    FOREIGN KEY (`gerente_id_gerente`)
    REFERENCES `mydb`.`gerente` (`id_gerente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_garcom1`
    FOREIGN KEY (`garcom_id_garcom`)
    REFERENCES `mydb`.`garcom` (`id_garcom`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`mesa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`mesa` (
  `id_mesa` INT NOT NULL AUTO_INCREMENT,
  `numero_mesa` INT NOT NULL,
  PRIMARY KEY (`id_mesa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`status_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`status_pedido` (
  `id_status_pedido` INT NOT NULL AUTO_INCREMENT,
  `descricao` ENUM('pendente', 'em_preparo', 'pronto', 'cancelado') NOT NULL,
  PRIMARY KEY (`id_status_pedido`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`pedido` (
  `id_pedido` INT NOT NULL,
  `garcom_id_garcom` INT NOT NULL,
  `mesa_id_mesa` INT NOT NULL,
  `status_pedido_id_status_pedido` INT NOT NULL,
  PRIMARY KEY (`id_pedido`, `garcom_id_garcom`, `mesa_id_mesa`, `status_pedido_id_status_pedido`),
  INDEX `fk_pedido_garcom1_idx` (`garcom_id_garcom` ASC) VISIBLE,
  INDEX `fk_pedido_mesa1_idx` (`mesa_id_mesa` ASC) VISIBLE,
  INDEX `fk_pedido_status_pedido1_idx` (`status_pedido_id_status_pedido` ASC) VISIBLE,
  CONSTRAINT `fk_pedido_garcom1`
    FOREIGN KEY (`garcom_id_garcom`)
    REFERENCES `mydb`.`garcom` (`id_garcom`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_mesa1`
    FOREIGN KEY (`mesa_id_mesa`)
    REFERENCES `mydb`.`mesa` (`id_mesa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_status_pedido1`
    FOREIGN KEY (`status_pedido_id_status_pedido`)
    REFERENCES `mydb`.`status_pedido` (`id_status_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`item` (
  `id_item` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `imagem` VARCHAR(255) NOT NULL,
  `preco` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_item`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categoria` (
  `id_categoria` INT NOT NULL,
  `quantidade_item_vendido` INT NOT NULL,
  `total_arrecadado` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`item_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`item_pedido` (
  `categoria_id_categoria` INT NOT NULL,
  `item_id_item` INT NOT NULL,
  `preco_unitario` DECIMAL(10,2) NOT NULL,
  `quantidade` INT NOT NULL,
  `data_hora` DATETIME NOT NULL,
  `pedido_id_pedido` INT NOT NULL,
  `pedido_garcom_id_garcom` INT NOT NULL,
  `pedido_mesa_id_mesa` INT NOT NULL,
  `pedido_status_pedido_id_status_pedido` INT NOT NULL,
  PRIMARY KEY (`categoria_id_categoria`, `item_id_item`, `pedido_id_pedido`, `pedido_garcom_id_garcom`, `pedido_mesa_id_mesa`, `pedido_status_pedido_id_status_pedido`),
  INDEX `fk_item_pedido_categoria1_idx` (`categoria_id_categoria` ASC) VISIBLE,
  INDEX `fk_item_pedido_item1_idx` (`item_id_item` ASC) VISIBLE,
  INDEX `fk_item_pedido_pedido1_idx` (`pedido_id_pedido` ASC, `pedido_garcom_id_garcom` ASC, `pedido_mesa_id_mesa` ASC, `pedido_status_pedido_id_status_pedido` ASC) VISIBLE,
  CONSTRAINT `fk_item_pedido_categoria1`
    FOREIGN KEY (`categoria_id_categoria`)
    REFERENCES `mydb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_item_pedido_item1`
    FOREIGN KEY (`item_id_item`)
    REFERENCES `mydb`.`item` (`id_item`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_item_pedido_pedido1`
    FOREIGN KEY (`pedido_id_pedido` , `pedido_garcom_id_garcom` , `pedido_mesa_id_mesa` , `pedido_status_pedido_id_status_pedido`)
    REFERENCES `mydb`.`pedido` (`id_pedido` , `garcom_id_garcom` , `mesa_id_mesa` , `status_pedido_id_status_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`prato_princiapal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`prato_princiapal` (
  `categoria_id_categoria` INT NOT NULL,
  PRIMARY KEY (`categoria_id_categoria`),
  CONSTRAINT `fk_prato_princiapal_categoria1`
    FOREIGN KEY (`categoria_id_categoria`)
    REFERENCES `mydb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sobremesas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`sobremesas` (
  `categoria_id_categoria` INT NOT NULL,
  PRIMARY KEY (`categoria_id_categoria`),
  CONSTRAINT `fk_table2_categoria1`
    FOREIGN KEY (`categoria_id_categoria`)
    REFERENCES `mydb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`lanches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`lanches` (
  `categoria_id_categoria` INT NOT NULL,
  PRIMARY KEY (`categoria_id_categoria`),
  CONSTRAINT `fk_lanches_categoria1`
    FOREIGN KEY (`categoria_id_categoria`)
    REFERENCES `mydb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bebidas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`bebidas` (
  `categoria_id_categoria` INT NOT NULL,
  `alcoolicas` VARCHAR(50) NOT NULL,
  `nao_alcoolicas` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`categoria_id_categoria`),
  CONSTRAINT `fk_bebidas_categoria1`
    FOREIGN KEY (`categoria_id_categoria`)
    REFERENCES `mydb`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`avaliacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`avaliacao` (
  `id_avaliacao` INT NOT NULL AUTO_INCREMENT,
  `nota_comida` TINYINT NULL,
  `nota_atendimento` TINYINT NULL,
  `comentario` VARCHAR(200) NULL,
  `garcom_id_garcom` INT NOT NULL,
  PRIMARY KEY (`id_avaliacao`, `garcom_id_garcom`),
  INDEX `fk_avaliacao_garcom1_idx` (`garcom_id_garcom` ASC) VISIBLE,
  CONSTRAINT `fk_avaliacao_garcom1`
    FOREIGN KEY (`garcom_id_garcom`)
    REFERENCES `mydb`.`garcom` (`id_garcom`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

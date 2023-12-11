-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema etl_dataset
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema etl_dataset
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `etl_dataset` DEFAULT CHARACTER SET utf8 ;
USE `etl_dataset` ;

-- -----------------------------------------------------
-- Table `etl_dataset`.`Country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`Country` (
  `country_code` INT NOT NULL,
  `country` VARCHAR(125) NOT NULL,
  `who_region` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`country_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`Departament`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`Departament` (
  `code_departament` INT NOT NULL,
  `departament` VARCHAR(75) NOT NULL,
  `country_code` INT NOT NULL,
  PRIMARY KEY (`code_departament`),
  INDEX `fx_Departament_Country_country_code_idx` (`country_code` ASC) VISIBLE,
  CONSTRAINT `fx_Departament_Country_country_code`
    FOREIGN KEY (`country_code`)
    REFERENCES `etl_dataset`.`Country` (`country_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`Town`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`Town` (
  `code_town` INT NOT NULL,
  `code_departament` INT NOT NULL,
  `town` VARCHAR(100) NOT NULL,
  `population` INT NOT NULL,
  PRIMARY KEY (`code_town`),
  INDEX `fx_Town_Departament_code_departament_idx` (`code_departament` ASC) VISIBLE,
  CONSTRAINT `fx_Town_Departament_code_departament`
    FOREIGN KEY (`code_departament`)
    REFERENCES `etl_dataset`.`Departament` (`code_departament`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`TownDemises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`TownDemises` (
  `idCase` INT NOT NULL AUTO_INCREMENT,
  `code_town` INT NOT NULL,
  `date` DATE NOT NULL,
  `deceases` INT NOT NULL,
  PRIMARY KEY (`idCase`),
  INDEX `fx_TownDemises_Town_code_town_idx` (`code_town` ASC) VISIBLE,
  CONSTRAINT `fx_TownDemises_Town_code_town`
    FOREIGN KEY (`code_town`)
    REFERENCES `etl_dataset`.`Town` (`code_town`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`CovidCases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`CovidCases` (
  `idCovidCase` INT NOT NULL AUTO_INCREMENT,
  `country_code` INT NOT NULL,
  `date_reported` DATE NOT NULL,
  PRIMARY KEY (`idCovidCase`, `country_code`),
  INDEX `fx_CovidCases_Country_country_code_idx` (`country_code` ASC) VISIBLE,
  CONSTRAINT `fx_CovidCases_Country_country_code`
    FOREIGN KEY (`country_code`)
    REFERENCES `etl_dataset`.`Country` (`country_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`SickCases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`SickCases` (
  `idCovidCase` INT NOT NULL,
  `new_cases` INT NOT NULL,
  `cumulative_cases` INT NOT NULL,
  PRIMARY KEY (`idCovidCase`),
  CONSTRAINT `fx_SickCases_CovidCases_idCovidCase`
    FOREIGN KEY (`idCovidCase`)
    REFERENCES `etl_dataset`.`CovidCases` (`idCovidCase`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `etl_dataset`.`DeceaseCases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `etl_dataset`.`DeceaseCases` (
  `idCovidCase` INT NOT NULL,
  `new_deaths` INT NOT NULL,
  `cumulative_deaths` INT NOT NULL,
  PRIMARY KEY (`idCovidCase`),
  CONSTRAINT `fx_DeceaseCases_CovidCases_idCovidCase`
    FOREIGN KEY (`idCovidCase`)
    REFERENCES `etl_dataset`.`CovidCases` (`idCovidCase`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

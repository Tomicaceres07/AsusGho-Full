DROP DATABASE IF EXISTS api_base;
CREATE DATABASE api_base;

USE api_base;

CREATE TABLE PERSON (
	ID_P int not null auto_increment,
	NAME varchar(30)NOT NULL,
	MAIL varchar(100) NOT NULL UNIQUE,
	TYPE BOOLEAN NOT NULL,
	C_ABSCENCE float not null,
	primary key (ID_P));

CREATE TABLE STUDENT(
	ID_ST int not null auto_increment,
	NAME varchar(30)NOT NULL,
	MAIL varchar(100) NOT NULL UNIQUE,
    C_ABSCENCE float not null,
	`YEAR` varchar(30) not null,
    primary key (ID_ST));

CREATE TABLE STORAGE (
	ID_ST int not null auto_increment,
    DATE_ST varchar(10) NOT NULL, 
	TEXT_ST varchar(400),
	TYPE_ST BOOLEAN NOT NULL,
    primary key (ID_ST));

CREATE TABLE PDF_STORAGE(
	ID_PDF_ST int NOT NULL auto_increment,
	NAME_PDF varchar(100) NOT NULL,
	TYPE_PDF_ST BOOLEAN NOT NULL,
	primary key (ID_PDF_ST));

CREATE TABLE MENU_STORAGE(
	ID_MENU_ST int NOT NULL auto_increment,
	primary key (ID_MENU_ST));

CREATE TABLE abs_detail(
	id int(10)NOT NULL auto_increment,
	mail varchar(100)NOT NULL,
	abs float,
	justified boolean,
	date varchar(10),
	primary key(id));

CREATE TABLE COURSES(
	ID int(10)NOT NULL auto_increment,
	NAME varchar(30)NOT NULL,
	GRADE int(5)NOT NULL,
	DIVISION varchar(5)NOT NULL,
	primary key (ID));

CREATE TABLE ACTIVITIES(
	ID int(10)NOT NULL auto_increment,
	ID_COURSES int(10)NOT NULL,
	TITLE varchar(30)NOT NULL,
	primary key (ID));

CREATE TABLE ROLL(
	ID int(10)NOT NULL auto_increment,
	ID_COURSES int(10)NOT NULL,
	ID_PERSON int(10),
	ID_STUDENT int(10),
	primary key (ID));
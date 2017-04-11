CREATE DATABASE `quant` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'quant'@'%' IDENTIFIED BY 'quant';
CREATE USER 'quant'@'localhost' IDENTIFIED BY 'quant';
GRANT ALL PRIVILEGES ON quant.* TO 'quant'@'%'  IDENTIFIED BY 'quant';
GRANT ALL PRIVILEGES ON quant.* TO 'quant'@'localhost'  IDENTIFIED BY 'quant';

use quant;
set names utf8;
CREATE TABLE `exchange` (
  `pkid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `abbrev` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) NULL,
  `country` varchar(255) NULL,
  `currency` varchar(255) NULL,
  `timezone_offset` time NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pkid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_vendor` (
  `pkid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `website_url` varchar(255) NULL,
  `support_email` varchar(255) NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pkid`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `symbol` (
  `pkid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `exchange_pkid` int NULL,
  `ticker` varchar(32) NOT NULL,
  `instrument` varchar(64) NOT NULL,
  `name` varchar(255) NULL,
  `sector` varchar(255) NULL,
  `currency` varchar(32) NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pkid`),
  KEY `index_exchange_pkid` (`exchange_pkid`),
  UNIQUE KEY `unique_index_ticker` (`ticker`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `daily_price` (
  `pkid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data_vendor_pkid` int NOT NULL,
  `ticker` varchar(10) NOT NULL,
  `price_date` datetime NOT NULL,
  `open_price` decimal(19,4) NULL,
  `high_price` decimal(19,4) NULL,
  `low_price` decimal(19,4) NULL,
  `close_price` decimal(19,4) NULL,
  `adj_close_price` decimal(19,4) NULL,
  `volume` bigint NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pkid`),
  KEY `index_data_vendor_pkid` (`data_vendor_pkid`),
  KEY `index_ticker` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE download_daily_price_process (
	`pkid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`ticker` varchar(100) NULL,
	`st` varchar(100) NULL,
	`et` varchar(100) NULL,
	`result` int(2) NULL,
	`fail_reason` text NULL,
	`created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (pkid)
)

INSERT INTO data_vendor
(pkid, name, website_url, support_email, created_at, updated_at)
VALUES(NULL, 'tushare', 'http://tushare.org', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO exchange
(pkid, abbrev, name, city, country, currency, timezone_offset, created_at, updated_at)
VALUES
(NULL, 'SH-A', '沪市A股', '上海', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(NULL, 'SH-B', '沪市B股', '上海', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(NULL, 'SZ-A', '深市A股', '深圳', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(NULL, 'SZ-B', '深市B股', '深圳', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(NULL, 'SME', '中小板', '深圳', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(NULL, 'GME', '中小板', '深圳', '中国', 'RMB', '8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
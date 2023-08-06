# Python Rent Properties Scraper in CABA

This script scrapes different pages and APIs to get information about rent properties in CABA. It run its in a schedule that works everyday

## .env

Complete the .env file with the following variables

```bash
HOST=${DB_HOST}
USERNAME_DB=${DB_USER}
PASSWORD_DB=${DB_PASSWORD}
DATABASE=${DB_NAME}
```

## In the database

Create a table with the following structure

```sql
CREATE TABLE `active_properties` (
    `property_id` bigint NOT NULL AUTO_INCREMENT,
    `url` varchar(500) NOT NULL,
    `prop_type` varchar(255) NOT NULL,
    `price` bigint NOT NULL,
    `currency` varchar(255) NOT NULL,
    `expenses` bigint NOT NULL,
    `total_area` bigint NOT NULL,
    `covered_area` bigint NOT NULL,
    `rooms` int NOT NULL,
    `bedrooms` int NOT NULL,
    `bathrooms` int NOT NULL,
    `address` varchar(255) NOT NULL,
    `neighborhood` varchar(255) NOT NULL,
    `garage` int NOT NULL,
    `page` varchar(255) NOT NULL,
    `pics_urls` text,
    `last_read_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    `click_count` int DEFAULT '0',
    `first_read_date` timestamp NULL DEFAULT current_timestamp(),
    PRIMARY KEY (`property_id`),
    UNIQUE KEY `url` (`url`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;
```

## Run with Docker using Makefile

```bash
make
```

To stop it

```bash
make stop
```

TO deleted and stop it

```bash
make clean
```


## Run in console

install requirements.txt

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

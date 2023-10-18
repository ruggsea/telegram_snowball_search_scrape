# Telegram Message Search App

## Overview

The Telegram Message Search App is a Python-based tool that enables users to crawl Telegram channels, store messages, and perform both normal and vector-based searches on the stored data. This README provides a comprehensive overview of the application's structure and usage.

## Features

- **Crawling**: The application allows you to specify a set of Telegram channels and a keyword for crawling. It fetches messages matching the keyword, saves the channels, and stores messages in an SQLite database.

- **Database Storage**: Crawled data, including channels and messages, is ingested into an SQLite database for easy retrieval and search.

- **Search Engine**: The application supports two types of searches:
  - **Normal Search**: A basic text search for finding messages relevant to a query.
  - **Vector Search**: Utilizes vector embeddings to find semantically similar messages to a given query.

## Structure

The application is organized into several key components:

- **Crawler**:
  - `telegram_crawler.py`: This script is responsible for fetching messages and channels based on a keyword search and ingesting the data into the SQLite database.
  - Define your channels, keyword, and database path within this script.

- **Search Engine**:
  - `search_engine.py`: This script contains functions for performing both normal and vector-based searches on the SQLite database.
  - Users can initiate searches and retrieve the most relevant messages using this component.

- **Database**:
  - The SQLite database file is stored in the `data/` directory (e.g., `data/telegram_channels.db`).

- **Main Program** (In the root folder, `main.py`):
  - `main.py` serves as the entry point and orchestrates the application's functionalities.
  - Users can choose between crawling and searching, and input relevant data.

- **Configuration** (In the `config/` folder):
  - `database_config.py`: Database connection details, including the database file path, should be stored in this file. This file is added to the \.gitignore because sqlite databases are not supposed to be committed.

## Getting Started

1. Clone the repository to your local machine:
  
  ```bash 
  git clone https://github.com/your-username/telegram_snowball_search_scrape.git
  ```

2. Cd into it and install the required dependencies using the `requirements.txt` file:

  ```bash
  cd telegram_snowball_search_scrape
  pip install -r requirements.txt
  ```

3. **Configuration**:
- Ensure that you have your Telegram API credentials (API ID and API hash, to get them see [here](https://core.telegram.org/api/obtaining_api_id)) and add them to your PATH. 
- The same applies to your Google Cloud credentials (see [here](https://cloud.google.com/docs/authentication/getting-started) and [here] (https://developers.perspectiveapi.com/)) if you want to use the Perspective API to add toxicity score to the messages.
- You can change the database file path in `config/database_config.py`.


4. **Crawling**:

5. **Enriching the database**:
- Run `python fill_in_db.py` and choose 




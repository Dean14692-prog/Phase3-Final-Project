# Phase3-Final-Project

This is a command-line interface (CLI) project for managing a simple database of users, notes, tags, and complaints. It allows you to initialize the database, seed it with sample data, and perform CRUD (Create, Read, Update, Delete) operations on the tables.

---

## Features

- Initialize the database schema
- Seed the database with sample data
- List data from any of the tables: users, notes, tags, complaints
- Add new entries to any table
- Delete entries by ID
- Update existing records

---

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:Dean14692-prog/Phase3-Final-Project.git
   cd <your folder that you have cloned the project>
   ```

2. Install dependencies

   ```bash
   pip install sqlalchemy

   ```
3. Ensure your database setup is correctly configured in `database.py` and models are defined in `models.py`.

## Usage
- Run the CLI tool by executing:
```bash
python cli.py [COMMAND]
```
- Replace [COMMAND] with the command name in the cli script file.

## Commands
1. initialize
- Drops all existing tables and recreates them, effectively resetting the database.

``` bash
python cli.py initialize
```
2. seed-db
- Populates the database with initial sample data including users, notes, tags, note-tag associations, and complaints.
``` bash
python cli.py seed-db
```
3. list-data
- Displays all records from a selected table.
``` bash
python cli.py list-data
```
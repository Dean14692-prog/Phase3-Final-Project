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
-You will be prompted to choose one of the following tables: users, notes, tags, complaints.

4. add-to-db
- Interactively add a new record to any table.
``` bash
python cli.py add-to-db
```
- You will be prompted to specify the table and enter the necessary fields.

5. delete-from-db
- Interactively delete a record by specifying the table and record ID.
``` bash
python cli.py delete-from-db
```
6. update-record
- Interactively update a specific field of a record by providing table name, record ID, field name, and new value.
``` bash
python cli.py update-record
```
## Models Overview

- **User**: Stores user information (username, email, password, creation timestamp)
- **Note**: Stores notes related to users (title, content, user_id, creation timestamp)
- **Tag**: Stores tags that can be associated with notes
- **NoteTag**: Many-to-many relationship table connecting notes and tags
- **Complaint**: Stores complaints made by users

## Dependencies

- [Click](https://palletsprojects.com/p/click/) — for building the CLI interface
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for database operations

# Hostel Management System

A desktop-based Hostel Management System (HMS) developed in Python for managing hostel rooms, residents, room types, floor allocations, reports, and database settings through a modern graphical user interface.

## Features

* Resident registration and management
* Room allocation and occupancy tracking
* Room type management
* Floor management engine
* Dashboard with hostel statistics
* Reports generation
* Database configuration and connection settings
* Support for both SQLite and MySQL databases
* Modern GUI built with CustomTkinter

## Technologies Used

* Python 3
* CustomTkinter
* SQLite
* MySQL (PyMySQL)
* SQL

## Project Structure

```text
hostel-management-system/
│
├── main.py
├── database.py
├── schema.sql
├── config.json
├── hostel_sandbox.db
│
├── gui/
│   ├── main_window.py
│   ├── theme.py
│   │
│   └── views/
│       ├── dashboard.py
│       ├── residents.py
│       ├── rooms.py
│       ├── room_types.py
│       ├── floor_engine.py
│       ├── reports.py
│       ├── settings.py
│       └── er_schema.py
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hostel-management-system
```

### 2. Install Dependencies

```bash
pip install customtkinter pymysql
```

### 3. Run the Application

```bash
python main.py
```

The application will automatically check for required dependencies and attempt to install missing packages.

## Database Configuration

The system supports two database options:

### SQLite (Default)

No additional setup is required. The application uses:

```text
hostel_sandbox.db
```

### MySQL

Update the `config.json` file:

```json
{
    "db_type": "mysql",
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "hostel_management"
}
```

Run the SQL schema located in:

```text
schema.sql
```

or allow the application to create the database automatically during connection.

## Main Modules

### Dashboard

Provides an overview of hostel statistics and occupancy information.

### Residents Management

Allows administrators to:

* Add residents
* Edit resident information
* Track check-in and check-out dates
* Monitor tuition and deposit information

### Rooms Management

Allows:

* Room creation and editing
* Occupancy tracking
* Room status management

### Room Types

Stores room categories, pricing, and inventory assets.

### Reports

Generates operational and management reports.

### Settings

Manages database connection settings and application configuration.

## Database Schema

The system consists of three primary entities:

* Room_Types
* Rooms
* Residents

Relationships:

```text
Room_Types (1) ──── (Many) Rooms
Rooms (1) ──── (Many) Residents
```

## Developers

### Front-End & Database Developer

**Aminov Shaxboz**
GitHub: https://github.com/aminv-kod

Responsibilities:

* User interface development
* GUI integration
* Database design and implementation
* System testing and optimization

### Back-End & Database Developer

**Orzuyev Shoxruxjon**
GitHub: https://github.com/wenzo-siut

Responsibilities:

* Application logic development
* Database architecture
* Data processing and management
* Backend integration

## License

This project was developed for educational and academic purposes.

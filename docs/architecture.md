# Architecture Overview

This document describes the internal structure, data flow, and design decisions of the Console Movie Search Application.
The application combines a relational database (`MySQL`) for primary film data with a document-oriented database (`MongoDB`) used for logging and analytics.
This hybrid approach separates transactional data from analytical workloads.

---

## 1) Core Components

### MySQL Access Layer
Responsible for querying the Sakila database and retrieving film-related data.

### MongoDB Logging Layer
Stores user search queries as structured documents and supports statistical analysis.

### Console Interface Layer
Handles user input, validation, and formatted output in the terminal.

---

## 2) Data Flow Overview

### 2.1 Movie Search Flow (MySQL)

1. User selects a search option in the console
2. UI module collects input parameters
3. Search query is executed against a **SQL view**
4. Results are returned as structured data
5. Data is formatted and displayed in a table
6. Search parameters are logged to MongoDB for analytics purposes

```
User Input
   ↓
UI (ui.py)
   ↓
MySQL Query (mysql_connector.py)
   ↓
SQL View: film_extended_view
   ↓
Formatted Output (display_utils.py)
   ↓
Query Log (MongoDB)
```

---

### 2.2 Statistics Flow (MongoDB)

1. User selects a statistics option
2. Application queries MongoDB
3. Aggregation or filtering is applied
4. Results are formatted and displayed

```
User Input
   ↓
UI (ui.py)
   ↓
MongoDB Aggregation (log_stats.py)
   ↓
Formatted Output (display_utils.py)
```

---

## 3) Database Design

### 3.1 MySQL — Relational Data

The application uses the **Sakila database** as the source of movie data.

To simplify querying, a custom SQL view named
**`film_extended_view`** is created.

This view aggregates data from:
* `film`
* `actor`
* `film_actor`
* `category`
* `film_category`

The view provides:
* film metadata
* actor list per film
* genre information

This approach:
* reduces query complexity in Python
* improves readability and maintainability
* centralizes relational logic in SQL

---

### 3.2 MongoDB — Query Logging

MongoDB is used to store **user search logs**.
All search queries are stored as documents with a fixed schema.
Each document contains all supported search parameters.
Parameters not used in a specific query are explicitly stored as `null`.

This design simplifies aggregation queries and ensures consistent analytics.

Each search is stored as a document with:
* `query_type`
* `params`
* `timestamp`

#### Fixed Schema Strategy

All documents share the same structure:
* all possible parameters are present
* unused parameters are set to `null`

Example benefits:
* simpler aggregation
* consistent analytics
* predictable document structure

---

## 4) Module Responsibilities

### 4.1 `main.py`

* Application entry point
* Initializes the main program loop
* Delegates control to the UI module

---

### 4.2 `ui.py`

* Implements all console menus
* Handles user input validation
* Controls navigation between menus
* Calls search and statistics functions
* Displays user-facing messages and delegates error handling to shared utilities.

This module contains **no database logic**.

---

### 4.3 `mysql_connector.py`

* Executes MySQL queries
* Connects to the `film_extended_view`
* Returns search results as Python dictionaries

Responsibilities:

* SQL execution
* Connection handling
* Query parameter binding

---

### 4.4 `settings.py`

* Loads environment variables
* Manages MySQL and MongoDB connections
* Provides shared access to database resources

This module centralizes configuration and credentials.

---

### 4.5 `log_writer.py`

* Writes search queries to MongoDB
* Enforces a fixed parameter schema
* Stores timestamps in UTC

Key responsibility:

* **logging only**, no analytics

---

### 4.6 `log_stats.py`

* Reads logs from MongoDB
* Performs aggregations and statistics
* Implements logic for:

  * top parameters
  * last queries
  * filtering by query type
  * frequency analysis

This module contains **business logic**, not UI formatting.

---

### 4.7 `display_utils.py`

* Formats data into tables
* Uses `tabulate` for structured output
* Applies ANSI colors for console readability

This module:

* receives already-prepared data
* does **not** perform calculations

---

### 4.8 `errors.py`

* Provides decorators for error handling
* Logs errors to a file
* Displays user-friendly error messages in the console
* Errors are logged independently from user query logs.

This keeps error handling consistent across modules.

---

## 5) Design Decisions

### 5.1 SQL View Instead of Raw Queries

* Simplifies Python code
* Moves complex joins into the database layer
* Improves maintainability

---

### 5.2 MongoDB for Analytics

* Document-oriented structure fits query logs
* Flexible aggregation capabilities
* Separation of transactional data and analytics

---

### 5.3 Separation of Concerns

* UI does not access databases directly
* Statistics logic is independent of presentation
* Utilities are reusable and isolated

---

## 6) Scalability Considerations

The current architecture allows:

* adding new search types
* extending analytics
* replacing the console UI with a web interface
* adding caching or export features

---

## 7) Summary

The application architecture demonstrates:

* clean modular design
* effective use of relational and non-relational databases
* clear data flow
* maintainable and extensible structure

This project serves as a solid foundation for more advanced data-driven applications.

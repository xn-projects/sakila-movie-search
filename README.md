# Console Movie Search Application (Sakila)

## 1. Project Overview

This educational project is a **console-based application** that allows users to search for films
stored in a **MySQL (Sakila) database** using **Python**.

A key feature of the application is its integration with **MongoDB**, which is used to log user search
queries for further analysis. Each search stores information about the search parameters and execution time.

The project demonstrates the combined use of **relational and non-relational databases**
within a single Python application.

---

## 2. Key Features

- Film search by:
  - keyword
  - genre and year range
  - actor name
  - film length range
- Paginated result display (10 films per page)
- Console-based user interface with input validation
- Query logging in MongoDB
- Statistical analysis of user search behavior
- Clean modular architecture

---

## 3. Technologies Used

- **Python**
- **MySQL** (Sakila database)
- **MongoDB**
- `pymysql`
- `pymongo`
- `python-dotenv`
- `tabulate`

---

## 4. Database Design Overview

### MySQL

The application uses the **Sakila database** as the primary data source.  
To simplify querying and reduce complexity in Python, a SQL view named  
**`film_extended_view`** is used.

The view aggregates data from multiple related tables and provides:
- film metadata
- actor lists
- genre information

The structure of the underlying database and the relationships used to build
the view are illustrated below:

![MySQL View Schema](docs/film_extended_view_schema.png)

### MongoDB

MongoDB is used exclusively for **logging user search queries** and performing analytics.
This separation allows transactional and analytical workloads to remain independent.

---

## 5. MongoDB Logging Example

Each user search is stored as a document with a fixed schema.
The JSON below represents the logical structure of a query log document as written by the application:

```json
{
  "query_type": "length_range",
  "params": {
    "keyword": null,
    "genre": null,
    "year_from": null,
    "year_to": null,
    "first_name": null,
    "last_name": null,
    "min_length": 120,
    "max_length": 120
  },
  "timestamp": "2025-06-30T17:07:12Z"
}
```

The screenshot below shows the same document as it appears in MongoDB, including the automatically generated `_id` field:

![MongoDB Query Log Example](docs/mongodb_query_log_example.png)

Unused parameters are explicitly stored as `null`, which simplifies aggregation and statistical analysis.

---

## 6. Project Structure

```
sakila-movie-search/
├── src/
│   ├── __init__.py
│   ├── display_utils.py
│   ├── errors.py
│   ├── log_stats.py
│   ├── log_writer.py
│   ├── main.py
│   ├── mysql_connector.py
│   ├── settings.py
│   └── ui.py
│   
├── sql/
│   └── film_extended_view.sql
│   
├── docs/
│   ├── architecture.md
│   ├── usage.md
│   ├── film_extended_view_schema.png
│   ├── main_menu.png
│   ├── keyword_search_example.png
│   ├── genre_year_search_example.png
│   ├── actor_search_results.png
│   ├── length_range_search_results.png
│   ├── frequency_by_query_type.png
│   ├── last_5_search_queries.png
│   ├── queries_by_type_length_range.png
│   ├── top_5_most_used_search_parameters.png
│   └── mongodb_query_log_example.png
│   
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 7. How to Run

1. Clone the repository.

2. Create and configure a `.env` file with the required database credentials.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:
```bash
python -m src.main
```

---

## 8. Documentation

- **User Guide:** [`docs/usage.md`](docs/usage.md)
- **Architecture Overview:** [`docs/architecture.md`](docs/architecture.md)

---

## 9. Summary

This project demonstrates a clean and modular approach to building
a data-driven console application using Python.

It highlights:

- effective separation of concerns
- integration of relational and document-oriented databases
- practical logging and analytics
- maintainable and extensible design

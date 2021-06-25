# fender-exercise

This project demonstrates ETL in Python, using the [Open Library API](https://openlibrary.org/developers/api). 
The idea is to create reusable, scalable objects to serivce our data needs. The code found with the ETL directory
contains an extractor, transformer and loader module. This project uses a local sqllite3 database as its target 
but could easily be modified to load another, remote target.

Data Model:
The model consists of books, a dimension containing denormalized books from the catalog, authors, a denormalized
dimension with details about all the authors for all books in Books, and books_and_authors, that links the two
tables together.

Setup:  
`make install`
  
Running:
`python ddl/src/setup_db.py`
`python etl/extract/src/extract.py`
`python etl/transform/src/transform.py`
`python etl/load/src/load.py`

Tests:  
`make coverage`

Potential enhancements:
- Parallelism through multithreading or multiprocessing would make extract step faster
- Dynamically provide file or directory names as inputs to each module, through some sort of orchestrator.

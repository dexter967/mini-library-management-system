# Mini Library Management System 📚

A lightweight, zero-dependency command-line interface (CLI) Library Management System built in Python. Designed using pure standard Python data structures (`dict`, `list`), string formatting, standard I/O, and `datetime` arithmetic.

---

## 🚀 Features

- **Inventory Management**: Add new books, search by Title, Author, or ID.
- **Lending Control**: Check out and return books with automated availability validation.
- **Overdue Tracking**: Calculates due dates (14-day standard window) and flags overdue books dynamically.
- **Library Analytics**: Displays executive summaries of total inventory, checked-out items, and available stock.
- **Data Persistence**: Loads initial datasets from JSON and exports active borrowing logs to a formatted `.txt` report.

---

## 🛠️ Repository Structure

```text
├── library.py             # Main application CLI script
├── sample_books.json      # Initial seed inventory dataset
├── borrowing_records.txt  # Generated export file log of active loans
├── obstacle_log.md        # Log of development challenges & fixes
└── README.md              # Project documentation

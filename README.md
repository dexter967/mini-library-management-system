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


Notes on the design
Overdue window: a book is overdue if it's still checked out more than LOAN_PERIOD_DAYS (14, set at the top of library.py) days after the borrow date. Change that constant to adjust the loan period.
Book IDs auto-increment based on the highest existing ID, so adding books mid-session won't collide with the sample data.
See obstacle_log.md for the reasoning behind these choices and a few bugs that came up along the way.
Push to GitHub
git init
git add .
git commit -m "Mini library management system"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main

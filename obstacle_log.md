# Obstacle Log: Mini Library Management System

This document outlines the technical challenges, edge cases, and architectural choices made during the development of the Mini Library Management System.

---

### Obstacle 1: Datetime Comparison Errors
* **Issue:** Initial attempts to compare `datetime.now()` directly against string values stored in `due_date` raised `TypeError: unorderable types`.
* **Resolution:** Standardized all stored dates in the dataset using ISO string format (`YYYY-MM-DD`). Converted date strings back into `datetime.date` objects using `datetime.strptime()` before performing comparison logic for overdue checks.

---

### Obstacle 2: Preventing Invalid State Overwrites
* **Issue:** When returning a book, leaving old metadata (such as `borrower` or `due_date`) inside the book dictionary led to misleading reports during subsequent checkouts.
* **Resolution:** Explicitly reset `borrower`, `borrow_date`, and `due_date` back to `None` upon successful invocation of `return_book()`.

---

### Obstacle 3: Formatting Fixed-Width Output in Text File Log
* **Issue:** Varying title lengths and borrower names skewed column alignments in the exported `.txt` log file.
* **Resolution:** Implemented Python string formatting width specifiers (e.g., `{title[:30]:<30}`) to slice extra-long strings and right-pad entries to uniform fixed widths.

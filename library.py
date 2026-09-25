"""
Mini Library Management System
------------------------------
A CLI system to manage books, borrowers, and lending activity using core
Python data structures, built-in file I/O, and datetime arithmetic.
"""

from datetime import datetime, timedelta
import json
import os

STANDARD_BORROW_DAYS = 14


# ==========================================
# Step 1: Data Structures & Initialization
# ==========================================

def load_initial_data(json_file="sample_books.json"):
    """Loads initial book inventory from JSON file if available."""
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Fallback default dataset
    return {
        "101": {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "is_available": True,
            "borrower": None,
            "borrow_date": None,
            "due_date": None,
        },
        "102": {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "is_available": False,
            "borrower": "Alice",
            "borrow_date": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
            "due_date": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"),
        },
        "103": {
            "title": "Design Patterns",
            "author": "Erich Gamma",
            "is_available": True,
            "borrower": None,
            "borrow_date": None,
            "due_date": None,
        },
    }


# ==========================================
# Step 2 & 3: Core Functions & Business Logic
# ==========================================

def add_book(library, book_id, title, author):
    """Adds a new book to the library catalog."""
    if book_id in library:
        print(f"❌ Error: Book ID '{book_id}' already exists in system.")
        return False

    library[book_id] = {
        "title": title,
        "author": author,
        "is_available": True,
        "borrower": None,
        "borrow_date": None,
        "due_date": None,
    }
    print(f"✅ Book '{title}' (ID: {book_id}) added successfully!")
    return True


def search_books(library, search_term):
    """Searches books by title, author, or ID."""
    term = search_term.strip().lower()
    results = []

    for b_id, details in library.items():
        if (term in b_id.lower() or 
            term in details["title"].lower() or 
            term in details["author"].lower()):
            results.append((b_id, details))

    if not results:
        print(f"🔍 No books found matching '{search_term}'.")
        return []

    print(f"\n--- Search Results for '{search_term}' ---")
    for b_id, details in results:
        status = "Available" if details["is_available"] else f"Borrowed by {details['borrower']}"
        print(f"[{b_id}] '{details['title']}' by {details['author']} — ({status})")
    return results


def borrow_book(library, book_id, borrower_name):
    """Handles borrowing logic with availability check and due date calculation."""
    if book_id not in library:
        print(f"❌ Error: Book ID '{book_id}' not found.")
        return False

    book = library[book_id]

    if not book["is_available"]:
        print(f"⚠️ Unavailable: '{book['title']}' is currently checked out by {book['borrower']}.")
        if book["due_date"]:
            print(f"   Expected due date: {book['due_date']}")
        return False

    today = datetime.now()
    due_date = today + timedelta(days=STANDARD_BORROW_DAYS)

    book["is_available"] = False
    book["borrower"] = borrower_name
    book["borrow_date"] = today.strftime("%Y-%m-%d")
    book["due_date"] = due_date.strftime("%Y-%m-%d")

    print(f"✅ Successful checkout!")
    print(f"   Book: '{book['title']}'")
    print(f"   Borrower: {borrower_name}")
    print(f"   Due Date: {book['due_date']}")
    return True


def return_book(library, book_id):
    """Processes returning a borrowed book."""
    if book_id not in library:
        print(f"❌ Error: Book ID '{book_id}' not found.")
        return False

    book = library[book_id]

    if book["is_available"]:
        print(f"⚠️ Book '{book['title']}' was not checked out.")
        return False

    borrower = book["borrower"]
    book["is_available"] = True
    book["borrower"] = None
    book["borrow_date"] = None
    book["due_date"] = None

    print(f"✅ '{book['title']}' successfully returned by {borrower}.")
    return True


def display_summary(library):
    """Generates an executive overview of the library state."""
    total_books = len(library)
    available_books = [b for b in library.values() if b["is_available"]]
    borrowed_books = [b for b in library.values() if not b["is_available"]]
    overdue_books = check_overdue_books(library, print_output=False)

    print("\n" + "=" * 45)
    print("         LIBRARY SYSTEM SUMMARY")
    print("=" * 45)
    print(f"Total Books Cataloged : {total_books}")
    print(f"Available Books       : {len(available_books)}")
    print(f"Currently Borrowed    : {len(borrowed_books)}")
    print(f"Overdue Books         : {len(overdue_books)}")
    print("-" * 45)


def check_overdue_books(library, print_output=True):
    """Identifies books whose due dates are prior to today."""
    today = datetime.now().date()
    overdue_list = []

    for b_id, details in library.items():
        if not details["is_available"] and details["due_date"]:
            due_dt = datetime.strptime(details["due_date"], "%Y-%m-%d").date()
            if due_dt < today:
                days_overdue = (today - due_dt).days
                overdue_list.append((b_id, details, days_overdue))

    if print_output:
        print("\n--- OVERDUE BOOKS REPORT ---")
        if not overdue_list:
            print("✨ No overdue books! All items are within schedule.")
        else:
            for b_id, details, days in overdue_list:
                print(f"🚨 [{b_id}] '{details['title']}' | Borrower: {details['borrower']} | Overdue by: {days} days (Due: {details['due_date']})")

    return overdue_list


# ==========================================
# Step 4: Save Lending Activity Log
# ==========================================

def save_borrowing_records(library, filename="borrowing_records.txt"):
    """Saves all current active and past borrowing activity to a text log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=====================================================\n")
        f.write(f"     LIBRARY BORROWING RECORDS LOG\n")
        f.write(f"     Generated on: {timestamp}\n")
        f.write("=====================================================\n\n")

        f.write(f"{'ID':<6} | {'Book Title':<30} | {'Borrower':<12} | {'Due Date':<10} | {'Status':<10}\n")
        f.write("-" * 75 + "\n")

        for b_id, details in library.items():
            if not details["is_available"]:
                today = datetime.now().date()
                due_dt = datetime.strptime(details["due_date"], "%Y-%m-%d").date()
                status = "OVERDUE" if due_dt < today else "ACTIVE"
                
                f.write(
                    f"{b_id:<6} | {details['title'][:30]:<30} | "
                    f"{details['borrower'][:12]:<12} | {details['due_date']:<10} | {status:<10}\n"
                )

        f.write("\n=====================================================\n")
        f.write("End of Records Log\n")

    print(f"\n💾 Records successfully persisted to '{filename}'.")


# ==========================================
# Main Execution / Interactive CLI
# ==========================================

def main():
    library = load_initial_data()

    while True:
        print("\n" + "=" * 35)
        print("  MINI LIBRARY MANAGEMENT SYSTEM")
        print("=" * 35)
        print("1. Search Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. Add New Book")
        print("5. View Library Summary")
        print("6. Check Overdue Books")
        print("7. Export Records Log & Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            term = input("Enter search term (Title/Author/ID): ")
            search_books(library, term)
        elif choice == "2":
            b_id = input("Enter Book ID to borrow: ")
            borrower = input("Enter Borrower Name: ")
            borrow_book(library, b_id, borrower)
        elif choice == "3":
            b_id = input("Enter Book ID to return: ")
            return_book(library, b_id)
        elif choice == "4":
            b_id = input("Enter Unique Book ID: ")
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            add_book(library, b_id, title, author)
        elif choice == "5":
            display_summary(library)
        elif choice == "6":
            check_overdue_books(library, print_output=True)
        elif choice == "7":
            save_borrowing_records(library)
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()

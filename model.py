from config import get_db_connection
from datetime import date 

def add_books(cursor, books):
    cursor.executemany(
        "INSERT INTO books (name, category) VALUES (%s, %s)", books
    )
    
    
def add_members(cursor, members):
    cursor.executemany(
        "INSERT INTO members (name, birth_date, address) VALUES (%s, %s, %s)", members
    )

def create_borrow_transactions(cursor, transactions):
    cursor.executemany(
        "INSERT INTO transactions (member_id, book_id, borrow_date, status) VALUES (%s, %s, %s, %s)", transactions
    )
    
def fetch_borrow_report(cursor):
    cursor.execute("""
        SELECT m.name, m.birth_date, m.address, b.name AS book_name, t.borrow_date, t.status
        FROM transactions t
        JOIN members m ON t.member_id = m.id
        JOIN books b ON t.book_id = b.id
    """)
    return cursor.fetchall()


def fetch_today_transactions(cursor):
    today = date.today()
    cursor.execute("""
        SELECT m.name, m.birth_date, m.address, b.name AS book_name, t.borrow_date, t.status
        FROM transactions t
        JOIN members m ON t.member_id = m.id
        JOIN books b ON t.book_id = b.id
        WHERE t.borrow_date = %s
    """, (today,))
    return cursor.fetchall()
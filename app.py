from config import get_db_connection
from model import (add_books, add_members, create_borrow_transactions,
                   fetch_borrow_report, fetch_today_transactions)


def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Vui lòng nhập số dương.")
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")


def add_books_menu(cursor, connection):
    while True:
        books = []
        print("=== Nhập thông tin sách ===")
        book_count = get_positive_integer("Nhập số lượng sách bạn muốn thêm: ")
        for i in range(1, book_count + 1):
            book_name = input(f"Tên sách {i}: ")
            category = input(f"Thể loại sách {i}: ")
            books.append((book_name, category))

        add_books(cursor, books)
        connection.commit()  # Lưu thay đổi vào database
        print(f"Đã thêm {book_count} cuốn sách thành công.")

        continue_choice = input("Bạn có muốn thêm sách nữa không? (có/không): ").strip().lower()
        if continue_choice != "có":
            break


def add_members_menu(cursor, connection):
    while True:
        members = []
        print("\n=== Nhập thông tin thành viên ===")
        member_count = get_positive_integer("Nhập số lượng thành viên bạn muốn thêm: ")
        for i in range(1, member_count + 1):
            member_name = input(f"Tên thành viên {i}: ")

            while True:
                birth_date = input(f"Ngày sinh {i} (YYYY-MM-DD): ")
                try:
                    year, month, day = map(int, birth_date.split("-"))
                    break
                except ValueError:
                    print("Ngày sinh không hợp lệ. Định dạng cần là YYYY-MM-DD.")

            address = input(f"Địa chỉ {i}: ")
            members.append((member_name, birth_date, address))

        add_members(cursor, members)
        connection.commit()  # Lưu thay đổi vào database
        print(f"Đã thêm {member_count} thành viên thành công.")

        continue_choice = input("Bạn có muốn thêm thành viên nữa không? (có/không): ").strip().lower()
        if continue_choice != "có":
            break


def add_transactions_menu(cursor, connection):
    while True:
        transactions = []
        print("\n=== Nhập thông tin giao dịch mượn sách ===")
        transaction_count = get_positive_integer("Nhập số lượng giao dịch bạn muốn thêm: ")
        for _ in range(transaction_count):
            member_id = get_positive_integer("Nhập mã thành viên: ")
            book_id = get_positive_integer("Nhập mã sách: ")

            while True:
                borrow_date = input("Nhập ngày mượn (YYYY-MM-DD): ")
                try:
                    year, month, day = map(int, borrow_date.split("-"))
                    break
                except ValueError:
                    print("Ngày mượn không hợp lệ. Định dạng cần là YYYY-MM-DD.")

            status = ""
            while status not in ["Đang mượn", "Đã trả"]:
                status = input("Nhập trạng thái (Đang mượn / Đã trả): ")
                if status not in ["Đang mượn", "Đã trả"]:
                    print("Trạng thái không hợp lệ. Vui lòng nhập 'Đang mượn' hoặc 'Đã trả'.")

            transactions.append((member_id, book_id, borrow_date, status))

        create_borrow_transactions(cursor, transactions)
        connection.commit()  # Lưu thay đổi vào database
        print(f"Đã thêm {transaction_count} giao dịch mượn sách thành công.")

        continue_choice = input("Bạn có muốn thêm giao dịch nữa không? (có/không): ").strip().lower()
        if continue_choice != "có":
            break


def show_borrow_report_menu(cursor):
    while True:
        print("\n=== Báo cáo mượn sách ===")
        borrow_report = fetch_borrow_report(cursor)
        
        header = f"{'STT':<5} | {'Tên Thành Viên':<20} | {'Ngày Sinh':<12} | {'Địa Chỉ':<15} | {'Tên Sách':<25} | {'Ngày Mượn':<12} | {'Trạng Thái':<10}"
        print(header)
        print("-" * len(header))

        for i, row in enumerate(borrow_report, start=1):
            print(
                f"{i:<5} | {row[0]:<20} | {row[1]:<12} | {row[2]:<15} | {row[3]:<25} | {row[4]:<12} | {row[5]:<10}"
            )

        continue_choice = (
            input("Bạn có muốn xem lại báo cáo không? (có/không): ").strip().lower()
        )
        if continue_choice != "có":
            break



def show_today_transactions_menu(cursor):
    while True:
        print("\n=== Giao dịch trong ngày hôm nay ===")
        today_transactions = fetch_today_transactions(cursor)
        
        if today_transactions:
            header = f"{'STT':<5} | {'Tên Thành Viên':<20} | {'Ngày Sinh':<12} | {'Địa Chỉ':<15} | {'Tên Sách':<25} | {'Ngày Mượn':<12} | {'Trạng Thái':<10}"
            print(header)
            print("-" * len(header))

            for i, row in enumerate(today_transactions, start=1):
                print(
                    f"{i:<5} | {row[0]:<20} | {row[1]:<12} | {row[2]:<15} | {row[3]:<25} | {row[4]:<12} | {row[5]:<10}"
                )
        else:
            print("Không có giao dịch nào trong ngày hôm nay.")

        continue_choice = (
            input("Bạn có muốn xem lại giao dịch trong ngày không? (có/không): ")
            .strip()
            .lower()
        )
        if continue_choice != "có":
            break




def main():
    connection = get_db_connection()
    cursor = connection.cursor()

    while True:
        print("\n=== MENU ===")
        print("1. Thêm sách")
        print("2. Thêm thành viên")
        print("3. Thêm giao dịch mượn sách")
        print("4. Hiển thị báo cáo mượn sách")
        print("5. Hiển thị giao dịch trong ngày hôm nay")
        print("6. Thoát")

        choice = input("Chọn một tùy chọn (1-6): ")

        if choice == "1":
            add_books_menu(cursor, connection)
        elif choice == "2":
            add_members_menu(cursor, connection)
        elif choice == "3":
            add_transactions_menu(cursor, connection)
        elif choice == "4":
            show_borrow_report_menu(cursor)
        elif choice == "5":
            show_today_transactions_menu(cursor)
        elif choice == "6":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()

import tkinter as tk
import mysql.connector as mc
from tkinter import messagebox
from tkinter import ttk

myConnnection =""
cursor=""
user=0

        
def MYSQLconnectionCheck ():
    global myConnection
    myConnection=mc.connect(host="localhost",user='root',passwd='8520',)
    if myConnection:
        print("\n CONGRATULATIONS ! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED !")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS librarymanager")
        
        #complete this when the project is done

        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`member` (mem_id INT NOT NULL PRIMARY KEY,contact_1 BIGINT,mem_fname VARCHAR(20),mem_addr VARCHAR(50),age INT,book_id INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`admin` (admin_id INT NOT NULL PRIMARY KEY, admin_name VARCHAR(50), pssw VARCHAR(20) NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`library` (Lib_name VARCHAR(100), contact_no BIGINT, Lib_addr VARCHAR(100), lib_id INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`employee` (emp_id INT NOT NULL PRIMARY KEY, contact_no BIGINT, psswd VARCHAR(20), Emp_fname VARCHAR(20), Emp_lname VARCHAR(20), lib_id INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`books` (book_id INT NOT NULL PRIMARY KEY, title VARCHAR(75), price INT, status VARCHAR(20), Author_id INT, lib_id INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS `librarymanager`.`author` (Author_id INT NOT NULL PRIMARY KEY, Author_fname VARCHAR(20), Author_lname VARCHAR(20));")
        cursor.execute("")
        cursor.execute("COMMIT")
        print("\n DB AND TABLE CREATED SUCCESSFULLY.")
        return myConnection
        cursor.close()
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")

#MODULE TO ESTABLISHED MYSQL CONNECTION
def MYSQLconnection ():
    global myConnection   
    myConnection=mc.connect(host="localhost",user='root',passwd='8520' ,database='libraryManager')
    if myConnection:
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")
    myConnection.close()

def mysql_exe(iq):
    cursor=myConnection.cursor()
    if myConnection:
        cursor.execute(iq)
        cursor.execute("")
        cursor.execute("COMMIT")
        print("\nstatement executed.")
        cursor.close()
    else:
        print("Could not enter data")
def mysql_out(oq,x):
    cursor = myConnection.cursor()
    if myConnection:
        cursor.execute(oq)
        D = cursor.fetchall()
        
        if x==1:
            for x in D: 
                for i in x:
                    print(str(i))
                print("\t")
        
            for result in cursor.stored_results():
                for row in result.fetchall():
                    print(row)
        
            cursor.close()
        else:
            return D
    else:
        print("Connection not established")

def last(ide,tab):
    cursor=myConnection.cursor()
    cursor.execute('SELECT {} FROM {} WHERE {} = (SELECT MAX({}) FROM {});'.format(ide, tab, ide,ide,tab))
    q=cursor.fetchall()
    return q[0][0]

def login(emp_id,password):
    global user
    cursor = myConnection.cursor()
    if myConnection:
        if emp_id and password:
            sql = "SELECT * FROM `librarymanager`.`employee` WHERE emp_id = {}".format(emp_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                if result[2] == password:
                    user=emp_id
                    messagebox.showinfo("Login Successful", "Welcome, {}!".format(result[3]))
                    if int(user)==1:
                        admin_page()
                    else:
                        emp_page()
                    
                else:
                    messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
                    
            else:
                messagebox.showerror("Login Failed", "Invalid user ID. Please try again.")
                
        else:
            messagebox.showerror("Login Failed", "Please enter both employee ID and password.")

            
def add_emp(fname,lname,cont,pssw):
    out = last('emp_id', 'employee') + 1
    q = "INSERT INTO employee (emp_id, contact_no, psswd, Emp_fname, Emp_lname, lib_id) VALUES ({}, {}, '{}', '{}', '{}', {})".format(out, cont, pssw, fname, lname, 1001)
    mysql_exe(q)
    messagebox.showinfo("Employee Added", "Employee added successfully.")
    admin_page()
def input_employee_data():
    clear_widgets()
    
    tk.Label(root, text="First Name:",bg='#76C4AE').pack(pady=(20,0))
    fname_entry = tk.Entry(root)
    fname_entry.pack(pady=(10,0))

    tk.Label(root, text="Last Name:",bg='#76C4AE').pack(pady=(20,0))
    lname_entry = tk.Entry(root)
    lname_entry.pack(pady=(10,0))

    tk.Label(root, text="Contact:",bg='#76C4AE').pack(pady=(20,0))
    cont_entry = tk.Entry(root)
    cont_entry.pack(pady=(10,0))

    tk.Label(root, text="Password:",bg='#76C4AE').pack(pady=(20,0))
    pssw_entry = tk.Entry(root, show='*')
    pssw_entry.pack(pady=(10,0))

    tk.Button(root, text="Add Employee", command=lambda: add_emp(fname_entry.get(), lname_entry.get(), cont_entry.get(), pssw_entry.get())).pack(pady=(20,0))
    tk.Button(root, text="Back", command=admin_page).pack(pady=(20,0))

def del_emp(ide):
    q="DELETE FROM employee where emp_id={}".format(int(ide))
    mysql_exe(q)
    messagebox.showinfo("Employee Removed", "Employee removed successfully.")
    admin_page()
def delete_employee_data():
    clear_widgets()

    tk.Label(root, text="Employee ID:",bg='#76C4AE').pack(pady=(20,0))
    emp_id_entry = tk.Entry(root)
    emp_id_entry.pack(pady=(10,0))
    tk.Button(root, text="Delete Employee", command=lambda: del_emp(int(emp_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=admin_page).pack(pady=(20,0))
    

def add_book(title, price, author_id):
    q = 'SELECT * FROM author WHERE Author_id={}'.format(author_id)
    out = mysql_out(q, 0)

    if not out:
        messagebox.showinfo("Author Not Found", "Author not found. Please enter a new author.")
        input_author_data(author_id)
        return

    ide = last('book_id', 'books') + 1
    q = "INSERT INTO books (book_id, title, price, status, Author_id, lib_id) VALUES ({}, '{}', {}, '{}', {}, {})".format(ide, title, price, 'Available', author_id, 1001)
    mysql_exe(q)
    messagebox.showinfo("Success", "Book added successfully.")
    emp_page()

def input_book_data():
    clear_widgets()

    tk.Label(root, text="Title:",bg='#76C4AE').pack(pady=(20,0))
    title_entry = tk.Entry(root)
    title_entry.pack(pady=(10,0))

    tk.Label(root, text="Price:",bg='#76C4AE').pack(pady=(20,0))
    price_entry = tk.Entry(root)
    price_entry.pack(pady=(10,0))

    tk.Label(root, text="Author ID:",bg='#76C4AE').pack(pady=(20,0))
    author_id_entry = tk.Entry(root)
    author_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Add Book", command=lambda: add_book(title_entry.get(), int(price_entry.get()), int(author_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))
    

def add_author(fname, lname, ide=0):
    if ide == 0:
        ide = last('Author_id', 'author')
        ide = ide + 1
    
    q = "INSERT INTO author (Author_id, Author_fname, Author_lname) VALUES ({}, '{}', '{}');".format(ide, fname, lname)
    mysql_exe(q)
    messagebox.showinfo("Success", "Author added successfully.")
    emp_page()
def input_author_data(ide=0):
    clear_widgets()

    tk.Label(root, text="First Name:",bg='#76C4AE').pack(pady=(20,0))
    fname_entry = tk.Entry(root)
    fname_entry.pack(pady=(10,0))

    tk.Label(root, text="Last Name:",bg='#76C4AE').pack(pady=(20,0))
    lname_entry = tk.Entry(root)
    lname_entry.pack(pady=(10,0))

    tk.Button(root, text="Add Author", command=lambda: add_author(fname_entry.get(), lname_entry.get(), ide)).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

    

def del_book(ide):
    q = 'DELETE FROM books WHERE book_id={};'.format(ide)
    mysql_exe(q)
    messagebox.showinfo("Success", "Book removed successfully.")
    emp_page()
def del_book_gui():
    clear_widgets()

    tk.Label(root, text="Book ID:",bg='#76C4AE').pack(pady=(20,0))
    book_id_entry = tk.Entry(root)
    book_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Delete Book", command=lambda: del_book(int(book_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def del_author(ide):
    q = 'DELETE FROM author WHERE author_id={};'.format(ide)
    mysql_exe(q)
    messagebox.showinfo("Success", "Author removed successfully.")
    emp_page()
def del_author_gui():
    clear_widgets()

    tk.Label(root, text="Author ID:",bg='#76C4AE').pack(pady=(20,0))
    author_id_entry = tk.Entry(root)
    author_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Delete Author", command=lambda: del_author(int(author_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def add_member(contact, name, addr, age, book_id):
    ide = last('mem_id', 'member') + 1
    q = "INSERT INTO member (mem_id, contact_1, mem_fname, mem_addr, age, book_id) VALUES ({}, '{}', '{}', '{}', {}, {});".format(ide, contact, name, addr, age, book_id)
    mysql_exe(q)
    messagebox.showinfo("Success", "Member added successfully.")
    emp_page()
def add_member_gui():
    clear_widgets()

    tk.Label(root, text="Phone Number:",bg='#76C4AE').pack(pady=(20,0))
    contact_entry = tk.Entry(root)
    contact_entry.pack(pady=(10,0))

    tk.Label(root, text="First Name:",bg='#76C4AE').pack(pady=(20,0))
    name_entry = tk.Entry(root)
    name_entry.pack(pady=(10,0))

    tk.Label(root, text="Address:",bg='#76C4AE').pack(pady=(20,0))
    addr_entry = tk.Entry(root)
    addr_entry.pack(pady=(10,0))

    tk.Label(root, text="Age:",bg='#76C4AE').pack(pady=(20,0))
    age_entry = tk.Entry(root)
    age_entry.pack(pady=(10,0))

    tk.Label(root, text="Issued Book ID:",bg='#76C4AE').pack(pady=(20,0))
    book_id_entry = tk.Entry(root)
    book_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Add Member", command=lambda: add_member(contact_entry.get(), name_entry.get(), addr_entry.get(), int(age_entry.get()), int(book_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def del_member(mem_id):
    q = 'DELETE FROM member WHERE mem_id={};'.format(mem_id)
    mysql_exe(q)
    messagebox.showinfo("Success", "Member removed successfully.")
    emp_page()
def del_member_gui():
    clear_widgets()

    tk.Label(root, text="Member ID:",bg='#76C4AE').pack(pady=(20,0))
    mem_id_entry = tk.Entry(root)
    mem_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Delete Member", command=lambda: del_member(int(mem_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def issue_book(mem_id, book_id):

    member_exists_q = "SELECT * FROM member WHERE mem_id={};".format(mem_id)
    member_exists = mysql_out(member_exists_q, 0)
    if not member_exists:
        messagebox.showerror("Book Issue Failed", "Member ID {} does not exist.".format(mem_id))
        return

    book_status_q = "SELECT status FROM books WHERE book_id={};".format(book_id)
    book_status = mysql_out(book_status_q, 0)
    if not book_status:
        messagebox.showerror("Book Issue Failed", "Book ID {} does not exist.".format(book_id))
        return
    elif book_status[0][0] != 'Available':
        messagebox.showerror("Book Issue Failed", "Book ID {} is not available for issue.".format(book_id))
        return

    q = 'UPDATE member SET book_id={} WHERE mem_id={};'.format(book_id, mem_id)
    mysql_exe(q)
    messagebox.showinfo("Book Issued", "Book issued successfully.")
    emp_page()

def input_issue_data():
    clear_widgets()

    tk.Label(root, text="Member ID:",bg='#76C4AE').pack(pady=(20,0))
    mem_id_entry = tk.Entry(root)
    mem_id_entry.pack(pady=(10,0))

    tk.Label(root, text="Book ID:",bg='#76C4AE').pack(pady=(20,0))
    book_id_entry = tk.Entry(root)
    book_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Issue Book", command=lambda: issue_book(int(mem_id_entry.get()), int(book_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def return_book(mem_id, book_id):

    member_exists_q = "SELECT * FROM member WHERE mem_id={};".format(mem_id)
    member_exists = mysql_out(member_exists_q, 0)
    if not member_exists:
        messagebox.showerror("Book Return Failed", "Member ID {} does not exist.".format(mem_id))
        return

    book_status_q = "SELECT book_id FROM member WHERE mem_id={} AND book_id={};".format(mem_id, book_id)
    book_status = mysql_out(book_status_q, 0)
    if not book_status:
        messagebox.showerror("Book Return Failed", "Book ID {} is not issued to Member ID {}.".format(book_id, mem_id))
        return

    q = 'UPDATE member SET book_id=NULL WHERE mem_id={};'.format(mem_id)
    mysql_exe(q)
    messagebox.showinfo("Book Returned", "Book returned successfully.")
    emp_page()
def return_book_gui():
    clear_widgets()
    
    tk.Label(root, text="Member ID:").pack(pady=(20,0))
    mem_id_entry = tk.Entry(root)
    mem_id_entry.pack(pady=(10,0))

    tk.Label(root, text="Book ID:").pack(pady=(20,0))
    book_id_entry = tk.Entry(root)
    book_id_entry.pack(pady=(10,0))

    tk.Button(root, text="Return Book", command=lambda: return_book(int(mem_id_entry.get()), int(book_id_entry.get()))).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))

def print_books():
    clear_widgets()
    D = mysql_out('SELECT * FROM books;', 0)
    display_books_table(D)
def display_books_table(data):
    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    
    tree = ttk.Treeview(root, columns=("Book ID", "Title", "Price", "Status", "Author ID", "Library ID"), show="headings", style="Treeview")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
    
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack()
    button = tk.Button(root, text="Back", command=table_page)
    button.pack(pady=20)

def print_members():
    clear_widgets()
    D = mysql_out('SELECT * FROM member;', 0)
    display_members_table(D)
def display_members_table(data):
    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    
    tree = ttk.Treeview(root, columns=("Member ID", "Contact", "First Name", "Address", "Age", "Book ID"), show="headings", style="Treeview")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
    
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack()
    button = tk.Button(root, text="Back", command=table_page)
    button.pack(pady=20)

def print_authors():
    clear_widgets()
    D = mysql_out('SELECT * FROM author;', 0)
    display_authors_table(D)
def display_authors_table(data):
    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    
    tree = ttk.Treeview(root, columns=("Author ID", "First Name", "Last Name"), show="headings", style="Treeview")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
    
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack()
    button = tk.Button(root, text="Back", command=table_page)
    button.pack(pady=20)

def print_books_authors():
    clear_widgets()
    D = mysql_out('SELECT * FROM books_authors_view;', 0)
    display_books_authors_table(D)
def display_books_authors_table(data):
    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    
    tree = ttk.Treeview(root, columns=("Author ID", "First Name", "Last Name", "Book ID", "Title", "Status"), show="headings", style="Treeview")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
    
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack()
    button = tk.Button(root, text="Back", command=table_page)
    button.pack(pady=20)

def print_employee_library():
    clear_widgets()
    D = mysql_out('SELECT * FROM employee_library_view;', 0)
    display_employee_library_table(D)
def display_employee_library_table(data):
    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    
    tree = ttk.Treeview(root, columns=("Employee ID", "Library Name"), show="headings", style="Treeview")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
    
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack()
    button = tk.Button(root, text="Back", command=table_page)
    button.pack(pady=20)

def print_employee():
    clear_widgets()
    D=mysql_out('Select * from employee;',0)

    style = ttk.Style()
    style.configure("Treeview", background="#76C4AE", fieldbackground="#76C4AE", foreground="white")
    tree = ttk.Treeview(root, columns=("emp_id", "contact_no", "psswd", "Emp_fname", "Emp_lname", "lib_id"), show="headings", style="Treeview")
    
    tree.heading("emp_id", text="emp_id")
    tree.heading("contact_no", text="contact_no")
    tree.heading("psswd", text="psswd")
    tree.heading("Emp_fname", text="Emp_fname")
    tree.heading("Emp_lname", text="Emp_lname")
    tree.heading("lib_id", text="lib_id")

    for row in D:
        tree.insert("", tk.END, values=row)
    tree.pack()
    button = tk.Button(root, text="Back", command=admin_page)
    button.pack(pady=20)

def login_page():
    clear_widgets()
    username_label = tk.Label(root, text="Username:",bg='#76C4AE', font=('Helvetica', 10))
    username_label.pack(pady=(10,0))
    entr1 = tk.Entry(root, width=30, bg='#9FC2BA', font=('Helvetica', 10, "italic"))
    entr1.pack(pady=10)  

    password_label = tk.Label(root, text="Password:",bg='#76C4AE', font=('Helvetica', 10))
    password_label.pack(pady=(10,0))
    entr2 = tk.Entry(root, width=30, bg='#9FC2BA', font=('Helvetica', 10, 'italic'),show='*')
    entr2.pack(pady=10)  # Adjust padding as needed

        # Button to trigger data retrieval
    button = tk.Button(root, text="Login", command=lambda: login(entr1.get(), entr2.get()))
    button.pack(pady=10)# Adjust padding as needed
    

def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

def logout():
    global user
    user = 0
    login_page()
    return
    
def admin_page():
    clear_widgets()
    button1 = tk.Button(root, text="Add Employee", command=input_employee_data)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="Remove Employee", command=delete_employee_data)
    button2.pack(pady=10)
    button3 = tk.Button(root, text="Print Employee table", command=print_employee)
    button3.pack(pady=1)
    button4 = tk.Button(root, text="Logout", command=logout)
    button4.pack(pady=10)

def emp_page():
    clear_widgets()
    button1 = tk.Button(root, text="Add Book", command=input_book_data)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="Remove Book", command=del_book_gui)
    button2.pack(pady=10)
    button3 = tk.Button(root, text="Add Member", command=add_member_gui)
    button3.pack(pady=10)
    button4 = tk.Button(root, text="Remove Member", command=del_member_gui)
    button4.pack(pady=10)
    button5 = tk.Button(root, text="Add Author", command=input_author_data)
    button5.pack(pady=10)
    button6 = tk.Button(root, text="Remove Author", command=del_author_gui)
    button6.pack(pady=10)
    button7 = tk.Button(root, text="Issue book", command=input_issue_data)
    button7.pack(pady=10)
    button8 = tk.Button(root, text="Return Book", command=return_book_gui)
    button8.pack(pady=10)
    button9 = tk.Button(root, text="Show tables", command=table_page)
    button9.pack(pady=10)
    button10 = tk.Button(root, text="Logout", command=logout)
    button10.pack(pady=10)
        
def table_page():
    clear_widgets()
    tk.Button(root, text="Books Table", command=print_books).pack(pady=(20,0))
    tk.Button(root, text="Members Table", command=print_members).pack(pady=(20,0))
    tk.Button(root, text="Authors Table", command=print_authors).pack(pady=(20,0))
    tk.Button(root, text="Books & Authors Table", command=print_books_authors).pack(pady=(20,0))
    tk.Button(root, text="Employee & Library Table", command=print_employee_library).pack(pady=(20,0))
    tk.Button(root, text="Back", command=emp_page).pack(pady=(20,0))
    
myConnection = MYSQLconnectionCheck()
    
root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='#76C4AE')
root.title("Library Manager")

if myConnection:
    MYSQLconnection()
    login_page()
    
root.mainloop()

#                                                                      ربنا واشرح لي صدري وييسر لي أمري

'''

Download pandas >> pip install pandas

This code created by Mohammad Al Jadallah >> developerx

You can help to make this code more better

Follow me in 

Instagram >> developerx2
TikTok >> developerx2
Youtube >> developerx

Thank you,

'''

import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import sqlite3
import pandas as pd
from _tkinter import TclError
from threading import Thread

class App:
    def __init__(self):
        # set up the screen
        self.root = Tk()
        self.root.iconbitmap(r"./img/icon.ico")
        self.page_number = 0
        # style
        self.style = ttk.Style()

        # set image as background
        self.img = PhotoImage(file="./img/bgSplash.png")

        self.label_background = Label(self.root, image=self.img)
        self.label_background.place(x=0, y=0)

        # Splash Screen
        self.geo = self.root.geometry("1300x690")
        self.resizeable = self.root.resizable(False, False)
        self.title = self.root.title("       SQLITE VIEWER")

        # btn to ask open file, this will make us access to the button and destroy it from the window
        self.btn_open_file = None

        self.name_file = None
        # varibale instance to store text of box queries
        # variables for database
        self.box_queries = None

        self.cols = None
        self.data = None

        self.res_name_table = None
        self.res_info_table = None

        # tree
        self.tree = ttk.Treeview()

    def open_file_screen(self):
        self.page_number = 1  # now we ar in the second page
        # Now create a window for drop sql files
        self.label_background.destroy()
        self.img = PhotoImage(file="./img/bgDropFile.png")

        self.label_background = Label(self.root, image=self.img)
        self.label_background.place(x=0, y=0)

        self.btn_open_file = Button(self.root, text="Open File", font=("Comic Sans MS", 40, "bold"),
                                    relief=FLAT, cursor="hand2", bg='#fcc2e7', activebackground="#fcc2e7",
                                    highlightcolor="#a1b0e4", default='active', highlightthickness=4, bd=0,
                                    command=lambda: self.open_sql_file())
        self.btn_open_file.place(x=350, y=345, width=600, height=200)

    # ask user to open the file and after choose the file return the path
    # to use the path when we want to connect with the database

    def open_sql_file(self):
        try:
            # to make sure the open window not open if execute btn pressed
            # if self.btn_open_file["text"] == "Execute":
            self.name_file = filedialog.askopenfile()
            return self.name_file.name

        except (TypeError, AttributeError):
            # messagebox.showerror(title="Error", message="This is Error ")
            pass
            # print(name_file.name) to know the path of the file >> name='C:/Users/yourname/Downloads/210906.jpg'
        finally:
            # when we press cancel button will return None
            if self.name_file is None:
                print('Cancel is pressed')

            if self.page_number == 1 and self.name_file is not None:
                self.btn_open_file.destroy()
                self.label_background.destroy()
                self.main_screen()
                self.collect_data_about_database_and_execute()

            else:  # now we in main page which means second page
                if self.name_file is None:
                    pass
                else:
                    try:
                        def remove_many():
                            x = self.tree.get_children()
                            for record in x:
                                self.tree.delete(record)

                        remove_many()
                        self.box_queries.delete(0.0, 'end-1c')
                        self.collect_data_about_database_and_execute()

                    except TclError:
                        def remove_many():
                            x = self.tree.get_children()
                            for record in x:
                                self.tree.delete(record)

                        remove_many()
                        self.box_queries.delete(0.0, 'end-1c')
                        self.collect_data_about_database_and_execute()
                        # messagebox.showwarning("Warning", "you are use the same file")

    def main_screen(self):
        self.page_number = 2  # second page
        # Here is the main screen to show data of the database file
        self.img = PhotoImage(file="./img/bgMain.png")
        self.label_background = Label(self.root, image=self.img)
        self.label_background.place(x=0, y=0)

        self.style.configure("Treeview", font=("normal", 11, "bold"), rowheight=30)
        self.style.configure("Treeview.Heading", font=("normal", 14, "bold"))
        # scorbar
        scroll_frame = Frame(self.root)
        scroll_frame.pack(side=TOP, fill=X)

        ysbar = Scrollbar(scroll_frame)
        ysbar.pack(side=RIGHT, fill=Y)

        # X scrollbar

        xsbar = Scrollbar(scroll_frame, orient="horizontal")
        xsbar.pack(side=BOTTOM, fill=X)

        # treeview
        self.tree = ttk.Treeview(scroll_frame, columns=self.res_info_table, show="headings", selectmode="extended",
                                 yscrollcommand=ysbar.set,
                                 xscrollcommand=xsbar.set, height=11)

        # how to change color of selected row: map to make dynamic values usnig opetion we use
        self.style.map("Treeview", background=[("selected", '#fea8dc')], foreground=[("selected", "black")])

        # config scrollbar
        ysbar.config(command=self.tree.yview)
        xsbar.config(command=self.tree.xview)

        # config the form of the rows
        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("evenrow", background="#d9d3ee")

        self.tree.pack(fill=X)

        # Frame to put text widget on it
        frame_box_queries = Frame(self.root)
        frame_box_queries.place(x=250, y=400, width=800, height=150)

        # Scrollbar for text_box_queries
        scrollbar_y_queries_box = Scrollbar(frame_box_queries)
        scrollbar_y_queries_box.pack(side=RIGHT, fill=Y)

        # box for queries

        self.box_queries = Text(frame_box_queries, font=("normal", 18),  # Comic Sans MS
                                yscrollcommand=scrollbar_y_queries_box.set,
                                spacing1=8, undo=TRUE, insertbackground="#013449", background="#F4DFEB", relief=FLAT,
                                bd=5, highlightcolor="#ff83cd", highlightthickness=4, highlightbackground="#b4a7e0",
                                selectbackground="#b4a7e0", selectforeground="black",  wrap="word")
        self.box_queries.pack()  # wrap="word" to wrap words and to be the last word not as division

        # Config Y scrollbar
        scrollbar_y_queries_box.config(command=self.box_queries.yview)

        # open file button
        self.btn_open_file = Button(self.root, text="Open File", font=("Comic Sans MS", 20, "bold"),
                                    relief=FLAT, cursor="hand2", bg='#fcc2e7', activebackground="#fcc2e7",
                                    highlightcolor="#a1b0e4", default='active', highlightthickness=4, bd=0,
                                    command=lambda: self.open_sql_file())

        self.btn_open_file.place(x=50, y=400, width=200)

        # donwload data in csv fil button
        self.btn_open_file = Button(self.root, text="Download CSV File", font=("Comic Sans MS", 14, "bold"),
                                    relief=FLAT, cursor="hand2", bg='#fcc2e7', activebackground="#fcc2e7",
                                    highlightcolor="#a1b0e4", default='active', highlightthickness=4, bd=0,
                                    command=lambda: Thread(target=self.download_csv_file()).start)

        self.btn_open_file.place(x=50, y=480, width=200, height=70)

        # execute code button
        self.btn_open_file = Button(self.root, text="Execute", font=("Comic Sans MS", 18, "bold"),
                                    relief=FLAT, cursor="hand2", bg='#fcc2e7', activebackground="#fcc2e7",
                                    highlightcolor="#a1b0e4", default='active', highlightthickness=4, bd=0,
                                    command=lambda: Thread(target=self.execute_command()).start)

        self.btn_open_file.place(x=1070, y=400, width=200, height=70)
        self.tree.bind("<Double-1>", self.copy_cell)

    def connect_database(self, commands_execute):
        path_of_file = str(self.name_file.name)

        print(path_of_file)
        try:  # try to connect with database
            connect_database_ = sqlite3.connect(f'file:{path_of_file}?mode=ro', uri=True)  # "database.sqlite"
            print("Conncet successfully...")

            cour_ = connect_database_.cursor()

            # get columns names using pandas
            self.cols = list(pd.read_sql_query(commands_execute, connect_database_).columns)
            print("Command is executed successfully...\n")

            # set treeview
            self.tree.delete(*self.tree.get_children())

            self.tree.configure(columns=self.cols)
            # column of data
            for i in self.cols:  # range(len(self.cols)):

                if self.cols[-1] == i:
                    self.tree.column(column=i, stretch=NO, width=1300)
                    self.tree.heading(column=i, text=f"{i}", anchor=W)

                else:
                    self.tree.column(column=i, stretch=NO, width=200)
                    self.tree.heading(column=i, text=f"{i}", anchor=W)
            self.tree.update()
            # insert data and determin if the row index is eve or odd to make stripped rows
            data = commands_execute
            data = cour_.execute(data).fetchall()

            for value, index in zip(data, range(len(data))):
                # if even
                if index % 2 == 0:
                    self.tree.insert(parent="", index=END, values=value, iid=index, tags="evenrow")
                else:  # if odd
                    self.tree.insert(parent="", index=END, values=value, iid=index, tags="oddrow")

        except (pd.io.sql.DatabaseError, sqlite3.OperationalError) as e:
            if str(e).endswith('attempt to write a readonly database'):
                true_or_false = messagebox.askretrycancel("Modify Database", "You are trying to modifying on the"
                                                                             " database.\n"
                                                                             "are you sure to do that")
                if true_or_false:

                    # تم حل مشكلة عدم السماح بالكتابة داخل الملف من خلال وضع الكيرسور هنا حتى يفهم على الملف
                    # Execution failed on sql 'create table toto(id int primary_key,
                    # name text, age int);': attempt to write a readonly database

                    connect_database_ = sqlite3.connect(path_of_file)
                    print("Permissions of Database Changed To Write Mode...")
                    data = commands_execute
                    cour_ = connect_database_.cursor()
                    data = cour_.execute(data)
                    print("Command is executed successfully...\n")

                else:
                    print("Permissions of Database Denied")
            else:
                if str(e).endswith("syntax error"):
                    messagebox.showerror("operation error",
                                         f"if you execute more than one command\nonly one command you can execute\n"
                                         f"use comment for other commands\n\n"
                                         f"{e}")
                else:
                    messagebox.showerror("operation error", f"{e}")

        except sqlite3.DatabaseError:
            messagebox.showerror("Error Connection",
                                 "Error connection with the database\ncheck if the file is database")

        except TypeError as e:

            if self.box_queries.get(0.0, 'end - 1c').lower().strip():
                pass  # here if we put this line when the text box empty the message error will pop up no command
                        # but when there is anything else heppen cause of the Typeerror,
                        # as when we use create table if not exists toto(id in, name text),
                        # we don't need to show popup or error because the command is true
                        # and indeed the table is exists

            else:
                messagebox.showerror("Error Commands", "There is no commands")

    def execute_command(self):
        # get the database after connection
        # get text of text box quereies self.box_queries.get(1.0, "end-1c") direct to get the latest text
        self.connect_database(self.box_queries.get(1.0, "end-1c"))

    def collect_data_about_database_and_execute(self):
        path_of_file = str(self.name_file.name)

        try:  # try to connect with database
            connect_database_ = sqlite3.connect(f'file:{path_of_file}?mode=ro', uri=True)  # "database.sqlite"
            print("Conncet successfully...")

            cour_ = connect_database_.cursor()
            # ========================================================

            # let me know what are the tebles exists in database
            query1 = 'SELECT name FROM sqlite_master WHERE type = "table"'
            # we execute the above query and get any table, so we will get the first table [0][0]
            self.res_name_table = cour_.execute(query1).fetchall()[0][0]

            # get info of table to get columns name
            query2 = f'PRAGMA table_info({self.res_name_table})'
            self.res_info_table = [col[1] for col in cour_.execute(query2).fetchall()]  # we need them for tree

            # give me information of that table
            self.box_queries.insert(END, f"SELECT * FROM {self.res_name_table} LIMIT 0, 15;")  # query executed...
            # print(self.res_info_table)

            # set treeview
            self.tree.configure(columns=self.res_info_table)
            # column of data
            for i in range(len(self.res_info_table)):
                if self.res_info_table[-1] == self.res_info_table[i]:
                    self.tree.column(column=self.res_info_table[i], stretch=NO, width=1300)
                    self.tree.heading(column=self.res_info_table[i], text=f"{self.res_info_table[i]}", anchor=W)
                else:
                    self.tree.column(column=self.res_info_table[i], stretch=NO, width=500)
                    self.tree.heading(column=self.res_info_table[i], text=f"{self.res_info_table[i]}", anchor=W)
            self.tree.update()

            # insert data and determin if the row index is eve or odd to make stripped rows
            data = f'SELECT * FROM {self.res_name_table} LIMIT 0, 15;'
            data = cour_.execute(data).fetchall()

            for value, index in zip(data, range(len(data))):
                # if even
                # print(value)
                if index % 2 == 0:
                    self.tree.insert(parent="", index=END, values=value, iid=index, tags="evenrow")
                else:
                    self.tree.insert(parent="", index=END, values=value, iid=index, tags="oddrow")

        except sqlite3.OperationalError as e:
            messagebox.showerror("operation error",
                                 f"{e}")

        except sqlite3.DatabaseError:
            def remove_many():
                x = self.tree.get_children()
                for record in x:
                    self.tree.delete(record)
            remove_many()
            fake_columns_view = ["columns1", "columns2", "columns3"]
            self.tree.configure(columns=fake_columns_view)
            for i in range(len(fake_columns_view)):
                self.tree.column(column=fake_columns_view[i], stretch=NO, width=500)
                self.tree.heading(column=fake_columns_view[i], text=f"{fake_columns_view[i]}", anchor=W)
            self.tree.update()
            messagebox.showerror("Error Connection",
                                 "Error connection with the database\ncheck if the file is database")

        except IndexError:
            def remove_many():
                x = self.tree.get_children()
                for record in x:
                    self.tree.delete(record)
            remove_many()
            fake_columns_view = ["columns1", "columns2", "columns3"]
            self.tree.configure(columns=fake_columns_view)
            for i in range(len(fake_columns_view)):
                self.tree.column(column=fake_columns_view[i], stretch=NO, width=500)
                self.tree.heading(column=fake_columns_view[i], text=f"{fake_columns_view[i]}", anchor=W)
            self.tree.update()

            messagebox.showerror("Error",
                                 "There is no tables or columns in the file\n"
                                 "please make sure the database contains tables")

    def download_csv_file(self):
        try:
            data = []
            for line in self.tree.get_children():
                data += [self.tree.item(line)['values']]

            df = pd.DataFrame(data, columns=self.tree['columns'])

            file_to_save = filedialog.asksaveasfilename(filetypes=[('CSV files', '*.csv')])
            df.to_csv(file_to_save, index=False)
            print("finished...")

        except FileNotFoundError:
            print("No Files Saved...")

    # create event to copy cell after two click(double click)
    def copy_cell(self, event):
        focus_item = self.tree.item(self.tree.focus())  # focus will focus on the specified item
        col = self.tree.identify_column(event.x)  # event.x will identify the columns
        self.root.clipboard_clear()
        self.root.clipboard_append(focus_item['values'])
        print("The column specified and clicked is " + col)  # when pressed clipboard

    def run(self):
        self.root.after(3000, self.open_file_screen)
        mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
    print("SQLITE VIEWER is Closed By User")


# تم بحمد الله
# Finished

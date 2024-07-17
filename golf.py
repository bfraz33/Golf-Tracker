import tkinter as tk
from tkinter import ttk
import pyodbc

def connect_to_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=.\SQLEXPRESS;'
                          'DATABASE=MyGolfData;'
                          'Trusted_Connection=yes;')
    return conn

def insert_course_data(Name, num_holes, nine_type):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (Name, number_of_holes, nine_type)
            VALUES (?, ?, ?)
        """, (Name, num_holes, nine_type))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        print("Error in connection:", e)

def insert_player_data(player_name):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Player (Player_name)
            VALUES (?)
        """, (player_name,))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        print("Error in connection:", e)

def insert_date_data(month, year):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Date (month, year)
            VALUES (?, ?)
        """, (month, year))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        print("Error in connection:", e)

def insert_hole_data(num_holes, nine_type):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        for i in range(num_holes):
            hole_number = hole_entries[i]['hole_number'].get()
            par = hole_entries[i]['par'].get()
            fairways_in_play = hole_entries[i]['fairways_in_play'].get()
            fairways_not_in_play = hole_entries[i]['fairways_not_in_play'].get()
            greens_in_regulation = hole_entries[i]['greens_in_regulation'].get()
            greens_not_in_regulation = hole_entries[i]['greens_not_in_regulation'].get()
            putts = hole_entries[i]['putts'].get()
            score = hole_entries[i]['score'].get()

            cursor.execute("""
                INSERT INTO Hole (hole_number, par, fairways_in_play, fairways_not_in_play, greens_in_regulation, greens_not_in_regulation, putts_on_hole, score, nine_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            """, (hole_number, par, fairways_in_play, fairways_not_in_play, greens_in_regulation, greens_not_in_regulation, putts, score, nine_type))
        
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        print("Error in connection:", e)

root = tk.Tk()
root.title("Golf Data Entry")

# Initial setup for course selection
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Month:").grid(column=0, row=0, padx=10, pady=5)
month_entry = ttk.Entry(frame)
month_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(frame, text="Year:").grid(column=0, row=1, padx=10, pady=5)
year_entry = ttk.Entry(frame)
year_entry.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(frame, text="Select Course:").grid(column=0, row=2, padx=10, pady=5)
course_entry = ttk.Entry(frame)
course_entry.grid(column=1, row=2, padx=10, pady=5)

ttk.Label(frame, text="Player:").grid(column=0, row=3, padx=10, pady=5)
player_entry = ttk.Entry(frame)
player_entry.grid(column=1, row=3, padx=10, pady=5)

ttk.Label(frame, text="Select 9 or 18 Holes:").grid(column=0, row=4, padx=10, pady=5)
holes_var = tk.StringVar(value="9")
ttk.Radiobutton(frame, text="9 Holes", variable=holes_var, value="9").grid(column=1, row=4, padx=10, pady=5)
ttk.Radiobutton(frame, text="18 Holes", variable=holes_var, value="18").grid(column=2, row=4, padx=10, pady=5)

ttk.Label(frame, text="Select Front 9 or Back 9:").grid(column=0, row=5, padx=10, pady=5)
nine_type_var = tk.StringVar(value="Front")
ttk.Radiobutton(frame, text="Front 9", variable=nine_type_var, value="Front").grid(column=1, row=5, padx=10, pady=5)
ttk.Radiobutton(frame, text="Back 9", variable=nine_type_var, value="Back").grid(column=2, row=5, padx=10, pady=5)

def handle_next():
    course_name = course_entry.get()
    player_name = player_entry.get()
    num_holes = int(holes_var.get())
    nine_type = nine_type_var.get()
    insert_course_data(course_name, num_holes, nine_type)
    insert_player_data(player_name)
    insert_date_data(month_entry.get(), year_entry.get())
    create_hole_input_fields(num_holes)

def submit_and_exit():
    num_holes = int(holes_var.get())
    nine_type = nine_type_var.get()
    insert_hole_data(num_holes, nine_type)
    root.destroy()

ttk.Button(frame, text="Next", command=handle_next).grid(column=1, row=6, padx=10, pady=5)

hole_entries = []

def create_hole_input_fields(num_holes):
    global hole_entries
    hole_entries = []

    hole_detail_frame = ttk.Frame(root, padding="10")
    hole_detail_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    headers = ["Hole Number", "Par", "Fairways in Play", "Fairways Not in Play", "Greens in Regulation", "Greens Not in Regulation", "Putts", "Score"]
    for col, header in enumerate(headers):
        ttk.Label(hole_detail_frame, text=header).grid(row=0, column=col, padx=5, pady=5)

    for i in range(num_holes):
        row_entries = {
            'hole_number': ttk.Entry(hole_detail_frame, width=5),
            'par': ttk.Entry(hole_detail_frame, width=5),
            'fairways_in_play': ttk.Entry(hole_detail_frame, width=5),
            'fairways_not_in_play': ttk.Entry(hole_detail_frame, width=5),
            'greens_in_regulation': ttk.Entry(hole_detail_frame, width=5),
            'greens_not_in_regulation': ttk.Entry(hole_detail_frame, width=5),
            'putts': ttk.Entry(hole_detail_frame, width=5),
            'score': ttk.Entry(hole_detail_frame, width=5)
        }
        for col, key in enumerate(row_entries):
            row_entries[key].grid(row=i+1, column=col, padx=5, pady=5)
        hole_entries.append(row_entries)

    ttk.Button(hole_detail_frame, text="Submit", command=submit_and_exit).grid(row=num_holes+1, columnspan=8, padx=5, pady=5)

root.mainloop()

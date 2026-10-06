import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("Artist.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")

conn.commit()

#CREATE

def add_artist():

    artist_name = artist_name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    
    if artist_name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO artists (artist_name, age, genre) VALUES (?, ?, ?)",
        (artist_name, age, genre)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Artist added successfully."
    )

    clear_fields()
    display_artists()



#READ

def display_artists():

    for item in tree.get_children():
        tree.delete(item)

    cursor.execute(
        "SELECT * FROM artists"
    )

    artists = cursor.fetchall()

    for artist in artists:
        tree.insert("",tk.END, values=artist)

#UPDATE
def update_artist():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an artist to update."
        )
        return

    artist_id = tree.item(
        selected[0]
    )["values"][0]

    
    artist_name = artist_name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if artist_name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return
    try:
        age = int(age)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        """
        UPDATE artists
        SET artist_name = ?, age = ?, genre = ?
        WHERE id = ?
        """, (artist_name, age, genre, artist_id)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Artist updated successfully."
    )

    clear_fields()
    display_artists()

#DELETE
def delete_artist():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an artist to delete."
        )
        return

    artist_id = tree.item(
        selected[0]
    )["values"][0]
    
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this artist?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM artists WHERE id = ?",
            (artist_id,)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Artist deleted successfully."
        )

        clear_fields()
        display_artists()

#CLEAR INPUT FIELDS
def clear_fields():

    artist_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

# SELECT ARTIST
def select_artist(event):
    selected = tree.selection()

    if selected:
        artist = tree.item(selected[0])["values"]

        clear_fields()
        artist_name_entry.insert(0, artist[1])
        age_entry.insert(0, artist[2])
        genre_entry.insert(0, artist[3])



#EXIT PROGRAM
def exit_program():
    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )
    if confirm:
        conn.close()
        root.destroy()


# MAIN WINDOW
root = tk.Tk()
root.title(
    "Song Artist Information"
)
root.geometry(
    "750x550"
)

# COLORS
BG_COLOR = "#EAF4FB"
TITLE_COLOR = "#154360"
LABEL_COLOR = "#1F618D"
ENTRY_BG = "#FFFFFF"
ADD_COLOR = "#27AE60"
UPDATE_COLOR = "#F39C12"
DELETE_COLOR = "#E74C3C"
CLEAR_COLOR = "#7F8C8D"
EXIT_COLOR = "#34495E"
BUTTON_TEXT = "white"
root.configure(
    bg=BG_COLOR
)



# TITLE
title_label = tk.Label(
    root,
    text="Song Artist Information",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(
    pady=10
)



# INPUT FRAME

input_frame = tk.Frame(
    root,
    bg="white"
)
input_frame.pack(pady=10)



# ARTIST NAME

tk.Label(
    input_frame,
    text="Artist Name:",
    bg="white",
    fg=LABEL_COLOR,
    font=("Arial", 10, "bold")
).grid(row=0,column=0,padx=5,pady=5)

artist_name_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121"
)

artist_name_entry.grid(row=0,column=1,padx=5,pady=5)

# AGE
tk.Label(
    input_frame,
    text="Age:",
    bg="white",
    fg=LABEL_COLOR,
    font=("Arial", 10, "bold")
).grid(row=1,column=0,padx=5,pady=5)


age_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121"
)

age_entry.grid(row=1,column=1,padx=5,pady=5)


# GENRE

tk.Label(
    input_frame,
    text="Genre:",
    bg="white",
    fg=LABEL_COLOR,
    font=("Arial", 10, "bold")
).grid(row=2,column=0,padx=5,pady=5)


genre_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121"
)

genre_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


# BUTTON FRAME
button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(
    pady=10
)


# ADD BUTTON
tk.Button(
    button_frame,
    text="Add",
    width=10,
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#1E8449",
    activeforeground="white",
    command=add_artist
).grid(row=0,column=0,padx=5)

# UPDATE BUTTON

tk.Button(
    button_frame,
    text="Update",
    width=10,
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#D68910",
    activeforeground="white",
    command=update_artist
).grid(row=0,column=1,padx=5)


# DELETE BUTTON

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#C0392B",
    activeforeground="white",
    command=delete_artist
).grid(row=0,column=2,padx=5)

# CLEAR BUTTON
tk.Button(
    button_frame,
    text="Clear",
    width=10,
    bg=CLEAR_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#626567",
    activeforeground="white",
    command=clear_fields
).grid(row=0,column=3,padx=5)

# EXIT BUTTON
tk.Button(
    button_frame,
    text="Exit",
    width=10,
    bg=EXIT_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#212F3D",
    activeforeground="white",
    command=exit_program
).grid(row=0,column=4,padx=5)



# TREEVIEW STYLE
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview.Heading",
    background="#1F618D",
    foreground="white",
    font=("Arial", 10, "bold")
)


style.configure(
    "Treeview",
    background="white",
    foreground="#212121",
    fieldbackground="white",
    rowheight=30
)


style.map(
    "Treeview",
    background=[
        ("selected", "#5DADE2")
    ],
    foreground=[
        ("selected", "white")
    ]
)


# TABLE
tree = ttk.Treeview(
    root,
    columns=(
        "ID",
        "Artist Name",
        "Age",
        "Genre"
    ),
    show="headings"
)


#HEADINGS
tree.heading("ID", text="ID")
tree.heading("Artist Name", text="Artist Name")
tree.heading("Age", text="Age")
tree.heading("Genre", text="Genre")


#COLUMN WIDTHS
tree.column("ID", width=50)
tree.column("Artist Name", width=220)
tree.column("Age", width=80)
tree.column("Genre", width=180)

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

tree.bind(
    "<<TreeviewSelect>>",
    select_artist
)

display_artists()

root.mainloop()



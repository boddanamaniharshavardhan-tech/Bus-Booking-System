import sqlite3


conn = sqlite3.connect("bus_booking.db")
cursor = conn.cursor()

# Admin Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    route TEXT NOT NULL,
    travel_date TEXT NOT NULL,
    seats INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Default Admin
cursor.execute("""
INSERT OR IGNORE INTO admin(username,password)
VALUES('Harshavardhan','Harsha@1234')
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS routes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route TEXT,
    price INTEGER,
    time TEXT,
    seats INTEGER
)
""")

cursor.executemany("""
INSERT INTO routes(route, price, time, seats)
VALUES (?, ?, ?, ?)
""", [
    ("Hyderabad-Vizag", 850, "10:30 PM", 40),
    ("Pathapatnam-Srikakulam", 90, "2:15 PM", 30),
    ("Vizag-Hyderabad", 850, "9:00 PM", 40),
    ("Pathapatnam-Palakonda", 65, "4:00 PM", 40),
    ("Pathapatnam-Palakonda", 65, "9:00 AM", 40),
    ("Hyderabad-Visakhapatnam", 1800, "5:15 PM", 68),
    ("Tirupati-Chennai", 160, "10:00 PM", 68),
    ("Vijayawada-Bengaluru", 450, "5:00 AM", 68),
    ("Visakhapatnam-Rajahmundry", 530, "12:30 PM", 68)
])

conn.commit()
conn.close()

print("Routes added successfully.")

print("Database Created Successfully")
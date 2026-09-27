from flask import Flask, request, jsonify,render_template,redirect
from flask_cors import CORS
import sqlite3
from flask import send_file


app = Flask(__name__)
CORS(app)
 
# Booking status
booking_open = True

def get_db():
    conn = sqlite3.connect("bus_booking.db")
    conn.row_factory = sqlite3.Row
    return conn
# Bus data
bus_data = {
    "Hyderabad-Vizag": {
        "price": 850,
        "time": "10:30 PM",
        "seats": 40
    },
    "Pathapatnam-Srikakulam": {
        "price": 90,
        "time": "2:15 PM",
        "seats": 30
    },
    "Vizag-Hyderabad": {
        "price": 850,
        "time": "9:00 PM",
        "seats": 40
    },
    "Pathapatnam-palakonda":{
        "price":65,
        "time":"4:00 PM",
        "seats":40
    },
    "Pathapatnam-palakonda":{
        "price":65,
        "time":"9:00 AM",
        "seats":40
    },
    "Hyderabad-Visakhapatnam":{
        "price":1800,
        "time":"5:15 PM",
        "seats":68
    },
    "Tirupati-Chennai":{
        "price":160,
        "time":"10:00 PM",
        "seats":68
        
    },
    "Vijayawada-Bengaluru":{
        "price":450,
        "time":"5:00 AM",
        "seats":68
    },
    "Visakhapatnam-Rajahmundry":{
        "price":530,
        "time":"12:30 PM",
        "seats":68
    }
}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        conn=get_db()

        admin=conn.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        conn.close()

        if admin:

            return redirect("/dashboard")

        else:

            return render_template(
                "login.html",
                message="Invalid Username or Password"
            )

    return render_template("login.html")


@app.route("/book", methods=["POST"])
def book():

    data=request.get_json()

    amount=int(data["seats"])*500

    conn=get_db()

    conn.execute("""

    INSERT INTO bookings(

    passenger_name,

    phone,

    route,

    travel_date,

    seats,

    amount

    )

    VALUES(?,?,?,?,?,?)

    """,(

    data["name"],

    data["phone"],

    data["route"],

    data["date"],

    data["seats"],

    amount

    ))

    conn.commit()

    conn.close()

    return {"success":True}
 
@app.route("/dashboard")
def dashboard():

    conn=get_db()

    total=conn.execute(

    "SELECT COUNT(*) FROM bookings"

    ).fetchone()[0]

    revenue=conn.execute(

    "SELECT IFNULL(SUM(amount),0) FROM bookings"

    ).fetchone()[0]

    bookings=conn.execute(

    "SELECT * FROM bookings ORDER BY id DESC LIMIT 10"

    ).fetchall()

    today = conn.execute("""

    SELECT COUNT(*)

    FROM bookings

    WHERE DATE(booking_time)=DATE('now')

    """).fetchone()[0]

    conn.close()

    return render_template(

    "dashboard.html",

    total=total,

    today=today,

    revenue=revenue,

    bookings=bookings

    )

@app.route("/delete/<int:id>")
def delete(id):

    conn=get_db()

    conn.execute(

    "DELETE FROM bookings WHERE id=?",

    (id,)

    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")
#============================ ROUTES===========================#
@app.route("/bookings")
def bookings_page():

    conn = get_db()

    bookings = conn.execute(
        "SELECT * FROM bookings ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "bookings.html",
        bookings=bookings
    )


@app.route("/routes")
def routes():

    conn = get_db()

    routes = conn.execute(
        "SELECT * FROM routes"
    ).fetchall()

    conn.close()

    return render_template(
        "routes.html",
        routes=routes
    )
@app.route("/add_route", methods=["POST"])
def add_route():

    route = request.form["route"]
    price = request.form["price"]
    time = request.form["time"]
    seats = request.form["seats"]

    conn = get_db()

    conn.execute(
        "INSERT INTO routes(route,price,time,seats) VALUES(?,?,?,?)",
        (route, price, time, seats)
    )

    conn.commit()
    conn.close()

    return redirect("/routes")
@app.route("/delete_route/<int:id>")
def delete_route(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM routes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/routes")

@app.route("/reports")
def reports():

    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM bookings"
    ).fetchone()[0]

    revenue = conn.execute(
        "SELECT IFNULL(SUM(amount),0) FROM bookings"
    ).fetchone()[0]

    today = conn.execute(
        "SELECT COUNT(*) FROM bookings WHERE DATE(booking_time)=DATE('now')"
    ).fetchone()[0]

    routes = conn.execute(
        "SELECT COUNT(*) FROM routes"
    ).fetchone()[0]

    bookings = conn.execute(
        "SELECT * FROM bookings ORDER BY id DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return render_template(
        "reports.html",
        total=total,
        revenue=revenue,
        today=today,
        routes=routes,
        bookings=bookings
    )

@app.route("/change_password",methods=["POST"])
def change_password():

    username=request.form["username"]
    old=request.form["old_password"]
    new=request.form["new_password"]

    conn=get_db()

    admin=conn.execute(

    "SELECT * FROM admin WHERE username=? AND password=?",

    (username,old)

    ).fetchone()

    if admin:

        conn.execute(

        "UPDATE admin SET password=? WHERE username=?",

        (new,username)

        )

        conn.commit()

    conn.close()

    return redirect("/settings")
@app.route("/reset_bookings")
def reset_bookings():

    conn=get_db()

    conn.execute("DELETE FROM bookings")

    conn.commit()

    conn.close()

    return redirect("/settings")

@app.route("/backup")
def backup():

    return send_file(

        "bus_booking.db",

        as_attachment=True

    )


@app.route("/settings")
def settings():

    return render_template("settings.html")

@app.route("/logout")
def logout():

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
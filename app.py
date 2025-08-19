from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DB_NAME = "tickets.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        movie TEXT NOT NULL,
        seats INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Home Page with Buttons
@app.route("/")
def home():
    return render_template_string("""
        <h1>🎟️ Welcome to Simple Ticket Booking App!</h1>
        <a href="/book_form"><button>Book a Ticket</button></a>
        <a href="/bookings"><button>View All Bookings</button></a>
    """)

# Booking Form (UI)
@app.route("/book_form")
def book_form():
    return render_template_string("""
        <h2>Book Your Ticket</h2>
        <form action="/book" method="post">
            Name: <input type="text" name="name" required><br><br>
            Movie: <input type="text" name="movie" required><br><br>
            Seats: <input type="number" name="seats" min="1" required><br><br>
            <button type="submit">Book Ticket</button>
        </form>
        <br>
        <a href="/"><button>Back to Home</button></a>
    """)

# Book Ticket (Form + API)
@app.route("/book", methods=["POST"])
def book_ticket():
    # Check if coming from form
    if request.form:
        name = request.form.get("name")
        movie = request.form.get("movie")
        seats = request.form.get("seats")
    else:  # JSON request
        data = request.json
        name = data.get("name")
        movie = data.get("movie")
        seats = data.get("seats")

    if not name or not movie or not seats:
        return jsonify({"error": "Missing fields"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (name, movie, seats) VALUES (?, ?, ?)", (name, movie, seats))
    conn.commit()
    conn.close()

    return render_template_string("""
        <h2>✅ Booking Successful!</h2>
        <a href="/"><button>Home</button></a>
        <a href="/book_form"><button>Book Another</button></a>
        <a href="/bookings"><button>View Bookings</button></a>
    """)

# View All Bookings
@app.route("/bookings", methods=["GET"])
def get_bookings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    conn.close()

    bookings = [{"id": r[0], "name": r[1], "movie": r[2], "seats": r[3]} for r in rows]

    # Render as HTML Table
    html = """
        <h2>🎟️ All Bookings</h2>
        <table border="1" cellpadding="5">
            <tr><th>ID</th><th>Name</th><th>Movie</th><th>Seats</th></tr>
    """
    for b in bookings:
        html += f"<tr><td>{b['id']}</td><td>{b['name']}</td><td>{b['movie']}</td><td>{b['seats']}</td></tr>"
    html += "</table><br>"
    html += '<a href="/"><button>Home</button></a>'
    html += '<a href="/book_form"><button>Book Ticket</button></a>'
    return html


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)

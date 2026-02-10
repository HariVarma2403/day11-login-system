from flask import Flask, request, jsonify, render_template
import json
import os
import re

app = Flask(__name__)

USERS_FILE = "users.json"

# ---------------- HELPER FUNCTIONS ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")

    # VALIDATIONS
    if len(username) < 4:
        return jsonify({"error": "Username must be at least 4 characters"}), 400

    if not email.endswith("@gmail.com"):
        return jsonify({"error": "Email must end with @gmail.com"}), 400

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Phone must be 10 digits"}), 400

    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*]", password):
        return jsonify({"error": "Password must include letter, number & symbol"}), 400

    users = load_users()

    if any(u["email"] == email for u in users):
        return jsonify({"error": "User already exists"}), 400

    users.append({
        "username": username,
        "email": email,
        "phone": phone,
        "password": password   # (hash later)
    })

    save_users(users)

    return jsonify({"message": "Registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)

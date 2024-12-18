import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, allowing cross-origin requests

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'BROTHER'
}

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table():
    """Create the emails table if it doesn't exist."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
            CREATE TABLE IF NOT EXISTS emails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(query)
            connection.commit()
            print("Table 'emails' is ready.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_email(email):
    """Insert an email into the database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = "INSERT INTO emails (email) VALUES (%s)"
            cursor.execute(query, (email,))
            connection.commit()
            print(f"Email '{email}' inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/servercheck', methods=['GET'])
def servercheck():
    """Health check endpoint to verify server status."""
    print("Server is running...")
    return jsonify({"message": "Server is running", "status": "success"}), 200

@app.route('/submit_email', methods=['POST'])
def submit_email():
    """Handle email submission."""
    try:
        data = request.get_json()  # Get JSON data from the request body
        email = data.get('email')  # Retrieve the email from the JSON

        if email:
            insert_email(email)
            return jsonify({"message": "Email submitted successfully!"}), 200
        else:
            return jsonify({"message": "Please provide a valid email."}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to process the request."}), 500

if __name__ == '__main__':
    create_table()  # Ensure the table exists
    app.run(debug=True, host='127.0.0.1', port=5001)

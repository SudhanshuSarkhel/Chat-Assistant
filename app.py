from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    return sqlite3.connect('employees.db')

# Function to execute a query and fetch results
def execute_query(query, params=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    results = cursor.fetchall()
    conn.close()
    return results

# Function to handle queries
def handle_query(query):
    # Query 1: Show all employees in a department
    match = re.match(r"show me all employees in the (\w+) department", query, re.IGNORECASE)
    if match:
        department = match.group(1).capitalize()
        query = "SELECT * FROM Employees WHERE Department = ?"
        results = execute_query(query, (department,))
        if results:
            return "\n".join([f"ID: {row[0]}, Name: {row[1]}, Salary: {row[3]}, Hire Date: {row[4]}" for row in results])
        return "No employees found in that department."

    # Query 2: Who is the manager of a department
    match = re.match(r"who is the manager of the (\w+) department", query, re.IGNORECASE)
    if match:
        department = match.group(1).capitalize()
        query = "SELECT Manager FROM Departments WHERE Name = ?"
        results = execute_query(query, (department,))
        if results:
            return f"The manager of the {department} department is {results[0][0]}."
        return "No manager found for that department."

    # Query 3: List all employees hired after a date
    match = re.match(r"list all employees hired after (\d{4}-\d{2}-\d{2})", query, re.IGNORECASE)
    if match:
        hire_date = match.group(1)
        query = "SELECT * FROM Employees WHERE Hire_Date > ?"
        results = execute_query(query, (hire_date,))
        if results:
            return "\n".join([f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Salary: {row[3]}" for row in results])
        return "No employees found hired after that date."

    # Query 4: Total salary expense for a department
    match = re.match(r"what is the total salary expense for the (\w+) department", query, re.IGNORECASE)
    if match:
        department = match.group(1).capitalize()
        query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
        results = execute_query(query, (department,))
        if results:
            return f"The total salary expense for the {department} department is {results[0][0]}."
        return "No salary data found for that department."

    # Default response if no matching query
    return "Sorry, I didn't understand that query."

# Define the home route to interact with the assistant
@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        query = request.form['query']
        response = handle_query(query)
        return jsonify({"response": response})
    return '''
        <form method="post">
            Query: <input type="text" name="query">
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is secret to protect the session

# Sample users (Replace with actual database or persistent storage)
users = {
    "student@example.com": generate_password_hash("password123"),
    "admin@example.com": generate_password_hash("adminpassword")
}

@app.route('/')
def home():
    # Check if user is logged in
    if 'user' in session:
        return redirect(url_for('internships'))
    return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login page
    
    user = session['user']
    # Admin-specific logic (e.g., checking if the user is admin)
    if user != "admin@example.com":  # Example: If the logged-in user is not an admin
        return redirect(url_for('internships'))  # Redirect to the internships page if not admin

    # Render the admin dashboard page if the user is an admin
    return render_template('admin_dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Sample users dictionary, replace with actual user storage (e.g., database)
        users = {
            "student@example.com": generate_password_hash("password123"),
            "admin@example.com": generate_password_hash("adminpassword")
        }

        if email in users and check_password_hash(users[email], password):
            session['user'] = email  # Store user in session
            flash("Login successful!", "success")
            return redirect(url_for('internships'))  # Redirect to internships page
        else:
            flash("Invalid login credentials", "danger")
    
    return render_template('login.html')  # Return login form if GET request

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm password match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))
        
        # Check if email is already in use
        if email in users:
            flash("Email is already registered!", "danger")
            return redirect(url_for('register'))

        # Hash the password and store the user
        users[email] = generate_password_hash(password)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')  # Render the registration form


@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash("You have been logged out", "info")
    return redirect(url_for('home'))

@app.route('/apply/<int:internship_id>', methods=['POST'])
def apply(internship_id):
    if 'user' not in session:
        flash("You must be logged in to apply", "warning")
        return redirect(url_for('login'))
    
    # Mock list of internships
    internships = [
        {"id": 1, "title": "Software Engineer Intern", "company": "TechCorp", "location": "Remote"},
        {"id": 2, "title": "Marketing Intern", "company": "MarketPro", "location": "New York"}
    ]
    
    # Get the internship being applied for
    internship = next((i for i in internships if i['id'] == internship_id), None)
    
    if internship:
        # You can store the application in a real database
        flash(f"You have successfully applied for {internship['title']}!", "success")
    else:
        flash("Internship not found", "danger")
    
    return redirect(url_for('internships'))  # Redirect back to internships page

# Route to show the list of internships

@app.route('/internships')
def internships():
    try:
        # Check if user is logged in
        if 'user' not in session:
            flash("You must be logged in to view internships", "warning")
            return redirect(url_for('login'))  # Redirect to login if user is not logged in

        # Internship data (this can be replaced with actual data fetching from a database)
        internships = [
            {"id": 1,"title": "Software Engineer Intern", "company": "TechCorp", "location": "Remote"},
            {"id": 2,"title": "Marketing Intern", "company": "MarketPro", "location": "New York"}
        ]
        print(internships)

        # Render the internships page with the internship data
        return render_template('internships.html', internships=internships)
    
    except Exception as e:
        # Log the error and return a generic 500 error page
        print(f"Error: {e}")
        flash("An error occurred while loading the internships page.", "danger")
        return render_template('error.html')  # This could be a custom error page (you can create one)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Define severity levels
SEVERITY_LEVELS = ['Critical', 'High', 'Medium', 'Low']

# Define keywords for category prediction
CATEGORY_KEYWORDS = {
    'Network': ['network', 'internet', 'server', 'connection', 'down'],
    'Hardware': ['hardware', 'device', 'machine', 'laptop', 'printer', 'broken'],
    'Software': ['software', 'app', 'program', 'crash', 'bug', 'error'],
    'Security': ['security', 'hack', 'breach', 'virus', 'malware', 'attack'],
    'Performance': ['performance', 'slow', 'lag', 'delay', 'unresponsive'],
    'Others': ['others', 'miscellaneous']
}

# Initialize Flask app and database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
db = SQLAlchemy(app)

# Define the Incident model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    assigned_to = db.Column(db.String(255))
    time_reported = db.Column(db.DateTime, default=datetime.utcnow)
    time_resolved = db.Column(db.DateTime)

# Home route to display the most recent incident
@app.route('/')
def home():
    # Retrieve the most recent incident
    latest_incident = Incident.query.order_by(Incident.id.desc()).first()
    return render_template('index.html', incident=latest_incident)

# Function to automatically categorize incidents based on description
def categorize_incident(description):
    description = description.lower()  # Convert to lowercase to make it case-insensitive
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description:
                print(f"Category: {category}, Keyword Matched: {keyword}")  # Debugging output
                return category
    return 'Others'  # Default category if no match found

# Route to handle incident submission
@app.route('/submit', methods=['POST'])
def submit_incident():
    title = request.form['incident_title']
    description = request.form['incident_description']
    severity = request.form['severity']
    assigned_to = request.form['assigned_engineer']
    status = request.form['status']

    # Automatically determine category based on description
    category = categorize_incident(description)

    new_incident = Incident(
        title=title,
        description=description,
        category=category,  # Set the automatically determined category
        severity=severity,
        status=status,
        assigned_to=assigned_to
    )

    # Add the new incident to the database
    db.session.add(new_incident)
    db.session.commit()

    # Redirect back to home page after submission
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()  # This will create the tables, including 'incident'

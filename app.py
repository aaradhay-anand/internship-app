from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLAlchemy: Use DATABASE_URL if set, otherwise fallback to a local SQLite file.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///internships.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Internship model.
class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Internship {self.title}>'

# Create the database tables if they don't exist.
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    internships = Internship.query.all()
    return render_template('index.html', internships=internships)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        company = request.form.get('company')
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        internship = Internship(company=company, title=title, description=description, location=location)
        db.session.add(internship)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html')

@app.route('/internship/<int:internship_id>')
def internship_detail(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    return render_template('internship.html', internship=internship)

if __name__ == '__main__':
    app.run(debug=True)

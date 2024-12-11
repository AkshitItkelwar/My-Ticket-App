from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# Database model for tickets
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Home route
@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

# Route for booking tickets
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_name = request.form['event_name']
        quantity = request.form['quantity']

        if not name or not email or not event_name or not quantity:
            flash('All fields are required!', 'danger')
            return redirect(url_for('book'))

        ticket = Ticket(name=name, email=email, event_name=event_name, quantity=int(quantity))
        db.session.add(ticket)
        db.session.commit()

        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('book.html')

# Route for deleting tickets
@app.route('/delete/<int:id>')
def delete(id):
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('index'))

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

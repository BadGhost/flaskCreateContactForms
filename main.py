###############################################
#          Import some packages               #
###############################################
from flask import Flask, render_template, request, jsonify
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
from os import environ

###############################################
#          Define flask app                   #
###############################################
app = Flask(__name__)
app.secret_key = 'dev fao football app'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


###############################################
#       Render Contact page                   #
###############################################

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)
    def __repr__(self):
        return f'<Contact {self.name}>'

# Create tables
with app.app_context():
  db.create_all()

# Route to render the contact page
@app.route('/contactus', methods=["GET", "POST"])
def get_contact():
    form = ContactForm()
    
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        try:
            # Create a Contact instance and add it to the database
            contact = Contact(name=name, email=email, subject=subject, message=message)
            db.session.add(contact)
            db.session.commit()
            return render_template('contact.html', form=form)
        except Exception as e:
             # Handle the database insertion error and return a 500 Internal Server Error
            db.session.rollback()
            app.logger.error(f"Error inserting into the database: {e}")
            return jsonify(error=str(e)), 500
        
    return render_template('contact.html', form=form)


###############################################
#                Run app                      #
###############################################
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
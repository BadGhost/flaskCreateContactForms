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

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)

@app.route('/contactus', methods=["GET", "POST"])
def get_contact():
    form = ContactForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        try:
            # Create a ContactMessage instance and add it to the database
            contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
            db.session.add(contact_message)
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
    db.create_all()  # Create the database tables
    app.run(debug=True, host='0.0.0.0', port=4000)
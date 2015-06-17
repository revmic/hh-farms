from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import Form
from flask.ext.mail import Message, Mail
from wtforms import TextField, TextAreaField, SubmitField, validators
from wtforms.validators import Required

from config import *

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mhilema@gmail.com'
app.config['MAIL_PASSWORD'] = '8qar9wor'
# mail.init_app(app)
app.config['SECRET_KEY'] = SECRET_KEY


""" VIEWS """
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html')


@app.route('/hopcam')
def hopcam():
    return render_template('hopcam.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            send_email("Inquiry", "inquiry")
        except Exception as e:
            print(e)
            flash("Something went wrong while sending your message. "
                  "Please email info@hh-farms.com with your question. "
                  "And if you're feeling generous with your time, "
                  "send us a message about this error. "
                  "Sorry about this!", "error")
        else:
            flash("Your message was sent successfully. "
                  "I'll get back to you soon!", "success")
        return redirect(url_for('contact'))

    return render_template("contact.html", title='Contact', form=form)


""" FORMS """
class ContactForm(Form):
    name = TextField('Name', validators=[Required(message="Required")])
    email = TextField('Email', validators=[
        Required(message="Email required"), validators.Email()])
    phone = TextField('Phone Number')
    body = TextAreaField('Message', validators=[Required()])
    send = SubmitField('Send')


""" MODELS """


""" HELPERS """
def send_email(subject, template, **kwargs):
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mhilema@gmail.com'
    MAIL_PASSWORD = '8qar9wor'

    msg = Message('[HH-Farms] ' + subject,
                  sender='mhilema@gmail.com',
                  recipients=['mhilema@gmail.com'])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', form=ContactForm(), **kwargs)
    mail.send(msg)


if __name__ == '__main__':
    app.run(port=5002, debug=True)

from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators
from wtforms.validators import Required

from config import *

app = Flask(__name__)
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
        flash("Email send action", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


""" FORMS """
class ContactForm(Form):
    name = TextField('Name', validators=[Required(message="Required")])
    email = TextField('Email', validators=[
        Required(message="Email required"), validators.Email()])
    phone = TextField('Phone Number')
    body = TextAreaField('Message', validators=[Required()])
    send = SubmitField('Send')


""" MODELS """


if __name__ == '__main__':
    app.run(port=5002, debug=True)

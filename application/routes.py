from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from application import app, db
from application.models import Contact
from application.scripts_riotapi import two_players_search, collapsed_table_info
from application.forms import RegistrationForm, LoginForm


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    contact = Contact(webpage=request.full_path, description=request.form.get('description'), submit_time=datetime.utcnow())
    db.session.add(contact)
    db.session.commit()
    flash('Your message has been sent', "success")
    return redirect(url_for("home"))


@app.route("/search_result", methods=['POST', 'GET'])
def search_result():
    if request.method == 'GET':
        return f"The URL /search_result is accessed directly. Try going to '/home' to submit form"
    if request.method == "POST":
        player1 = request.form.get("player1")
        player2 = request.form.get("player2")
        region = request.form.get("region")
        all_info = {}
        for match in two_players_search(player1, player2, region):
            for match_id in match:
                all_info[match_id] = collapsed_table_info(player1, region, match_id)
        return render_template('search_result.html', title='search_result', player1=player1,
                               player2=player2, region=region, data=all_info)

    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods={'GET', 'POST'})
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gromps.com' and form.password.data == 'password':
            flash('You have been logged in as admin!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/test", methods=['GET', 'POST'])
def test():
    return render_template('test.html')



from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from application import app, db
from application.models import Contact
from application.scripts_riotapi import two_players_search, collapsed_table_info
from application.forms import RegistrationForm, LoginForm

@app.route("/contact", methods=['GET'])
def contact():
    contact = Contact(
        webpage=request.full_path,
        description=request.form.get('description'),
        submit_time=datetime.utcnow()
        )
    db.session.add(contact)
    db.session.commit()
    flash('Your message has been sent', "success")
    return redirect(url_for("search"))


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
        return render_template(
            'search_result.html',
            title='Search result',
            player1=player1,
            player2=player2,
            region=region,
            data=all_info
            )
    return render_template('search.html')


@app.route("/")
@app.route("/home")
@app.route("/search_two_players")
def search():
    return render_template('search.html', title='Search two players')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/pro_search")
def pro_search():
    return render_template('prosearch.html', title='Search Pro')


@app.route("/pro_search_result",  methods=['POST', 'GET'])
def pro_search_result():
    if request.method == 'GET':
        return f"The URL /pro_search_result is accessed directly. Try going to '/pro_search' to submit form"
    if request.method == "POST":
        player1 = request.form.get("player1")

        region = request.form.get("region")
        all_info = {}
        for match in two_players_search(player1, player2, region):
            for match_id in match:
                all_info[match_id] = collapsed_table_info(player1, region, match_id)
        return render_template(
            'pro_search_result.html',
            title='Pro search result',
            player1=player1,
            player2=player2, 
            region=region,
            data=all_info
            )

    return render_template('pro_search.html')


@app.route("/test")
def test():
    return render_template('test.html')



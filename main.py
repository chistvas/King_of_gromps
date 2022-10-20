from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from scripts_riotapi import two_players_search, get_all_players_list_stats, collapsed_table_info
from scripts_riotapi import kda

app = Flask(__name__)


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
                all_info[match_id] = get_all_players_list_stats(region, match_id, kda)
        return render_template('search_result.html', title='search_result', player1=player1,
                               player2=player2, region=region, all_info=all_info)

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
    region = "euw1"
    player1 = "metalonot"
    player2 = "Karini"
    all_info = {}
    for match in two_players_search(player1, player2, region):
        for match_id in match:
            all_info[match_id] = collapsed_table_info(player1, player2, region)
    return render_template('test.html', data=all_info)

# @app.route("/search_result", methods={'GET', 'POST'})
# def search_result():
#     return render_template('search_result.html', title='search_result')


if __name__ == "__main__":
    app.run(debug=True)

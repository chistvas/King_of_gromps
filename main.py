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
    # player1 = "StePanzer"
    # player2 = "MrNoct"
    region= "ru"
    all_info = {'RU_414497367': {'championName': 'Malphite', 'win': 'Defeat', 'kda': '2, 13, 6', 'items': [3041, 3102, 2055], 'left_side_prt': ['Андрей Поддержка', 'MrNoct', 'ArsadoX', 'Тильтхен', 'StePanzer'], 'right_side_prt': ['kolopak', 'FluffyCheshire', 'Neltarionko', 'ragnar1329', 'Hluix']}, 'RU_414489695': {'championName': 'Irelia', 'win': 'Victory', 'kda': '11, 5, 8', 'items': [3153, 6333, 3047, 3110, 1033, 6630], 'left_side_prt': ['UkPaTuTeJLb', 'KOLYASIIIKK', 'penzil', 'Семпай Хентай', 
'InanityS'], 'right_side_prt': ['StePanzer', 'MrNoct', 'ArsadoX', 'Андрей Поддержка', 'Тильтхен']}, 'RU_414484603': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '16, 2, 8', 'items': [1055, 3111, 6694, 1036, 3065, 6630], 'left_side_prt': ['StepanRed12', 'Братишка Мурад', 'llPROFFESSORll', 'Malkarn', 'Настя Свитер'], 
'right_side_prt': ['StePanzer', 'MrNoct', 'Bald brother', 'FZN Chow', 'Mellivõra']}, 'RU_414479230': {'championName': 'KogMaw', 'win': 'Defeat', 'kda': '2, 7, 4', 'items': [1055, 3153, 3124, 3006, 6670, 1018], 'left_side_prt': ['ГуБиТеЛьПiВа', 'MrNoct', 'MrTEP', 'StePanzer', 'Orcha'], 'right_side_prt': ['Jangiriko', 'The Real Yoshi', 'НАТАХТАРИ ', 'AltGaminG', 'Йой Най Буде']}, 'RU_414476418': {'championName': 'Ornn', 'win': 'Victory', 'kda': '1, 0, 0', 'items': [1054], 'left_side_prt': ['Nyorikenoichi', 'DORLL', 'Taskinsam', 'EDATH13', 'Кастрюля'], 'right_side_prt': ['StePanzer', 'MrNoct', 'hidemovement', 'Fеnrisulfr', 'Счастьице']}, 'RU_414064349': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '13, 6, 11', 'items': [3065, 3047, 6694, 3071, 6630], 'left_side_prt': ['StePanzer', 'MrNoct', 'dogorad', 'LesbianFanboy', 'SirExtraSex'], 'right_side_prt': ['FLAWxxxLE55', 'ВкругуКретинов', 'Gmeer', 'Disciple', 'CYBERDEDOK']}, 'RU_413920971': {'championName': 
'Aatrox', 'win': 'Victory', 'kda': '10, 8, 7', 'items': [3047, 3153, 6632, 3075, 3211], 'left_side_prt': ['Kastie', 'Живой ', 'dgeims', 'Black Mamba', 'Absolute'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Распутный Тёма ', 'pbIk', 'Бойчик']}, 'RU_413659735': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '11, 6, 4', 
'items': [6333, 6694, 3047, 3044, 1037, 6630], 'left_side_prt': ['AkaliJustShadow', 'БезголовыйДжек', 'SHS Regenaild', 'LOLER123234', 'Dramamotic'], 'right_side_prt': ['StePanzer', 'not your Gоd', 'Clown Pepega ', 'RusSsk1i', 'MrNoct']}, 'RU_413334510': {'championName': 'Yorick', 'win': 'Victory', 'kda': '4, 5, 2', 'items': [6694, 6692, 3009, 3071, 3181], 'left_side_prt': ['StePanzer', 'MrNoct', 'Люблю Поезда', 'imaglacial', 'Buccelatti'], 'right_side_prt': ['Shaclоne', 'RavenoZoro', 'Vovinio', 'Holovachlena', 'Caring egoist']}, 'RU_413331187': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '6, 6, 7', 'items': [6333, 6694, 3111, 4401, 
6693], 'left_side_prt': ['MeldyE', 'BlаckMооn', 'AoAndoN', 'lMeatxboyl', 'creek5'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Прaид', 'joij', 'kolley']}, 'RU_413326449': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '2, 9, 4', 'items': [1054, 3047, 6333, 3067, 3133, 6630], 'left_side_prt': ['Rost1slav999', 'ПРОЕКТ Каин', 'Capitan Permach', 'Андрюха М16', 'RelictForm'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Wave of  Sound', 'WraithFn', 'TetraziklinE']}}
    # for match in two_players_search(player1, player2, region):
    #     for match_id in match:
    #         all_info[match_id] = collapsed_table_info(player1, region, match_id)
    return render_template('test.html', data=all_info, region=region)



if __name__ == "__main__":
    app.run(debug=True)

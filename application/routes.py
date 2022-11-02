from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from application import app, db
from application.models import Contact
from application.scripts_riotapi import two_players_search, collapsed_table_info
from application.forms import RegistrationForm, LoginForm, ContactForm


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
    # player1 = "StePanzer"
    # player2 = "MrNoct"
    region= "ru"
    all_info = {'RU_414497367': {'championName': 'Malphite', 'win': 'Defeat', 'kda': '2, 13, 6', 'items': [3041, 3102, 2055], 'left_side_prt': {'Андрей Поддержка': 'Darius', 'MrNoct': 'Viego', 'ArsadoX': 'Aphelios', 'Тильтхен': 'Draven', 'StePanzer': 'Malphite'}, 'right_side_prt': {'kolopak': 'Aatrox', 'FluffyCheshire': 'Nautilus', 'Neltarionko': 'AurelionSol', 'ragnar1329': 'Lucian', 'Hluix': 'Blitzcrank'}}, 'RU_414489695': {'championName': 'Irelia', 'win': 'Victory', 'kda': '11, 5, 8', 'items': [3153, 6333, 3047, 3110, 1033, 6630], 'left_side_prt': {'UkPaTuTeJLb': 'Yone', 'KOLYASIIIKK': 'Shaco', 'penzil': 'Garen', 'Семпай Хентай': 'Jinx', 'InanityS': 'Xerath'}, 'right_side_prt': {'StePanzer': 'Irelia', 'MrNoct': 'Shyvana', 'ArsadoX': 'Aphelios', 'Андрей Поддержка': 'Draven', 'Тильтхен': 'Bard'}}, 'RU_414484603': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '16, 2, 8', 'items': [1055, 3111, 6694, 1036, 3065, 6630], 'left_side_prt': {'StepanRed12': 'Kayle', 'Братишка Мурад': 'Nautilus', 'llPROFFESSORll': 'Lux', 'Malkarn': 'Varus', 'Настя Свитер': 'Soraka'}, 'right_side_prt': {'StePanzer': 'Aatrox', 'MrNoct': 'FiddleSticks', 
'Bald brother': 'Zed', 'FZN Chow': 'Caitlyn', 'Mellivõra': 'Yuumi'}}, 'RU_414479230': {'championName': 'KogMaw', 'win': 'Defeat', 'kda': '2, 7, 4', 'items': [1055, 3153, 3124, 3006, 6670, 1018], 'left_side_prt': {'ГуБиТеЛьПiВа': 'Yone', 'MrNoct': 'FiddleSticks', 'MrTEP': 'Katarina', 'StePanzer': 'KogMaw', 'Orcha': 'Zyra'}, 'right_side_prt': {'Jangiriko': 'Sion', 'The Real Yoshi': 'Maokai', 'НАТАХТАРИ ': 'Galio', 'AltGaminG': 'Jhin', 'Йой Най Буде': 'Senna'}}, 'RU_414476418': {'championName': 'Ornn', 'win': 'Victory', 'kda': '1, 0, 0', 'items': [1054], 'left_side_prt': {'Nyorikenoichi': 'Sion', 'DORLL': 'Graves', 'Taskinsam': 'Vladimir', 'EDATH13': 'Nilah', 'Кастрюля': 'Morgana'}, 'right_side_prt': {'StePanzer': 'Ornn', 'MrNoct': 'FiddleSticks', 'hidemovement': 'Gangplank', 'Fеnrisulfr': 'Lucian', 'Счастьице': 'Nami'}}, 'RU_414064349': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '13, 6, 11', 'items': [3065, 3047, 6694, 3071, 6630], 'left_side_prt': {'StePanzer': 'Aatrox', 'MrNoct': 'FiddleSticks', 'dogorad': 'Fizz', 'LesbianFanboy': 'Jhin', 'SirExtraSex': 'Alistar'}, 'right_side_prt': {'FLAWxxxLE55': 'Riven', 
'ВкругуКретинов': 'Shaco', 'Gmeer': 'Lux', 'Disciple': 'MissFortune', 'CYBERDEDOK': 'Nami'}}, 'RU_413920971': {'championName': 'Aatrox', 'win': 'Victory', 'kda': 
'10, 8, 7', 'items': [3047, 3153, 6632, 3075, 3211], 'left_side_prt': {'Kastie': 'Kled', 'Живой ': 'Evelynn', 'dgeims': 'Yasuo', 'Black Mamba': 'Twitch', 'Absolute': 'Lux'}, 'right_side_prt': {'StePanzer': 'Aatrox', 'MrNoct': 'FiddleSticks', 'Распутный Тёма ': 'Sylas', 'pbIk': 'Caitlyn', 'Бойчик': 'Soraka'}}, 'RU_413659735': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '11, 6, 4', 'items': [6333, 6694, 3047, 3044, 1037, 6630], 'left_side_prt': {'AkaliJustShadow': 'Akali', 'БезголовыйДжек': 'Ekko', 'SHS Regenaild': 'Zed', 'LOLER123234': 'Yasuo', 'Dramamotic': 'MonkeyKing'}, 'right_side_prt': {'StePanzer': 'Aatrox', 'not your Gоd': 'Lillia', 'Clown Pepega ': 'Yone', 'RusSsk1i': 'Kaisa', 'MrNoct': 'Morgana'}}, 'RU_413334510': {'championName': 'Yorick', 'win': 'Victory', 'kda': '4, 5, 2', 'items': [6694, 6692, 3009, 3071, 3181], 'left_side_prt': {'StePanzer': 'Yorick', 'MrNoct': 'Lillia', 'Люблю Поезда': 'Annie', 'imaglacial': 'MissFortune', 'Buccelatti': 
'Soraka'}, 'right_side_prt': {'Shaclоne': 'Gangplank', 'RavenoZoro': 'Diana', 'Vovinio': 'Yasuo', 'Holovachlena': 'Draven', 'Caring egoist': 'Blitzcrank'}}, 'RU_413331187': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '6, 6, 7', 'items': [6333, 6694, 3111, 4401, 6693], 'left_side_prt': {'MeldyE': 'Malphite', 'BlаckMооn': 'Diana', 'AoAndoN': 'Syndra', 'lMeatxboyl': 'Kaisa', 'creek5': 'Lux'}, 'right_side_prt': {'StePanzer': 'Aatrox', 'MrNoct': 'Lillia', 'Прaид': 'Kassadin', 'joij': 'Ashe', 'kolley': 'Lulu'}}, 'RU_413326449': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '2, 9, 4', 'items': [1054, 3047, 6333, 3067, 3133, 6630], 'left_side_prt': {'Rost1slav999': 'Urgot', 'ПРОЕКТ Каин': 'Kayn', 'Capitan Permach': 'Cassiopeia', 'Андрюха М16': 'Jinx', 'RelictForm': 'Lux'}, 'right_side_prt': {'StePanzer': 'Aatrox', 'MrNoct': 'Diana', 'Wave of  Sound': 'Ahri', 'WraithFn': 'Tristana', 'TetraziklinE': 'Braum'}}}
    # for match in two_players_search(player1, player2, region):
    #     for match_id in match:
    #         all_info[match_id] = collapsed_table_info(player1, region, match_id)
    return render_template('test.html', data=all_info, region=region)



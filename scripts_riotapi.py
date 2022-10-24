from riotwatcher import LolWatcher
import time

key = "RGAPI-fff42a3e-8118-4e18-91fb-2466d1ccea30"
kda = ["kills", "deaths", "assists"]
table_stats = ["championName", "win"]


def my_timer(orig_func):
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f"Function {orig_func} ran in: {t2} sec")
        return result

    return wrapper


def two_players_search(player1_nickname, player2_nickname, region_name, count=20):
    watcher = LolWatcher(key)
    player1 = watcher.summoner.by_name(region_name, player1_nickname)
    player2 = watcher.summoner.by_name(region_name, player2_nickname)
    match_list = watcher.match.matchlist_by_puuid(region_name, player1["puuid"], count=count)
    games_together = []
    for match in match_list:
        match_info = watcher.match.by_id(region_name, match)
        for player in match_info["metadata"]["participants"]:
            if player == player2["puuid"]:
                games_together.append({match: player})
        time.sleep(0.1)
    return games_together


def get_match_info(match_id, region_name):
    watcher = LolWatcher(key)
    match_info = watcher.match.by_id(region_name, match_id)
    return match_info


def get_player_all_stats(match_id, region_name, player_puuid):
    watcher = LolWatcher(key)
    match_info = watcher.match.by_id(region_name, match_id)
    for i in range(10):
        if match_info["info"]["participants"][i]["puuid"] == player_puuid:
            player_info = match_info["info"]["participants"][i]
            return player_info


def get_player_list_stats(player_stats, list_stats):
    stats = {}
    for stat in list_stats:
        stats[stat] = player_stats[stat]
    return stats


def get_players_kda_from_scratch(player_name, region_name, match_id):
    watcher = LolWatcher(key)
    kda = ["kills", "deaths", "assists"]
    player_puuid = watcher.summoner.by_name(region_name, player_name)
    player_stats = get_player_all_stats(match_id, region_name, player_puuid)
    return get_player_list_stats(player_stats, kda)


def get_all_players_list_stats(region_name, match_id, list_stats):
    watcher = LolWatcher(key)
    all_player_stats = {}
    match_info = watcher.match.by_id(region_name, match_id)
    for i in range(10):
        player_info = match_info["info"]["participants"][i]
        stats = get_player_list_stats(player_info, list_stats)
        all_player_stats[watcher.summoner.by_puuid(region_name, match_info["info"]["participants"][i]["puuid"])["name"]] = stats
    return all_player_stats


def collapsed_table_info(player, region, match_id):
    watcher = LolWatcher(key)
    player_puuid = watcher.summoner.by_name(region, player)["puuid"]
    # for match in two_players_search(player1, player2, region):
    #     for match_id in match:
    player1_stats = get_player_all_stats(match_id, region, player_puuid)
    info = get_player_list_stats(player1_stats, table_stats)
    if info["win"] == True:
        info["win"] = "Victory"
    else:
        info["win"] = "Defeat"
    info["kda"] = ", ".join([str(player1_stats["kills"]), str(player1_stats["deaths"]), str(player1_stats["assists"])])
    info["items"] = [player1_stats["item0"], player1_stats["item1"], player1_stats["item2"], player1_stats["item3"], player1_stats["item4"], player1_stats["item5"]]
    info["items"][:] = (item for item in info["items"] if item != 0)
    left_side_prt = []
    right_side_prt = []
    i=0
    for participant in watcher.match.by_id(region, match_id)["metadata"]["participants"]:
        if i <= 4:
            left_side_prt.append(watcher.summoner.by_puuid(region, participant)["name"])
        else:
            right_side_prt.append(watcher.summoner.by_puuid(region, participant)["name"])
        time.sleep(0.1)
        i += 1
    info["left_side_prt"] = left_side_prt
    info["right_side_prt"] = right_side_prt
    return info



if __name__ == "__main__":
    print("Script started")
    t1 = time.time()
    watcher = LolWatcher(key)
    match_id2 = "EUW1_6101420783"
    puuid1 = "-Mv1lSgoxtGzZWIiEerb3xQMJ3BtBVvjjs1fgdD42G5Hlp7q2dGD3T1zs0kKodesY0bylrAbDKdfTQ"
    region = "ru"
    player1 = "StePanzer"
    player2 = "MrNoct"
    all_info = {'RU_414497367': {'championName': 'Malphite', 'win': 'Defeat', 'kda': '2, 13, 6', 'items': [3041, 3102, 2055], 'left_side_prt': ['Андрей Поддержка', 'MrNoct', 'ArsadoX', 'Тильтхен', 'StePanzer'], 'right_side_prt': ['kolopak', 'FluffyCheshire', 'Neltarionko', 'ragnar1329', 'Hluix']}, 'RU_414489695': {'championName': 'Irelia', 'win': 'Victory', 'kda': '11, 5, 8', 'items': [3153, 6333, 3047, 3110, 1033, 6630], 'left_side_prt': ['UkPaTuTeJLb', 'KOLYASIIIKK', 'penzil', 'Семпай Хентай', 
    'InanityS'], 'right_side_prt': ['StePanzer', 'MrNoct', 'ArsadoX', 'Андрей Поддержка', 'Тильтхен']}, 'RU_414484603': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '16, 2, 8', 'items': [1055, 3111, 6694, 1036, 3065, 6630], 'left_side_prt': ['StepanRed12', 'Братишка Мурад', 'llPROFFESSORll', 'Malkarn', 'Настя Свитер'], 
    'right_side_prt': ['StePanzer', 'MrNoct', 'Bald brother', 'FZN Chow', 'Mellivõra']}, 'RU_414479230': {'championName': 'KogMaw', 'win': 'Defeat', 'kda': '2, 7, 4', 'items': [1055, 3153, 3124, 3006, 6670, 1018], 'left_side_prt': ['ГуБиТеЛьПiВа', 'MrNoct', 'MrTEP', 'StePanzer', 'Orcha'], 'right_side_prt': ['Jangiriko', 'The Real Yoshi', 'НАТАХТАРИ ', 'AltGaminG', 'Йой Най Буде']}, 'RU_414476418': {'championName': 'Ornn', 'win': 'Victory', 'kda': '1, 0, 0', 'items': [1054], 'left_side_prt': ['Nyorikenoichi', 'DORLL', 'Taskinsam', 'EDATH13', 'Кастрюля'], 'right_side_prt': ['StePanzer', 'MrNoct', 'hidemovement', 'Fеnrisulfr', 'Счастьице']}, 'RU_414064349': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '13, 6, 11', 'items': [3065, 3047, 6694, 3071, 6630], 'left_side_prt': ['StePanzer', 'MrNoct', 'dogorad', 'LesbianFanboy', 'SirExtraSex'], 'right_side_prt': ['FLAWxxxLE55', 'ВкругуКретинов', 'Gmeer', 'Disciple', 'CYBERDEDOK']}, 'RU_413920971': {'championName': 
    'Aatrox', 'win': 'Victory', 'kda': '10, 8, 7', 'items': [3047, 3153, 6632, 3075, 3211], 'left_side_prt': ['Kastie', 'Живой ', 'dgeims', 'Black Mamba', 'Absolute'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Распутный Тёма ', 'pbIk', 'Бойчик']}, 'RU_413659735': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '11, 6, 4', 
    'items': [6333, 6694, 3047, 3044, 1037, 6630], 'left_side_prt': ['AkaliJustShadow', 'БезголовыйДжек', 'SHS Regenaild', 'LOLER123234', 'Dramamotic'], 'right_side_prt': ['StePanzer', 'not your Gоd', 'Clown Pepega ', 'RusSsk1i', 'MrNoct']}, 'RU_413334510': {'championName': 'Yorick', 'win': 'Victory', 'kda': '4, 5, 2', 'items': [6694, 6692, 3009, 3071, 3181], 'left_side_prt': ['StePanzer', 'MrNoct', 'Люблю Поезда', 'imaglacial', 'Buccelatti'], 'right_side_prt': ['Shaclоne', 'RavenoZoro', 'Vovinio', 'Holovachlena', 'Caring egoist']}, 'RU_413331187': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '6, 6, 7', 'items': [6333, 6694, 3111, 4401, 
    6693], 'left_side_prt': ['MeldyE', 'BlаckMооn', 'AoAndoN', 'lMeatxboyl', 'creek5'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Прaид', 'joij', 'kolley']}, 'RU_413326449': {'championName': 'Aatrox', 'win': 'Defeat', 'kda': '2, 9, 4', 'items': [1054, 3047, 6333, 3067, 3133, 6630], 'left_side_prt': ['Rost1slav999', 'ПРОЕКТ Каин', 'Capitan Permach', 'Андрюха М16', 'RelictForm'], 'right_side_prt': ['StePanzer', 'MrNoct', 'Wave of  Sound', 'WraithFn', 'TetraziklinE']}}
    # for match in two_players_search(player1, player2, region):
    #     for match_id in match:
    #         all_info[match_id] = collapsed_table_info(player1, region, match_id)
    # print(all_info)
    # t2 = time.time()
    # print(f"{t2-t1} seconds")
    for game in all_info:
        print("/n")
        for participant in all_info[game]["left_side_prt"]:
          print(participant)
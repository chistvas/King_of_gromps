from riotwatcher import LolWatcher
import time

key = "RGAPI-78d8d828-9c2c-46ae-a5af-e7a58ce8eea4"
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


def two_players_search(player1_nickname, player2_nickname, region_name, count=2):
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
    info["items"] = ", ".join([str(player1_stats["item0"]), str(player1_stats["item1"]), str(player1_stats["item2"]), str(player1_stats["item3"]), str(player1_stats["item4"]), str(player1_stats["item5"])])
    enemys_list = []
    for participant in watcher.match.by_id(region, match_id)["metadata"]["participants"]:
        enemys_list.append(watcher.summoner.by_puuid(region, participant)["name"])
        time.sleep(0.1)
        info["enemys"] = ", ".join(enemys_list)
    return info



if __name__ == "__main__":
    print("Script started")
    t1 = time.time()
    watcher = LolWatcher(key)
    match_id2 = "EUW1_6101420783"
    puuid1 = "-Mv1lSgoxtGzZWIiEerb3xQMJ3BtBVvjjs1fgdD42G5Hlp7q2dGD3T1zs0kKodesY0bylrAbDKdfTQ"
    region = "ru"
    player1 = "StePanzer"
    player2 = "LesbianFanboy"
    all_info = {}
    for match in two_players_search(player1, player2, region):
        for match_id in match:
            all_info[match_id] = collapsed_table_info(player1, region, match_id)
    print(all_info)
    t2 = time.time()
    print(f"{t2-t1} seconds")
    for game in all_info:
        print("/n")
        for keys in all_info[game]:
          print(all_info[game][keys])
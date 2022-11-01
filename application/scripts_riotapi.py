from riotwatcher import LolWatcher
import time

key = "RGAPI-59686a90-f6cc-41b6-9632-12b63ed22c39"
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
    player1_stats = get_player_all_stats(match_id, region, player_puuid)
    info = get_player_list_stats(player1_stats, table_stats)
    if info["win"] == True:
        info["win"] = "Victory"
    else:
        info["win"] = "Defeat"
    info["kda"] = ", ".join([str(player1_stats["kills"]), str(player1_stats["deaths"]), str(player1_stats["assists"])])
    info["items"] = [player1_stats["item0"], player1_stats["item1"], player1_stats["item2"], player1_stats["item3"], player1_stats["item4"], player1_stats["item5"]]
    info["items"][:] = (item for item in info["items"] if item != 0)
    left_side_prt = {}
    right_side_prt = {}
    i=0
    gamedata = watcher.match.by_id(region, match_id)
    for participant in gamedata["metadata"]["participants"]:
        name = watcher.summoner.by_puuid(region, participant)["name"]
        if i <= 4:
            left_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
        else:
            right_side_prt[name] = gamedata["info"]["participants"][i]["championName"]
        time.sleep(0.1)
        i += 1
    info["left_side_prt"] = left_side_prt
    info["right_side_prt"] = right_side_prt
    return info



if __name__ == "__main__":
    print("Script started")
    watcher = LolWatcher(key)
    match_id2 = "EUW1_6101420783"
    puuid1 = "-Mv1lSgoxtGzZWIiEerb3xQMJ3BtBVvjjs1fgdD42G5Hlp7q2dGD3T1zs0kKodesY0bylrAbDKdfTQ"
    region = "ru"
    player1 = "StePanzer"
    player2 = "MrNoct"
    all_info = {}
    gamedata = watcher.match.by_id(region, match_id2)
    print(gamedata)

    # info_two_players_search = two_players_search(player1, player2, region)
    # time_api = 0
    # tstart = time.time()
    # for match in info_two_players_search:
    #     for match_id in match:
    #         t2 = time.time()
    #         info_collapsed_table_info = collapsed_table_info(player1, region, match_id)
    #         time_api += time.time() - t2
    #         print(time_api)
    #         all_info[match_id] = info_collapsed_table_info
    # tend = time.time() - tstart - time_api
    # print(all_info, tend)
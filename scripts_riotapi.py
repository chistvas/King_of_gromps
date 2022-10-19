from riotwatcher import LolWatcher


key = "RGAPI-4204ebcd-0245-4b2f-bdfb-67f6effc93cd"
kda = ["kills", "deaths", "assists"]

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




if __name__ == "__main__":
    print("Script started")
    match_id2 = "EUW1_6101420783"
    puuid1 = "-Mv1lSgoxtGzZWIiEerb3xQMJ3BtBVvjjs1fgdD42G5Hlp7q2dGD3T1zs0kKodesY0bylrAbDKdfTQ"
    region = "euw1"
    player1 = "metalonot"
    player2 = "Karini"
    all_info = {}
    for match in two_players_search(player1, player2, region):
        for match_id in match:
            all_info[match_id] = get_all_players_list_stats(region, match_id, kda)
    print(all_info)
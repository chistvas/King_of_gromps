# from scripts_riotapi import

if __name__ == "__main__":
    data = {'RU_414064349': {'championName': 'Aatrox', 'win': 'Victory', 'kda': '13, 6, 11', 'items': '3065, 3047, 6694, 3071, 0, 6630', 'enemys': 'StePanzer, MrNoct, dogorad, LesbianFanboy, SirExtraSex, FLAWxxxLE55, ВкругуКретинов, Gmeer, Disciple, CYBERDEDOK'}} 
    for game in data:
        print(data[game]["championName"]
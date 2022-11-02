from riotwatcher import LolWatcher
import time
from application.models import Summoner, Game, Proplayers
from application import db, app
import mwclient
import json
from sqlalchemy import Table
key = "RGAPI-82ff421b-4838-4326-9fb0-8e7a87df3932"
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

def proplayers_into_db(where):
    site = mwclient.Site('lol.fandom.com', path='/')
    response = site.api('cargoquery', limit = 'max', tables = "Players", fields="Player, Name, Age, Team, Role, SoloqueueIds, IsRetired", where=where)
    parsed = json.dumps(response)
    decoded = json.loads(parsed)
    for player in decoded["cargoquery"]:
        new_player = Proplayers(
            player=player["title"]["Player"], 
            name=player["title"]["Name"], 
            age=player["title"]["Age"], 
            team=player["title"]["Team"], 
            role=player["title"]["Role"], 
            soloqueueids=player["title"]["SoloqueueIds"], 
            isretired=player["title"]["IsRetired"]
        )
        db.session.add(new_player)
        db.session.commit()
    return print('end')

if __name__ == "__main__":
    app.app_context().push()
    for id in range(0, 15000, 500):
        where = f"id >= {id}"
        print(id, where)
        proplayers_into_db(where)
        time.sleep(5)
import requests


def data_upd():
    database_upd = open('data.db', 'wb')
    upd = requests.get('https://drive.google.com/uc?export=download&id=1EIU2yTyCKs9S2xNRoXCqDr2foEVskICE')
    database_upd.write(upd.content)
    database_upd.close()

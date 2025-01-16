import sqlite3

def InsertScore(player_score, ai_score):
    connection = sqlite3.connect('database/database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO history (player_score, ai_score) VALUES (?, ?)', (player_score, ai_score))
    connection.commit()
    connection.close()


def GetScore():
    connection = sqlite3.connect('database/database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT player_score, ai_score FROM history')
    scores = cursor.fetchall()
    connection.close()
    # scores_map = {
    #     'player': [score[0] for score in scores],
    #     'ai': [score[1] for score in scores]
    # }
    # return scores_map
    return scores
import sqlite3

def InsertScore(player_score, ai_score, name):
    connection = sqlite3.connect('database/database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO history (player_score, ai_score, name) VALUES (?, ?, ?)', (player_score, ai_score, name))
    connection.commit()
    connection.close()


def GetScore(name):
    connection = sqlite3.connect('database/database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT player_score, ai_score FROM history WHERE name = ?', (name,))
    scores = cursor.fetchall()
    connection.close()
    # scores_map = {
    #     'player': [score[0] for score in scores],
    #     'ai': [score[1] for score in scores]
    # }
    # return scores_map
    return scores
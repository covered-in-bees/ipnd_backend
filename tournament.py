#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player (and thus, match) records from the database."""
    deleteMatches()
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def dropPlayer(player_id):
    """Remove one player from the tournament, but maintain thier match history"""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players WHERE id = %s" % (int(player_id),))
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) as num FROM players")
    for row in c.fetchall():
        return row[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    text = str(name)
    DB = connect()
    c = DB.cursor()
    c.execute ("INSERT INTO players (name) VALUES (%s)", (text,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute ("""SELECT players.id, name, max(wins) as wins,
                max(wins+losses) as matches
                FROM players
                JOIN wincount on players.id=wincount.id
                JOIN losscount on players.id=losscount.id
                GROUP BY players.id ORDER BY wins DESC""")

    standings = [(row[0], row[1], int(row[2]), int(row[3])) for row in c.fetchall()]
    return standings

def reportMatch(winner, loser , draw='n'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    #the following line is in place to facilitate future implementation of
    #draws and avoiding rematches in the bracket. It also conveniently reports
    #match history.

    c.execute ("""INSERT INTO matches (winner, loser, draw)
                VALUES (%s, %s, %s)""", ((winner,), (loser,), (draw,)))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    If there is an odd number of players, the lowest in standing will recieve a
    bye, which is automatically reported.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings=playerStandings()
    id_index=0
    name_index=1
    player_count=countPlayers()
    #pairs players based on standing, pairing the top two , 3rd and 4th, etc.
    pairings=[(standings[x-1][id_index], standings[x-1][name_index],
                standings[x][id_index], standings[x][name_index])
                for x in range(player_count) if x%2==1]
    if player_count%2==1:
        pairings.append((standings[player_count-1][id_index],
                        standings[player_count-1][name_index], 0, 'BYE'))
        reportMatch(standings[player_count-1][id_index], 0)
    return pairings

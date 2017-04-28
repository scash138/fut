# -*- coding: utf-8 -*-

"""
fut.db
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's database.

"""
import requests
import re
from .config import timeout
from .urls import urls


class Player(object):
    """Player object.

    :param id: player id/base_id.
    :param firstname: firstname.
    :param lastname: lastname.
    :param surname: surname, not every player has it.
    :param rating: rating.
    :param nationality: nationality.
    """
    def __init__(self, id, firstname, lastname, surname, rating, nationality):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.rating = rating
        self.nationality = nationality


# TODO: optimize messages, xml parser might be faster
def nations(timeout=timeout):
    """Return all nations in dict {id0: nation0, id1: nation1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="search.nationName.nation([0-9]+)">\n        <source>(.+)</source>', rc)
    nations = {}
    for i in data:
        nations[int(i[0])] = i[1]
    return nations


def leagues(year=2017, timeout=timeout):
    """Return all leagues in dict {id0: league0, id1: legaue1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="global.leagueFull.%s.league([0-9]+)">\n        <source>(.+)</source>' % year, rc)
    leagues = {}
    for i in data:
        leagues[int(i[0])] = i[1]
    return leagues


def teams(year=2017, timeout=timeout):
    """Return all teams in dict {id0: team0, id1: team1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="global.teamFull.%s.team([0-9]+)">\n        <source>(.+)</source>' % year, rc)
    teams = {}
    for i in data:
        teams[int(i[0])] = i[1]
    return teams

def players(timeout=timeout):
    """Return all players in dict {id: c, f, l, n, r}.
    id, rank, nationality(?), first name, last name.
    """
    rc = requests.get('{0}{1}.json'.format(urls('pc')['card_info'], 'players'), timeout=timeout).json()
    players = {}
    for i in rc['Players'] + rc['LegendsPlayers']:
        players[i['id']] = Player(id=i['id'],
                                  fistname=i['f'],
                                  lastname=i['l'],
                                  surname=i.get('c'),
                                  rating=i['r'],
                                  nationality=i['n'])  # replace with nationality object when created
    return players

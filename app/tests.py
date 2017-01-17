#!/usr/bin/env python3

import unittest
import requests
from flask.ext.testing import TestCase
from sqlalchemy import create_engine
from flask import Flask
from unittest import main
from flask.ext.sqlalchemy import SQLAlchemy
from app import search

t_app = Flask(__name__)

db = SQLAlchemy(t_app)

from test_models import *

class TestApp (TestCase):

    def create_app(self):
        t_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        t_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        t_app.config['TESTING'] = True
        return t_app

    def setUp(self):
        db.create_all();

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # --------------------
    # Test search in app.y
    # --------------------

    # def test_search_1(self):
    #     summ1 = Champion(10, "test_name_one", "bronze", "V", 50, 0.60, 70)
    #     summ2 = Champion(20, "test_name_two", "silver", "I", 1, 0.2, 3)
    #     db.session.add(summ1)
    #     db.session.add(summ2)
    #     db.session.commit()

    #     res = json.loads(search("one"))

    #     self.assertEqual(res["or_set"][0]["context"][0], "name: test_name_one")

    # def test_search_2(self):
    #     pass

    # def test_search_3(self):
    #     pass

    # -----------
    # Champions
    # -----------

    def test_champion_1(self):
        champ = Champion(0, '', '', 0, 0, 0, 0, "")
        self.assertEqual(champ.name,  '')
        self.assertEqual(champ.id, 0)
        self.assertEqual(champ.hp, 0)
        self.assertEqual(champ.mp, 0)
        self.assertEqual(champ.movespeed, 0)
        self.assertEqual(champ.spellblock, 0)
    
    def test_champion_2(self):
        champ = Champion(1, 'name', 'title', 50, 100, 200, 0, "url")
        self.assertEqual(champ.id, 1)
        self.assertEqual(champ.name, 'name')
        self.assertEqual(champ.title, 'title')
        self.assertEqual(champ.hp, 50)
        self.assertEqual(champ.mp, 100)
        self.assertEqual(champ.movespeed, 200)
        self.assertEqual(champ.spellblock, 0)
        self.assertEqual(champ.portrait_url, "url")

    def test_champion_3(self):
        d = json.loads(requests.get('http://dudecarry.me/api/champion/103').text)
        self.assertEqual(d['name'], 'Ahri')
        self.assertEqual(d['id'], 103)
        self.assertEqual(d['hp'], 514.4)
        self.assertEqual(d['mp'], 334.0)

    # -------------
    # Summoners
    # -------------

    def test_summoner_1(self):
        summoner = Summoner(0, "", "", "", 0, 0, 0)
        self.assertEqual(summoner.id, 0)
        self.assertEqual(summoner.name, "")
        self.assertEqual(summoner.win_percentage, 0.0)       

    def test_summoner_2(self):
        summoner = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        self.assertEqual(summoner.id, 10)
        self.assertEqual(summoner.name, 'test_name')

    def test_summoner_3(self):
        d = json.loads(requests.get('http://dudecarry.me/api/summoner/35590582').text)
        self.assertEqual(d['name'], 'Annie Bot')
        self.assertEqual(d['id'], 35590582)
        self.assertEqual(d['lp'], 509)
        self.assertEqual(d['total_games'], 481)

    # -------------
    # Teams
    # -------------

    def test_team_1(self):
        team = Team("", "", "", False, 0, 0, "")
        self.assertEqual(team.id, "")
        self.assertEqual(team.tag, "")
        self.assertEqual(team.win_percentage, 0)       

    def test_team_2(self):
        team = Team("team_id", "test-name", "test_tag", True, 0.52, 56, "123123")
        self.assertEqual(team.id, "team_id")
        self.assertEqual(team.name, 'test-name')

    def test_team_3(self):
        d = json.loads(requests.get('http://dudecarry.me/api/team/TEAM-8fb9ac60-918b-11e5-b39e-c81f66dcfb5a').text)
        
        self.assertEqual(d['id'], "TEAM-8fb9ac60-918b-11e5-b39e-c81f66dcfb5a")
        self.assertEqual(d['name'], "Akimu")
        self.assertEqual(d['win_percentage'], None)
        self.assertEqual(d['name'], "Akimu")       

    # ----------------------
    # Test Search API calls
    # ----------------------

    def test_apiCallSearch_3(self):
        d = json.loads(requests.get('http://dudecarry.me/api/search/aatrox').text)
        
        self.assertEqual(d['results'][0]["context"][0], "name: Aatrox")
        self.assertEqual(d['results'][0]["type"], "champion")

    # ---------------------------
    # Test database functionality
    # ---------------------------

    def db_1(self):
        summ = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        
        db.session.add(summ)
        db.session.commit()

        ret = Summoner.query.filter(Summoner.id == 10).first()

        self.assertEqual(summ.id, ret.id)
        self.assertEqual(summ.name, ret.name)
        self.assertEqual(summ.tier, ret.tier)
        self.assertEqual(summ.division, ret.division)
        self.assertEqual(summ.lp, ret.lp)

        db.session.delete(summ)
        db.session.commit()

    def db_2(self):
        champ = Champion(10, "test_name", "bronze champ op", 1, 2, 3, 100, "")
        db.session.add(champ)
        db.session.commit()

        ret = Champion.query.filter(Champion.id == 10).first()

        self.assertEqual(champ.id, ret.id)
        self.assertEqual(champ.name, ret.name)
        self.assertEqual(champ.hp, ret.hp)
        self.assertEqual(champ.spellblock, ret.spellblock)
        self.assertEqual(champ.movespeed, ret.movespeed)

        db.session.delete(champ)
        db.session.commit()

    def db_3(self):
        tm = Team("team_id", "team_name", "test_tag", True, 0.52, 56, "123123")

        db.session.add(tm)
        db.session.commit()

        ret = Team.query.filter(Team.id == "team_id").first()

        self.assertEqual(tm.id, ret.id)
        self.assertEqual(tm.name, ret.name)
        self.assertEqual(tm.status, ret.status)
        self.assertEqual(tm.total_games, ret.total_games)
        self.assertEqual(tm.win_percentage, ret.win_percentage)

        db.session.delete(tm)
        db.session.commit()

    # --------------------------------
    # Test test_models.py API functions
    # --------------------------------

    def test_apiFunc_1(self):
        summ = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        
        db.session.add(summ)
        db.session.commit()

        summoner = Summoner.query.filter(Summoner.id == 10).first()

        summ_true = {
            "id":               10,
            "name":             "test_name",
            "rank":             180,
            "tier":             "bronze",
            "division":         "I",
            "lp":               56,
            "win_percentage":   0.52,
            "total_games":      100,
            "teams":            [],
            "top_3_champs":     []
        }


        summ_test = summoner_to_json(summoner)
       

        for field in summ_true:
            self.assertEqual(summ_true[field], summ_test[field])

        db.session.delete(summ)
        db.session.commit()


    def test_apiFunc_2(self):
        tm = Team("team_id", "team_name", "test_tag", True, 0.52, 56, "123123")
        db.session.add(tm)
        db.session.commit()

        team = Team.query.filter(Team.id == "team_id").first()

        team_true = {
            "id":                           "team_id",
            "name":                         "team_name",
            "tag":                          "test_tag",
            "status":                       True,
            "win_percentage":               0.52,
            "total_games":                  56,
            "most_recent_member_timestamp": "123123",
            "summoners":                    []    
        }

        team_test = team_to_json(team)

        for field in team_true:
            self.assertEqual(team_true[field], team_test[field])

        db.session.delete(tm)
        db.session.commit()

    def test_apiFunc_3(self):

        champ = Champion(10, "test_name", "bronze champ op", 1, 2, 3, 100, "")
        db.session.add(champ)
        db.session.commit()

        champ = Champion.query.filter(Champion.id == 10).first()

        champ_true = {
            "id":         10,
            "name":       "test_name",
            "title":      "bronze champ op",
            "hp":         1,
            "mp":         2,
            "movespeed":  3,
            "spellblock": 100,
            "icon_url":   ""
        }

        champ_test = champion_to_json(champ)

        for field in champ_true:
            self.assertEqual(champ_true[field], champ_test[field])

        db.session.delete(champ)
        db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity = 2)

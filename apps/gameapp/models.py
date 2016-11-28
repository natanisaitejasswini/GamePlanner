from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date, timedelta, time
from time import strftime
from ..loginreg.models import User
# Create your models here.

class GameManager(models.Manager):
	def create_game(self, data):
		errors =[]
		if data['date'] == "":
			errors.append("Please Enter a Date")
		if data['date'] != "" and data['date'] < strftime('%Y-%m-%d'):
			errors.append("Date Must be in the Future")
		if data['time'] == "":
			errors.append("Please Enter a Time")
		if not errors:
			return(True, data)
		else:
			return(False,errors)
# this table has what we are wanting to preasign as admin for any new game
class GameType(models.Model):
	game = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

# this table is what the user will use to start (create) a new game

class Game(models.Model):
	players = models.CharField(max_length=100)
	date = models.DateField()
	time = models.TimeField()
	gametype = models.ForeignKey(GameType, related_name="gamestype")
	game_starter = models.ForeignKey('loginreg.User', related_name="usersstarts")
	game_joiner = models.ManyToManyField('loginreg.User', related_name="joingame")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	gameManager = GameManager()
	objects = models.Manager()

game_types1 = ['Baseball', 'Basketball', 'Football' , 'Soccer', 'Rugby', 'Volleyball']
game_types2 = ['Frisbee', 'Pokemon GO' ]
game_types3 = ['Walking']
game_types4 = ['Running']


for game_type in game_types1:
	if not GameType.objects.filter(game=game_type):
		GameType.objects.create(game=game_type,location='Surrey Downs Park')
for game_type in game_types2:
	if not GameType.objects.filter(game=game_type):
		GameType.objects.create(game=game_type,location='Bellevue Park')
for game_type in game_types3:
	if not GameType.objects.filter(game=game_type):
		GameType.objects.create(game=game_type,location='Mercer Slough Nature Park')
for game_type in game_types4:
	if not GameType.objects.filter(game=game_type):
		GameType.objects.create(game=game_type,location='Bellevue Botanical Garden')

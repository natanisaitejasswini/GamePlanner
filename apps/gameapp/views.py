from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from ..loginreg.models import User
from .models import GameType, Game, GameManager
from django.db.models import Count
import bcrypt
import datetime
# from datetime import datetime

def landing(request):
    return render(request, 'gameapp/landing.html')

def start(request):
	context = {
		'gametypes':GameType.objects.all()
		}
	return render(request, 'gameapp/start.html',context)
#create game and process request.POST
def start_game(request):
    new_game = Game.gameManager.create_game(request.POST)
    if new_game[0] == False:
        for error in new_game[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/start')
    else:
        gametype = GameType.objects.get(id=request.POST['gametype_selection'])
        gamestarter = User.objects.get(id=request.session['user'])
        Game.objects.create(players=request.POST['players'], date=request.POST['date'], time=request.POST['time'], gametype=gametype, game_starter=gamestarter)
        return redirect('/join')

def join(request):
    game_starter = User.objects.get(id=request.session['user'])
    context = {
        'games': Game.objects.filter(game_starter__id=request.session['user']),
        'friends':Game.objects.exclude(game_starter__id=request.session['user']).exclude(game_joiner__id=request.session['user']),
        'joiners': Game.objects.filter(game_joiner__id=request.session['user']),
        }
    print context['games']
    return render(request, 'gameapp/join.html', context)

def join_game(request, id):
    game = Game.objects.get(id=id)
    game.game_joiner.add(User.objects.get(id=request.session['user']))
    game.save()
    return redirect('/join')

def info(request, id):
    context = {
        'id': id,
        'game':Game.objects.get(id=id)
        }
    print context['game']
    return render(request, 'gameapp/info.html', context)

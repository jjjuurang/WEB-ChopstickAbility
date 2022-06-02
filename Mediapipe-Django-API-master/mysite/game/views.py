from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from mysite.game.game_class.Game import gen
from mysite.game.game_class.Game import Game


def game_easy(request):
    game = Game("easy")
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def game_normal(request):
    game = Game("normal")
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def game_hard(request):
    game = Game("hard")
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def game_01(request):
    return render(request, 'game_01.html')

def game_02(request):
    return render(request, 'game_02.html')

def game_03(request):
    return render(request, 'game_03.html')
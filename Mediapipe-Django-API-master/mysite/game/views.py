from django.contrib.auth import get_user_model
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from mysite.core.models import UserGameRecord, Ranking
from mysite.game.game_class.Game import gen
from mysite.game.game_class.Game import Game


def game_easy(request):
    game = Game("easy", request.user)
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def game_normal(request):
    game = Game("normal",request.user)
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def game_hard(request):
    game = Game("hard",request.user)
    vid = StreamingHttpResponse(gen(game),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

@csrf_exempt
def user_game_count(request, username):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    object = get_object_or_404(get_user_model(), username=userMODEL.username)

    print(userMODEL)

    count = UserGameRecord.objects.get(NAME=userMODEL)

    context = {'count': count.COUNT}

    return JsonResponse(context)

def game_01(request):

    userMODEL = get_user_model().objects.get(username=request.user.username)
    object = get_object_or_404(get_user_model(), username=userMODEL.username)

    print(userMODEL)

    count = UserGameRecord.objects.get(NAME=userMODEL)

    context = {'count': count.COUNT}

    return render(request, 'game_01.html', context)

def game_02(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    object = get_object_or_404(get_user_model(), username=userMODEL.username)

    print(userMODEL)

    count = UserGameRecord.objects.get(NAME=userMODEL)

    context = {'count': count.COUNT}

    return render(request, 'game_02.html', context)

def game_03(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    object = get_object_or_404(get_user_model(), username=userMODEL.username)

    print(userMODEL)

    count = UserGameRecord.objects.get(NAME=userMODEL)

    context = {'count': count.COUNT}
    return render(request, 'game_03.html', context)


def ranking(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    score= Ranking.objects.filter(NAME=userMODEL).order_by('-NAME_id')[0]

    print(score.SCORE)

    rank = Ranking.objects.raw("""
        select *, rank() over (partition by MODE order by SCORE desc) as rank, auth_user.username as name
        from core_ranking, auth_user
        where auth_user.id = core_ranking.username
    """)

    print(rank[0].SCORE)

    my_record = Ranking.objects.raw("""
        SELECT DISTINCT rank_table.rank as ranking, 1 as id
        FROM (select *, rank() over (partition by MODE order by SCORE desc) as rank
        from core_ranking) as rank_table
        WHERE rank_table.SCORE = """ + (str)(score.SCORE)+""";"""
    )


    print(my_record[0].ranking)

    context = {
        'score': score.SCORE,
        'record' : my_record,
        'rank' : rank[0:4],
    }


    return render(request, 'ranking.html', context)
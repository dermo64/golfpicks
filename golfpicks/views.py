from django.shortcuts import render
from golfpicks.models import Pick
from django.http import JsonResponse

import requests
import json

# Create your views here.
from golfpicks.models import Golfer, Pick, Punter, Event

def get_cutscore(players):
    """Return the score of the first player cut"""
    scores = [get_score(i['position']) for i in players if get_score(i['position']) != 999]

    return max(scores) + scores.count(max(scores))

def get_score(pos):
        if pos is None:
            return 0
        return int(pos) if pos[0] != 'T' else int(pos[1:])

def get_par(golfer):
    if(golfer['status'] in ('Cut', 'Withdrawn', 'Disqualified')):
        return 1000
    return int(golfer['overallPar'])

def get_standing(pick, scores):
    """Returnn a string comprised of golfers and their scores and the total score for a punter's picks"""
    standing = {'punter': pick.punter}

    golfers = [pick.picks.values()[0]['name'], pick.picks.values()[1]['name'], pick.picks.values()[2]['name']]
    
    standing['golfer1'] = golfers[0] + ': ' + (str(scores[golfers[0]]) if scores[golfers[0]] != 1000 else 'Elim')
    standing['golfer2'] = golfers[1] + ': ' + (str(scores[golfers[1]]) if scores[golfers[1]] != 1000 else 'Elim')
    standing['golfer3'] = golfers[2] + ': ' + (str(scores[golfers[2]]) if scores[golfers[2]] != 1000 else 'Elim')
    standing['score'] = scores[golfers[0]] + scores[golfers[1]] + scores[golfers[2]]

    #standing['position'] = 1

    standing['eliminated'] = scores[golfers[0]] == 1000 or scores[golfers[1]] == 1000 or scores[golfers[2]] == 1000

    return standing

def index(request):
    """View function for home page of site."""

    r =requests.get('https://www.golfchannel.com/api/v2/events/19208/leaderboard')

    picks = Pick.objects.filter(event__external_id__exact=19208).order_by('punter__name')

    my_json = json.loads(r.text)

    cut_score = get_cutscore(my_json['result']['golfers'])

    #scores = dict(
    #    [(n['firstName'] + ' ' + n['lastName'], min(get_score(n['position']), cut_score)) for n in my_json['result']['golfers'] ])
    scores = dict(
        [(n['firstName'] + ' ' + n['lastName'], get_par(n)) for n in my_json['result']['golfers'] ])   

    standings = sorted([get_standing(pick, scores) for pick in picks], key = lambda standing: standing['score'])

    position = 0
    cur_score = -1000
    for standing in standings:
        if cur_score != standing['score']:
            position += 1
            cur_score = standing['score']
        standing['position'] = position

    context = {
        'event_name': my_json['result']['eventName'],
        'standings': standings,
        'picks': picks,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def test(request):
    picks = Pick.objects.all().values()  # or simply .values() to get all fields
    pick_list = list(picks)  # important: convert the QuerySet to a list object
    return JsonResponse(pick_list, safe=False)




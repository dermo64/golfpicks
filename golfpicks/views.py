from django.shortcuts import render
from golfpicks.models import Pick
from django.http import JsonResponse

import requests
import json

# Create your views here.
from golfpicks.models import Golfer, Pick, Punter, Event

def get_score(pos):
        if pos is None:
            return 0
        else:
            print("Not none")
        return int(pos) if pos[0] != 'T' else int(pos[1:])

def get_standing(pick, scores):
    """Returnn a string comprised of golfers and their scores and the total score for a punter's picks"""
    standing = {'punter': pick.punter}

    golfers = [pick.picks.values()[0]['name'], pick.picks.values()[1]['name'], pick.picks.values()[2]['name']]
    
    standing['golfer1'] = golfers[0] + ' ' + str(scores[golfers[0]])
    standing['golfer2'] = golfers[1] + ' ' + str(scores[golfers[1]])
    standing['golfer3'] = golfers[2] + ' ' + str(scores[golfers[2]])
    standing['score'] = scores[golfers[0]] + scores[golfers[1]] + scores[golfers[2]]

    return standing


#from background_task import background

# @background(schedule=1)
# def bk_task():
#     r =requests.get('https://www.golfchannel.com/api/v2/events/19163/leaderboard')

#     my_json = json.loads(r.text)
#     print('im in here')
#     print(my_json['result']['eventName'])

def index(request):
    """View function for home page of site."""

  #  bk_task()

    # Generate counts of some of the main objects
    
    # Available books (status = 'a')
#    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    r =requests.get('https://www.golfchannel.com/api/v2/events/19164/leaderboard')

    picks = Pick.objects.filter(event__external_id__exact=19164)

    my_json = json.loads(r.text)

    scores = dict([(n['firstName'] + ' ' + n['lastName'], get_score(n['position'])) for n in my_json['result']['golfers'] ])

    standings = sorted([get_standing(pick, scores) for pick in picks], key = lambda standing: standing['score'])
    
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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from social_auth import __version__ as version
from frontend.events.models import Event, Status
import tweepy

# Create your views here.
@login_required
def dashboard(request, event_id):
    """Login complete view, displays user data"""

    event = Event.objects.get(id=event_id)
    user = request.user
    status = Status.objects.filter(user=user.id).latest('time')

    twitter_user = tweepy.api.get_user(user.username)

    ctx = {'accounts': request.user.social_auth.all(),
           'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'user': user,
           'event': event,
           'status': status,
            'profile_image_url': twitter_user.profile_image_url.replace('_normal', '_bigger'),
           }
    return render_to_response('events/dashboard.html', ctx, RequestContext(request))


"""The MIT License (MIT)	

Copyright (c) 2018 Giuliano Gozza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import requests
import json

API_KEY = 'c706da75'
BASE_URL = 'http://www.omdbapi.com'

# This has to be called when Mycroft reacts to the intent
def request_imdb_rating(movie_name):
    response = requests.get(BASE_URL, params = {'apikey': API_KEY, 't': movie_name})
    if response.status_code !=200:
        raise ApiError('GET /tasks/ {}'.format(response.status_code))
    else:
        ratings = response.json()['Ratings']
        for rating in ratings:
            if rating['Source'] == 'Internet Movie Database':
                imdb_rating = ''
                for char in rating['Value']:
                    if char == '/':
                        break
                    imdb_rating += char
        return imdb_rating

def request_imdb_movie_actors(movie_name):
    response = requests.get(BASE_URL, params = {'apikey': API_KEY, 't': movie_name})
    if response.status_code !=200:
        raise ApiError('GET /tasks/ {}'.format(response.status_code))
    else:
        actors = response.json()['Actors']
        actor_list = actors.split(',')
        return actor_list

class IMDBRatingSkill(MycroftSkill):
    
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(IMDBRatingSkill, self).__init__(name="IMDBRatingSkill")

    @intent_handler(IntentBuilder("").optionally("IMDB").require("Rating").require("Movie"))
    def handle_rating_intent(self, message):
        movie_name = message.data.get("Movie")
        try:
            imdb_rating = request_imdb_rating(movie_name)
        except APIError:
            self.speak_dialog("cannot.connect")
            return
        self.speak_dialog("movie.is.rated", {'rating': imdb_rating})

    @intent_handler(IntentBuilder("").require("Actors").optionally("Acting").require("Movie_Actors"))
    def handle_actor_intent(self, message):
        movie_name = message.data.get("Movie")
        try:
            movie_actors = request_imdb_movie_actors(movie_name)
        except APIError:
            self.speak_dialog("cannot.connect")
            return
        self.speak_dialog("actors.are.in.movie", {'actors': movie_actors})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return IMDBRatingSkill()

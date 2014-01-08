#!/usr/bin/env python
#
# Copyright 2010 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
From: https://github.com/pythonforfacebook/facebook-sdk/blob/master/examples/appengine/example.py

A barebones AppEngine application that uses Facebook for login.

1.  Make sure you add a copy of facebook.py (from python-sdk/src/)
    into this directory so it can be imported.
2.  Don't forget to tick Login With Facebook on your facebook app's
    dashboard and place the app's url wherever it is hosted
3.  Place a random, unguessable string as a session secret below in
    config dict.
4.  Fill app id and app secret.
5.  Change the application name in app.yaml.

Modified by Louis, Christian

This module is modified to extract and present the user with information based
on facebook graph data of the current logged in facebook user.

It is further modified to create a post on the users facebook wall,
based on graph data as well.   

"""
FACEBOOK_APP_ID = "476583549131549"
FACEBOOK_APP_SECRET = "08bc3e1c03aefe92cd28047244f82bff"


import facebook
import PostAnalysis
import webapp2
import os
import jinja2
import UrlGetterGoogle as UGG
from google.appengine.ext import db
from webapp2_extras import sessions
from google.appengine.api import urlfetch

config = {}
config['webapp2_extras.sessions'] = dict(secret_key='jsdafkjlsdkflskajfjirifjsl')

#the following line extends the wait for the responce to 45 seconds. (60 is max!) 
urlfetch.set_default_fetch_deadline(45)

class User(db.Model):
    
    """
    Class to create data base user objects.
    """
    id = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    updated = db.DateTimeProperty(auto_now = True)
    name = db.StringProperty(required = True)
    profile_url = db.StringProperty(required = True)
    access_token = db.StringProperty(required = True)
    post_type = db.StringProperty(required = False)
    post_day = db.StringProperty(required = False)
    post_time = db.StringProperty(required = False)
    post_word_number = db.StringProperty(required = False)
    post_characters = db.StringProperty(required = False)
    post_signs = db.StringProperty(required = False)
    post_multiple_signs = db.StringProperty(required = False)
    post_questions = db.StringProperty(required = False)
    post_exclamations = db.StringProperty(required = False)
    post_names = db.StringProperty(required = False)
    post_emoticons = db.StringProperty(required = False)
    post_like_number = db.StringProperty(required = False)
    
    post_type_like = db.StringProperty(required = False)
    post_day_like = db.StringProperty(required = False)
    post_time_like = db.StringProperty(required = False)
    post_word_number_like = db.StringProperty(required = False)
    post_characters_like = db.StringProperty(required = False)
    post_signs_like = db.StringProperty(required = False)
    post_multiple_signs_like = db.StringProperty(required = False)
    post_questions_like = db.StringProperty(required = False)
    post_exclamations_like = db.StringProperty(required = False)
    post_names_like = db.StringProperty(required = False)
    post_emoticons_like = db.StringProperty(required = False)
    
    post_word = db.StringProperty(required = False)
    post_word_like = db.StringProperty(required = False)
    
    post_emoticons_signs = db.StringProperty(required = False)



class BaseHandler(webapp2.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    
    """
    @property
    def current_user(self):   
        """
        In this function the access to the active facebook user is used to mine
        the facebook graph Api. The data is passed on to PostAnalysis for 
        analysis and results are returned and stored in a User object.
        
        """
        
        if self.session.get("user"):
            # User is logged in
            #logging.debug('User is already logged in')
            return self.session.get("user")
        else:
            # Either used just logged in or just saw the first page
            # We'll see here
            #logging.debug('User is NOT logged in')
            cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:
                #logging.debug('Cookie Yes')
                # Okay so user logged in.
                # Now, check to see if existing user
                user = User.get_by_key_name(cookie["uid"])
            
                # Not an existing user so get user info
                graph = facebook.GraphAPI(cookie["access_token"])
                
                profile = graph.get_object("me")
                
                fb_friends = graph.get_connections("me", "friends", limit=100)
                fb_friends_names = ""
                for dat in fb_friends['data']:
                    name = dat['name'].encode("utf-8")
                    fb_friends_names = fb_friends_names + str(name)+ " "
                    
                all_posts = graph.get_connections("me", "posts", limit=100)

                result_dict = PostAnalysis.do_analysis(all_posts, fb_friends_names)
                user = User(
                    key_name=str(profile["id"]),
                    id=str(profile["id"]),
                    name=profile["name"],
                    profile_url=profile["link"],
                    access_token=cookie["access_token"],
                    post_type=str(result_dict["type"]),
                    post_day=str(result_dict["day"]).decode("utf-8"),
                    post_time=str(result_dict["time"]),
                    post_word_number=str(result_dict["word_number"]),
                    post_characters=str(result_dict["characters"]),
                    post_signs=str(result_dict["signs"]),
                    post_multiple_signs=str(result_dict["multiple_signs"]),
                    post_questions=str(result_dict["questions"]),
                    post_exclamations=str(result_dict["exclamations"]),
                    post_names=str(result_dict["names"]),
                    post_emoticons=str(result_dict["emoticons"]),
                    post_like_number=str(result_dict["like_number"]),
                    post_type_like=str(result_dict["type_like"]),
                    post_day_like=str(result_dict["day_like"]),
                    post_time_like=str(result_dict["time_like"]),
                    post_word_number_like=str(result_dict["word_number_like"]),
                    post_characters_like=str(result_dict["characters_like"]),
                    post_signs_like=str(result_dict["signs_like"]),
                    post_multiple_signs_like=str(result_dict["multiple_signs_like"]),
                    post_questions_like=str(result_dict["questions_like"]),
                    post_exclamations_like=str(result_dict["exclamations_like"]),
                    post_names_like=str(result_dict["names_like"]),
                    post_emoticons_like=str(result_dict["emoticons_like"]),
                    post_word = ' '.join(result_dict["words"]),
                    post_word_like = str(result_dict["words_like"]),
                    post_emoticons_signs=' '.join(result_dict["emoticons_signs"])
                    
                    )
                user.put()

                # User is now logged in
                self.session["user"] = dict(
                    name=user.name,
                    profile_url=user.profile_url,
                    id=user.id,
                    access_token=user.access_token,
                    post_type=user.post_type,
                    post_day=user.post_day,
                    post_time=user.post_time,
                    post_word_number=user.post_word_number,
                    post_characters=user.post_characters,
                    post_signs=user.post_signs,
                    post_multiple_signs=user.post_multiple_signs,
                    post_questions=user.post_questions,
                    post_exclamations=user.post_exclamations,
                    post_names=user.post_names,
                    post_emoticons=user.post_emoticons,
                    post_like_number=user.post_like_number,
                    post_type_like=user.post_type_like,
                    post_day_like=user.post_day_like,
                    post_time_like=user.post_time_like,
                    post_word_number_like=user.post_word_number_like,
                    post_characters_like=user.post_characters_like,
                    post_signs_like=user.post_signs_like,
                    post_multiple_signs_like=user.post_multiple_signs_like,
                    post_questions_like=user.post_questions_like,
                    post_exclamations_like=user.post_exclamations_like,
                    post_names_like=user.post_names_like,
                    post_emoticons_like=user.post_emoticons_like,
                    post_word = user.post_word,
                    post_word_like = user.post_word_like,
                    post_emoticons_signs=user.post_emoticons_signs
                )

                return self.session.get("user")
            else:
                #logging.debug('Cookie No')


                return None

    def dispatch(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        return self.session_store.get_session()


class HomeHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(dict(
            facebook_app_id=FACEBOOK_APP_ID,
            current_user=self.current_user
        )))

    def post(self):
        """
            Function to get and set the parameters for calling the put_wall_post from the facebook module
            and thereby create a post on the user facebook wall.
            It is called from html and uses the requested message for setting the message in the post.
            The dictionary "attachment" is updated with a picture/link/video url fetched by the module UrlGetterGoogle                     
        
        """
        message = self.request.get('message')
        #print(message.encode("utf-8"))
        message = message.encode("utf-8")
        
        attachment = {}
        #"name": "Link name", "link": "http://www.example.com/", "caption": "Caption text", "description": "Description Text"

        user = self.session["user"]
        #types: status, link, video, photo, checkin, note, swf, music, question..
        
        if user["post_type"] == "photo":
            search_terms = user["post_word"]
            search_url = UGG.url_from_google(search_terms, user["post_type"])
            attachment.update({"picture": search_url})
            
        elif user["post_type"] == "video" or user["post_type"] == "link":
            search_terms = user["post_word"]
            search_url = UGG.url_from_google(search_terms, user["post_type"])
            attachment.update({"link": search_url})

        graph = facebook.GraphAPI(self.current_user['access_token'])
        graph.put_wall_post(message, attachment, "me")     
        
        self.redirect('http://www.facebook.com/')


class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.session['user'] = None

        self.redirect('/')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication(
    [('/', HomeHandler), ('/logout', LogoutHandler)],
    debug=True,
    config=config
)


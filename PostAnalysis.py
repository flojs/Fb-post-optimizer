# -*- coding: utf-8 -*-
"""
Here data is extracted from facebook and analysed in terms of what features of the posts that seems to give likes.

@author: Louis, Christian
"""
#pip install facebook-sdk

import LikeTextAnalysis as LTA
import time
from operator import itemgetter
import sys

###
#Coverage:
# pip install coverage
# in command window navigate to folder with file to be tested.
# command: coverage run facebookApiTest.py
# command: coverage report -m
# see more: http://nedbatchelder.com/code/coverage/ 
###


def parse_fb_time(fb_time):
    """
    This function  will parse a date/time instance extracted from facebook 
    to a "cleaned up" format. 
    >>> parse_fb_time('2011-12-31T20:42:06+0000')
    ['204206', '2011-12-31']
    
    """
    
    temp_time = ['','']
    date = fb_time.split('T')
    temp_val = date[1].split('+')
    temp_val = temp_val[0].split(':')
    temp_val = temp_val[0] + temp_val[1] + temp_val[2]
    temp_time[0] = temp_val
    temp_time[1] = date[0]
    return temp_time


def get_day_week(date_string):
    """
    This function  will return the day of week of the input date in the form 
    0-6 where monday is 0.
    >>> get_day_week('2011-12-31')
    5
    
    """
    # day of week (Monday = 0) of a given month/day/year
    time1 = time.strptime(date_string,"%Y-%m-%d")
    # year in time_struct t1 can not go below 1970 (start of epoch)!
    time2 = time.mktime(time1)
    return(time.localtime(time2)[6])

def get_time_day(time_string):
    """
    This function divides the day into three periods, 
    returning the period for the input time value.
    >>> get_time_day('054206')
    'Natten (kl. 24-08)'
    
    >>> get_time_day('204206')
    'Aftenen (kl. 16-24)'

    >>> get_time_day('104206')
    'Dagen (kl. 08-16)'
    
    """
    if int(time_string) < 80001:
        return 'Natten (kl. 24-08)'
    elif int(time_string) > 160001:
        return 'Aftenen (kl. 16-24)'
    else:
        return 'Dagen (kl. 08-16)'
  
def calc_average_duplicate_in_list(all_names, all_values):
    """
    This function takes two lists as input 
    (names in one list and values to the names in the other list).
    It averages the values of the equal names, sorts and returns a list of tuples
    >>> calc_average_duplicate_in_list(['status', 'photo', 'photo'],[3,4,1])
    [('status', 3.0), ('photo', 2.5)]
    
    """
    averages = {}
    counts = {}
    for name, value in zip(all_names, all_values):
        if name in averages:
            averages[name] += value
            counts[name] += 1
        else:
            averages[name] = value
            counts[name] = 1
    for name in averages:
        averages[name] = averages[name]/float(counts[name]) 

    sorted_averages = sorted(averages.items(), key=itemgetter(1), reverse=True)
    #print(sorted_averages)
    return sorted_averages
    
def get_potential_emoticons(search_value):
    """
        Function to get a list of emoticons with the nearest emotional value of the input value.  
        
        >>> get_potential_emoticons(2.166666666666)
        [':)', ':*', '(-:', '(:', ':}', ':]', '8)', ':-]', ':-}', ';)', ':-*', ':-)', '8-)', ':->', ':o)', ';-)']
        
    """   
   
    potential_icons = []
    search_value = round(search_value)
    try:
        filename_emoticons = 'Nielsen2011Responsible_emoticon.csv'
        #emot = dict(map(lambda (w, s): (w, int(s)), [ ws.strip().split('\t') for ws in open(filename_emoticons) ]))
        emot = dict([[w, int(s)] for w, s in [ 
                ws.strip().split('\t') for ws in open(filename_emoticons) ]])
                
        for icon, value in emot.iteritems():
            if value == search_value:
                #print icon
                potential_icons.append(icon)
        return potential_icons
    
    except IOError, err:
        sys.stderr.write('Error reading %s: %s' % (filename_emoticons, err[1]))



def do_analysis(all_posts, fb_friends_names):
    """
    This function extracts information for each of the provided posts like:
    -type, message, time, likes
    as well as the text specific through call to the LikeTextAnalysis module.
    It further calculates the average like score of all categories.
    The function returns a dict with the most liked instances of the individual 
    categories calculated with help from the calc_average_duplicate_in_list.
    
    >>> do_analysis({"data": [ { "message": "Nu halvt hello Andersen ses!", "type": "link","created_time": "2013-12-05T09:45:32+0000", "likes": { "data": [ { "id": "523922533","name": "Malene Ertner Andersen" } ]}}]}," Hans Maya Russel")
    {'words': ['!', 'ses', 'hello', 'halvt', 'Andersen'], 'multiple_signs': 0, 'names': 0, 'questions': 0, 'signs': 1, 'exclamations_like': 1.0, 'time_like': 1.0, 'type_like': 1.0, 'questions_like': 1.0, 'emoticons': 0, 'characters_like': 1.0, 'like_number': 1.0, 'emoticons_like': 1.0, 'words_like': [1.0, 1.0, 1.0, 1.0, 1.0], 'type': 'link', 'exclamations': 1, 'signs_like': 1.0, 'word_number': 6, 'characters': 24, 'day': 'Torsdagen', 'names_like': 1.0, 'word_number_like': 1.0, 'emoticons_signs': [], 'day_like': 1.0, 'multiple_signs_like': 1.0, 'time': 'Dagen (kl. 08-16)'}

    case with less than 5 words:    
    >>> do_analysis({"data": [ { "message": "Andersen ses!", "type": "link","created_time": "2013-12-05T09:45:32+0000", "likes": { "data": [ { "id": "523922533","name": "Malene Ertner Andersen" } ]}}]}," Hans Maya Russel")
    {'words': [''], 'multiple_signs': 0, 'names': 0, 'questions': 0, 'signs': 1, 'exclamations_like': 1.0, 'time_like': 1.0, 'type_like': 1.0, 'questions_like': 1.0, 'emoticons': 0, 'characters_like': 1.0, 'like_number': 1.0, 'emoticons_like': 1.0, 'words_like': [], 'type': 'link', 'exclamations': 1, 'signs_like': 1.0, 'word_number': 3, 'characters': 12, 'day': 'Torsdagen', 'names_like': 1.0, 'word_number_like': 1.0, 'emoticons_signs': [], 'day_like': 1.0, 'multiple_signs_like': 1.0, 'time': 'Dagen (kl. 08-16)'}
        
    case with no message and no likes:    
    >>> do_analysis({"data": [ { "description": "Some descriptive text", "type": "link","created_time": "2013-12-05T09:45:32+0000", }]}," Hans Maya Russel")
    {'words': [''], 'multiple_signs': 0, 'names': 0, 'questions': 0, 'signs': 0, 'exclamations_like': 0.0, 'time_like': 0.0, 'type_like': 0.0, 'questions_like': 0.0, 'emoticons': 0, 'characters_like': 0.0, 'like_number': 0.0, 'emoticons_like': 0.0, 'words_like': [], 'type': 'link', 'exclamations': 0, 'signs_like': 0.0, 'word_number': 3, 'characters': 19, 'day': 'Torsdagen', 'names_like': 0.0, 'word_number_like': 0.0, 'emoticons_signs': [], 'day_like': 0.0, 'multiple_signs_like': 0.0, 'time': 'Dagen (kl. 08-16)'}
    
    case with no message and other type:    
    >>> do_analysis({"data": [ { "description": "Some descriptive text", "type": "Check-in","created_time": "2013-12-05T09:45:32+0000", "likes": { "data": [ { "id": "523922533","name": "Malene Ertner Andersen" } ]}}]}," Hans Maya Russel")
    {'words': [''], 'multiple_signs': 0, 'names': 0, 'questions': 0, 'signs': 0, 'exclamations_like': 1.0, 'time_like': 1.0, 'type_like': 1.0, 'questions_like': 1.0, 'emoticons': 0, 'characters_like': 1.0, 'like_number': 1.0, 'emoticons_like': 1.0, 'words_like': [], 'type': 'Check-in', 'exclamations': 0, 'signs_like': 1.0, 'word_number': 0, 'characters': 0, 'day': 'Torsdagen', 'names_like': 1.0, 'word_number_like': 1.0, 'emoticons_signs': [], 'day_like': 1.0, 'multiple_signs_like': 1.0, 'time': 'Dagen (kl. 08-16)'}
     
    """
    
    all_text_words = []
    all_text_words_likes = []

    all_posts_word_number = []
    all_posts_characters = []
    all_posts_signs = []
    all_posts_multiple_signs = []
    all_posts_questions = []
    all_posts_exclamations = []
    all_posts_names = []
    all_posts_emoticons = []

    all_posts_type = []
    all_posts_time = []
    all_posts_day = []
    all_posts_likes = []

    text_analysis = []


    day_list = ["Mandagen", "Tirsdagen", "Onsdagen", "Torsdagen", "Fredagen", "Lørdagen", "Søndagen"]
    
    #data extraction from all_posts
    for data in all_posts['data']:
        post_type = data['type']
        all_posts_type.append(post_type)

        try:
            post_message = data['message']
        except KeyError:
            post_message = None
        #Time
        post_created_time = parse_fb_time(data['created_time'])
        #print("time created: "+str(post_created_time))
        post_time_of_day = get_time_day(post_created_time[0])
        all_posts_time.append(post_time_of_day)
        #print("time of day: "+str(post_time_of_day))
        post_day_of_week = get_day_week(post_created_time[1])
        all_posts_day.append(day_list[post_day_of_week])

        try:
            post_likes = len(data['likes']['data'])
            #print("likes: "+str(post_likes))
        except KeyError:
            post_likes = 0
            #print("likes: "+ str(post_likes))
        all_posts_likes.append(post_likes)

        try:
            post_description = data['description']
            #print("description: "+str(post_description))
        except KeyError:
            post_description = None

        #If the post contains a text message
        if post_message != None:
            text_analysis = LTA.text_calculations(post_message, fb_friends_names)
            all_posts_word_number.append(text_analysis[0])
            all_posts_characters.append(text_analysis[1])
            all_posts_signs.append(text_analysis[2])
            all_posts_multiple_signs.append(text_analysis[3])
            all_posts_questions.append(text_analysis[4])
            all_posts_exclamations.append(text_analysis[5])
            all_posts_names.append(text_analysis[6])
            all_posts_emoticons.append(text_analysis[7])

            all_text_words.extend(text_analysis[8])
            temp_list_w = [post_likes] * len(text_analysis[8])
            all_text_words_likes.extend(temp_list_w)

        #if the post contains a description
        elif post_type == "photo" and post_description != None or post_type == "video" and post_description != None or post_type == "link" and post_description != None:

            text_analysis = LTA.text_calculations(post_description, fb_friends_names)
            all_posts_word_number.append(text_analysis[0])
            all_posts_characters.append(text_analysis[1])
            all_posts_signs.append(text_analysis[2])
            all_posts_multiple_signs.append(text_analysis[3])
            all_posts_questions.append(text_analysis[4])
            all_posts_exclamations.append(text_analysis[5])
            all_posts_names.append(text_analysis[6])
            all_posts_emoticons.append(text_analysis[7])
                   
            all_text_words.extend(text_analysis[8])
            temp_list_w = [post_likes] * len(text_analysis[8])
            all_text_words_likes.extend(temp_list_w)

        else:

            all_posts_word_number.append(0)
            all_posts_characters.append(0)
            all_posts_signs.append(0)
            all_posts_multiple_signs.append(0)
            all_posts_questions.append(0)
            all_posts_exclamations.append(0)
            all_posts_names.append(0)
            all_posts_emoticons.append(0)


    # --- done extracting ---

#    print("all_posts_type: "+str(all_posts_type))
#    print("all_posts_time: "+str(all_posts_time))
#    print("all_posts_day: "+str(all_posts_day))
#    print("all_posts_likes: "+str(all_posts_likes))
#
#    print("all_posts_word_number: " + str(all_posts_word_number))
#    print("all_posts_characters: " + str(all_posts_characters))
#    print("all_posts_signs: " + str(all_posts_signs))
#    print("all_text_num_multiple_signs: " + str(all_posts_multiple_signs))
#    print("all_posts_questions: " + str(all_posts_questions))
#    print("all_posts_exclamations: " + str(all_posts_exclamations))
#    print("all_posts_names: " + str(all_posts_names))
#    print("all_posts_emoticons: " + str(all_posts_emoticons))

    #Calculate what people like:
        
    dict_of_values = {}
    like_number = []

    keys = ['type', 'day', 'time', 'word_number', 'characters', 'signs', 'multiple_signs', 'questions', 'exclamations', 'names', 'emoticons']
    for inst in keys:
        base = "all_posts_" + inst
        base_like = inst + "_like"
        
        most_liked_posts = calc_average_duplicate_in_list(eval(base) , all_posts_likes)
        dict_of_values[inst] = most_liked_posts[0][0]
        dict_of_values[base_like] = most_liked_posts[0][1]
        like_number.append(most_liked_posts[0][1])
        
    dict_of_values["emoticons_signs"] = get_potential_emoticons(dict_of_values['emoticons']) 

    most_liked_words = calc_average_duplicate_in_list(all_text_words, all_text_words_likes)
    #print("most_liked_5_words: %s, %s, %s, %s, %s: " % (most_liked_words[0][0],most_liked_words[1][0],most_liked_words[2][0],most_liked_words[3][0],most_liked_words[4][0] ))

    if len(most_liked_words) > 4:
        word_list = [most_liked_words[0][0], most_liked_words[1][0], most_liked_words[2][0], most_liked_words[3][0], most_liked_words[4][0]]
        word_like_list = [most_liked_words[0][1], most_liked_words[1][1], most_liked_words[2][1], most_liked_words[3][1], most_liked_words[4][1]]
        like_number.extend(word_like_list)
    else:
        word_list = [""]
        word_like_list = []
     
    
    dict_of_values['words'] = word_list
    dict_of_values['words_like'] = word_like_list
    
    dict_of_values['like_number'] = sum(like_number) / len(like_number)
    
    return dict_of_values



import doctest
doctest.testmod()



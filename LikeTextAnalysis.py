# -*- coding: utf-8 -*-

"""
LikeTextAnalysis.py

Uses nltk, regular expressions and a list of emoticons to get some insights on the provided
texts.

This is done to find patterns in when a post get the thump up by other users.

@author: Louis, Christian

"""

from nltk import word_tokenize
import re
import sys

def text_calculations(input_text, fb_friends_names):
    """
    Uses nltk to tokenize and convert to nltk text.
    
    Uses nltk functions and regular expressions to extract information of the
    input text in the forms:
        - 0: Number of words
        - 1: Number of characters in the words (without whitespaces)
        - 2: Number of signs
        - 3: Number of instances of multiple signs
        - 4: If text contains questions
        - 5: If text contains exclamations
        - 6: If text contain the users facebook friends names  
        - 7: The sentiment of the emoticons in the text
        - 8: The words in the text
        
    >>> text_calculations("xD and this :-? is not fun Hans ;-)", "Hans")
    [13, 27, 6, 2, 1, 0, 1, 1.3333333333333333, ['xD', 'and', 'this', ':', '-', '?', 'is', 'not', 'fun', 'Hans', ';', '-', ')']]
    
    """
    

    
    text_data = []    
    
    token_text = word_tokenize(input_text)
    #print(token_text)
    
    #The number of words incl. numbers and signs.
    number_words = len(token_text)
    text_data.append(number_words)
    #print("number_words: %i" % (number_words))  
    
    #The number of characters (without whitespaces) in all words (incl. numbers and signs)
    characters_words = sum([len(each_word) for each_word in token_text])
    text_data.append(characters_words)
    #print("characters_words: %i" % (characters_words))
    
    #number of signs
    signs = re.findall(r'[^\w\s]', input_text) # [not,( Any whitespace character, Any alphanumeric character)]
    text_data.append(len(signs))  
    #print("len(signs): %i - %s " % (len(signs), str(signs)))

    #number of instances of multiple following signs - could be smileys, !!!!!
    multiple_signs = re.findall(r'[^\w\s]{2,}', input_text) # At least 2 repeats of signs.
    text_data.append(len(multiple_signs))    
    #print(multiple_signs)
    #print("len(multiple_signs): %i" % len(multiple_signs))
    
    #If text contains questions based on "?"
    contain_question = re.findall(r'[?]', input_text)
    text_data.append(len(contain_question))
    #print("len(contain_question): %i" % len(contain_question))
    
    #if it contains statements based on "!"
    contain_exclamation = re.findall(r'[!]', input_text)
    text_data.append(len(contain_exclamation))
    #print("len(contain_exclamation): %i" % len(contain_exclamation))
    
    #If the text contain the users facebook friends names 
 
    mentioned_names = find_names(input_text, fb_friends_names)
    contain_user_friends_names = len(mentioned_names)
    text_data.append(contain_user_friends_names)

    #test_string = ":-) and this is not fun ;-)"
    emoticon_score = emoticons(input_text)     
    text_data.append(emoticon_score)
     
    #all the words in the text
    all_nltk_words = [each_word for each_word in token_text]
    text_data.append(all_nltk_words)    

    return text_data
    
def find_names(text_string, search_string):
    """
    Function that takes two strings as input. It finds and returns a list
    of the words in the first string that also are present in the other string.
    
    >>> find_names("Russel and Maya and Russel are there!", " Hans Maya Russel" )
    ['Russel', 'Maya', 'Russel']
    """
    splitted_text = text_string.encode("utf-8").split()
    
    splitted_search = search_string.split()
    
    found_names = [search_word for search_word in splitted_text if search_word in splitted_search]
    return found_names
     

def sentiment(input_text, input_dict):
    """
    Code based on http://finnaarupnielsen.wordpress.com/2011/06/20/simplest-sentiment-analysis-in-python-with-af/ 
        
    Function that takes a text and a dictionary of (in this case emoticons, sentiment)..
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    
    >>> sentiment("xD and this :-? is not fun ;-)", {'xD': 3, ':-?': -1, ';-)': 2} )
    1.3333333333333333
    
    The case if no emoticons are in the text: 
    >>> sentiment("this is not fun ", {'xD': 3, ':-?': -1, ';-)': 2} )
    0
    """
    # Word splitter pattern, simply on spaces
    words = input_text.split()
    sentiments = [input_dict.get(word, 0) for word in words]
    
    emo_counter = 0

    for item in sentiments:
        if item != 0:
            emo_counter = emo_counter + 1
        
    # How should you weight the individual word sentiments? 
    # You could do N, sqrt(N) or 1 for example. 
    # Here we use N != 0.. ..the number of emoticons in the text. 
    if emo_counter == 0:
        sentiments = 0
    else:    
        sentiments = float(sum(sentiments))/emo_counter 
    return sentiments
    
def emoticons(input_text):
    """
    function that extracts the content from a file into a dict. 
    It further user that dict to call the sentiment function. 
    It finally returns the resulting score. 
    
    >>> emoticons("xD and this :-? is not fun ;-)")
    1.3333333333333333
       
    >>> raise IOError()
    Traceback (most recent call last):
      File "C:\Python27\lib\doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.emoticons[1]>", line 1, in <module>
        raise IOError()
    IOError
       
    """
    try:
        filename_emoticons = 'Nielsen2011Responsible_emoticon.csv'
#       With map / lambda 
#       emot = dict(map(lambda (w, s): (w, int(s)), [ 
#                ws.strip().split('\t') for ws in open(filename_emoticons) ]))
        
        emot = dict([[w, int(s)] for w, s in [
                ws.strip().split('\t') for ws in open(filename_emoticons) ]])

        score = sentiment(input_text, emot)
        #print("Emoticon score: %0.2f, text: %s" % (score, input_text))
        return score
    except IOError, err:
        sys.stderr.write('Error reading %s: %s' % (filename_emoticons, err[1]))
        return 0

import doctest
doctest.testmod()
# -*- coding: utf-8 -*-
"""
Containing function to get url from google search of specified type.

@author: Louis, Christian
"""
#import urllib
import urllib2
import json


#searchTerm = "barack obama"

def url_from_google(search_terms, url_type):
    """
        Function to get a url to a photo/link/video from google based on the input words.
        Simply returns the url.
        
        >>> url_from_google("barack obama", "photo")
        u'http://www.whitehouse.gov/sites/default/files/administration-official/ao_image/president_official_portrait_hires.jpg'
        
        >>> url_from_google("barack obama", "link")
        u'http://www.barackobama.com/'
        
        >>> url_from_google("barack obama", "video")
        'http://youtube.googleapis.com/v/geyAFbSDPVk&source=uds&autoplay=1'
    """

    search_terms = search_terms.replace(' ','%20')
       
    if url_type == "photo":
        base_url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
           'v=1.0&q='+search_terms+'&rsz=1')

    elif url_type == "link":
        base_url = ('https://ajax.googleapis.com/ajax/services/search/web?' +
           'v=1.0&q='+search_terms+'&rsz=1')
    
    elif url_type == "video":
        base_url = ('https://ajax.googleapis.com/ajax/services/search/video?' +
           'v=1.0&q='+search_terms+'&rsz=1')
    
    request = urllib2.Request(base_url, None, {'Referer': 'http://www.post-optimizer.appspot.com/'})
    response = urllib2.urlopen(request)
    
    # Process the JSON string.
    results = json.load(response)
    
    r_data = results['responseData']
    r_data_results = r_data['results']

    #example url if no can be found.
    an_url = "https://www.youtube.com/v/Oi1BcouEmio"
    
    for url in r_data_results:
        if url_type == "video":
            an_url = str(url['playUrl'])
            an_url_list = an_url.split("\\")
            an_url = an_url_list[0]
        else:
            an_url = url['unescapedUrl']
            
    return an_url

import doctest
doctest.testmod()
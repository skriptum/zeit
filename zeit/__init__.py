#%%
import requests
import pandas as pd

#%%

# helpful functions

def facetter(response):
    """ takes in the json of a response, returns a time series of the facets""" 

    time_series = pd.Series()
    for a,b in response["facets"]["release_date"].items():
        if type(b) != str:
            date = pd.to_datetime(a)
            count = b
            time_series[date] = count

    time_series = time_series.sort_index()
    return time_series





#%%

#the central API Class
class API():
    def __init__(self):
        self.base_url = "http://api.zeit.de"
        
    
    #general check
    def get_status(self):
        """checks the status of the connection with the api, takes a API-KEY as input
        raises Error when not workin
        """
        header = {"X-Authorization":self.token}
        url = "http://api.zeit.de/client"
        status = requests.get(url, headers = header)

        if status:
            return "everything ok"
        else:
            assert f"something gone wrong, code: {status.status_code}"
    
    #definte the token method
    def set_token(self, api_key):
        """ set the api key, expects key
        raises Error when key is not proper"""
        #check
        check = requests.get(
            "http://api.zeit.de/client", headers = {"X-Authorization":api_key})
        if check:
            self.token = api_key
        else:
            assert "Not a good key"

    #general get function
    def get(self, url = "http://api.zeit.de/content", limit = 10, search = False, time_range = False, fields = False, facet_time = False):
        """ function to get content from the api, really broadly defined
        Arguments: 
            url: content endpoint, default = api.zeit.de/content is standard content endpoint
            limit: number results, default : 10
            search: a specific search string
            time-range: expects tuple of two datetime objects, default False
            fields: return specific fields of the repsonse, expects a list
            facetting = the time frame specified, e.g "1year"

        Returns: 
            pure web response in json format
        """
        header = {"X-Authorization":self.token}

        parameters = {}
        parameters["limit"] = limit

        if search:
            parameters["q"] = search

        if fields:
            parameters["fields"] = f"{*fields,}"
        
        if time_range:
            time1, time2 = time_range[0].isoformat(), time_range[1].isoformat
            parameters["q"] = f'"+search+" AND release_date:[{time1.isoformat()} TO {time2.isoformat()}]'

        if facet_time:
            parameters["facet_date"] = facet_time
        response = requests.get(url, params = parameters, headers = header).json()
        return response


    #specific get functions
    def get_article(self, article_id):
        """ function to get an article by ist article id"""
        url = self.base_url + f"/content/{article_id}"
        response = self.get( url, limit=1)
        return response

    def get_author(self, author_id, limit = 1):
        """ get an author by id, expects a valid author id 
        and optionally a limit on the number of articles"""
        if author_id.startswith("http://"):
            url = author_id
        else:
            url = self.base_url + f"/author/{author_id}"

        response = self.get( url, limit = limit)
        return response

    def get_keyword(self, keyword_id, limit = 1, facet_time = False):
        """ get information about a keyword, expects keyword id and
        optionally a limit on the number of articles returned"""

        if keyword_id.startswith("http://"):
            url = keyword_id
        else:
            url = self.base_url + f"/keyword/{keyword_id}"


        if facet_time:
            response = self.get( url, limit = limit, facet_time=facet_time)
            keyword = Keyword(response)
            keyword.set_facets()
        else:
            response = self.get( url, limit = limit)
            keyword = Keyword(response)

        return keyword


    #search functions 

    def search_for(self, search_string, search_type = "content", limit = 10, time_range = False, facet_time = False):
        """ search the API for a specified string, one word only
            allowed search types = content, keyword, department, author, product author
            allows a time range of the format tuple(time1, time2)
            also allows for facetting by setting a facet_time line '1year' etc.

            returns a Search Class
        """
        string = "*"
        string += search_string
        string += "*"
        url = self.base_url+f"/{search_type}"

        if facet_time:
            response = self.get( url, limit = limit, search = string, time_range=time_range, facet_time=facet_time)
            search = Search(search_string, response)
            search.set_facets()

        else:
            response = self.get( url, limit = limit, search = string, time_range=time_range)
            search = Search(search_string, response)

        return search










#%%
class BaseClass():

    def set_facets(self):
        """ add facets to the object, only works if response has facetting activated """
        try:
            ts = facetter(self.response)
            self.time_series = ts
        except:
            raise Exception("no facets in the response")

    def get_facets(self):
        """ get facets of the object, needs set_facets called before
        returns a pandas time series """
        try:
            return self.time_series
        except:
            raise Exception("you forgot to set facets")

    def has_facets(self):
        """function to see if object has facets or not
        True if it has facets, False if not"""
        try:
            self.time_series
            return True
        except:
            return False


    
#%%
#the simple response class
class Search(BaseClass):
    """ class which makes the response of a search prettier and easier to understand"""
    def __init__(self, search_term, response,):
        self.name = search_term
        self.found = response["found"]
        self.limit = response["limit"]
        self.matches = response["matches"]

        self.response = response
    
    def __repr__(self):
        string = f" Search for '{self.name}': {self.found} results, limit: {self.limit}, matches : \n \n"
        
        for name, match in self.get_matches().items():
            uri = match["uri"]
            string += f"{name}: {uri}\n"
        
        return string

    def get_matches(self):
        """ get the matches of the search result , returns a dictionary
        of type {title:json}"""
        matches = {}

        try: 
            for m in self.matches:
                
                #checks if the matches are articles, which do not have a value field,
                #or anything else
                value = m["value"]
                matches[value] = m
            return matches

        except:
            for m in self.matches:
                title = m["title"]
                matches[title] = m
            return matches
       

    def get_raw(self):
        """ get the pure json of the search"""
        return self.response



# %%

#the keyword class
class Keyword(BaseClass):
    def __init__(self, response):
        """ initialize a keyword instance from a json response""" 
        self.name = response["id"]
        self.uri = response["uri"]
        self.lexical = response["lexical"]
        self.score = response["score"]
        self.type = response["type"]
        self.matches = response["found"]

        #save response for possible later usage
        self.response = response

    def __repr__(self):
        string = f"Keyword: '{self.lexical}' with id '{self.name}',\
        keyword type: '{self.type}' with score {self.score} and {self.matches} matches"
        return string 

    def get_raw(self):
        """ get raw json response of the keyword"""
        return self.response

    def get_articles(self):
        """ get the articles associated with the response,
        only works if there were articles in the initilization
        
        returns a dict of keys : article ids and values : a list of type [title, subtitle, zeitonline link]"""
        articles = {}
        for a in self.response["matches"]:
            id = a["uuid"]
            title = a["title"]
            href = a["href"]
            sub = a["subtitle"]
            articles[id] = [title, sub, href]
        return articles


#%%
#simple article class , todo: web scraper
class Article():
    def __init__(self, response):
        self.title = response["title"]
        self.href = response["href"]
        self.text = response["teaser_text"]
        self.id = response["uuid"]
        self.supertitle = response["supertitle"]

        self.response = response

    def get_keywords(self):
        """ get the keywords linked to the article, returns
        a dict of {"uri":"name", "uri":"name"}"""
        answer = {}
        for i in self.response["keywords"]:
            uri, name = i["uri"], i["name"]
            answer[uri] = name

        return answer

    def get_authors(self):
        """ get the authors linked to the article, returns 
        a dict of {uri:name, uri:name}"""
        answer = {}
        for i in self.response["creators"]:
            uri, name = i["uri"], i["name"]
            answer[uri] = name

        return answer

    def get_date(self):
        """ get release date of the article, returns a pandas timestamp"""
        date = self.response["release_date"]
        date = pd.to_datetime(date)
        return date

    def get_raw(self):
        return self.response


# %%

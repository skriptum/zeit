#%%
import pandas as pd

#%%
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

    def get_raw(self):
        """ get the pure json of the object"""
        return self.response

    def get_matches(self):
        """ extracts the articles of the object, if there were articles in the initilization
        returns a dict in form if {uuid:[title, subtitle, zeitonline link]}
        """
        articles = {}
        for a in self.matches:
            id = a["uuid"]
            title = a["title"]
            href = a["href"]
            sub = a["subtitle"]
            articles[id] = [title, sub, href]

        return articles

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
        
        for uri, tuple in self.get_matches().items():
            desc = tuple[0]
            string += f"{desc}: {uri}\n"
        
        return string

    def get_matches(self):
        """ get the matches of the search result , returns a dictionary
        of type {title: (description, match_json) }"""
        matches = {}

        try: 
            for m in self.matches:
                
                #checks if the matches are articles, which do not have a value field,
                #or anything else
                desc = m["value"]
                uri = m["uri"]
                matches[uri] = (desc, m)
            return matches

        except:
            for m in self.matches:
                desc = m["title"]
                uri = m["uri"]
                matches[uri] = (desc, m)
            return matches





#the keyword class
class Keyword(BaseClass):
    def __init__(self, response):
        """ initialize a keyword instance from a json response""" 
        self.name = response["value"]
        self.uri = response["uri"]
        self.lexical = response["lexical"]
        self.href = response["href"]
        self.score = response["score"]
        self.type = response["type"]
        self.matches = response["matches"]
        self.found = response["found"]

        #save response for possible later usage
        self.response = response

    def __repr__(self):
        string = f"Keyword: '{self.lexical}' with id '{self.name}' \n,\
        keyword type: '{self.type}' with score {self.score} and {self.found} matches \n\n\
        matches: {self.matches}"
        return string 

#%%

class Department(BaseClass):
    def __init__(self, response):
        self.uri = response["uri"]
        self.name = response["value"]
        self.parent = response["parent"]
        self.href = response["href"]
        self.matches = response["matches"]
        self.found = response["found"] 

        self.response = response
    
    def __repr__(self):
        string  = f"Department {self.name} \n Articles: {self.found}; \n uri:{self.uri} \n "
        if self.has_parent():
            string += f"parent : {self.parent}"
        else:
            string += "no parent"
        return string

    def has_parent(self):
        """ check if the department has a parent department """ 
        if self.parent == "":
            return False
        return True
#%%
class Client():
    def __init__(self, response):
        self.name = response["name"]
        self.email = response["email"]
        self.reset = response["reset"]
        self.api_key = response["api_key"]
        self.requests = response["requests"]
        self.quota = response["quota"]

        self.response = response

    def __repr__(self):
        string = f"Client: Client Name: {self.name} \n \
             Client Key: {self.api_key} "

        return string

    def requests_left(self):
        """ function to get the remaining requests left with your key"""
        left = self.quota - self.requests
        return left

    def reset_time(self):
        """ shows the time when the counter will reset"""
        date = pd.to_datetime(self.reset, unit = "s")
        return date

#%%

#simple article class , todo: web scraper
class Article():
    def __init__(self, response):
        self.title = response["title"]
        self.href = response["href"]
        self.text = response["teaser_text"]
        self.id = response["uuid"]
        self.supertitle = response["supertitle"]
        self.uri = response["uri"]

        self.response = response
    
    def __repr__(self):
        string = f"Article with title '{self.title}' UUID: {self.id}, URI: {self.uri}\
            teaser_text: '{self.text}'"
        return string

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
        """ get the raw json of the initilazation"""
        return self.response



import requests
import pandas as pd
from .classes import *

def id_check(id, endpoint = "http://api.zeit.de/content"):
    """ check ids, input id and endpoint like "http://api.zeit.de/content", returns url"""
    if id.startswith("http://"):
        url = id
    else:
        url = f"{endpoint}/{id}"

    return url

#the central API Class
class API():
    def __init__(self):
        self.base_url = "http://api.zeit.de"
        self.token = None
        
    def __repr__(self):
        return f"API Object of zeit-online module"

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
            raise Exception(f"something gone wrong, code: {status.status_code}")
    
    def client(self):
        """ get the complete client request from the API,
        returns a Client Object"""
        url = self.base_url + "/client"
        response = self.get(url)
        cli = Client(response)
        return cli

    #definte the token method
    def set_token(self, api_key):
        """ set the api key, expects key
        raises Error when key is not proper"""
        #check
        check = requests.get(
            "http://api.zeit.de/client", headers = {"X-Authorization":api_key}
            )
        
        if check:
            self.token = api_key
        else:
            raise Exception("Not a good key")


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
            time1, time2 = time_range[0].isoformat(), time_range[1].isoformat()
            if time1[-1] != "Z":
                time1 += "Z"
                time2 += "Z"

            parameters["q"] = f'"{search}" AND release_date:[{time1} TO {time2}]'

        if facet_time:
            parameters["facet_date"] = facet_time
        response = requests.get(url, params = parameters, headers = header).json()
        return response



    #specific get functions
    def get_article(self, article_id):
        """ function to get an article by its article id
        returns a Article Object"""

        endpoint = self.base_url + "/content"
        url = id_check(article_id, endpoint)

        response = self.get( url, limit=1)
        article = Article(response)

        return article

    def get_author(self, author_id, limit = 1):
        """ get an author by id, expects a valid author id 
        and optionally a limit on the number of articles"""
        endpoint = self.base_url + "/author"
        url = id_check(author_id, endpoint)

        response = self.get( url, limit = limit)
        return response

    def get_keyword(self, keyword_id, limit = 1, facet_time = False):
        """ get information about a keyword, expects keyword id and
        optionally a limit on the number of articles returned"""

        endpoint = self.base_url + "/keyword"
        url = id_check(keyword_id, endpoint)

        if facet_time:
            response = self.get( url, limit = limit, facet_time=facet_time)
            keyword = Keyword(response)
            keyword.set_facets()
        else:
            response = self.get( url, limit = limit)
            keyword = Keyword(response)

        return keyword

    def get_department(self, department_id, limit = 1):
        """ get a department by id, returns a Department object"""
        endpoint = self.base_url + "/department"
        url = id_check(department_id, endpoint)

        response = self.get( url, limit=1)
        department = Department(response)

        return department
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















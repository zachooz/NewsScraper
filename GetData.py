import requests as requests


def get(url, jsondata):
    return requests.get(url, params=jsondata)


class Gaurdian(object):
    def __init__(self,
                 api_key="",
                 search_endpoint="https://content.guardianapis.com/search"):
        self.api_key = api_key
        self.search_endpoint = search_endpoint

    '''
    string q: the query
    string from_date: year-month-day
    string to_date: year-month-day
    
    out:
    Response from api get request. Doc found on Gaurdian dev website.
    '''
    def guardian_get(self,
                     q,
                     from_date,
                     to_date,
                     page,
                     url=None,
                     api_key=None,
                     page_size=50):
        # default
        if url is None:
            url = self.search_endpoint
        if api_key is None:
            api_key = self.api_key

        # create jsondata
        jsondata = {}
        if q is not None and q != "":
            jsondata = {
                "api-key": api_key,
                "q": q,
                "from-date": from_date,
                "to-date": to_date,
                "page": page,
                "page-size": page_size
            }
        else:
            jsondata = {
                "api-key": api_key,
                "from-date": from_date,
                "to-date": to_date,
                "page": page,
                "page-size": page_size
            }
        # request
        return get(url, jsondata).json()

    
class Alphavantage(object):
    def __init__(self, api_key="", search_endpoint="https://www.alphavantage.co/query"):
        self.api_key = api_key
        self.search_endpoint = search_endpoint

    def alpha_vantage_get(self,
                          company_symbol,
                          url=None,
                          api_key=None,
                          function="TIME_SERIES_DAILY",
                          outputsize="full",
                          datatype="json"):
        if url is None:
            url = self.search_endpoint
        if api_key is None:
            api_key = self.api_key

        jsondata = {
            "apikey": api_key,
            "function": function,
            "symbol": company_symbol,
            "datatype": datatype,
            "outputsize": outputsize
        }
        ret = get(url, jsondata).json()
        return ret

    '''
    input: alpha_vantage_get data
    output: list of tuples:
    [
        (
            'yr-month-day',
            {
            '1. open': 'val',
            '2. high': 'val',
            '3. low' : 'val',
            '4. close' : 'val',
            '5. volume' : 'val';'
            }
        ), ....
    ]
    '''
    def stock_data_to_list(self, stock_data):
        stock_dic = stock_data['Time Series (Daily)']
        return tuple(stock_dic.items())

    '''
    input: stock_data_to_list data
    output: list of lists:
    [
        [
        string yr-month-day,
        float open,
        float high,
        float low,
        float close,
        float volume
        ], .....
    ]
    '''
    def parse_stock_list(self, stock_data):
        output = []
        for data in stock_data:
            element = []
            element.append(data[0])
            stock_data_vals = list(data[1].values())
            for value in stock_data_vals:
                element.append(float(value))
            output.append(element)
        return output
    '''
    input: alpha_vantage_get data
    output: list of lists:
    [
     [
     string yr-month-day,
     float open,
     float high,
     float low,
     float close,
     float volume
     ], ...
    ]
    '''
    def full_parse(self, stock_data):
        return self.parse_stock_list(self.stock_data_to_list(stock_data))
  

class NYT(object):
    def __init__(self,
                 archive_api_key="",
                 archive_endpoint="https://api.nytimes.com/svc/archive/v1/"):
        self.archive_api_key = archive_api_key
        self.archive_endpoint = archive_endpoint

    '''
    int year: > 1990
    int month: 1-12
    
    out:
    Response from api get request. Doc found on NYT dev website.
    '''
    def archive_get(self,
                    year,
                    month,
                    api_key=None):
        # default
        if api_key is None:
            api_key = self.archive_api_key

        # create jsondata
        jsondata = {
            "api-key": api_key,
        }
        # request
        return get(self.archive_endpoint+str(year)+"/"+str(month)+".json", jsondata).json()

import requests
from datetime import datetime
import pyrebase

ALPACA_HOST = 'https://data.alpaca.markets'
alpaca_session = requests.Session()
alpaca_session.headers["APCA-API-KEY-ID"] = 'PK9SPEPNIYHXF6MH3PQI'
alpaca_session.headers["APCA-API-SECRET-KEY"] = 'zMU0UivOioKFg8WTFKMk7mAPcrVbqvTm6FNeVAWJ'

ALPHAV_HOST = 'https://www.alphavantage.co/query'
alphav_session = requests.Session()
alphav_session.params["apikey"] = '29GR5RNIYPUF47T1'

NEWSAPI_HOST = 'https://newsapi.org/v2'
newsapi_session = requests.Session()
newsapi_session.params["apiKey"] = 'd65c94e8083e4fa8b1f1a8d3a2ab8ebe'


firebaseConfig = {
    'apiKey': "AIzaSyAu2Jbm6u_u3D9DuZ52K0aeSlInRfNhSxo",
    'authDomain': "finneas-ca058.firebaseapp.com",
    'databaseURL': "https://finneas-ca058.firebaseio.com",
    'projectId': "finneas-ca058",
    'storageBucket': "finneas-ca058.appspot.com",
    'messagingSenderId': "345418517191",
    'appId': "1:345418517191:web:1f83b7964ff713d23b0ce2"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

def query_db(symbol):
    all_symbols = database.child('companies').get()
    all_symbols = all_symbols.val().keys()
    if symbol in list(all_symbols):
        return True
    return False

def get_company_name(symbol):
    data = database.child('companies').child(symbol).get()
    name = data.val()['name']
    print('name', name)
    return name 
    


options = {
    'alpaca':alpaca_session.get,
    'newsapi':newsapi_session.get,
    'alphav':alphav_session.get
}


def _get_data(API, url, params=None):
    response = options[API](url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.raise_for_status()


def get_historical_1(request):
    '''

    Returns historical open, high, low, close (for charting you use the closing price).
    Timespan can be either minute or 1Min, 5Min, 15Min, day or 1D.
    Limit is maximum number of data points.
    request = {
        'symbol':'AAPL',
        'timespan':'day',
        'from':'2020-01-01',
        'to':'2019-02-01',
        'limit':500
    }
    '''
    url     = f"{ALPACA_HOST}/v1/bars/{request['timespan']}"
    params  = {
        'symbols':request['symbol'],
        'limit':request['limit']
    }
    #'limit': request['limit'],
    #'end':request['to']
    raw_data = _get_data('alpaca', url, params)
    data = raw_data[request['symbol']]
    new_data = []
    for d in data:
        #T%H:%M:%S
        #.strftime('%Y-%m-%d')
        new = {
            'Date':datetime.fromtimestamp(d['t']).strftime('%Y-%m-%d %H:%M:%S'),

            'Open':d['o'],
            'High':d['h'],
            'Low':d['l'],
            'Close':d['c'],
            'Volume':d['v']
        }
        new_data.append(new)
        #d['t'] = datetime.utcfromtimestamp(d['t']).strftime('%Y-%m-%dT%H:%M:%S')
    return new_data
# General financial data

def get_historical(request):
    '''

    Returns historical open, high, low, close (for charting you use the closing price).
    Timespan can be either minute or 1Min, 5Min, 15Min, day or 1D.
    Limit is maximum number of data points.
    request = {
        'symbol':'AAPL',
        'timespan':'day',
        'from':'2020-01-01',
        'to':'2019-02-01',
        'limit':500
    }
    '''
    url     = f"{ALPACA_HOST}/v1/bars/{request['timespan']}"
    params  = {
        'symbols':request['symbol'],
        'start':request['from'],
        'end':request['to']
    }
    #'limit': request['limit'],
    #'end':request['to']
    raw_data = _get_data('alpaca', url, params)
    data = raw_data[request['symbol']]
    new_data = []
    for d in data:
        #T%H:%M:%S
        #.strftime('%Y-%m-%d')
        new = {
            'Date':datetime.fromtimestamp(d['t']).strftime('%Y-%m-%d %H:%M:%S'),

            'Open':d['o'],
            'High':d['h'],
            'Low':d['l'],
            'Close':d['c'],
            'Volume':d['v']
        }
        new_data.append(new)
        #d['t'] = datetime.utcfromtimestamp(d['t']).strftime('%Y-%m-%dT%H:%M:%S')
    return new_data

def get_historical_2(request):
    '''

    Returns historical open, high, low, close (for charting you use the closing price).
    Timespan can be either minute or 1Min, 5Min, 15Min, day or 1D.
    Limit is maximum number of data points.
    request = {
        'symbol':'AAPL',
        'timespan':'day',
        'from':'2020-01-01',
        'to':'2019-02-01',
        'limit':500
    }
    '''
    url     = f"{ALPACA_HOST}/v1/bars/{request['timespan']}"
    params  = {
        'symbols':request['symbol'],
        'start':request['from'],
        'end':request['to']
    }
    raw_data = _get_data('alpaca', url, params)
    data = raw_data[request['symbol']]
    new_data = []
    for d in data:
        new = {
            'Date':datetime.fromtimestamp(d['t']).isoformat(), #.strftime("%d %b %Y %H:%M"),

            'Open':d['o'],
            'High':d['h'],
            'Low':d['l'],
            'Close':d['c'],
            'Volume':d['v']
        }
        new_data.append(new)
    return new_data

def get_company_overview(request):
    '''
    Returns company data like description, exchange it trades at, market cap, etc
    request = {
        'symbol':'AAPL'
    }
    '''
    url     = ALPHAV_HOST
    params  = {
        'function':'OVERVIEW',
        'symbol':request['symbol']
    }
    return _get_data('alphav', url, params)


def get_last_price(request):
    '''
    Returns last price
    request = {
        'symbol':'AAPL'
    }
    '''
    url     = f"{ALPACA_HOST}/v1/last/stocks/{request['symbol']}"
    response = _get_data('alpaca', url)
    data = {}
    data['Symbol'] = request['symbol']
    data['Last Price'] = response['last']['price']
    dt = int(str(response['last']['timestamp'])[:10])
    data['Timestamp'] = dt
    return data

    
def get_last_quote(request):
    '''
    Returns last bid and ask
    request = {
        'symbol':'AAPL'/
    }
    '''
    url     = f"{ALPACA_HOST}/v1/last_quote/stocks/{request['symbol']}"
    return _get_data('alpaca', url)


# Financial Statements

def get_IS(request):
    '''
    Returns Income Statement
    request = {
        'symbol':'AAPL'
    }
    '''
    url     = ALPHAV_HOST
    params  = {
        'function':'INCOME_STATEMENT',
        'symbol':request['symbol']
    }
    return _get_data('alphav', url, params)


def get_BS(request):
    '''
    Returns Balance Sheet
    request = {
        'symbol':'AAPL'
    }
    '''
    url     = ALPHAV_HOST
    params  = {
        'function':'BALANCE_SHEET',
        'symbol':request['symbol']
    }
    return _get_data('alphav', url, params)


def get_CS(request):
    '''
    Returns Cash Flow Statement
    request = {
        'symbol':'AAPL'
    }
    '''
    url     = ALPHAV_HOST
    params  = {
        'function':'CASH_FLOW',
        'symbol':request['symbol']
    }
    return _get_data('alphav', url, params)

            

# News

def get_general_news(request):
    '''
    Returns general business news from the US.
    request = {
        'from':'2020-10-15T15:30:39'
        'size':50
    }
    '''
    url     = f"{NEWSAPI_HOST}/top-headlines"
    params  = {
        'country':'us',
        'category':'business',
        #'from':request['from']
        'pageSize':request['size']
    }
    response = _get_data('newsapi', url, params)
    data = []
    articles = response['articles']
    for article in articles:
        data_point = {}
        data_point['data'] = {
            'Source':article['source']['name'],
            'Title':article['title'],
            'Description':article['description'],
        }
        data_point['support'] = {
            'URL':article['url']
        }
        data.append(data_point)
    return data
        
def get_company_news(request):
    '''
    Returns company news.
    request = {
        'symbol':'AAPL',
        'from':'2020-10-15T15:30:39'
    }
    '''
    url     = f"{NEWSAPI_HOST}/everything"
    params  = { 
        'language':'en',
        'q':request['symbol'],
        'qInTitle':request['symbol'],
        'pageSize':request['size'],
        'sortBy':'relevance'
    }
    # 'from':request['from']
    response = _get_data('newsapi', url, params)
    data = []
    articles = response['articles']
    for article in articles:
        data_point = {}
        data_point['data'] = {
            'Source':article['source']['name'],
            'Title':article['title'],
            'Description':article['description'],
        }
        data_point['support'] = {
            'URL':article['url']
        }
        # data_point['Source'] = article['source']['name']
        # data_point['Title'] = article['title']
        # data_point['Description'] = article['description']
        # data_point['URL'] = article['url']
        data.append(data_point)
    return data


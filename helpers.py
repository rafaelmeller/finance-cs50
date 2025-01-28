import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    ''' 
    OLD VERSION (CS50)
    f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
    f"?period1={int(start.timestamp())}"
    f"&period2={int(end.timestamp())}"
    f"&interval=1d&events=history&includeAdjustedClose=true"
    '''

    url = (
        f"https://query2.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history"
    )

    # DEBUG: Print the URL
    print(f"Request URL: {url}")

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # DEBUG: Print the response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        # Adapt from JSON to list of dictionaries
        quotes= conv_json(response)

        '''
        CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        '''

        # Extract the latest price
        price = round(float(quotes[-1]["adjclose"]), 2)
        return {"price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError) as e:
        # Debug: Print the exception
        print(f"Exception: {e}")
        return None

def conv_json(resp):
    j = resp.json()
    timestamps = j['chart']['result'][0]['timestamp']
    quotes = j['chart']['result'][0]['indicators']['quote'][0]
    adjclose = j['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

    data = []
    for i in range(len(timestamps)):
        data.append({
            'timestamp': timestamps[i],
            'open': quotes['open'][i],
            'high': quotes['high'][i],
            'low': quotes['low'][i],
            'close': quotes['close'][i],
            'volume': quotes['volume'][i],
            'adjclose': adjclose[i]
        })

    return data

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

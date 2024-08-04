from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StockForm
from .models import Stock


def get_stock_quote(ticker: str):
    # import datetime
    import re
    import os

    import requests

    error_response: str = ""
    company_response: dict = {}
    latest_timeseries_data: dict = {}
    past_timeseries_data: dict = {}
    stock_quote: dict = {}
    # aday = datetime.datetime.now() + datetime.timedelta(days=1)
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")
    try:
        company_response = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={str(ticker).upper()}&apikey={api_key}"
        ).json()
        # timeseries_response = requests.get(
        #     "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
        # ).json()

        stock_quote_response = requests.get(
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={str(ticker).upper()}&apikey={api_key}"
        ).json()

        if stock_quote_response:
            stock_quote = stock_quote_response.get("Global Quote")
            stock_quote = dict(map(
                lambda x: (re.sub(r"^\d+\. |\s+", "", x[0]), x[1]),
                stock_quote.items()
            ))

        # while not latest_timeseries_data:
        #     aday = aday - datetime.timedelta(days=1)
        #     latest_timeseries_data = timeseries_response["Time Series (Daily)"].get(aday.strftime("%Y-%m-%d"))

        # aday = aday - datetime.timedelta(days=1)
        # past_timeseries_data = timeseries_response["Time Series (Daily)"].get(aday.strftime("%Y-%m-%d"))

        # if latest_timeseries_data:
        #     latest_timeseries_data = dict(map(
        #         lambda x: (re.sub(r"^\d+\. ", "", x[0]), x[1]), latest_timeseries_data.items()
        #     ))

        # if past_timeseries_data:
        #     past_timeseries_data = dict(map(lambda x:
        #       (re.sub(r"^\d+\. ", "", x[0]), x[1]), past_timeseries_data.items()))
    except Exception as ex:
        error_response = f"Error: {ex}"

    return {
        "company_response": company_response,
        "latest_timeseries_data": latest_timeseries_data,
        "past_timeseries_data": past_timeseries_data,
        "stock_quote": stock_quote,
        "error": error_response,
    }


# Create your views here.
def home(request):
    # import datetime
    import re
    import os

    import requests

    if request.method == "POST":
        ticker = request.POST.get("ticker")
    else:
        return render(request, "home.html", {"welcome_message": "Enter ticket synmbol to get stock data..."})

    return render(
        request,
        'home.html',
        get_stock_quote(ticker=ticker),
    )

def about(request):
    return render(request, 'about.html', {})

def add_stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added successfully!")
            return redirect("add_stocks")
    else:
        tickers = Stock.objects.all()
        tickers_metadata: dict = []
        for ticker in tickers:
            stock_quote = get_stock_quote(ticker=ticker)
            stock_quote["ticker"] = str(ticker).upper()
            stock_quote["id"] = ticker.id
            tickers_metadata.append(stock_quote)

        return render(
            request,
            "add_stocks.html",
            {"tickers": tickers, "tickers_metadata": tickers_metadata}
        )
    
def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted successfully!")
    return redirect("add_stocks")

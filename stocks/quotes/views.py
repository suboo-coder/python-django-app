from django.shortcuts import render

# Create your views here.
def home(request):
    import datetime
    import re

    import requests

    if request.method == "POST":
        ticker = request.POST.get("ticker")
    else:
        return render(request, "home.html", {"welcome_message": "Enter ticket synmbol to get stock data..."})

    error_response: str = ""
    company_response: dict = {}
    latest_timeseries_data: dict = {}
    past_timeseries_data: dict = {}
    stock_quote: dict = {}
    aday = datetime.datetime.now() + datetime.timedelta(days=1)
    try:
        company_response = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=demo"
        ).json()
        # timeseries_response = requests.get(
        #     "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
        # ).json()

        stock_quote_response = requests.get(
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey=demo"
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

    return render(
        request,
        'home.html',
        {
            "company_response": company_response,
            "latest_timeseries_data": latest_timeseries_data,
            "past_timeseries_data": past_timeseries_data,
            "stock_quote": stock_quote,
            "error": error_response,
        },
    )

def about(request):
    return render(request, 'about.html', {})

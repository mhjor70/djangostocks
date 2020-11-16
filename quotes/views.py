from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm


# Create your views here.
# Stockquote api pk_3915e6fe527140fab09763d5570ee0de
def home(request):
    import requests
    import json
    if request.method == 'POST':
        ticker = str(request.POST['ticker'])
        ticker = ticker.upper()
        urlpre = 'https://cloud.iexapis.com/stable/stock/'
        urlpost = "/quote?token=pk_3915e6fe527140fab09763d5570ee0de"
        urlfull = urlpre + ticker + urlpost
        api_request = requests.get(urlfull)
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."

        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Please enter a ticker in the search"})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    
    if request.method == 'POST':
        ticker = str(request.POST['ticker'])
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Stock has been added '))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        import requests
        import json
        output = []
        for ticker_item in ticker:
            #ticker = ticker_item.upper()
            urlpre = 'https://cloud.iexapis.com/stable/stock/'
            urlpost = "/quote?token=pk_3915e6fe527140fab09763d5570ee0de"
            urlfull = urlpre + str(ticker_item) + urlpost
            api_request = requests.get(urlfull)
            api_result = json.loads(api_request.content)
            output.append(api_result)
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock has been deleted'))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})

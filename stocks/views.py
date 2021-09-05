from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import Stock


@login_required(login_url='/authentication/login')
def index(request):
    user = request.user

    if(user.is_superuser):
        stocks = Stock.objects.all()
    else:
        stocks = Stock.objects.filter(owner=user)

    paginator = Paginator(stocks, 10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'stocks/index.html', context)


@login_required(login_url='/authentication/login')
def add_stock(request):
    try:
        stocks = Stock.objects.all()
        context = {
            'values': request.POST
        }
        if request.method == 'GET':
            return render(request, 'stocks/add_stock.html', context)

        if request.method == 'POST':
            stock_id = request.POST['stock_id']
            stock_name = request.POST['stock_name']

            if not stock_name:
                messages.error(request, 'Name is required')
                return render(request, 'stocks/add_stock.html', context)

            stock_count = stocks.filter(name__iexact = stock_name).count()
            if(stock_count == 1):
                messages.error(request, 'Stock Name already present')
                return render(request, 'stocks/add_stock.html', context)
                
            try:
                Stock.objects.create(owner=request.user, id=stock_id, name=stock_name)
            except IntegrityError as e:
                messages.error(request, 'Invalid Input, Try again!')

            messages.success(request, 'Stock saved successfully')

            return redirect('stocks')
    except Exception as e:
        messages.error(request, f'Something went wrong while adding stock : {e}')
        return redirect('stocks')


@login_required(login_url='/authentication/login')
def edit_stock(request, id):
    try:
        stocks = Stock.objects.all()
        stock = Stock.objects.get(pk=id)

        context = {
            'stock': stock,
        }

        if request.method == 'GET':
            return render(request, 'stocks/edit_stock.html', context)

        if request.method == 'POST':
            stock_name = request.POST['stock_name']
            stock_id = request.POST['stock_id']

            if not stock_name:
                messages.error(request, 'Name is required')
                return render(request, 'stocks/edit_stock.html', context)
            
            user = request.user
            stock.id = stock_id
            stock.name = stock_name
            stock.owner = user

            stock.save()
            messages.success(request, f'{stock_name} updated  successfully')
            return redirect('stocks')
    except Exception as e:
        messages.error(request, f'Something went wrong while editing stock : {e}')
        return redirect('stocks')


def delete_stock(request, id):
    try:
        stock = Stock.objects.get(pk=id)
        if request.method == 'POST':
            stock.delete()
            messages.success(request, 'Stock Deleted')
            return redirect('stocks')

        return render(request, 'partials/_delete_item.html', {'item' : stock})
    except Exception as e:
        messages.error(request, f'Something went wrong while deleting stock : {e}')
        return redirect('stocks')

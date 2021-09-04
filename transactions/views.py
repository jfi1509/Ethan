from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import IntegrityError, DataError

from transactions.models import Transaction
from stocks.models import Stock


@login_required(login_url='/authentication/login')
def dashboard(request):
    return redirect('transactions')


@login_required(login_url='/authentication/login')
def index(request):
    user = request.user

    if(user.is_superuser):
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.filter(owner=user)

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'transactions/index.html', context)


@login_required(login_url='/authentication/login')
def add_transaction(request):
    try:
        transactions = Transaction.objects.all()
        stocks = Stock.objects.all()
        error_msg = ''

        context = {
            'values': request.POST,
            'stocks': stocks
        }
        if request.method == 'GET':
            return render(request, 'transactions/add_transaction.html', context)

        if request.method == 'POST':
            post_data = request.POST
            stock_name = post_data['stock_name']
            stock_price = post_data['stock_price']
            stock_quantity = post_data['stock_quantity']
            transaction_date = post_data['transaction_date']
            transaction_id = post_data['transaction_id']

            if not transaction_date:
                error_msg = 'Date is required'

            if not stock_quantity:
                error_msg = 'Quantity is required'

            if not stock_price:
                error_msg = 'Price is required'

            if not transaction_id:
                error_msg = 'ID is required'
            
            if error_msg != '':
                messages.error(request, error_msg)
                return render(request, 'transactions/add_transaction.html', context)

            stock = stocks.filter(name__iexact = stock_name).first()
        
            try:
                Transaction.objects.create( 
                    id=transaction_id,
                    date=transaction_date,
                    stock_id=stock,
                    stock_name=stock,
                    stock_price=stock_price,
                    stock_quantity=stock_quantity,
                    owner=request.user
                )
            except IntegrityError as e:
                messages.error(request, 'Invalid Input, Try again!')
                return render(request, 'transactions/add_transaction.html', context)
            except DataError as de:
                messages.error(request, 'ID should less than or equal to 20 characters')
                return render(request, 'transactions/add_transaction.html', context)

            messages.success(request, 'Transaction saved successfully')

            return redirect('transactions')

    except Exception as e:
        messages.error(request, f'Something went wrong while adding transaction : {e}')
        return redirect('transactions')

@login_required(login_url='/authentication/login')
def edit_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
        stocks = Stock.objects.all()
        error_msg = ''

        context = {
            'transaction': transaction,
            'stocks': stocks
        }

        if request.method == 'GET':
            return render(request, 'transactions/edit_transaction.html', context)

        if request.method == 'POST':
            post_data = request.POST
            stock_name = post_data['stock_name']
            stock_price = post_data['stock_price']
            stock_quantity = post_data['stock_quantity']
            transaction_date = post_data['transaction_date']
            transaction_id = post_data['transaction_id']

            if not transaction_date:
                error_msg = 'Date is required'

            if not stock_quantity:
                error_msg = 'Quantity is required'

            if not stock_price:
                error_msg = 'Price is required'
            
            if error_msg != '':
                messages.error(request, error_msg)
                return render(request, 'transactions/edit_transaction.html', context)

            stock = stocks.filter(name__iexact = stock_name).first()

            transaction.id = transaction_id
            transaction.date = transaction_date
            transaction.stock_id = stock
            transaction.stock_name = stock
            transaction.stock_price = stock_price
            transaction.stock_quantity = stock_quantity
            transaction.owner = request.user

            transaction.save()

            messages.success(request, 'Transaction updated successfully')
            return redirect('transactions')
    except Exception as e:
        messages.error(request, f'Something went wrong while editing transaction : {e}')
        return redirect('transactions')



def delete_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
        transaction.delete()
        messages.success(request, 'Transaction Deleted')
    except Exception as e:
        messages.error(request, f'Something went wrong while deleting transaction : {e}')
    finally:
        return redirect('transactions')

import json

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth


class EmailValidationView(View):
    def post(self, request):
        # load the request body
        data = json.loads(request.body)
        email = data['email']
        # using validate_email to validate the emails
        if not validate_email(email):
            # sending JSON response with status codes
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            # Resource already allocated status code
            return JsonResponse({'email_error': 'Sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        # Check for only alphanumeric values in the username
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        
        # Check if the username if already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, Username in use, choose another one!'}, status=409)
        
        # If username is valid
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Extracting data from POST call
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        # Check if user exists or not
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                # password validation
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                # Creating the user
                user = User.objects.create_user(username=username, email=email)
                # setting password
                user.set_password(password)
                # by default, user will not be active
                user.is_active = False
                # saving the user instance
                user.save()

                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        # pulling data from POST request
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            # Validations
            if user:
                if user.is_active:
                    auth.login(request, user)
                    # Login successful
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('transactions')

                return render(request, 'authentication/login.html')
            # Incorrect Credentials
            messages.error(request, 'Invalid Credentials, Try again!')
            return render(request, 'authentication/login.html')

        # Login form not complete
        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        # logging out the user
        auth.logout(request)
        # proper messaging for better UX
        messages.success(request, 'You have been logged out')
        # Redirecting to the login page
        return redirect('login')
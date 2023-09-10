from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Author
from .forms import AuthorForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .mail import send_confirmation_mail, send_password_reset_mail
from django.utils.crypto import get_random_string
from django.utils import timezone


# Author @login_required decorator
def login_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            # get token from session
            token = request.session['token']
            author = Author.objects.get(login_token=token)
            if author.login_token_expires_at < timezone.now():
                return redirect('/author/login')
            return func(request, *args, **kwargs)
        except:
            return redirect('/author/login')
    return wrapper

# Author Registration View
class AuthorRegistrationView(View):

    # GET request
    def get(self, request):
        form = AuthorForm()
        return render(request, 'author/author_registration.html', {'form': form})
    
    # POST request
    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # generate token for email verification
        token = get_random_string(length=32)
        if Author.objects.filter(email=email).exists():
            return render(request, 'author/author_registration.html', {'error': 'Email already exists'})
        
        # password hashing
        value = {
            'name': name,
            'email': email,
            'password': make_password(password),
            'token': token
        }
        form = Author(**value)
        form.save()
        user = {'email': email, 'name': name}
        
        # send mail
        send_confirmation_mail(user, token)
        return render(request, 'author/author_registration.html', {'success': 'Registration Successful, Please confirm your email'})
    

# Author Login View
class AuthorLoginView(View):

    # GET request
    def get(self, request):
        return render(request, 'author/author_login.html')
  
    # POST request
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Author.objects.get(email=email)
            if check_password(password, user.password):
                if user.is_confirmed == False:
                    return render(request, 'author/author_login.html', {'error': 'Please confirm your email'})
                else:
                    # generate token for session
                    token = get_random_string(length=32)
                    user.login_token = token
                    # set token in session
                    request.session['token'] = token
                    # set token expiry time to 30 minutes
                    user.login_token_expires_at = timezone.now() + timezone.timedelta(minutes=30)
                    user.save()
                    return render(request, 'author/author_dashboard.html')
            else:
                return render(request, 'author/author_login.html', {'error': 'Invalid Credentials'})
        except:
            return render(request, 'author/author_login.html', {'error': 'Invalid Credentials'})
        

# Author Email Confirmation View
class AuthorEmailConfirmationView(View):
        
        # GET request
        def get(self, request, token):
            try:
                user = Author.objects.get(token=token)
                if user.is_confirmed == True:
                    return render(request, 'author/author_email_confirmation.html', {'success': 'Email already confirmed'})
                user.is_confirmed = True
                user.save()
                return render(request, 'author/author_email_confirmation.html', {'success': 'Email confirmed'})
            except:
                return render(request, 'author/author_email_confirmation.html', {'error': 'Invalid Token'})
            

# Author Resend Confirmation Mail View
class AuthorResendConfirmationMailView(View):
        
        # GET request
        def get(self, request):
            return render(request, 'author/author_resend_confirmation_mail.html')
        
        # POST request
        def post(self, request):
            email = request.POST['email']
            try:
                user = Author.objects.get(email=email)
                if user.is_confirmed == True:
                    return render(request, 'author/author_resend_confirmation_mail.html', {'error': 'Email already confirmed'})
                else:
                    token = get_random_string(length=32)
                    user.token = token
                    user.save()
                    name = user.name
                    user = {'email': email, 'name': name}
                    send_confirmation_mail(user, token)
                    return render(request, 'author/author_resend_confirmation_mail.html', {'success': 'Confirmation mail sent'})
            except:
                return render(request, 'author/author_resend_confirmation_mail.html', {'error': 'Email does not exist'})
            

# Author Forgot Password View
class AuthorForgotPasswordView(View):
            @login_required
            # GET request
            def get(self, request):
                return render(request, 'author/author_forgot_password.html')
            
            # POST request
            def post(self, request):
                email = request.POST['email']
                try:
                    user = Author.objects.get(email=email)
                    if user.is_confirmed == False:
                        return render(request, 'author/author_forgot_password.html', {'error': 'Please confirm your email'})
                    else:
                        token = get_random_string(length=32)
                        user.password_reset_token = token
                        user.password_reset_token_expires_at = timezone.now() + timezone.timedelta(minutes=15)
                        user.save()
                        name = user.name
                        user = {'email': email, 'name': name}
                        send_password_reset_mail(user, token)
                        return render(request, 'author/author_forgot_password.html', {'success': 'Password reset mail sent'})
                except:
                    return render(request, 'author/author_forgot_password.html', {'error': 'Email does not exist'})
                

# Author Reset Password View
class AuthorResetPasswordView(View):
    # GET request
    def get(self, request, token):
        try:
            user = Author.objects.get(password_reset_token=token)
            if user.password_reset_token_expires_at < timezone.now():
                return render(request, 'author/author_reset_password.html', {'error': 'Link expired'})
            else:
                return render(request, 'author/author_reset_password.html', {'change_password': 'true', 'token': token})
        except:
            return render(request, 'author/author_reset_password.html', {'error': 'Invalid Token'})
        
    # POST request
    def post(self, request, token):
        
        password = request.POST['password']
        try:
            user = Author.objects.get(password_reset_token=token)
            if user.password_reset_token_expires_at < timezone.now():
                return HttpResponse('Link expired')
            else:
                user.password = make_password(password)
                user.password_reset_token = None
                user.password_reset_token_expires_at = None
                user.save()
                return render(request, 'author/author_reset_password.html', {'success': 'Password changed successfully'})
        except:
            return render(request, 'author/author_reset_password.html', {'error': 'Invalid Token'})
        





# Author Dashboard View
class AuthorDashboardView(View):
    # GET request
    @login_required
    def get(self, request):
        return render(request, 'author/author_dashboard.html')
    

# Author Sample View
@login_required
def sample(request):
    return HttpResponse('Sample View')


    


# index template
class index(TemplateView):
    template_name = 'index.html'
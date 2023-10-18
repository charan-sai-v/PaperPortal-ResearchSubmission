from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Author, Contact, Paper
from .forms import AuthorForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .mail import send_confirmation_mail, send_password_reset_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from maineditor.models import Conference


def login_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            # get token from session
            token = request.session['token']
            print(token)
            author = Author.objects.get(login_token=token)
            if author.login_token_expires_at < timezone.now():
                return redirect('/author/login')
            return func(request, author, *args, **kwargs)
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
        confirm_pasword = request.POST['confirm_password']

        # check if password and confirm password are same
        if password != confirm_pasword:
            return render(request, 'author/author_registration.html', {'error': 'Password and Confirm Password are not same'})

        if Author.objects.filter(email=email).exists():
            return render(request, 'author/author_registration.html', {'error': 'Email already exists'})
        # generate token for email verification
        token = get_random_string(length=32)
        
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
        # if user is already logged in
        try:
            token = request.session['token']
            author = Author.objects.get(login_token=token)
            if author.login_token_expires_at < timezone.now():
                return render(request, 'author/author_login.html')
            return redirect('/author/dashboard')
        except:
            return render(request, 'author/author_login.html')



    # POST request
    def post(self, request):
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = Author.objects.get(email=email)
            if check_password(password, user.password):
                token = get_random_string(length=32)
                user.login_token = token
                # set token in session
                request.session['token'] = token
                # set token expiry time to 30 minutes
                user.login_token_expires_at = timezone.now() + timezone.timedelta(minutes=30)
                user.save()
                if user.is_confirmed == False:
                    # remove this line after mail server setup
                    send_confirmation_mail(user, token)
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
                    return redirect('/author/dashboard')
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
            try:
                email = request.POST['email']
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
            def get(self, request):
                return render(request, 'author/author_forgot_password.html')
            
            # POST request
            def post(self, request):
                try:
                    email = request.POST['email']
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
                return render(request, 'author/author_reset_password.html', {'error': 'Link expired'})
            else:
                user.password = make_password(password)
                user.password_reset_token = None
                user.password_reset_token_expires_at = None
                user.save()
                return render(request, 'author/author_reset_password.html', {'success': 'Password changed successfully'})
        except:
            return render(request, 'author/author_reset_password.html', {'error': 'Invalid Token'})
        

#Author Logout View
class AuthorLogoutView(View):
    # GET request
    def get(self, request):
        try:
            del request.session['token']
            return redirect('/author/login')
        except:
            return redirect('/author/login')
        

# Author Dashboard View
class AuthorDashboardView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET request
    def get(self, request, author):
        # get the papers of the author
        author = Author.objects.get(login_token=request.session['token'])
        # get the papers of the author that should be 5 recent papers
        papers = Paper.objects.filter(author_id=author).order_by('-id')[:5]
        # get the conference which is is available for paper submission
        current_date = timezone.now().date()
        conference = Conference.objects.get(paper_submission_deadline__gte=current_date)
        if conference == None:
            return render(request, 'author/author_dashboard.html', {"page": "dashboard", "papers": papers, 'error': 'No conference available for paper submission'})
        return render(request, 'author/author_dashboard.html', {"page": "dashboard", "papers": papers, 'conference': conference})
    

# Author Sample View
@login_required
def sample(request):
    return HttpResponse('Sample View')


# Author Paper upload View
class AuthorPaperUploadView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET request
    def get(self, request, author):
        try:
            # get the conference which is is available for paper submission
            current_date = timezone.now().date()
            conference = Conference.objects.get(paper_submission_deadline__gte=current_date)

            # if conference is not available
            if conference == None:
                return render(request, 'author/author_upload_paper.html', {'error': 'No conference available for paper submission'})

            papers = Paper.objects.filter(author_id=author, conference_id=conference)
            if papers.count() > 0:
                return render(request, 'author/author_upload_paper.html', {'error': 'You have already submitted a paper for this conference'})
            


            return render(request, 'author/author_upload_paper.html', {'conference': conference})
        except Exception as e:
            print(e)
            return render(request, 'author/author_upload_paper.html', {'error': 'No conference available for paper submission'})

    # POST request
    def post(self, request, author):
        message = ''
        try:
            title = request.POST['title']
            abstract = request.POST['abstract']
            file = request.FILES['file']
            no_of_authors = request.POST['no_of_authors']
            author_1 = ''
            author_2 = ''
            author_3 = ''
            author_4 = ''
            author_5 = ''
            author_6 = ''
            if no_of_authors == '1':
                author_1 = request.POST['author_1']
            elif no_of_authors == '2':
                author_1 = request.POST['author_1']
                author_2 = request.POST['author_2']
            elif no_of_authors == '3':
                author_1 = request.POST['author_1']
                author_2 = request.POST['author_2']
                author_3 = request.POST['author_3']
            elif no_of_authors == '4':
                author_1 = request.POST['author_1']
                author_2 = request.POST['author_2']
                author_3 = request.POST['author_3']
                author_4 = request.POST['author_4']
            elif no_of_authors == '5':
                author_1 = request.POST['author_1']
                author_2 = request.POST['author_2']
                author_3 = request.POST['author_3']
                author_4 = request.POST['author_4']
                author_5 = request.POST['author_5']
            elif no_of_authors == '6':
                author_1 = request.POST['author_1']
                author_2 = request.POST['author_2']
                author_3 = request.POST['author_3']
                author_4 = request.POST['author_4']
                author_5 = request.POST['author_5']
                author_6 = request.POST['author_6']
            else:
                return render(request, 'author/author_upload_paper.html', {'error': 'Invalid number of authors'})
            author = Author.objects.get(login_token=request.session['token'])
            # get the conference which is is available for paper submission
            current_date = timezone.now().date()
            conference = Conference.objects.get(paper_submission_deadline__gte=current_date)
            value = {
                'title': title,
                'abstract': abstract,
                'author_id': author,
                'file': file,
                'no_of_authors': no_of_authors,
                'author_1': author_1,
                'author_2': author_2,
                'author_3': author_3,
                'author_4': author_4,
                'author_5': author_5,
                'author_6': author_6,
                'conference': conference
            }

            form = Paper(**value)
            form.save()
            message = 'successfull'
        except Exception as e:
            print(e)
            message = 'failed'
        return render(request, 'author/author_upload_paper.html', {'message': message})


# Author View Papers View
class AuthorViewPapersView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET request
    def get(self, request, author):
        # get the papers of the author
        papers = Paper.objects.filter(author_id=author)
        return render(request, 'author/author_papers.html', {"page": "view_papers", "papers": papers})


# Author View Paper View
class AuthorViewPaperView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET request
    def get(self, request, author, paper_id):
        try:
            paper = Paper.objects.get(id=paper_id, author_id=author)
            return render(request, 'author/author_paper_by_id.html', {"page": "view_paper", "paper": paper})
        except:
            return render(request, 'author/author_paper_by_id.html', {"page": "view_paper", "error": "Paper not found"})
        


# Author Contact View
class AuthorContactView(View):
    # GET request
    def get(self, request):
        return render(request, 'author/author_contact.html')

    # POST request
    def post(self, request):
        try:
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            value = {
                'email': email,
                'subject': subject,
                'message': message
            }
            form = Contact(**value)
            form.save()
            return render(request, 'author/author_contact.html', {'success': 'Message sent successfully'})
        except:
            return render(request, 'author/author_contact.html', {'error': 'Message sending failed'})

    


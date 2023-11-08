from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from .models import MainEditor, Conference
from author.models import Author, Paper

# django_mailer settings
from django.core.mail import send_mail
from django.conf import settings


# Login Required Decorator
def login_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            token = request.session['token']
            maineditor = MainEditor.objects.get(login_token=token)
            if maineditor.login_token_expires_at < timezone.now():
                return redirect('/maineditor/login')
            # return maineditor
            return func(request, maineditor, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('/maineditor/login')
    return wrapper

# Login Page View
class LoginView(View):
    def get(self, request):
        return render(request, 'maineditor/maineditor_login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            main_editor = MainEditor.objects.get(email=email)
            # check if password is changed
            if main_editor.is_password_changed == False:
                # generate token
                token = get_random_string(length=32)
                main_editor.password_reset_token = token
                main_editor.password_reset_token_expires_at = timezone.now() + timezone.timedelta(days=1)
                main_editor.save()

                # send email
                subject = 'Reset Password'
                message = f'Click on the link to reset password http://localhost:8000/maineditor/reset_password/{token}'
                email_from = 'support@wpless.com'
                recipient_list = [email,]
                send_mail( subject, message, email_from, recipient_list )
                return render(request, 'maineditor/maineditor_login.html', {'error': 'Password Not Changed. Reset Password Link Sent To Your Email'})
                
            if check_password(password, main_editor.password):
                # generate token
                token = get_random_string(length=32)
                main_editor.login_token = token
                main_editor.login_token_expires_at = timezone.now() + timezone.timedelta(days=1)
                main_editor.save()

                # set token in session
                request.session['token'] = token
                request.session['main_editor_id'] = main_editor.id
                return redirect('/maineditor/dashboard')
            else:
                return render(request, 'maineditor/maineditor_login.html', {'error': 'Invalid Password'})
        except MainEditor.DoesNotExist:
            return render(request, 'maineditor/maineditor_login.html', {'error': 'Main Editor Does Not Exist'})
        

# Main Editor Email Reset Password View
class MainEditorEmailResetPasswordView(View):
    def get(self, request):
        return render(request, 'maineditor/maineditor_email_reset_password.html')
    
    def post(self, request):
        try:
            email = request.POST.get('email')
            main_editor = MainEditor.objects.get(email=email)
            # generate token
            token = get_random_string(length=32)
            main_editor.password_reset_token = token
            main_editor.password_reset_token_expires_at = timezone.now() + timezone.timedelta(days=1)
            main_editor.save()

            # send email
            subject = 'Reset Password'
            message = f'Click on the link to reset password http://localhost:8000/maineditor/reset_password/{token}'
            email_from = 'support@wpless.com'
            recipient_list = [email,] 
            send_mail( subject, message, email_from, recipient_list )
            return render(request, 'maineditor/maineditor_email_reset_password.html', {'success': 'Reset Password Link Sent Successfully'})
        except Exception as e:
            print(e)
            if 'MainEditor matching query does not exist' in str(e):
                return render(request, 'maineditor/maineditor_email_reset_password.html', {'error': 'Main Editor Does Not Exist'})
            return render(request, 'maineditor/maineditor_email_reset_password.html', {'error': 'Something Went Wrong'})


# Main Editor Reset Password View
class MainEditorResetPasswordView(View):
    def get(self, request, token):
        try:
            main_editor = MainEditor.objects.get(password_reset_token=token)
            if main_editor.password_reset_token_expires_at < timezone.now():
                return render(request, 'maineditor/maineditor_reset_password.html', {'error': 'Reset Password Link Expired'})
            return render(request, 'maineditor/maineditor_reset_password.html', {'token': token})
        except MainEditor.DoesNotExist:
            return render(request, 'maineditor/maineditor_reset_password.html', {'error': 'Reset Password Link Invalid'})
        
    def post(self, request, token):
        try:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                return render(request, 'maineditor/maineditor_reset_password.html', {'error': 'Password and Confirm Password Does Not Match'})
            main_editor = MainEditor.objects.get(password_reset_token=token)
            main_editor.password = make_password(password)
            main_editor.is_password_changed = True
            main_editor.password_reset_token = None
            main_editor.password_reset_token_expires_at = None
            main_editor.save()
            return render(request, 'maineditor/maineditor_reset_password.html', {'success': 'Password Reset Successfully'})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_reset_password.html', {'error': 'Something Went Wrong'})
        




# Main Editor Dashboard View
class MainEditorDashboardView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        return render(request, 'maineditor/maineditor_dashboard.html', {'maineditor': maineditor})
    


# Main Editor Add Conference View
class MainEditorAddConferenceView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        return render(request, 'maineditor/maineditor_add_conference.html')
    
    def post(self, request):
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            venue = request.POST.get('venue')
            paper_submission_deadline = request.POST.get('paper_submission_deadline')
            paper_review_deadline = request.POST.get('paper_review_deadline')
            paper_acceptance_deadline = request.POST.get('paper_acceptance_deadline')
            paper_publish_deadline = request.POST.get('paper_publish_deadline')
            no_of_papers = request.POST.get('no_of_papers')
            main_editor_id = request.session.get('main_editor_id')
            main_editor = MainEditor.objects.get(id=main_editor_id)
            conference = Conference(title=title, description=description, image=image, start_date=start_date, end_date=end_date, venue=venue, paper_submission_deadline=paper_submission_deadline, paper_review_deadline=paper_review_deadline, paper_acceptance_deadline=paper_acceptance_deadline, paper_publish_deadline=paper_publish_deadline, no_of_papers=no_of_papers, main_editor_id=main_editor)
            conference.save()
            return render(request, 'maineditor/maineditor_add_conference.html', {'success': 'Conference Added Successfully'})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_add_conference.html', {'error': 'Something Went Wrong'})
        


# Main Editor View Conference View
class MainEditorViewConferenceView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            conferences = Conference.objects.filter(main_editor_id=maineditor)
            return render(request, 'maineditor/maineditor_conferences.html', {'conferences': conferences})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_conferences.html', {'error': 'Something Went Wrong'})
        


# Main Editor Edit Conference View
class MainEditorEditConferenceView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, conference_id):
        try:
            conference = Conference.objects.get(id=conference_id)
            return render(request, 'maineditor/maineditor_edit_conference.html', {'conference': conference})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_edit_conference.html', {'error': 'Something Went Wrong'})
        
    def post(self, request, conference_id):
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            venue = request.POST.get('venue')
            paper_submission_deadline = request.POST.get('paper_submission_deadline')
            paper_review_deadline = request.POST.get('paper_review_deadline')
            paper_acceptance_deadline = request.POST.get('paper_acceptance_deadline')
            paper_publish_deadline = request.POST.get('paper_publish_deadline')
            no_of_papers = request.POST.get('no_of_papers')
            conference = Conference.objects.get(id=conference_id)
            conference.title = title
            conference.description = description
            conference.image = image
            conference.start_date = start_date
            conference.end_date = end_date
            conference.venue = venue
            conference.paper_submission_deadline = paper_submission_deadline
            conference.paper_review_deadline = paper_review_deadline
            conference.paper_acceptance_deadline = paper_acceptance_deadline
            conference.paper_publish_deadline = paper_publish_deadline
            conference.no_of_papers = no_of_papers
            conference.save()
            return render(request, 'maineditor/maineditor_edit_conference.html', {'success': 'Conference Updated Successfully'})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_edit_conference.html', {'error': 'Something Went Wrong'})
        

# Main Editor Delete Conference View
class MainEditorDeleteConferenceView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, conference_id):
        try:
            conference = Conference.objects.get(id=conference_id)
            conference.delete()
            return redirect('/maineditor/conferences')
        except Exception as e:
            print(e)
            return redirect('/maineditor/conferences')
        


# Main Editor Logout View
class MainEditorLogoutView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            del request.session['token']
            del request.session['main_editor_id']
            return redirect('/maineditor/login')
        except Exception as e:
            print(e)
            return redirect('/maineditor/login')
        

# Main Editor Profile View
class MainEditorProfileView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        return render(request, 'maineditor/maineditor_profile.html', {'maineditor': maineditor})
    
    def post(self, request, maineditor):
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            maineditor.name = name
            maineditor.email = email
            maineditor.save()
            return render(request, 'maineditor/maineditor_profile.html', {'maineditor': maineditor, 'success': 'Profile Updated Successfully'})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_profile.html', {'maineditor': maineditor, 'error': 'Something Went Wrong'})
        

# Main Editor Upload Profile Image
class MainEditorUploadProfileImageView(View):
    @method_decorator(login_required)
    def post(self, request, maineditor):
        try:
            image = request.FILES.get('image')
            maineditor.image = image
            maineditor.save()
            return redirect('/maineditor/profile')
        except Exception as e:
            print(e)
            return redirect('/maineditor/profile')
        

# Main Editor Review Papers View
class MainEditorReviewPapersView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            paper = Paper.objects.filter(status='pending')
            return render(request, 'maineditor/maineditor_review_papers.html', {'papers': paper})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_review_papers.html', {'error': 'Something Went Wrong'})
        

# Main Editor Review Paper By Id View
class MainEditorReviewPaperByIdView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, paper_id):
        try:
            paper = Paper.objects.get(id=paper_id)
            return render(request, 'maineditor/maineditor_review_paper_by_id.html', {'paper': paper})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_review_paper_by_id.html', {'error': 'Something Went Wrong'})
    # @method_decorator(login_required)
    def post(self, request, paper_id):
        try:
            status = request.POST.get('status')
            paper = Paper.objects.get(id=paper_id)
            if status == 'accept':
                paper.status = 'Accepted'
            else:
                paper.status = 'Rejected'
            paper.review_remark_1 = request.POST.get('remarks')
            paper.is_review_1_completed = True
            maineditor = MainEditor.objects.get(login_token=request.session['token'])
            paper.maineditor = maineditor
            paper.save()
            return redirect('/maineditor/review_papers')
        except Exception as e:
            print(e)
            return redirect('/maineditor/review_papers')
        


# Main Editor Paper Download By ID
class MainEditorPaperDownloadByIdView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, paper_id):
        try:
            paper = Paper.objects.get(id=paper_id)
            # get file path and send file
            file_path = paper.file
            file = open(file_path.path, 'rb')
            # check if file is pdf or docx
            if file_path.path.endswith('.pdf'):
                response = HttpResponse(file, content_type='application/pdf')
            elif file_path.path.endswith('.docx'):
                response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            else:
                response = HttpResponse(file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=' + file_path.name
            return response
        except Exception as e:
            print(e)
            return redirect('/maineditor/review_papers')
        
        


# Main Editor View Accepted Papers View
class MainEditorViewAcceptedPapersView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            papers = Paper.objects.filter(status='Main Editor Accepted')
            return render(request, 'maineditor/maineditor_accepted_papers.html', {'papers': papers})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_accepted_papers.html', {'error': 'Something Went Wrong'})
        

# Main Editor View Rejected Papers View
class MainEditorViewRejectedPapersView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            papers = Paper.objects.filter(status='Main Editor Rejected')
            return render(request, 'maineditor/maineditor_rejected_papers.html', {'papers': papers})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_rejected_papers.html', {'error': 'Something Went Wrong'})
        

# Main Editor View All Papers View
class MainEditorViewAllPapersView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            papers = Paper.objects.all()
            return render(request, 'maineditor/maineditor_all_papers.html', {'papers': papers})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_all_papers.html', {'error': 'Something Went Wrong'})
        

# Main Editor View Paper By Id View
class MainEditorViewPaperByIdView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, paper_id):
        try:
            paper = Paper.objects.get(id=paper_id)
            return render(request, 'maineditor/maineditor_view_paper_by_id.html', {'paper': paper})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_view_paper_by_id.html', {'error': 'Something Went Wrong'})
        

# Main Editor View Authors View
class MainEditorViewAuthorsView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor):
        try:
            authors = Author.objects.all()
            return render(request, 'maineditor/maineditor_authors.html', {'authors': authors})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_authors.html', {'error': 'Something Went Wrong'})
        

# Main Editor View Author By Id View
class MainEditorViewAuthorByIdView(View):
    @method_decorator(login_required)
    def get(self, request, maineditor, author_id):
        try:
            author = Author.objects.get(id=author_id)
            return render(request, 'maineditor/maineditor_view_author_by_id.html', {'author': author})
        except Exception as e:
            print(e)
            return render(request, 'maineditor/maineditor_view_author_by_id.html', {'error': 'Something Went Wrong'})
        

        

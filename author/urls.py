from django.urls import path
from .views import  AuthorRegistrationView, AuthorLoginView, AuthorEmailConfirmationView, AuthorResendConfirmationMailView, AuthorForgotPasswordView, AuthorResetPasswordView, AuthorDashboardView, AuthorPaperUploadView, AuthorViewPapersView, AuthorContactView, AuthorLogoutView, AuthorViewPaperView

urlpatterns = [
    path('register', AuthorRegistrationView.as_view(), name='author_registration'),
    path('login', AuthorLoginView.as_view(), name='author_login'),
    path('logout', AuthorLogoutView.as_view(), name='author_logout'),
    path('confirmation/<str:token>', AuthorEmailConfirmationView.as_view(), name='author_email_confirmation'),
    path('resend_confirmation_mail', AuthorResendConfirmationMailView.as_view(), name='author_resend_confirmation_mail'),
    path('forgot_password', AuthorForgotPasswordView.as_view(), name='author_forgot_password'),
    path('reset_password/<str:token>', AuthorResetPasswordView.as_view(), name='author_reset_password'),
    path('dashboard', AuthorDashboardView.as_view() , name='author_dashboard'),
    path('upload_paper', AuthorPaperUploadView.as_view(), name='author_upload_paper'),
    path('papers', AuthorViewPapersView.as_view(), name='author_view_papers'),
    path('paper/<int:paper_id>', AuthorViewPaperView.as_view(), name='author_view_paper'),
    path('contact', AuthorContactView.as_view(), name='author_contact'),
]
from django.urls import path
from .views import index, AuthorRegistrationView, AuthorLoginView, AuthorEmailConfirmationView, AuthorResendConfirmationMailView, AuthorForgotPasswordView, AuthorResetPasswordView, AuthorDashboardView

urlpatterns = [
    path('h', index.as_view(), name='index'),
    path('author/register', AuthorRegistrationView.as_view(), name='author_registration'),
    path('author/login', AuthorLoginView.as_view(), name='author_login'),
    path('author/confirmation/<str:token>', AuthorEmailConfirmationView.as_view(), name='author_email_confirmation'),
    path('author/resend_confirmation_mail', AuthorResendConfirmationMailView.as_view(), name='author_resend_confirmation_mail'),
    path('author/forgot_password', AuthorForgotPasswordView.as_view(), name='author_forgot_password'),
    path('author/reset_password/<str:token>', AuthorResetPasswordView.as_view(), name='author_reset_password'),
    path('author/dashboard', AuthorDashboardView.as_view() , name='author_dashboard')
]
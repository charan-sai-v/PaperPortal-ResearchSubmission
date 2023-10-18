
from django.urls import path
from .views import LoginView, MainEditorDashboardView, MainEditorAddConferenceView, MainEditorEmailResetPasswordView, MainEditorResetPasswordView, MainEditorViewConferenceView, MainEditorReviewPapersView, MainEditorReviewPaperByIdView, MainEditorPaperDownloadByIdView

urlpatterns = [
    path('login', LoginView.as_view(), name='maineditor_login'),
    path('dashboard', MainEditorDashboardView.as_view(), name='maineditor_dashboard'),
    path('add_conference', MainEditorAddConferenceView.as_view(), name='maineditor_add_conference'),
    path('conferences', MainEditorViewConferenceView.as_view(), name='maineditor_conferences'),
    path('forgot_password', MainEditorEmailResetPasswordView.as_view(), name='maineditor_email_reset_password'),
    path('reset_password/<str:token>', MainEditorResetPasswordView.as_view(), name='maineditor_reset_password'),
    path('review_papers', MainEditorReviewPapersView.as_view(), name='maineditor_review_papers'),
    path('review_paper/<int:paper_id>', MainEditorReviewPaperByIdView.as_view(), name='maineditor_review_paper_by_id'),
    path('download_paper/<int:paper_id>', MainEditorPaperDownloadByIdView.as_view(), name='maineditor_download_paper_by_id'),

]

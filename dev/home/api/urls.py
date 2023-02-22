from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet,basename='AdminSignupView'),
# router.register(r'admin-signup', AdminSignupView , basename='AdminSignupView')



urlpatterns=[
    
    path('', include(router.urls)),
    path('school-signup/', SchoolSignupView.as_view(), name='SchoolSignupView'),
    path('admin-signup/', AdminSignupView.as_view(), name='AdminSignupView'),
    path('teacher-signup/', TeacherSignupView.as_view(), name='TeacherSignupView'),
    path('QuestionBankCreate/', QuestionBankCreateView.as_view(), name='QuestionBankCreate'),
    # path('QuestionCreateView/', QuestionCreateView.as_view(), name='QuestionCreateView'),
    # path('QuestionCreateView/<int:pk>/', QuestionCreateView.as_view(), name='QuestionCreateView'),
    path('AdminList/', AdminListView.as_view(), name='AdminListView'),
    path('TeacherList/', TeacherListView.as_view(), name='TeacherListView'),
    path('admin-school-questionbanks-list/', admin_school_questionbanks.as_view(), name='admin_school_questionbanks'),
    path('user-school-questions-list/', QuestionList.as_view(), name='user_school_questions'),
    path('SchoolDetail/', SchoolDetail.as_view(), name='SchoolDetail'),
    path('question-generator/', RandomQuestionView.as_view(), name='QuestionGeneratorView'),
     path('question-bank/<int:question_bank_id>/questions/', QuestionList.as_view()),
    path('login/', LoginView.as_view(), name='LoginView'),

]
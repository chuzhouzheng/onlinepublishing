from django.conf.urls import url
from test_online_publishing import views
urlpatterns = [
    url(r'^tasklist$', views.TaskList.as_view()),
    url(r'^addtask$', views.AddTask.as_view()),
    url(r'^edittask$', views.EditTask.as_view()),
]
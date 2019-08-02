from django.conf.urls import url
from test_online_publishing import views
urlpatterns = [
    url(r'^login', views.Login.as_view()),
    url(r'^logout', views.Logout.as_view()),
    url(r'^password_change', views.PasswordChange.as_view()),
    url(r'^tasklist', views.TaskList.as_view()),
    url(r'^addtask', views.AddTask.as_view()),
    url(r'^edittask', views.EditTask.as_view()),
    url(r'^operate', views.Operate.as_view()),
    url(r'^logdetail', views.GetLogDetail.as_view()),
    url(r'^test', views.Test.as_view()),
]
from products import views
from django.conf.urls import url

from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


app_name = 'products'

urlpatterns = [

    url(r'addProduct/$', login_required(views.AddProductView.as_view()), name='addProduct'),
    url(r'viewProduct/$', login_required(views.FullProductView.as_view()), name='viewProduct'),
    #url for product backlog
    url(r'^viewPBI/', login_required(views.PBIView.as_view()), name='viewPBI'),
    url(r'addPBI', login_required(views.AddPBIView.as_view()), name='addPBI'),
    url(r'viewFullPBI', login_required(views.FullPBIView.as_view()), name='veiwFullPBI'),
    url(r'^deletePBI/(?P<pk>\d+)/$',login_required(views.DeletePBIView.as_view()), name='deletePBI'),
    url(r'updatePBI/(?P<pk>\d+)/$', login_required(views.EditPBIView.as_view()), name='editPBI'),
    url(r'^viewPBIdetail/(?P<pk>\d+)/$', login_required(views.PBIDetailView.as_view()), name='pbiDetail'),
    url(r'^addtoSprint/(?P<pk>\d+)/$', login_required(views.addtoSprint.as_view()), name='addtoSprint'),

    #url for sprint backlog
    url(r'^sprintBacklog/$', login_required(views.SprintBacklogView.as_view()), name='sprintBacklog'),
    url(r'^fullSprintBacklog/$', login_required(views.FullSprintBacklogView.as_view()), name='fullSprintBacklog'),
    url(r'addTask', login_required(views.AddTaskView.as_view()), name='addTask'),
    url(r'^updateTask/(?P<pk>\d+)/$', login_required(views.EditTaskView.as_view()), name='editTask'),
    url(r'^deleteTask/(?P<pk>\d+)/$', login_required(views.DeleteTaskView.as_view()), name='deletePBI'),
    url(r'^viewTASKdetail/(?P<pk>\d+)/$', login_required(views.TaskDetailView.as_view()), name='taskDetail'),
    url(r'^profile/$', login_required(views.profile),name='profile'),

    url(r'^$', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    url(r'^register$',views.registerView, name='register'),
    url(r'^registerdev/$',views.DevRegisterView, name='devregister'),
    url(r'^registersm/$',views.SMRegisterView, name='smregister'),
    url(r'^registerpo/$',views.PoRegisterView, name='poregister'),



    url(r'^changeSprint/$', login_required(views.ChangeSprintView.as_view()), name='changeSprint'),

]

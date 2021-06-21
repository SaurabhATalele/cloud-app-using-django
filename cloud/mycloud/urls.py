from django.urls import path,include
import django.template
from . import views


urlpatterns=[

    path('',views.view.home,name="home"),
    path('search',views.view.search,name='search'),
    path('profile',views.view.profile,name='profile'),
    path('profile/edit',views.view.editProfile,name='edit'),
    path('profile/edit/<str:username>',views.view.edit_Profile,name='editprofile'),
    path('upload_file',views.view.upload,name="Upload_file"),
    path('f/<str:filename>', views.view.file, name="view_file"),
    path('d/console/', views.view.devconsole, name="dev_console"),
    path('d/user-agreement', views.view.dev_agreement, name="user_agreement"),
    path('d/create', views.view.create_devuser, name="createuser"),
    path('d/create-project', views.view.create_project, name="createproject"),
    path('d/create-folder', views.view.create_folder, name="createfolder"),
    path('cd/<str:folder>', views.view.changedir, name="cd"),
    path('back', views.view.back, name="back"),
    path('delete/<str:filename>', views.view.delete, name="del"),
    path('rename/<str:filename>/<str:newname>', views.view.renamefile, name="ren"),
    path('d/console/project/<str:projectname>', views.view.project_view, name="project"),
    path("buy-storage",views.view.buy_storage,name="Buy"),
    path("success/<str:pid>/<str:oid>/<str:sign>",views.view.success,name="success"),

]

handler404 = 'Cloud.views.view_404'
handler500 = 'Cloud.views.view_500'
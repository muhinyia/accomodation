from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [

    path('student', views.student_login, name='student_login'),
    path('landlord', views.landlord_login, name='landlord_login'),
    path('moderator', views.moderator_login, name='moderator_login'),
    path('register/', views.register, name='register'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/landlord/', views.landlord_register,
         name='landlord_register'),
    path('logout', views.logout, name='logout'),
    path('landlord/dashboard', views.dashboard, name='landlord_dashboard'),
    path('inquiry/<int:room_id>', views.get_inquiry, name='get_inquiry'),
    path('moderator/dashboard', views.moderator_dashboard,
         name='moderator_dashboard'),
    path('moderator/view', views.view_rooms,
         name='view_rooms'),
    path('approve/<int:room_id>', views.approve_room, name='approve_room'),
    path('dissaprove/<int:room_id>', views.dissaprove_room, name='dissaprove_room'),




]

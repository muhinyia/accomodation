from django.urls import path
from . import views

app_name = 'apartments'
urlpatterns = [

    path('', views.index, name='index'),
    path('<int:room_id>', views.room, name='room'),
    path('rooms', views.rooms, name='rooms'),
    path('add/', views.add_room, name='RoomCreate'),
    path('update/<int:pk>', views.RoomEditView.as_view(), name='RoomUpdate'),
    path('delete/<int:pk>', views.RoomDeleteView.as_view(), name='RoomDelete'),
    path('inquiry', views.inquiry, name='inquiry'),



]

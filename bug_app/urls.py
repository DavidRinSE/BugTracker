from django.urls import path
from bug_app import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('tickets/', views.view_tickets, name="homepage"),
    path('tickets/<int:id>/', views.view_ticket, name="ticket"),
    path('tickets/<int:id>/assign/', views.assign_self, name="assign"),
    path('tickets/<int:id>/invalid/', views.invalid_ticket, name="invalid"),
    path('tickets/<int:id>/complete/', views.complete_ticket, name="complete"),
    path('tickets/<int:id>/edit/', views.edit_ticket, name="edit"),
    path('tickets/newticket/', views.create_ticket, name="newticket"),
    path('account/', views.view_user, name="account"),
    path('logout/', views.logoutview, name="logout")
]
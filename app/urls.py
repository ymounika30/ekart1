from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('add-to-cart-<int:pro_id>/',views.AddToCartView.as_view(),name='addtocart'),
    path('mycart/',views.MyCartView.as_view(),name='mycart'),
    path('delete/<int:id>/', views.DeleteView.as_view(),name='delete'),
    path('login/',views.ulogin,name='login'),
    path('signup/',views.signup,name='signup'),
    path('contact/',views.contact,name='contact'),
    path('logout/', views.Logout, name='logout'),
]

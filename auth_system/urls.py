from django.urls import path
from auth_system import views
from auth_system.views import login_view


urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('delete-user/<int:user_id>/', views.delete_user, name = "delete_user"),
    path('admin/update-role/<int:user_id>/', views.update_user_role, name='update_user_role'),

]
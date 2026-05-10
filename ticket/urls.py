from django.urls import path
from . views import authentication
from . views import home
from . views import tickets
from . views import ajax
from . views import report
from . views import users
from . views import feedback



urlpatterns = [
path('', home.home, name='home'),
path('login/', authentication.login , name='login'),
path('logout/', authentication.logout , name='logout'),
# path('displaytickets/', tickets.displaytickets , name='displaytickets'),
path('filtertickets/', tickets.filtertickets , name='filtertickets'),
path('launchtickets/', tickets.launchtickets , name='launchtickets'),
path('get_child_divisions_for_zone/', ajax.get_child_divisions_for_zone , name='get_child_divisions_for_zone'),
path('get_child_districts_for_division/', ajax.get_child_districts_for_division , name='get_child_districts_for_division'),
path('get_child_cities_for_district/', ajax.get_child_cities_for_district , name='get_child_cities_for_district'),
path('addtickets/', tickets.addtickets , name='addtickets'),
path('get_values_for_ticket_updation/', ajax.get_values_for_ticket_updation , name='get_values_for_ticket_updation'),
path('update_response/', ajax.update_response , name='update_response'),
path('display_report_ticket/', report.display_report_ticket , name='display_report_ticket'),
path('export_report_ticket/', report.export_report_ticket , name='export_report_ticket'),
path('password_reset/', authentication.password_reset , name='password_reset'),
path('display_users/', users.display_users , name='display_users'),
path('display_add_user/', users.display_add_user , name='display_add_user'),
path('add_users/', users.add_users , name='add_users'),
path('change_password/', ajax.change_password , name='change_password'),
path('get_values_for_user_updation/', ajax.get_values_for_user_updation , name='get_values_for_user_updation'),
path('update_user_response/', ajax.update_user_response , name='update_user_response'),
path('update_feedback_response/', ajax.update_feedback_response , name='update_feedback_response'),
path('filterfeedbacks/', feedback.filterfeedbacks , name='filterfeedbacks'),
path('get_values_for_feedback_updation/', ajax.get_values_for_feedback_updation , name='get_values_for_feedback_updation'),
path('dashboard/', home.dashboard, name='dashboard'),
path('dash_view/', home.dash_view, name='dash_view'),
]






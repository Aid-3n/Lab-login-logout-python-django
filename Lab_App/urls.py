from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
				path('',views.Home,name="Home"),
				path('Admin_Login/',views.Admin_Login,name="Admin_Login"),
				path('Teacher_Login/',views.Teacher_Login,name="Teacher_Login"),
				path('Manage_Teacher/',views.Manage_Teacher,name="Manage_Teacher"),
				path('DeleteTeacher/<int:id>',views.DeleteTeacher,name="DeleteTeacher"),
				path('Add_Teacher/',views.Add_Teacher,name="Add_Teacher"),
				path('Update_Teacher/',views.Update_Teacher,name="Update_Teacher"),
				path('Assign/',views.Assign,name="Assign"),
				path('Update_Assign/',views.Update_Assign,name="Update_Assign"),
				path('Logout/',views.Logout,name="Logout"),
				path('Manage_student/',views.Manage_student,name="Manage_student"),
				path('Add_student/',views.Add_student,name="Add_student"),
				path('Update/',views.Update,name="Update"),
				path('Mark_Attendance/',views.Mark_Attendance,name="Mark_Attendance"),
				path('Manage_Timetable/',views.Manage_Timetable,name="Manage_Timetable"),
				path('View_Attendance/',views.View_Attendance,name="View_Attendance"),
				path('Assign_Lab/',views.Assign_Lab,name="Assign_Lab"),
				path('Real_time/',views.Real_time,name="Real_time"),
				path('Log_In/<int:id>/',views.Log_In,name="Log_In"),
				path('Log_Out/<int:id>/',views.Log_Out,name="Log_Out"),
                path('Log_Out_Manual/<int:id>/',views.Log_Out_Manual,name="Log_Out_Manual"),
				path('Generate_percentage/',views.Generate_percentage,name="Generate_percentage"),
				path('DeleteStudent/<int:id>',views.DeleteStudent,name="DeleteStudent"),
                path('Delete_Lab/<int:id>/', views.delete_lab, name='delete_lab'),
                path('data_upload/', views.data_upload, name='data_upload'),
				path('Assign_Department_Course_Teacher/',views.Assign_Department_Course_Teacher,name="Assign_Department_Course_Teacher"),

				

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
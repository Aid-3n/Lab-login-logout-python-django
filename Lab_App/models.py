from django.db import models

# Create your models here.

class AdminDetails(models.Model):
	username = models.CharField(max_length=100,default=None,unique=True)
	password = models.CharField(max_length=100,default=None)
	class Meta:
		db_table = 'AdminDetails'


class Teacher_Details(models.Model):
	#Personal Details
	Name 	 = models.CharField(max_length=100,default=None,null=True)
	username = models.CharField(max_length=100,default=None,null=True,unique=True)
	Gender = models.CharField(max_length=100,default=None,null=True)
	password = models.CharField(max_length=100,default=None,null=True)
	Semester= models.CharField(max_length=100,default=None,null=True)
	Subject  = models.CharField(max_length=100,default=None,null=True)
	Department  = models.CharField(max_length=100,default=None,null=True)
	Dept_assigned = models.CharField(max_length=100,default=None,null=True)
	
	class Meta:
		db_table = 'Teacher_Details'

class Student_Details(models.Model):
	Name= models.CharField(max_length=100,default=None,null=True)
	Age= models.CharField(max_length=3,default=None,null=True)
	Gender= models.CharField(max_length=100,default=None,null=True)
	Department= models.CharField(max_length=100,default=None,null=True)
	Semester= models.CharField(max_length=100,default=None,null=True)
	Barcode= models.CharField(max_length=5,default=None,unique=True)
	Subject = models.CharField(max_length=100,default=None,null=True)

class Meta:
		db_table = 'Student_Details'

class Lab(models.Model):	
	Teacher_Id = models.CharField(max_length=100,default=None,null=True)
	Subject = models.CharField(max_length=100,default=None,null=True)
	Day = models.CharField(max_length=100,default=None,null=True)
	Start_time = models.CharField(max_length=10,default=None,null=True)
	End_time = models.CharField(max_length=10,default=None,null=True)
	Semester = models.IntegerField(default=None,null=True)
	class Meta:
		db_table = "Lab"
		
class Attendance_New(models.Model):
	Attendence_id = models.CharField(max_length=100,default=None,null=True)
	Today_date = models.CharField(max_length=100,default=None,null=True)
	Teacher_ID = models.CharField(max_length=100,default=None,null=True)
	Current_Date = models.CharField(max_length=100,default=None,null=True)
	Current_Time = models.CharField(max_length=100,default=None,null=True)
	Student_ID = models.CharField(max_length=100,default=None,null=True)
	Name 	 = models.CharField(max_length=100,default=None,null=True)
	Subject = models.CharField(max_length=100,default=None,null=True)
	Login_Time = models.CharField(max_length=100,default=None,null=True)
	Logout_Time = models.CharField(max_length=100,default=None,null=True)
	Login_Status= models.CharField(max_length=100,default=None,null=True)
	Logout_Status= models.CharField(max_length=100,default=None,null=True)
	login_type = models.CharField(max_length=100,default=None,null=True)
	Semester = models.CharField(max_length=3,default=None,null=True)
	Barcode= models.CharField(max_length=5,default=None,unique=False)
	Attendance_status =  models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'Attendence_New'

class SubSem(models.Model):
	subject = models.CharField(max_length=100,default=None,null=True)
	semester = models.CharField(max_length=100,default=None,null=True)
	Dept = models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'subsem'



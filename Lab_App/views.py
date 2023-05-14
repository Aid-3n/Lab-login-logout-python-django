from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import connection
import cv2
from pyzbar import pyzbar
import pandas as pd

# Create your views here.

def Home(request):
    return render(request,"Home.html",{})



def Admin_Login(request):
    if request.method == "POST":
        A_username = request.POST['aname']
        A_password = request.POST['apass']
        if AdminDetails.objects.filter(username = A_username,password = A_password).exists():
            ad = AdminDetails.objects.get(username=A_username, password=A_password)
            print('d')
            messages.info(request,'Admin login is Sucessfull')
            request.session['type_id'] = 'Admin'
            request.session['UserType'] = 'Admin'
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            print('y')
            messages.error(request, 'Error wrong username/password')
            return render(request, "Admin_Login.html", {})
    else:
        return render(request, "Admin_Login.html", {})

def Teacher_Login(request):
    if request.method == "POST":
        C_name = request.POST['username']
        C_password = request.POST['password']
        if Teacher_Details.objects.filter(username=C_name, password=C_password).exists():
            users = Teacher_Details.objects.all().filter(username=C_name, password=C_password)
            messages.info(request,C_name+ ' logged in')
            request.session['UserId'] = users[0].id
            request.session['type_id'] = 'Teacher'
            request.session['UserType'] = C_name
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            messages.error(request, 'Admin has not added you')
            return redirect("/Teacher_Login")
    else:
        return render(request,'Teacher_Login.html',{})

    
def Manage_Teacher(request):
    details = Teacher_Details.objects.all()
    return render(request,"Manage_Teacher.html",{'details':details})

def Add_Teacher(request):
    if request.method == "POST":
        name = request.POST['name']
        Gender= request.POST['gender']
        username= request.POST['username']
        password= request.POST['password']
        obj = Teacher_Details(
                            Name=name
                            ,Gender=Gender
                            ,username=username
                            ,password=password)
        obj.save()
        messages.info(request,f"{name} is added")
        return redirect("/Manage_Teacher/")
    else:
        return render(request,"Add_Teacher.html",{})

def Update_Teacher(request):
    if request.method == "POST":
        T_id = request.POST['1updateid']
        name = request.POST['1updatename']
        Department = request.POST['1updatedept']
        Semester = request.POST['1updateSemester']
        Subject = request.POST['1updatesub']
        Teacher_Details.objects.filter(id=T_id).update(
                                                        Name=name,
                                                        Semester=Semester,
                                                        Department=Department,
                                                        Subject=Subject)
        messages.info(request,"Teacher details updated")
        return redirect("/Manage_Teacher/")
    else:
        return render(request,"Manage_Teacher.html",{})

def Assign(request):
    details = Teacher_Details.objects.all()
    return render(request,"Assign.html",{'details':details})

def Update_Assign(request):
    if request.method == "POST":
        T_id= request.POST['1updateid']
        details = Teacher_Details.objects.filter(id = T_id)
        for i in details:
            Semester = details[0].Subject
            department = details[0].Department
            print(f"{Semester}//{department}")
        # from django.utils.datastructures import MultiValueDictKeyError
        # try:
        # 	T_Subject = request.POST['1updatesub']
        # except MultiValueDictKeyError:
        # 	T_Subject = False
        T_Subject = request.POST.get('1updatesub',Semester)
        #value = request.POST.get('key', None)
        T_Department = request.POST.get('1updatedept',department)
        Teacher_Details.objects.filter(id=T_id).update(Subject=T_Subject,Department=T_Department)
        messages.info(request,"Semester and Department Assigned")
        return redirect("Assign")
    else:
        return redirect("Assign")

def DeleteTeacher(request,id):
    delcomp = Teacher_Details.objects.get(id=id) 
    delcomp.delete()
    return redirect('/Manage_Teacher/')

def Logout(request):
    Session.objects.all().delete()
    return redirect("/")

def Manage_student(request):
    Students = Student_Details.objects.all()
    return render(request,'Manage_student.html',{'Students':Students})

def Add_student(request):
    if request.method == "POST":
        Name = request.POST['Name']
        Age = request.POST['Age']
        Gender = request.POST['Gender']
        Barcode = request.POST['Barcode']
        Semester = request.POST['Semester']
        Department = request.POST['Department']
        Subjects = request.POST['sub']	
      
        # check if barcode already exists in the database
        if Student_Details.objects.filter(Barcode=Barcode).exists():
            messages.error(request, f"Admission Number {Barcode} already exists.")
            return redirect('/Add_student')
        else:
            data = Student_Details(Name=Name, Age=Age, Gender=Gender, Barcode=Barcode, Semester=Semester, Department=Department, Subject=Subjects)
            data.save()
            messages.info(request, f"{Name} is added")
            return redirect('/Manage_student/')
    else:
        return render(request, "Add_student.html", {})



def Update(request):
    if request.method == "POST":
        Student_Id = request.POST['update_id']
        Name= request.POST['update_name']
        Age= request.POST['update_Age']
        Gender= request.POST['update_Gender']
        Department= request.POST['update_Department']
        Semester= request.POST['update_Semester']
        Barcode= request.POST['update_Barcode']
        Student_Details.objects.filter(id=Student_Id).update(
                                                            Name=Name
                                                            ,Age=Age
                                                            ,Gender=Gender
                                                            ,Department=Department
                                                            ,Semester=Semester
                                                            ,Barcode=Barcode)
        messages.info(request,"Student details updated!")
        return redirect('/Manage_student/')
    else:
        return redirect('/Manage_student/')


def Mark_Attendance(request):
    if request.method == "POST":
        import datetime

        subjects = request.POST['Subject']
        selected = request.POST.get('Subject')
        tokens = selected.split("-")
        print("tokens")
        print(tokens)
        print('else')
        print(selected)
        Teacher_Id = request.session['UserId']
        WeekDay = datetime.datetime.now()
        WeekDay = WeekDay.strftime("%A")
        print(WeekDay)
        #if Lab.objects.all().filter(Teacher_Id = Teacher_Id,Subject = subjects,Day = WeekDay)
        # print('post')
        # print(subjects)
        
        x = datetime.datetime.now()
        x = x.strftime("%x")
        Current_Date = x
        request.session['Current_Date'] = Current_Date
        Attendence_id = str(Teacher_Id) + str(tokens[0]) + str(x) + str(WeekDay)
        print(Attendence_id)
        request.session['Subject'] = subjects
        data1 = Student_Details.objects.all().filter(Semester = tokens[0])
        print("iiiii")
        print(data1)
        for i in data1:
                Barcode = i.Barcode
                Subject = i.Subject
                Name = i.Name
        if Attendance_New.objects.all().filter(Barcode=Barcode,Today_date=Current_Date).exists():
            data = Attendance_New.objects.all().filter(Semester = tokens[0] ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subject_list = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay).order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subject_list})
        
        else:
            print("jjjjj")
            data1 = Student_Details.objects.all().filter(Semester = tokens[0])
            print(data1)
            for i in data1:
                Barcode = i.Barcode
                Subject = i.Subject
                Name = i.Name
                obj = Attendance_New(Teacher_ID = Teacher_Id,Barcode=Barcode,Name=Name,Semester=tokens[0],Today_date = Current_Date,Attendance_status = "Absent",Attendence_id = Attendence_id)
                obj.save() 
            data = Attendance_New.objects.all().filter(Semester = tokens[0] ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subject_list = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay).order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subject_list})
        
    else:
        import datetime
        Teacher_Id = request.session['UserId']
        WeekDay = datetime.datetime.now()
        WeekDay = WeekDay.strftime("%A")
        print(WeekDay)
        subjects = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay).order_by().values('Subject').distinct()
        print(subjects)
        print('else')
        #Attendance_New.objects.all().delete()

    return render(request,'Mark_Attendance.html',{'subjects':subjects})


def Manage_Timetable(request):
    details = Lab.objects.all()
    return render(request,"Manage_Timetable.html",{'details':details})

def Assign_Lab(request):
    Teacher_Id = request.session['UserId']
    if request.method == "POST":
        Day = request.POST['day']
        Time = request.POST['time']
        Subject = request.POST['subject']
        times = Time.split("-")
        start_time=times[0]
        end_time = times[1]
        if(start_time == "09:00"):
            start_time = start_time+" AM"
            end_time = end_time + " PM"
        else:
            start_time = start_time+" PM"
            end_time =end_time +" PM"
        Semester = request.POST['semester']  # get the value of the "semester" field
        if Lab.objects.filter(Day=Day,Start_time=start_time,End_time=end_time).exists():
            messages.info(request,"Lab is occupied")
            return redirect("/Manage_Timetable/")
        else:
            obj = Lab(
                Teacher_Id=Teacher_Id,
                Subject=str(Semester)+"-"+str(Subject),
                Day=Day,
                Start_time=start_time,
                End_time=end_time,
                Semester=Semester  # add the "Semester" field to the Lab object
            )
            obj.save()
            messages.info(request,"Lab is assigned ")
            return redirect("/Manage_Timetable/")
    else:
        return render(request,"Assign_Lab.html",{})

def View_Attendance(request):
    selected_date = None
    if request.method == "POST":
        selected_date = request.POST.get('Today_date')
        selected_subject = request.POST.get('Subject')
        print(selected_date)
        print(selected_subject)
        details = Attendance_New.objects.filter(Today_date=selected_date, Subject=selected_subject)
        print(details)
        td = Attendance_New.objects.order_by().values('Today_date').distinct()
        print("here-td")
        print(td)
        subjects =Attendance_New.objects.order_by().values('Subject').distinct()
        print("here-sub")
        print(subjects)
        if selected_date:
            subjects = subjects.filter(Today_date=selected_date)
        print(subjects)
        return render(request, 'View_Attendance.html', {'today':td,'details': details, 'subjects': subjects, 'selected_date': selected_date})
    else:
        td = Attendance_New.objects.order_by().values('Today_date').distinct()
        print("here-td")
        print(td)
        subjects =Attendance_New.objects.order_by().values('Subject').distinct()
        print("here-sub")
        print(subjects)
        return render(request, 'View_Attendance.html', {'today':td,'subjects': subjects, 'selected_date': selected_date})


def Real_time(request):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        #frame = read_barcodes(frame)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            Teacher_Id = request.session['UserId']
            import datetime
            x = datetime.datetime.now()
            x = x.strftime("%x")
            Current_Date = x
            y = datetime.datetime.now()
            y = y.strftime("%X")
            Current_Time = y
            #Student_id = id
            details =  Student_Details.objects.filter(Barcode = str(barcode_info))
            for i in details:
                Student_id = details[0].id
                Subject =  details[0].Subject
                barcode_number = details[0].Barcode
                print(barcode_number)
            Login_Time = Current_Time
            Logout_Time = Current_Time
            WeekDay = datetime.datetime.now()
            WeekDay = WeekDay.strftime("%A")
            #print(WeekDay)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
    print(str(barcode_info))
    details =  Student_Details.objects.filter(Barcode = str(barcode_info))
    print(details)
    for i in details:
        Student_id = details[0].id
        Subject =  details[0].Subject
        barcode_number = details[0].Barcode
        print(barcode_number)
    if Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Subject = Subject,Today_date = Current_Date,Login_Status = 'True').exists():
        Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Subject = Subject,Today_date = Current_Date).update(Current_Date=Current_Date,Current_Time=Current_Time,Logout_Time=Current_Time,Logout_Status = "True",login_type="Manual")
        messages.info(request,f"Student with ID {Student_id} logged out")
        data = Attendance_New.objects.all().filter(Subject = Subject ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
        subjects = Lab.objects.order_by().values('Subject').distinct()
        return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})
    else:
        Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Subject = Subject,Today_date = Current_Date).update(Current_Date=Current_Date,Current_Time=Current_Time,Login_Time=Login_Time,Login_Status="True",login_type="Manual",Attendance_status="Present")
        #obj.save()
        messages.info(request,f"Student with ID {Student_id} logged in")
        data = Attendance_New.objects.all().filter(Subject = Subject ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
        subjects = Lab.objects.order_by().values('Subject').distinct()
        return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})


    #print(f"Student id is {id}")
    
        

        
            
    #return redirect('/Mark_Attendance')

def Log_In(request, id):
    
    Teacher_Id = request.session['UserId']

    if request.method == "POST":
        bCode = request.POST['barcode']
        bCode = bCode.strip()
        id = str(id).strip()
        if(bCode!=id):
            messages.info(request,"Barcodes do not match")
            return redirect('/Mark_Attendance/')
    

    import datetime
    x = datetime.datetime.now()
    Current_Date = x.strftime("%x")
    y = datetime.datetime.now()
    Current_Time = y.strftime("%I:%M %p")
    print("opoiouyjthdvf")
    print(Current_Time)
    Student_id = id
    print("iddd")
    print(Student_id)

    WeekDay = datetime.datetime.now()
    WeekDay = WeekDay.strftime("%A")
    print(WeekDay)


    details = Student_Details.objects.filter(Barcode = Student_id)
    for i in details:
        Subject = details[0].Subject
        Semester = details[0].Semester
        print(Subject)
        print(Semester)

    LAB = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester)
    for i in LAB:
        Subject_list = LAB[0].Subject

    sub="BTS"
    s = Subject_list.split("-")
    print("hkhgjygdgfdzsfg")
    for i in Subject.split(","):
        if i in s:
            sub=i
            print("fdgfdgfdfds")
            print(sub)
    

    currentHr = y.strftime("%I")
    currentMin  =y.strftime("%M")
    currentTime = str(currentHr)+":"+str(currentMin)
    print(currentTime)
    start_time = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester).order_by().values('Start_time').distinct()
    print('djsjadkjasdis')
    print(start_time)
    print(start_time.count())

    currentStartTime = start_time[0]
    print(currentStartTime)
    s = currentStartTime["Start_time"].split(" ")
    print(s[0])

    e = s[0].split(":")
    print(e)
    endTime = e[0]+":"+"15"
    print(endTime)

    bCode = request.POST.get("barcode")
    if str(bCode)!=str(id):
        messages.info(request,"Barcodes do not match")
    else:
        if currentTime < s[0] or currentTime > endTime:
            messages.info(request, "Student login is only allowed between "+s[0]+" and "+endTime)
            data = Attendance_New.objects.all().filter(Semester=Semester, Teacher_ID=Teacher_Id, Today_date=Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request, 'Mark_Attendance.html', {'data': data, 'subjects': subjects})

        # Check if the student is already logged in
        if Attendance_New.objects.filter(Teacher_ID=Teacher_Id, Barcode=Student_id, Semester=Semester, Today_date=Current_Date, Login_Status='True',Login_Time=currentTime).exists():
            messages.info(request, f"Student with ID {Student_id} is already logged in")
            data = Attendance_New.objects.all().filter(Semester=Semester, Teacher_ID=Teacher_Id, Today_date=Current_Date,Login_Status='True',Login_Time=Current_Time)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request, 'Mark_Attendance.html', {'data': data, 'subjects': subjects})
        else:      
            # obj = Attendance_New(Attendence_id = attendance_id,Teacher_ID=Teacher_Id,Student_ID =Student_id,Subject=Subject,Today_date=Current_Date,Barcode=Student_id,Name=Name,Semester=Semester,Current_Date=Current_Date,Current_Time=Current_Time,Login_Time=Current_Time,Login_Status="True,",Attendance_status="Present")
            # obj.save()
            print("pppppppp")
            Attendance_New.objects.filter(Teacher_ID=Teacher_Id, Barcode=Student_id, Semester=Semester, Today_date=Current_Date).update(
                Subject = sub,Student_ID=Student_id,Current_Date=Current_Date, Current_Time=Current_Time, Login_Time=Current_Time, Login_Status="True",
                login_type="Manual", Attendance_status="Present")      
            messages.info(request, f"Student with ID {Student_id} logged in")
            data = Attendance_New.objects.all().filter(Semester=Semester, Teacher_ID=Teacher_Id, Today_date=Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request, 'Mark_Attendance.html', {'data': data, 'subjects': subjects})

def Log_Out(request,id):
    Teacher_Id = request.session['UserId']
    
    import datetime
    x = datetime.datetime.now()
    x = x.strftime("%x")
    Current_Date = x
    y = datetime.datetime.now()
    Current_Time = y.strftime("%I:%M %p")
    Student_id = id
    details =  Student_Details.objects.filter(Barcode = Student_id)
    for i in details:
        Subject =  details[0].Subject
        Semester = details[0].Semester
        print(Subject)
    Login_Time = Current_Time
    Logout_Time = Current_Time
    WeekDay = datetime.datetime.now()
    WeekDay = WeekDay.strftime("%A")
    print(WeekDay)

    LAB = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester)
    for i in LAB:
        Subject_list = LAB[0].Subject


    for i in Subject:
        if i in Subject_list:
            sub = i
    

    currentHr = y.strftime("%I")
    currentMin  =y.strftime("%M")
    currentTime = str(currentHr)+":"+str(currentMin)
    print(currentTime)
    
    end_time = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester).order_by().values('End_time').distinct()
    print('djsjadkjasdis')
    print(end_time)
    print(end_time.count())

    currentEndTime = end_time[0]
    print(currentEndTime)
    e = currentEndTime["End_time"].split(" ")
    print(e[0])

    s = e[0].split(":")
    print(s)
    t = str((int(s[0]) - 1)).zfill(2)
    startTime =str(t)+":"+"45"
    print(startTime)

    
    if request.method == "POST":
        bCode = request.POST['barcode']
        bCode = bCode.strip()
        id = str(id).strip()
        if(bCode!=id):
            messages.info(request,"Barcodes do not match")
            return redirect('/Mark_Attendance/')
        

    else:
        if currentTime > e[0] or currentTime < startTime:
            messages.info(request, "Student logout is only allowed between "+startTime+" and "+e[0])
            data = Attendance_New.objects.all().filter(Semester=Semester, Teacher_ID=Teacher_Id, Today_date=Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request, 'Mark_Attendance.html', {'data': data, 'subjects': subjects})

            #if Lab.objects.filter(Teacher_Id=Teacher_Id,Subject=Subject,Day=WeekDay).exists():
        if Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date,Logout_Status = 'True').exists():
            messages.info(request,f"Student with ID {Student_id} is already logged out")
            data = Attendance_New.objects.all().filter(Subject = sub ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})

        elif Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date,Login_Status='True').exists():
            Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date).update(Current_Date=Current_Date,Current_Time=Current_Time,Logout_Time=Current_Time,Logout_Status = "True",login_type="Manual")
            messages.info(request,f"Student with ID {Student_id} logged out")
            data = Attendance_New.objects.all().filter(Semester=Semester,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})
        else:
            messages.info(request,"Please login first")
    data = Attendance_New.objects.all().filter(Semester=Semester,Teacher_ID = Teacher_Id,Today_date = Current_Date)
    subjects = Lab.objects.order_by().values('Subject').distinct()
    return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})


def Log_Out_Manual(request,id):
    Teacher_Id = request.session['UserId']
    
    import datetime
    x = datetime.datetime.now()
    x = x.strftime("%x")
    Current_Date = x
    y = datetime.datetime.now()
    Current_Time = y.strftime("%I:%M %p")
    Student_id = id
    print("IDDDDD")
    print(Student_id)

    details =  Student_Details.objects.filter(Barcode = Student_id)
    for i in details:
        Subject =  details[0].Subject
        Semester = details[0].Semester
        print(Subject)
    Login_Time = Current_Time
    Logout_Time = Current_Time
    WeekDay = datetime.datetime.now()
    WeekDay = WeekDay.strftime("%A")
    print(WeekDay)

    LAB = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester)
    for i in LAB:
        Subject_list = LAB[0].Subject


    for i in Subject:
        if i in Subject_list:
            sub = i
    

    currentHr = y.strftime("%I")
    currentMin  =y.strftime("%M")
    currentTime = str(currentHr)+":"+str(currentMin)
    print(currentTime)
    
    end_time = Lab.objects.filter(Teacher_Id = Teacher_Id,Day = WeekDay,Semester = Semester).order_by().values('End_time').distinct()
    print('djsjadkjasdis')
    print(end_time)
    print(end_time.count())

    currentEndTime = end_time[0]
    print(currentEndTime)
    e = currentEndTime["End_time"].split(" ")
    print(e[0])

    s = e[0].split(":")
    print(s)
    t = str((int(s[0]) - 1)).zfill(2)
    startTime =str(t)+":"+"45"
    print(startTime)

    
    if currentTime > e[0] or currentTime < startTime:
            messages.info(request, "Student logout is only allowed between "+startTime+" and "+e[0])
            data = Attendance_New.objects.all().filter(Semester=Semester, Teacher_ID=Teacher_Id, Today_date=Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request, 'Mark_Attendance.html', {'data': data, 'subjects': subjects})

            #if Lab.objects.filter(Teacher_Id=Teacher_Id,Subject=Subject,Day=WeekDay).exists():
    if Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date,Logout_Status = 'True').exists():
            messages.info(request,f"Student with ID {Student_id} is already logged out")
            data = Attendance_New.objects.all().filter(Subject = sub ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})

    elif Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date,Login_Status='True').exists():
            Attendance_New.objects.filter(Teacher_ID = Teacher_Id,Student_ID=Student_id,Semester=Semester,Today_date = Current_Date).update(Current_Date=Current_Date,Current_Time=Current_Time,Logout_Time=Current_Time,Logout_Status = "True",login_type="Manual")
            messages.info(request,f"Student with ID {Student_id} logged out")
            data = Attendance_New.objects.all().filter(Semester=Semester,Teacher_ID = Teacher_Id,Today_date = Current_Date)
            subjects = Lab.objects.order_by().values('Subject').distinct()
            return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})
    else:
            messages.info(request,"Please login first")

    data = Attendance_New.objects.all().filter(Semester=Semester,Teacher_ID = Teacher_Id,Today_date = Current_Date)
    subjects = Lab.objects.order_by().values('Subject').distinct()
    return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects})


def delete_lab(request,id):
    delcomp = Lab.objects.get(id=id) 
    delcomp.delete()
    return redirect('/Manage_Timetable/')

def Generate_percentage(request):
    Teacher_Id = request.session['UserId']
    Subject =  request.session['subject']
    Current_Date = request.session['Current_Date']
    Data = Attendance_New.objects.all().filter(Teacher_ID = Teacher_Id,Subject = Subject,Today_date = Current_Date).count()
    Data1 = Attendance_New.objects.all().filter(Teacher_ID = Teacher_Id,Subject = Subject,Today_date = Current_Date,Attendance_status = "Present").count()
    print(Data1)
    percent = Data1/Data*100
    print(percent)
    data = Attendance_New.objects.all().filter(Subject = Subject ,Teacher_ID = Teacher_Id,Today_date = Current_Date)
    subjects = Lab.objects.order_by().values('Subject').distinct()
    return render(request,'Mark_Attendance.html',{'data':data,'subjects':subjects,'percent':percent})
        
def DeleteTeacher(request,id):
    delcomp = Teacher_Details.objects.get(id=id) 
    delcomp.delete()
    return redirect('/Manage_Teacher/')

def DeleteStudent(request,id):
    delcomp = Student_Details.objects.get(id=id) 
    delcomp.delete()
    return redirect('/Manage_student/')

def Assign_Department_Course_Teacher(request):
    if request.method == "POST":
        Teacher_Id = request.POST['teacher_id']
        Teacher_name = request.POST['teacher_name']
        Department = request.POST['Department']
        Semester = request.POST['Semester']
        Subject = request.POST['Subject']
        Teacher_Details.objects.filter(id=Teacher_Id,Name=Teacher_name).update(Department= Department,Semester = Semester,Subject=Subject,Dept_assigned = "True")
        messages.info(request,"Department and Semester Assigned Sucessfully")
        return redirect('/Manage_Teacher/')
    else:
        return redirect('/Manage_Teacher/')

from django.contrib import messages

def data_upload(request):
    if request.method == 'POST':
        try:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO lab_app_student_details (Name, Age, Gender, Department, Semester, Barcode, Subject) VALUES (%s, %s, %s, %s, %s, %s, %s)", [row['Name'], row['Age'], row['Gender'], row['Department'], row['Semester'], row['Barcode'], row['Subject']])
            messages.success(request, 'Successfully Uploaded')
        except Exception as e:
            messages.error(request, f'Error occurred,Please Upload Proper file')
        return HttpResponseRedirect('/Manage_student/')
    return render(request, 'Manage_student.html')


### Install cv2

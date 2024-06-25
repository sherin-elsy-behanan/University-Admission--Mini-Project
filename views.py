from datetime import date
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
import math
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from university_app.models import *
# Create your views here.
def index(request):
    return render(request,'index.html')
def User_registration(request):
    return render(request,'User_registration.html')
def sign_in(request):
    return render(request,'signin.html')
def sign_in_process(request):
    u=request.POST.get("username")
    p=request.POST.get("password")
    obj=authenticate(username=u,password=p)
    if obj is not None:
        if obj.is_superuser == 1:
            request.session['aname'] = u
            request.session['slogid'] = obj.id
            return redirect('/admin_home/')
        else:
          messages.add_message(request, messages.INFO, 'Invalid User.')
          return redirect('/index/')
    else:
        newp=p
        try:
            obj1=login.objects.get(username=u,password=newp)

            if obj1.Usertype=="Student":
                if(obj1.status=="Approved"):
                    request.session['sname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/student_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/sign_in/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/sign_in/')
            elif obj1.Usertype=="University":
                if(obj1.status=="Approved"):
                    request.session['uname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/university_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/sign_in/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/sign_in/')
            elif obj1.Usertype=="College":
                if(obj1.status=="Approved"):
                    request.session['cname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/college_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/sign_in/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/sign_in/')

            else:
                 messages.add_message(request, messages.INFO, 'Invalid User.')
                 return redirect('/sign_in/')
        except login.DoesNotExist:
         messages.add_message(request, messages.INFO, 'Invalid User.')
         return redirect('/sign_in/')
def admin_home(request):
    if 'aname' in request.session:
     return render(request,'Master/index.html')
    else:
      return redirect('/sign_in/')
def student_home(request):
    if 'sname' in request.session:
     return render(request,'Student/index.html')
    else:
      return redirect('/sign_in/')
def college_home(request):
    if 'cname' in request.session:
     return render(request,'College/index.html')
    else:
      return redirect('/sign_in/')
def university_home(request):
    if 'uname' in request.session:
     return render(request,'University/index.html')
    else:
      return redirect('/sign_in/')
def admin_logout(request):
    logout(request)
    request.session.delete()
    return redirect('/sign_in/')
def user_logout(request):
    logout(request)
    request.session.delete()
    return redirect('/sign_in/')


def display_district(request):
    state_id = request.GET.get("state_id")
    try:

        dist = district.objects.filter(state_id = state_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('district_id', 'district')), safe = False)

def check_username(request):
    username = request.GET.get("username")
    data = {
       'username_exists':      login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        data["success"]="Available"

    return JsonResponse(data)
def student_action(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        tbl1=login()
        username=request.POST.get("username")
        tbl1.username=request.POST.get("username")
        password=request.POST.get("password")
        tbl1.password=request.POST.get("password")
        tbl1.Usertype="Student"
        tbl1.status="Approved"
        tbl1.save()
        obj=login.objects.get(username=username,password=password)

        u=Student()
        u.login_id = obj.login_id
        u.student_name=request.POST.get("student_name")
    
        u.phone_number =request.POST.get("phone")
        u.Email=request.POST.get("Email")
        u.Address=request.POST.get("address")
        u.place=request.POST.get("place")

        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('/User_registration/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/User_registration/')
def add_university(request):
 if 'aname' in request.session:
    data = state.objects.all()
    return render(request,'Master/add_university.html',{'data':data})
 else:
    return redirect('/sign_in/')
def save_university(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):

        tbl1=login()

        tbl1.username=request.POST.get("username")

        tbl1.password=password
        tbl1.Usertype="University"
        tbl1.status="Approved"
        tbl1.save()
        obj=login.objects.get(username=username,password=password)

        u=university()
        u.login_id = obj.login_id
        u.university=request.POST.get("university")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.district_id=request.POST.get("district")
        u.place=request.POST.get("place")

        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('/add_university/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/add_university/')
def university_list(request):
    if 'aname' in request.session:
            cursor=connection.cursor()
            cursor.execute("select p.*,s.state,d.district from  tbl_university as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id ")
            data=cursor.fetchall()
            return render(request,'Master/university_list.html',{'data':data})
    else:
        return redirect('/sign_in/')
def edit_university(request,id):
 if 'aname' in request.session:
    data=university.objects.get(university_id=id)
    return render(request,'Master/edit_university.html',{'data':data})
 else:
      return redirect('/sign_in/')
def update_university(request,id):
 if 'aname' in request.session:
    u=university.objects.get(university_id=id)
    u.university=request.POST.get("university")
    u.address =request.POST.get("address")
    u.email=request.POST.get("email")
    u.phone_number=request.POST.get("phone_number")
    u.place=request.POST.get("place")
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/university_list/')
 else:
      return redirect('/sign_in/')
def delete_university(request,id):
 if 'aname' in request.session:
    tbl=university.objects.get(university_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/university_list/')
 else:
      return redirect('/sign_in/')

def Complaint_frm(request):
    if 'sname' in request.session:
        logid=request.session['slogid']
        data1 = complaint.objects.filter(user_login_id=logid)
        return render(request,'Student/complaint.html',{'data1':data1})
    else:
       return redirect('/sign_in/')
def save_complaint(request):
    if 'sname' in request.session:
        tbl=complaint()
        tbl.user_login_id=request.session['slogid']
        tbl.complaint_subject=request.POST.get("subject")
        tbl.complaint=request.POST.get("complaint")
        tbl.reply="No"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/complaint')
    else:
       return redirect('/sign_in/')

def delete_complaint(request,id):
    if 'sname' in request.session:
        tbl=complaint.objects.get(complaint_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/complaint')
    else:
       return redirect('/sign_in/')


def feedback_frm(request):
    if 'sname' in request.session:
        logid=request.session['slogid']
        data1 = feedback.objects.filter(user_login_id=logid)
        return render(request,'Student/feedback.html',{'data1':data1})
    else:
       return redirect('/sign_in/')
def save_feedback(request):
    if 'sname' in request.session:
        tbl=feedback()
        tbl.user_login_id=request.session['slogid']
        tbl.feedback_subject=request.POST.get("subject")
        tbl.feedback=request.POST.get("feedback")
        tbl.reply="No"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/feedback')
    else:
       return redirect('/sign_in/')

def delete_feedback(request,id):
    if 'sname' in request.session:
        tbl=feedback.objects.get(feedback_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/feedback')
    else:
       return redirect('/sign_in/')

    # ----------------Admin Complaint -------------
def view_complaints(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_complaint  as c inner join  tbl_student as u  on c.user_login_id =u.login_id where c.reply='No'  order by c.complaint_id desc")
        data=cursor.fetchall()
        return render(request,'Master/view_complaints.html',{'data':data})
    else:
       return redirect('/sign_in/')
def replied_list(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_complaint  as c inner join  tbl_student as u  on c.user_login_id =u.login_id where c.reply!='No' order by c.complaint_id desc")
        data=cursor.fetchall()
        return render(request,'Master/replied_complaints.html',{'data':data})
    else:
       return redirect('/sign_in/')
def adm_reply_complaint(request,id):
    if 'aname' in request.session:

        return render(request,'Master/reply_complaint.html',{'id':id})
    else:
       return redirect('/sign_in/')
def add_reply(request,id):
    tbl=complaint.objects.get(complaint_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('/replied_list')


# Admin feedback

def view_feedback(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_feedback  as c inner join  tbl_student as u  on c.user_login_id =u.login_id where c.reply='No'  order by c.feedback_id desc")
        data=cursor.fetchall()
        return render(request,'Master/view_feedback.html',{'data':data})
    else:
       return redirect('/sign_in/')
def feedback_replied_list(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_feedback  as c inner join  tbl_student as u  on c.user_login_id =u.login_id where c.reply!='No' order by c.feedback_id desc")
        data=cursor.fetchall()
        return render(request,'Master/replied_feedback.html',{'data':data})
    else:
       return redirect('/sign_in/')
def adm_reply_feedback(request,id):
    if 'aname' in request.session:

        return render(request,'Master/reply_feedback.html',{'id':id})
    else:
       return redirect('/sign_in/')
def add_reply_feedback(request,id):
    tbl=feedback.objects.get(feedback_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('/feedback_replied_list')

def Users_list(request):
 if 'aname' in request.session:
     data1 = student.objects.all()
     return render(request,'Master/Users_list.html',{'data':data1})
 else:
      return redirect('/sign_in/')
def add_college(request):
    if 'uname' in request.session:
        data = state.objects.all()
        return render(request,'University/add_college.html',{'data':data})
    else:
       return redirect('/sign_in/')
def save_college(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        logid=  request.session['slogid']
        tbl1=login()

        tbl1.username=request.POST.get("username")

        tbl1.password=password
        tbl1.Usertype="College"
        tbl1.status="Approved"
        tbl1.save()
        obj=login.objects.get(username=username,password=password)

        u=college()
        u.login_id = obj.login_id
        u.university_login_id = logid
        u.college=request.POST.get("college")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.district_id=request.POST.get("district")
        u.place=request.POST.get("place")

        u.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_college/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/add_college/')
def college_list(request):
    if 'uname' in request.session:
            logid=  request.session['slogid']
            cursor=connection.cursor()
            cursor.execute("select p.*,s.state,d.district from  tbl_college as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id where p.university_login_id="+str(logid))
            data=cursor.fetchall()
            return render(request,'University/college_list.html',{'data':data})
    else:
        return redirect('/sign_in/')
def edit_college(request,id):
 if 'uname' in request.session:
    data=college.objects.get(college_id=id)
    return render(request,'University/edit_college.html',{'data':data})
 else:
      return redirect('/sign_in/')
def update_college(request,id):
 if 'uname' in request.session:
    u=college.objects.get(college_id=id)
    u.college=request.POST.get("college")
    u.address =request.POST.get("address")
    u.email=request.POST.get("email")
    u.phone_number=request.POST.get("phone_number")
    u.place=request.POST.get("place")
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/college_list/')
 else:
      return redirect('/sign_in/')
def delete_college(request,id):
 if 'uname' in request.session:
    tbl=college.objects.get(college_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/college_list/')
 else:
      return redirect('/sign_in/')
 
def add_course(request):
    if 'uname' in request.session:
        logid=  request.session['slogid']
        data = course.objects.filter(university_login_id = logid)
        return render(request,'University/add_course.html',{'data':data})
    else:
       return redirect('/sign_in/')
def save_course(request):
    if 'uname' in request.session:
        c=request.POST.get("course")
     
        data = {
       'exists':      course.objects.filter(course=c).exists(),
        'error':"Already Exist"
        }
        if(data["exists"]==False):  
            logid=  request.session['slogid']
            u=course()
            u.university_login_id = logid
            u.course=request.POST.get("course")
            u.fee =request.POST.get("fee")
            u.course_type=request.POST.get("course_type")
            

            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_course/')
        else:
           messages.add_message(request, messages.INFO, 'Failed..  Course has been already added ')
           return redirect('/add_course/')
    else:
       return redirect('/sign_in/')

def edit_course(request,id):
 if 'uname' in request.session:
    data=course.objects.get(course_id=id)
    return render(request,'University/edit_course.html',{'data':data})
 else:
      return redirect('/sign_in/')
def update_course(request,id):
 if 'uname' in request.session:
    u=course.objects.get(course_id=id)
    u.course=request.POST.get("course")
    u.fee =request.POST.get("fee")
    u.course_type=request.POST.get("course_type")
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/add_course/')
 else:
      return redirect('/sign_in/')
def delete_course(request,id):
 if 'uname' in request.session:
    tbl=course.objects.get(course_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/add_course/')
 else:
      return redirect('/sign_in/')
 
#  Batch
def add_batch(request):
    if 'uname' in request.session:
        today = datetime.date.today()
        y=today.year
        year = []   
        y1=y+1
        year1=str(y)+"-"+str(y1)

        year.append(year1)
        y2=y+2
        year2=str(y)+"-"+str(y2)
        year.append(year2)
        y3=y+3
        year3=str(y)+"-"+str(y3)
        year.append(year3)
        y4=y+4
        year4=str(y)+"-"+str(y4)
        year.append(year4)
        y5=y+5
        year5=str(y)+"-"+str(y5)
        year.append(year5)
        logid=  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select b.*, c.* from tbl_batch as b inner join tbl_course as c on b.course_id = c.course_id where c.university_login_id = "+str(logid))
        data=cursor.fetchall()
        data1 = course.objects.filter(university_login_id = logid)
        return render(request,'University/add_batch.html',{'data':data,'data1':data1,'year':year})
    else:
       return redirect('/sign_in/')
def save_batch(request):
    if 'uname' in request.session:
        c=request.POST.get("course_id")
     
        data = {
       'exists':      batch.objects.filter(course_id=c).exists(),
        'error':"Already Exist"
        }
        if(data["exists"]==False):  
            u=batch()
            u.course_id = request.POST.get("course_id")
            u.batch=request.POST.get("batch")
        
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_batch/')
        else:
           messages.add_message(request, messages.INFO, 'Failed..  batch has been already added to this course ')
           return redirect('/add_batch/')
    else:
       return redirect('/sign_in/')


def delete_batch(request,id):
 if 'uname' in request.session:
    tbl=batch.objects.get(batch_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/add_batch/')
 else:
      return redirect('/sign_in/')
 
def offer_courses(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
        data = college.objects.filter(university_login_id = logid)
        data1 = course.objects.filter(university_login_id = logid)
        return render(request,'University/offer_course.html',{'data':data,'data1':data1})
    else:
       return redirect('/sign_in/')
def save_offer_course(request):
    if 'uname' in request.session:
        college= request.POST.get("college")
        course= request.POST.get("course")
        data = {
       'exists':      offer_course.objects.filter(college_login_id=college,course_id=course).exists(),
        'error':"Already Exist"
        }
        if(data["exists"]==False):       
            u=offer_course()
            u.college_login_id = request.POST.get("college")
            u.course_id=request.POST.get("course")
            u.seat=request.POST.get("seats")
        
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/offer_courses/')
        else:
            messages.add_message(request, messages.INFO, 'Failed.. this course has been already offered to this college ')
            return redirect('/offer_courses/')
    else:
        return redirect('/sign_in/')
def view_offered_courses(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select oc.offer_course_id,oc.seat, c.*,cl.*, oc.entry_date from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id inner join tbl_college as cl on cl.login_id=oc.college_login_id where c.university_login_id = "+str(logid))
        data=cursor.fetchall()
        colleges = college.objects.filter(university_login_id = logid)
        courses = course.objects.filter(university_login_id = logid)
        return render(request,'University/view_offered_courses.html',{'data':data,'colleges':colleges,'courses':courses})
    else:
       return redirect('/sign_in/')
    
def edit_course_offer(request,id):
    if 'uname' in request.session:
        data=offer_course.objects.get(offer_course_id=id)
        return render(request,'University/edit_course_offer.html',{'data':data})
    else:
        return redirect('/index/')
def update_course_offer(request,id):
    if 'uname' in request.session:
        u=offer_course.objects.get(offer_course_id=id)
       
        u.seat =request.POST.get("seats")
        u.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('/view_offered_courses/')
    else:
        return redirect('/sign_in/')
def delete_course_offer(request,id):
    if 'uname' in request.session:
        tbl=offer_course.objects.get(offer_course_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/view_offered_courses/')
    else:
        return redirect('/sign_in/')
def display_offered_courses(request):
    str1=" <table class='table table-striped table-bordered'><thead><th>Id</th><th>Seats</th><th>Course</th><th>Type</th><th>Fee</th><th>College Details</th><th>Offered date</th></thead><tr>"
    college_login_id=request.GET.get("college")
    cursor=connection.cursor()
    cursor.execute("select oc.offer_course_id,oc.seat, c.*,cl.*, oc.entry_date from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id inner join tbl_college as cl on cl.login_id=oc.college_login_id where oc.college_login_id="+str(college_login_id))
    data=cursor.fetchall()
    count=1
    for k in data:
       str1+="<tr><td>"+str(count)+"<td>"+str(k[1])+"</td><td>"+str(k[3])+"</td><td>"+str(k[4])+"</td><td>"+str(k[6])+"</td><td>College :<b>"+str(k[10])+"</b> <br>  <b>Address : "+str(k[11])+"</b><br> Email : <b>"+str(k[10])+"</b> <br>  Phone Number : "+str(k[13])+"</b><br> Place :<b>"+str(k[15])+"</b><br></td> <td>"+str(k[16])+"</td> <td><a href='/edit_course_offer/"+str(k[0])+"' class='btn btn-info'>Edit</a></td><td><a href='/delete_course_offer/"+str(k[0])+"' class='btn btn-danger'>Delete</a></td>"
                           
       count=count+1
                        

    str1+="</table>"                
    return HttpResponse(str1)
def add_notification(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
       
        data1 = course.objects.filter(university_login_id = logid)
        return render(request,'University/add_notification.html',{'data1':data1})
    else:
       return redirect('/index/')
def display_batch(request):
    course_id = request.GET.get("course_id")
    try:

        batchs = batch.objects.filter(course_id = course_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(batchs.values('batch_id', 'batch')), safe = False)
def save_notification(request):
    if 'uname' in request.session:
        batchs= request.POST.get("batch_id")
        data = {
       'exists':admission_notification.objects.filter(batch_id=batchs).exists(),
        'error':"Already Exist"
        }
        if(data["exists"]==False):       
            u=admission_notification()
            u.batch_id = request.POST.get("batch_id")
            u.eligibility=request.POST.get("eligibility")
            u.course_details=request.POST.get("course_details")
            u.last_date=request.POST.get("last_date")
            u.application_fee=request.POST.get("application_fee")
            
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_notification/')
        else:
            messages.add_message(request, messages.INFO, 'Failed.. Notification for this course and batch have been already added ')
            return redirect('/add_notification/')
    else:
        return redirect('/sign_in/')
def view_notification(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select n.*,b.batch,c.course from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id  where c.university_login_id = "+str(logid))
        data=cursor.fetchall()
        return render(request,'University/view_notification.html',{'data':data})
    else:
       return redirect('/sign_in/')
def edit_notification(request,id):
    if 'uname' in request.session:
        data=admission_notification.objects.get(admission_notification_id=id)
        return render(request,'University/edit_notification.html',{'data':data})
    else:
        return redirect('/sign_in/')
def update_notification(request,id):
    if 'uname' in request.session:
        u=admission_notification.objects.get(admission_notification_id=id)
        u.eligibility=request.POST.get("eligibility")
        u.course_details=request.POST.get("course_details")
        u.last_date=request.POST.get("last_date")
        u.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('/view_notification/')
    else:
        return redirect('/sign_in/')
def delete_notification(request,id):
    if 'uname' in request.session:
        tbl=admission_notification.objects.get(admission_notification_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/view_notification/')
    else:
        return redirect('/sign_in/')
    
def candidate_details(request):
    if 'sname' in request.session:
        logid =  request.session['slogid']
        data=Student.objects.get(login_id=logid)
        return render(request,'Student/candidate_details.html',{'data':data})
    else:
        return redirect('/sign_in/')
def save_candidate(request):
    if 'sname' in request.session:
            logid =  request.session['slogid']
            u=Student.objects.get(login_id=logid)
            u.date_of_birth = request.POST.get("dob")
            u.permanant_address=request.POST.get("permanant_address")
            u.father_name=request.POST.get("fname")
            u.mother_name=request.POST.get("mname")
            u.gender=request.POST.get("gender")
            u.nationality=request.POST.get("nationality")
            u.caste=request.POST.get("caste")
            u.religion=request.POST.get("religion")
            u.caste_category=request.POST.get("caste_category")
            u.adhaar_no=request.POST.get("adhaar_no")
            u.blood_group=request.POST.get("blood_group")
            u.status="Updated"
            photo=request.FILES['photo']

            split_tup = os.path.splitext(photo.name)
            file_extension = split_tup[1]
            # folder path
            dir_path = settings.MEDIA_ROOT
            count = 0
            # Iterate directory
            for path in os.listdir(dir_path):
            # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+"."+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,photo)
            url1=obj.url(file)
            u.photo=url1
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/candidate_details/')
       
    else:
        return redirect('/sign_in/')
def serach_notification(request):
    if 'sname' in request.session:
        
        cursor=connection.cursor()
        cursor.execute("select p.*,s.state,d.district from  tbl_university as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id ")
        data=cursor.fetchall()
        data1 = university.objects.all()
        return render(request,'Student/serach_notification.html',{'data1':data1,'data':data})
    else:
       return redirect('/sign_in/')
def view_notifications(request,id,college_id):

    cid=id
    today = date.today()
    cursor=connection.cursor()
    sql="select n.*,b.batch,c.course,c.course_type,c.fee,b.batch_id from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id inner join tbl_offer_course as oc on c.course_id=oc.course_id inner join tbl_college as cl on oc.college_login_id= cl.login_id  where c.course_id="+str(cid)+"  and n.last_date >= '"+str(today)+"'"
    cursor.execute(sql)
    data=cursor.fetchall()

    batch_id=0
    for i in data:
        batch_id=i[11]
    
    cursor=connection.cursor()
    cursor.execute("select count(*) from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id  inner join tbl_application as a on a.admission_notification_id= n.admission_notification_id inner join tbl_college as cl on a.college_login_id= cl.login_id  where a.college_login_id = "+str(college_id)+" and a.status='Approved' and n.batch_id="+str(batch_id)+" and c.course_id="+str(cid))
    data1=cursor.fetchall()
    
    count_appl=0
    for i in data1:
        count_appl=i[0]
  
    data3 = offer_course.objects.get(college_login_id=college_id, course_id=cid)
    tot_seat=data3.seat

    available=tot_seat-count_appl
    return render(request,'Student/view_notification.html',{'data':data,'college_id':college_id,'tot_seat':tot_seat,'available':available })
def display_college(request):
    university_login_id = request.GET.get("university_login_id")
    try:

        dist = college.objects.filter(university_login_id = university_login_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('login_id', 'college')), safe = False)
def display_offered_course(request):
    college_login_id = request.GET.get("college_login_id")
    cursor=connection.cursor()
    cursor.execute("select c.course_id,c.course from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id  where oc.college_login_id = "+str(college_login_id))
    data=cursor.fetchall()
    str1="<option value="">--Select--</option>"
    for k in data:
        str1+="<option value="+str(k[0])+">"+str(k[1])+"</option>"
                 
    return HttpResponse(str1)
def search_notification_result(request):
    if 'sname' in request.session:
        cid=request.POST.get("course")
        college_login_id=request.POST.get("college")
        today = date.today()
        cursor=connection.cursor()
        cursor.execute("select n.*,b.batch,c.course,c.course_type,c.fee from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id inner join tbl_offer_course as oc on c.course_id=oc.course_id inner join tbl_college as cl on oc.college_login_id= cl.login_id  where c.course_id="+str(cid)+" and cl.login_id="+str(college_login_id)+" and n.last_date >= '"+str(today)+"'")
        data=cursor.fetchall()
        
        data1 = university.objects.all()
        return render(request,'Student/search_notification_result.html',{'data':data,'data1':data1,'college_login_id':college_login_id})
    else:
       return redirect('/sign_in/')  
def view_colleges(request,id):
    if 'sname' in request.session:
           
            cursor=connection.cursor()
            cursor.execute("select p.*,s.state,d.district from  tbl_college as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id where p.university_login_id="+str(id))
            data=cursor.fetchall()
            return render(request,'Student/college_list.html',{'data':data})
    else:
        return redirect('/sign_in/')
def view_course_offered(request,id):
    if 'sname' in request.session:
        
        cursor=connection.cursor()
        cursor.execute("select oc.offer_course_id,oc.seat, c.*,cl.*, oc.entry_date from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id inner join tbl_college as cl on cl.login_id=oc.college_login_id  where oc.college_login_id = "+str(id))
        data=cursor.fetchall()

        return render(request,'Student/course_list.html',{'data':data,'college_login_id':id})
    else:
        return redirect('/sign_in/')
def apply_notification(request,id,college_id):
    if 'sname' in request.session:
        data3=Student.objects.filter(login_id=request.session['slogid'], status="Not Updated")
        data=admission_notification.objects.get(admission_notification_id=id)
        data1=application.objects.filter(admission_notification_id=id,candidate_login_id=request.session['slogid'],college_login_id=college_id)
        if data3:
            messages.add_message(request, messages.INFO, 'You have not updated more candidate details. Please update before you apply for a course')
            return redirect('/serach_notification/') 
        elif data1:
            messages.add_message(request, messages.INFO, 'Candidate has already been applied for this course')
            return redirect('/serach_notification/') 
        else:
            return render(request,'Student/apply_notification.html',{'id':id,'data':data,'college_id':college_id})
        
    else:
        return redirect('/sign_in/')
def save_application(request,id,college_id):
    if 'sname' in request.session:
        application_fee= request.POST.get("application_fee")
        tbl=application()
        tbl.college_login_id=college_id
        tbl.candidate_login_id=request.session['slogid']
        tbl.admission_notification_id=id
        tbl.application_fee=request.POST.get("application_fee")
        tbl.qualified_examination=request.POST.get("qualified_examination")
        tbl.qualified_examination_mark=request.POST.get("qualified_examination_mark")
        tbl.qualified_examination_total_mark=request.POST.get("qualified_examination_total_mark")
        tbl.quota=request.POST.get("quota")
        tbl.status="Paid"
        # Exam Certificate
        qualified_examination_certificate=request.FILES['qualified_examination_certificate']

        split_tup = os.path.splitext(qualified_examination_certificate.name)
        file_extension = split_tup[1]
        # folder path
        dir_path = settings.MEDIA_ROOT
        count = 0
        # Iterate directory
        for path in os.listdir(dir_path):
        # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        filecount=count+1
        filename=str(filecount)+"."+file_extension
        obj=FileSystemStorage()
        file=obj.save(filename,qualified_examination_certificate)
        url1=obj.url(file)
        tbl.qualified_examination_certificate=url1
        # End Exam certificate
        # .....................................................

        sslc_certificate=request.FILES['sslc_certificate']

        split_tup = os.path.splitext(sslc_certificate.name)
        file_extension = split_tup[1]
        # folder path
        dir_path = settings.MEDIA_ROOT
        count = 0
        # Iterate directory
        for path in os.listdir(dir_path):
        # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        filecount=count+1
        filename=str(filecount)+"."+file_extension
        obj=FileSystemStorage()
        file=obj.save(filename,sslc_certificate)
        url1=obj.url(file)
        tbl.sslc_certificate=url1
    #    .....................................................
        upload_file_type1 = request.FILES.get('income_certificate', None)
        if upload_file_type1 is not None:
            income_certificate=request.FILES['income_certificate']

            split_tup = os.path.splitext(income_certificate.name)
            file_extension = split_tup[1]
            # folder path
            dir_path = settings.MEDIA_ROOT
            count = 0
            # Iterate directory
            for path in os.listdir(dir_path):
            # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+"."+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,income_certificate)
            url1=obj.url(file)
            tbl.income_certificate=url1

     #    .....................................................
        upload_file_type2 = request.FILES.get('caste_certificate', None)
        if upload_file_type2 is not None:
            caste_certificate=request.FILES['caste_certificate']

            split_tup = os.path.splitext(caste_certificate.name)
            file_extension = split_tup[1]
            # folder path
            dir_path = settings.MEDIA_ROOT
            count = 0
            # Iterate directory
            for path in os.listdir(dir_path):
            # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+"."+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,caste_certificate)
            url1=obj.url(file)
            tbl.caste_certificate=url1

        tbl.save()
        messages.add_message(request, messages.INFO, 'Application Sent to College')
        c=application.objects.latest('application_id')
        app_id=c.application_id
        # return redirect('/application_payment/'+str(app_id))
        return redirect('/serach_notification/')
        
    else:
       return redirect('/sign_in/')
def application_payment(request,id):
    if 'sname' in request.session:
        
        data=application.objects.get(application_id=id)

        return render(request,'Student/application_fee_payment.html',{'application_id':id,'data':data})
    else:
        return redirect('/sign_in/')
def save_application_payment(request,id):
    if 'sname' in request.session:
        data=application.objects.get(application_id=id)
        data.status="Paid"
        data.save()
        messages.add_message(request, messages.INFO, 'Application  sent to College.. Paid Successfully .')
        return redirect('/serach_notification/')
    else:
        return redirect('/sign_in/')
def candidate_applications(request):
    if 'sname' in request.session:
        logid=request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select b.batch,c.course,c.course_type,cl.*,a.* from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id  inner join tbl_application as a on a.admission_notification_id= n.admission_notification_id inner join tbl_college as cl on a.college_login_id= cl.login_id  where a.candidate_login_id = "+str(logid))
        data=cursor.fetchall()
        return render(request,'Student/candidate_applications.html',{'data':data})
    else:
       return redirect('/sign_in//')
def change_password(request):
    if 'sname' in request.session:

        return render(request,'Student/change_password.html')
    else:
       return redirect('/sign_in//')
def update_password(request):
    if 'sname' in request.session:
        id=request.session['slogid']
        opass=request.POST.get("opassword")
        npass=request.POST.get("password")
        obj1=login.objects.filter(login_id=id,password=opass)
        if(obj1):
            tbl1=login.objects.get(login_id=id)
            tbl1.password=npass
            tbl1.save()
            messages.add_message(request, messages.INFO, 'Updated Please Login Using new Password.')
            return redirect('/sign_in//')
        else:
            messages.add_message(request, messages.INFO, 'Invalid Data')
            return redirect('/change_password/')
    else:
       return redirect('/sign_in/')
def applications(request):
    if 'cname' in request.session:
        logid =  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select b.batch,c.course,c.course_type,cl.*,a.* from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id  inner join tbl_application as a on a.admission_notification_id= n.admission_notification_id inner join tbl_college as cl on a.college_login_id= cl.login_id  where a.college_login_id = "+str(logid)+" and a.status='Paid'")
        data=cursor.fetchall()
        return render(request,'College/applications.html',{'data':data})
    else:
       return redirect('/sign_in/')
def view_candidate(request,id):
    if 'cname' in request.session:
      
        data=Student.objects.get(login_id=id)
        return render(request,'College/candidate_details.html',{'data':data})
    else:
        return redirect('/sign_in/')
    
def approve_application(request,id):
    if 'cname' in request.session:
        tbl=application.objects.get(application_id=id)
        tbl.status="Approved"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Approved successfully.')
        return redirect('/applications/')
    else:
       return redirect('/sign_in/')
def reject_application(request,id):
    if 'suname' in request.session:
        tbl=application.objects.get(application_id=id)
        tbl.status="Rejected"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Rejected successfully.')
        return redirect('/applications/')
    else:
        return redirect('/sign_in/')
def approved_student_list(request):
    if 'cname' in request.session:
        logid =  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select b.batch,c.course,c.course_type,cl.*,a.* from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id  inner join tbl_application as a on a.admission_notification_id= n.admission_notification_id inner join tbl_college as cl on a.college_login_id= cl.login_id  where a.college_login_id = "+str(logid)+" and a.status='Approved'")
        data=cursor.fetchall()
        return render(request,'College/approved_student_list.html',{'data':data})
    else:
       return redirect('/sign_in/')
def offered_course_list(request):
     if 'cname' in request.session:
        logid =  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select oc.offer_course_id,oc.seat, c.*,cl.*, oc.entry_date from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id inner join tbl_college as cl on cl.login_id=oc.college_login_id where oc.college_login_id = "+str(logid))
        data=cursor.fetchall()
        return render(request,'College/offered_course_list.html',{'data':data})
     else:
       return redirect('/sign_in/')
def admission_notifications(request):
    if 'cname' in request.session:
        
        college_login_id=request.session['slogid']
        today = date.today()
        cursor=connection.cursor()
        cursor.execute("select n.*,b.batch,c.course,c.course_type,c.fee from tbl_admission_notification as n inner join tbl_batch as b on b.batch_id=n.batch_id inner join tbl_course as c on b.course_id = c.course_id inner join tbl_offer_course as oc on c.course_id=oc.course_id inner join tbl_college as cl on oc.college_login_id= cl.login_id  where cl.login_id="+str(college_login_id)+" and n.last_date >= "+str(today))
        data=cursor.fetchall()
        
        
        return render(request,'College/college_admission_notification.html',{'data':data})
    else:
       return redirect('/sign_in/') 
def admin_college_List(request):
    if 'aname' in request.session:
        uni=university.objects.all()
        cursor=connection.cursor()
        # cursor.execute("select p.*,s.state,d.district from  tbl_college as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id where p.university_login_id="+str(id))
        cursor.execute("select p.*,s.state,d.district from  tbl_college as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id")
        data=cursor.fetchall()
        return render(request,'Master/admin_college_List.html',{'data':data,'uni':uni})
    else:
       return redirect('/sign_in/')
def admin_view_course_offered(request,id):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select oc.offer_course_id,oc.seat, c.*,cl.*, oc.entry_date from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id inner join tbl_college as cl on cl.login_id=oc.college_login_id where oc.college_login_id="+str(id))
        data=cursor.fetchall()
        return render(request,'Master/admin_view_course_offered.html',{'data':data})
    else:
        return redirect('/sign_in/')
def admin_college_list_by_university(request):
    if 'aname' in request.session:
        id=request.POST.get("university")
        uni=university.objects.all()
        cursor=connection.cursor()
        cursor.execute("select p.*,s.state,d.district from  tbl_college as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id where p.university_login_id="+str(id))
    
        data=cursor.fetchall()
        return render(request,'Master/admin_college_list_by_university.html',{'data':data,'uni':uni})
    else:
       return redirect('/sign_in/')
def student_List(request):
    if 'aname' in request.session:
        data1 = university.objects.all()
        return render(request,'Master/student_List.html',{'data1':data1})
    else:
       return redirect('/sign_in/')
def display_batch_list(request):
    course_id = request.GET.get("course_id")
    cursor=connection.cursor()
    cursor.execute("select batch_id,batch from  tbl_batch  where course_id = "+str(course_id))
    data=cursor.fetchall()
    str1="<option value="">--Select--</option>"
    for k in data:
        str1+="<option value="+str(k[0])+">"+str(k[1])+"</option>"
                 
    return HttpResponse(str1)
def student_list_filter(request):
    if 'aname' in request.session:
        course_id=request.POST.get("course")
        college_login_id=request.POST.get("college")
        batch_id=request.POST.get("batch")
        uni=university.objects.all()
        cursor=connection.cursor()
        cursor.execute("select s.*,c.course,b.batch from tbl_student as s inner join tbl_application as a on s.login_id=a.candidate_login_id inner join tbl_admission_notification as n on a.admission_notification_id=n.admission_notification_id inner join tbl_batch as b on n.batch_id=b.batch_id inner join tbl_course as c on c.course_id=b.course_id where n.batch_id="+str(batch_id)+" and c.course_id="+str(course_id)+" and a.college_login_id="+str(college_login_id)+" and a.status='Approved'")
    
        data=cursor.fetchall()
        return render(request,'Master/adm_student_list.html',{'data':data,'uni':uni})
    else:
       return redirect('/sign_in/')
def adm_view_candidate(request,id):
    if 'aname' in request.session:
      
        data=Student.objects.get(login_id=id)
        return render(request,'Master/candidate_details.html',{'data':data})
    else:
        return redirect('/index/')
def add_hostel_details(request):
    if 'cname' in request.session:
       
        return render(request,'College/add_hostel_details.html')
    else:
        return redirect('/sign_in/')
def hostel_list(request):
    if 'cname' in request.session:
        college_login_id=request.session['slogid']
        data=hostel.objects.filter(college_login_id=college_login_id)
        return render(request,'College/hostel_list.html',{'data':data})
    else:
        return redirect('/sign_in/')
    
def save_hostel(request):
    if 'cname' in request.session:
            u=hostel()
            college_login_id=request.session['slogid']
            u.college_login_id = college_login_id
            u.total_seat = request.POST.get("total_seat")
            u.seat_availability=request.POST.get("seat_availablity")
            u.address=request.POST.get("address")
            u.phone_number=request.POST.get("phone_number")
            u.rules=request.POST.get("rules")
            u.type=request.POST.get("hostel_type")
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_hostel_details/')
    else:
        return redirect('/sign_in/')
def edit_hostel(request,id):
    if 'cname' in request.session:
        data=hostel.objects.get(hostel_id=id)
        return render(request,'College/edit_hostel.html',{'id':id,'data':data})
    else:
        return redirect('/sign_in/')
    
def update_hostel(request,id):
    if 'cname' in request.session:
            u=hostel.objects.get(hostel_id=id)
            college_login_id=request.session['slogid']
            u.college_login_id = college_login_id
            u.total_seat = request.POST.get("total_seat")
            u.seat_availability=request.POST.get("seat_availablity")
            u.address=request.POST.get("address")
            u.phone_number=request.POST.get("phone_number")
            u.rules=request.POST.get("rules")
            u.type=request.POST.get("hostel_type")
            u.save()
            messages.add_message(request, messages.INFO, 'Updated successfully.')
            return redirect('/hostel_list/')
    else:
        return redirect('/sign_in/')
def delete_hostel(request,id):
 if 'cname' in request.session:
    tbl=hostel.objects.get(hostel_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/hostel_list/')
 else:
      return redirect('/sign_in/')
def add_bus_details(request):
    if 'cname' in request.session:
       
        return render(request,'College/add_bus_details.html')
    else:
        return redirect('/sign_in/')
def bus_list(request):
    if 'cname' in request.session:
        college_login_id=request.session['slogid']
        data=bus.objects.filter(college_login_id=college_login_id)
        return render(request,'College/bus_list.html',{'data':data})
    else:
        return redirect('/sign_in/')
    
def save_bus(request):
    if 'cname' in request.session:
            u=bus()
            college_login_id=request.session['slogid']
            u.college_login_id = college_login_id
            u.bus_number = request.POST.get("bus_number")
            u.route=request.POST.get("route")
            u.stops=request.POST.get("stops")
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_bus_details/')
    else:
        return redirect('/sign_in/')
def edit_bus(request,id):
    if 'cname' in request.session:
        data=bus.objects.get(bus_id=id)
        return render(request,'College/edit_bus.html',{'id':id,'data':data})
    else:
        return redirect('/sign_in/')
    
def update_bus(request,id):
    if 'cname' in request.session:
            u=bus.objects.get(bus_id=id)
            college_login_id=request.session['slogid']
            u.college_login_id = college_login_id
            u.bus_number = request.POST.get("bus_number")
            u.route=request.POST.get("route")
            u.stops=request.POST.get("stops")
            u.save()
            messages.add_message(request, messages.INFO, 'Updated successfully.')
            return redirect('/bus_list/')
    else:
        return redirect('/sign_in/')
def delete_bus(request,id):
 if 'cname' in request.session:
    tbl=bus.objects.get(bus_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/bus_list/')
 else:
      return redirect('/sign_in/')
 
def view_hostel(request,id):
    if 'sname' in request.session:
        college_login_id=id
        data=hostel.objects.filter(college_login_id=college_login_id)
        return render(request,'Student/view_hostel.html',{'data':data})
    else:
        return redirect('/sign_in/')
def view_bus(request,id):
    if 'sname' in request.session:
        college_login_id=id
        data=bus.objects.filter(college_login_id=college_login_id)
        return render(request,'Student/view_bus.html',{'data':data})
    else:
        return redirect('/sign_in/')
    
def university_student_List(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
        data=college.objects.filter(university_login_id=logid)
        return render(request,'University/university_student_List.html',{'data':data})
    else:
       return redirect('/sign_in/')
def university_student_list_filter(request):
    if 'uname' in request.session:
        logid =  request.session['slogid']
        course_id=request.POST.get("course")
        college_login_id=request.POST.get("college")
        batch_id=request.POST.get("batch")
        data=college.objects.filter(university_login_id=logid)
        cursor=connection.cursor()
        cursor.execute("select s.*,c.course,b.batch from tbl_student as s inner join tbl_application as a on s.login_id=a.candidate_login_id inner join tbl_admission_notification as n on a.admission_notification_id=n.admission_notification_id inner join tbl_batch as b on n.batch_id=b.batch_id inner join tbl_course as c on c.course_id=b.course_id where n.batch_id="+str(batch_id)+" and c.course_id="+str(course_id)+" and a.college_login_id="+str(college_login_id)+" and a.status='Approved'")
    
        data1=cursor.fetchall()
        return render(request,'University/university_student_list_filter.html',{'data1':data1,'data':data})
    else:
       return redirect('/sign_in/')
    
def uni_view_candidate(request,id):
    if 'uname' in request.session:
      
        data=Student.objects.get(login_id=id)
        return render(request,'University/candidate_details.html',{'data':data})
    else:
        return redirect('/index/')
    

def college_student_List(request):
    if 'cname' in request.session:
        logid =  request.session['slogid']
        college_login_id =logid
        cursor=connection.cursor()
        cursor.execute("select c.course_id,c.course from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id  where oc.college_login_id = "+str(college_login_id))
        data1=cursor.fetchall()
        return render(request,'College/college_student_List.html',{'data1':data1})
    else:
       return redirect('/sign_in/')
def college_student_list_filter(request):
    if 'cname' in request.session:
        logid =  request.session['slogid']
        course_id=request.POST.get("course")
        college_login_id=logid
        batch_id=request.POST.get("batch")
        cursor=connection.cursor()
        cursor.execute("select c.course_id,c.course from  tbl_offer_course as oc inner join tbl_course as c on oc.course_id = c.course_id  where oc.college_login_id = "+str(college_login_id))
        
        data1=cursor.fetchall()
        cursor.execute("select s.*,c.course,b.batch from tbl_student as s inner join tbl_application as a on s.login_id=a.candidate_login_id inner join tbl_admission_notification as n on a.admission_notification_id=n.admission_notification_id inner join tbl_batch as b on n.batch_id=b.batch_id inner join tbl_course as c on c.course_id=b.course_id where n.batch_id="+str(batch_id)+" and c.course_id="+str(course_id)+" and a.college_login_id="+str(college_login_id)+" and a.status='Approved'")
    
        data=cursor.fetchall()
        return render(request,'College/college_student_list_filter.html',{'data':data,'data1':data1})
    else:
       return redirect('/sign_in/')
    
def col_view_candidate(request,id):
    if 'cname' in request.session:
      
        data=Student.objects.get(login_id=id)
        return render(request,'College/candidate_details.html',{'data':data})
    else:
        return redirect('/index/')
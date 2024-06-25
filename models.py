import datetime
from django.db import models

# Create your models here.

class login(models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.TextField(null=True)
    Usertype=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_login'


class state(models.Model):
    state_id=models.AutoField(primary_key=True)
    country_id=models.IntegerField()
    state=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_state'

class district(models.Model):
    district_id=models.AutoField(primary_key=True)
    state_id=models.IntegerField()
    district=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_district'


class complaint(models.Model):
    complaint_id=models.AutoField(primary_key=True)
    complaint_subject=models.CharField(max_length=50)
    complaint=models.CharField(max_length=150)
    user_login_id=models.IntegerField()
    reply=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_complaint'


class Student(models.Model):
    user_id=models.AutoField(primary_key=True)
    login_id=models.IntegerField()
    student_name=models.CharField(max_length=50, null=True)
    phone_number=models.BigIntegerField(null=True)
    Email=models.CharField(max_length=50)
    Address=models.TextField()
    place=models.CharField(max_length=50, null=True)
    date_of_birth=models.DateField(null=True)
    permanant_address=models.TextField(null=True, blank=True)
    father_name=models.CharField(max_length=50,null=True, blank=True)
    mother_name=models.CharField(max_length=50,null=True, blank=True)
    photo=models.CharField(max_length=50,null=True, blank=True)
    gender=models.CharField(max_length=50,null=True, blank=True)
    nationality=models.CharField(max_length=50,null=True, blank=True)
    caste=models.CharField(max_length=50,null=True, blank=True)
    religion=models.CharField(max_length=50,null=True, blank=True)
    caste_category=models.CharField(max_length=50,null=True, blank=True)
    adhaar_no=models.CharField(max_length=50,null=True, blank=True)
    blood_group=models.CharField(max_length=50,null=True, blank=True)
    status=models.CharField(max_length=50,null=True, blank=True, default='Not Updated')
    class Meta:
        db_table='tbl_student'

class university(models.Model):
    university_id=models.AutoField(primary_key=True)
    login_id=models.IntegerField()
    university=models.CharField(max_length=50)
    address=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=50)
    phone_number=models.BigIntegerField(null=True)
    district_id=models.IntegerField()
    place=models.CharField(max_length=50)

    class Meta:
        db_table='tbl_university'
class complaint(models.Model):
    complaint_id=models.AutoField(primary_key=True)
    complaint_subject=models.CharField(max_length=50)
    complaint=models.CharField(max_length=150)
    user_login_id=models.IntegerField()
    reply=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_complaint'

class feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    feedback_subject=models.CharField(max_length=50)
    feedback=models.CharField(max_length=150)
    user_login_id=models.IntegerField()
    reply=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_feedback'
class college(models.Model):
    college_id=models.AutoField(primary_key=True)
    university_login_id=models.IntegerField()
    login_id=models.IntegerField()
    college=models.CharField(max_length=50)
    address=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=50)
    phone_number=models.BigIntegerField(null=True)
    district_id=models.IntegerField()
    place=models.CharField(max_length=50)

    class Meta:
        db_table='tbl_college'
class course(models.Model):
    course_id=models.AutoField(primary_key=True)
    course=models.CharField(max_length=50)
    course_type=models.CharField(max_length=50)
    university_login_id=models.IntegerField()
    fee=models.IntegerField()
    class Meta:
        db_table='tbl_course'

class batch(models.Model):
    batch_id=models.AutoField(primary_key=True)
    batch=models.CharField(max_length=50)
    course_id=models.IntegerField()
    class Meta:
        db_table='tbl_batch'
class offer_course(models.Model):
    offer_course_id=models.AutoField(primary_key=True)
    college_login_id=models.IntegerField()
    course_id=models.IntegerField()
    seat=models.IntegerField()
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table='tbl_offer_course'
class admission_notification(models.Model):
    admission_notification_id=models.AutoField(primary_key=True)
    batch_id=models.IntegerField()
    eligibility=models.CharField(max_length=500)
    course_details=models.CharField(max_length=500)
    last_date=models.DateField()
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    application_fee=models.IntegerField()
    class Meta:
        db_table='tbl_admission_notification'

class application(models.Model):
    application_id=models.AutoField(primary_key=True)
    admission_notification_id=models.IntegerField()
    application_fee=models.IntegerField()
    qualified_examination=models.CharField(max_length=50)
    qualified_examination_mark=models.IntegerField()
    qualified_examination_total_mark=models.IntegerField()
    qualified_examination_certificate=models.CharField(max_length=50)
    quota=models.CharField(max_length=50)
    sslc_certificate=models.CharField(max_length=50)
    income_certificate=models.CharField(max_length=50,null=True, blank=True)
    caste_certificate=models.CharField(max_length=50,null=True, blank=True)
    candidate_login_id=models.IntegerField()
    status=models.CharField(max_length=50,default='Not Paid')
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    college_login_id=models.IntegerField()
    
    class Meta:
        db_table='tbl_application'
class hostel(models.Model):
    hostel_id=models.AutoField(primary_key=True)
    college_login_id=models.IntegerField()
    total_seat=models.IntegerField()
    seat_availability=models.IntegerField()
    address=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)   
    type=models.CharField(max_length=50)
    rules=models.CharField(max_length=500)
    class Meta:
        db_table='tbl_hostel'
class bus(models.Model):
    bus_id=models.AutoField(primary_key=True)
    college_login_id=models.IntegerField()
    bus_number=models.IntegerField()
    route=models.CharField(max_length=500)
    stops=models.CharField(max_length=500)
    class Meta:
        db_table='tbl_bus'
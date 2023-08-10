from django.db import models

class student_sign(models.Model):
    name=models.CharField(max_length=264,db_column="name")
    roll_no=models.CharField(max_length=264,db_column="roll_no",primary_key=True)
    password=models.CharField(max_length=264,db_column="password")
    mobile=models.CharField(max_length=11,db_column="mobile_no")
    email=models.EmailField(db_column="email")
    dob=models.DateField(db_column="dob")
    tenth=models.IntegerField(db_column="tenth_mark")
    twelve=models.IntegerField(db_column="twelth_mark")
    twelth_cutoff=models.IntegerField(db_column="twelth_cutoff")
    address=models.CharField(max_length=264,db_column="address")
    dept=models.CharField(max_length=264,db_column="dept")
    year=models.IntegerField(db_column="year")
    school=models.CharField(max_length=264,db_column="school")
    cgpa=models.IntegerField(db_column="cgpa")
    class Meta:
        managed = False
        db_table = 'student_signup'

class staff_sign(models.Model):
    staffid=models.CharField(max_length=264,db_column="staff_id",primary_key=True)
    staffname=models.CharField(max_length=264,db_column="staff_name")
    staffemail=models.EmailField(db_column="staff_email")
    staffconfirm=models.CharField(max_length=264,db_column="staff_password")
    class Meta:
        managed = False
        db_table = 'staff_signup'
class photo_p(models.Model):
    batch=models.CharField(max_length=264,db_column="batch")
    dept=models.CharField(max_length=264,db_column="dept")
    year=models.IntegerField(db_column="year")
    roll_no=models.CharField(max_length=264,db_column='roll_no')
    ids=models.IntegerField(db_column="ids",primary_key=True)
    file_name=models.CharField(max_length=264,db_column="file_name")
    file=models.BinaryField(db_column="file")
    event_name=models.TextField(db_column="event_type")
    from_date=models.DateField(db_column="from_date")
    to_date=models.DateField(db_column="to_date")
    event_org=models.TextField(db_column="event_org")
    academic=models.TextField(db_column="ac_year")
    title=models.TextField(db_column="event_title")
    
    class Meta:
        db_table='student_files'
        managed=False
class staff_up(models.Model):
    staff_id=models.CharField(max_length=264,db_column='staff_id')
    ids=models.IntegerField(db_column="ids",primary_key=True)
    file_name=models.CharField(max_length=264,db_column="file_name")
    file=models.BinaryField(db_column="file")
    from_date=models.DateField(db_column="from_date")
    to_date=models.DateField(db_column="to_date")
    journal=models.CharField(max_length=264,db_column="journal")
    title=models.CharField(max_length=264,db_column="title")
    host=models.CharField(max_length=264,db_column='host')
    student=models.CharField(max_length=244,db_column="tot_stu")
    yer=models.CharField(max_length=255,db_column="year")
    dep=models.CharField(max_length=222,db_column="dept")
    amount=models.CharField(max_length=244,db_column="amount")
    sub=models.CharField(max_length=244,db_column='submission')
    class Meta:
        db_table='staff_files'
        managed=False
class mark(models.Model):
    staff_id=models.CharField(max_length=264,db_column="staff_id")
    stu_id=models.IntegerField(db_column="id",primary_key=True)
    roll_no=models.CharField(max_length=264,db_column="roll_no")
    sem=models.CharField(max_length=264,db_column="sem")
    subject=models.CharField(max_length=264,db_column="subject")
    mark1=models.IntegerField(db_column="internal1")
    mark2=models.IntegerField(db_column="internal2")
    mark3=models.IntegerField(db_column="internal3")
    assessment1=models.IntegerField(db_column="assessment1")
    assessment2=models.IntegerField(db_column="assessment2")
    assessment3=models.IntegerField(db_column="assessment3")
    unit1=models.IntegerField(db_column="unitTest1")
    unit2=models.IntegerField(db_column="unitTest2")
    unit3=models.IntegerField(db_column="unitTest3")
    class Meta:
        db_table='mark'
        managed=False
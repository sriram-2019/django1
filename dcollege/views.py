from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from dcollege.models import staff_sign
from dcollege.models import student_sign
from dcollege.models import photo_p
from dcollege.models import staff_up
from dcollege.models import mark
import mysql.connector as mysql
from django.db.models import Q
import re
from io import BytesIO
import zlib
import os
from datetime import datetime
def index(request):
        if request.method=="POST":
            if "sign_up" in request.POST:
                print("hel")
                return render(request,"student_signup.html")
            elif 'stu_log' in request.POST:
               print("hello")
            elif("mysub" in request.POST):
                    username = request.POST.get('user', '')
                    if username == '':
                        return JsonResponse({'success': False, 'error': 'Username is required'})
                    else:
                        # Process the form data
                        return JsonResponse({'success': True})
            elif("staff_sub" in request.POST):
                return render(request,'staff_reg.html')
            elif("staffs" in request.POST):
                staff_name=request.POST.get('staff_name','')
                if(staff_name==''):
                    return JsonResponse({'success':False,'error':'username must filled'})
                else:
                    return JsonResponse({'success':True})
        return render(request,'l.html')
def sign_for_stu(request):
    return render(request,'student_signup.html')
def student_signs(request):
    if(request.method=="POST"):
        name=request.POST["user"]
        password=request.POST["password"]
        roll=request.POST["roll"]
        mobile=request.POST["mobile"]
        school=request.POST["school"]
        address=request.POST["address"]
        email=request.POST["email"]
        dob=request.POST["dob"]
        tenth=request.POST["10th"]
        twelth=request.POST["12th"]
        cutoff=request.POST["cutoff"]
        cgpa=request.POST["poly"]
        dept=request.POST.get('dept')
        year=request.POST.get('year')
        if(cgpa==''):
            cgpa=0
        save_db=student_sign(name=name,roll_no=roll,password=password,mobile=mobile,email=email,dob=dob,school=school,address=address,dept=dept,year=int(year),tenth=tenth,twelve=twelth,twelth_cutoff=cutoff,cgpa=cgpa)
        save_db.save()
    return render(request,'ll.html')
def staff(request):
     
     if(request.method=="POST"):
            staffid = request.POST["staffid"]
            staffname = request.POST["staffname"]
            staffemail = request.POST["staffmail"]
            staffconfirm = request.POST["staffconfirm"]
            staff=staff_sign(staffid=staffid,staffname=staffname,staffemail=staffemail,staffconfirm=staffconfirm)
            staff.save()
            data={
                 'message':'successfully registerd'
            }
            return JsonResponse(data)
def staff_log(request):
     staff_name=request.POST.get('staff_id')
     staff_pass=request.POST.get('staff_pass')
     try: 
        res=staff_sign.objects.get(staffid=staff_name)
        request.session["staff_name"]=staff_name
        if(res.staffconfirm!=staff_pass):
             data={
                  'message':'password is incorrect '
             }
             return JsonResponse(data)
        else:
             data={
                  'message': 'success'
             }
             return JsonResponse(data)
             
     except:
            data={
                  'message':'invalid username'
             }
            return JsonResponse(data)
     return render(request,'ll.html')
def staff_logout(request):
     return render(request,'l.html')
def staff_red(request):
    if('logouts' in request.method):
          print('hi')
    if("upload" in request.POST):
         return render(request,"staff_upload.html")
    if("student_cert" in request.POST):
        return render(request, "select_staff.html")
    if("edit" in request.POST):
        return render(request,"select_ac.html")
    if("Internal" in request.POST):
         return render(request,'ac.html')
    if('Assessment' in request.POST):
         return render(request,'assessment.html')
    if('unit test' in request.POST):
         return render(request,'unittest.html')
    if("res" in request.POST):
        return render(request,'get_info_stu.html')
    if("sem_marks" in request.POST):
        sem=request.POST.get('semester')
        type=request.POST.get('type')
        roll_no=request.session.get('staff_name')
        if type=="Internal":
            get=mark.objects.filter(staff_id=roll_no).filter(Q(sem=sem)).values("sem","subject","mark1","mark2","mark3")
            context={'form':get}
            return render(request,"dis_tab.html",context)
        if type=="Assessment":
            get = mark.objects.filter(staff_id=roll_no, sem=sem).values("sem", "subject", "assessment1", "assessment2", "assessment3")
            context = {'forms': get}
            return render(request, "assess.html", context)
        if type=="Unit Test":
            get=mark.objects.filter(staff_id=roll_no, sem=sem).values("sem","subject","unit1","unit2","unit3")
            context={'formss':get}
            return render(request,"unit.html",context)
       
    if("Download" in request.POST):
        staff_name=request.session.get("staff_name")
        res=staff_up.objects.filter(staff_id=staff_name).values("title","journal","host","file_name","from_date","to_date","student",'amount')
        context={"file":res}
        return render(request,'table4.html',context)
    return render(request,'staff_logs.html')
def student_red(request):
    dept=request.session.get("d")
    yearss=request.session.get("year")
    batch=request.session.get("batch")
    result = photo_p.objects.filter(dept=dept).filter(Q(year=yearss) | Q(batch=batch))
    context={'form':result}
    return render(request,'table5.html',context) 
def student_view(request):
    dept=request.POST.get('dept')
    request.session["d"]=dept
    years=request.POST.get('year')
    batch=request.POST.get('aca')
    request.session["year"]=years
    request.session["b"]=batch
    return render(request,'ll.html')
def student_download(request):
    name=request.POST.get('file_name')
    dept=request.session.get("d")
    year=request.session.get("year") 
    print(dept,year)
    res= photo_p.objects.filter(dept=dept).filter(Q(year=year))
    context={'form':res}
    return render(request,'table5.html',context)
def download_by(request):
    name=request.POST.get('file_name')
    if name:
        name=name.strip()
        res=photo_p.objects.get(file_name=name)
        compressed_data = zlib.decompress(res.file)
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{name}"'
        with BytesIO(compressed_data) as f:
                response.write(f.read())
        return response
def staff_ups(request):
    if(request.method=="POST"):
        event_name=request.POST.get('names')
        if(event_name=='fdp' or event_name=="seminar" or event_name=="webinar" or event_name=="workshop"):
            name=request.POST.get('journal')
            attended = request.POST.get('rad1')
            if(attended=='student'):
                student_no=request.POST.get("student")
                try:
                    student_no=int(student_no)
                except:
                    message="total no of student should be a number"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                year=request.POST.get('year')
                dept=request.POST.get('dept')
                host=request.POST.get('host')
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')
                file=request.FILES.get('file_input')
                if not file.name.lower().endswith('.pdf'):
                    message="Only Pdf file only"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                from_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_obj=datetime.strptime(to_date,"%Y-%m-%d")
                year=from_obj.strftime("%Y")
                from_month=from_obj.strftime("%m")
                from_year=from_obj.strftime("%y")
                to_year=to_obj.strftime("%y")
                to_month=to_obj.strftime("%m")
                from_day=from_obj.strftime("%d")
                to_day=to_obj.strftime("%d")
                current_month = datetime.now().month
                current_year = datetime.now().year
                message="message"
                from_month=int(from_month)
                to_month=int(to_month)
                from_year=int(from_year)
                to_year=int(to_year)
                if(from_month>current_month and from_year==current_year):
                    message="from date month is greater than current month "
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                elif(from_month>to_month and from_year==to_year):
                        message="from_date month must be less than to_date month"
                        data={
                            'message':message
                        }
                        return JsonResponse(data)
                elif((from_day>to_day and from_month<to_month)):
                    message="from_date day must be less than to_date day"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                else:
                    staff_id=request.session.get('staff_name')
                    with file.open(mode="rb") as f:
                        reads=f.read()
                    compressed=zlib.compress(reads)
                    saved=staff_up(staff_id=staff_id,title=event_name,journal=name,file_name=f"{datetime.now()}.pdf",file=compressed,from_date=from_date,to_date=to_date,host=host,student=student_no,yer=year,dep=dept,amount=0)
                    saved.save()
                    message="saved successfully"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
            if(attended=="staff"):
                staff_no=request.POST.get('staffs')
                host=request.POST.get('host')
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')
                file=request.FILES.get('file_input')
                if not file.name.lower().endswith('.pdf'):
                    message="Only Pdf file only"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                from_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_obj=datetime.strptime(to_date,"%Y-%m-%d")
                year=from_obj.strftime("%Y")
                from_month=from_obj.strftime("%m")
                from_year=from_obj.strftime("%y")
                to_year=to_obj.strftime("%y")
                to_month=to_obj.strftime("%m")
                from_day=from_obj.strftime("%d")
                to_day=to_obj.strftime("%d")
                current_month = datetime.now().month
                current_year = datetime.now().year
                message="message"
                from_month=int(from_month)
                to_month=int(to_month)
                from_year=int(from_year)
                to_year=int(to_year)
                if(from_month>current_month and from_year==current_year):
                    message="from date month is greater than current month "
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                elif(from_month>to_month and from_year==to_year):
                        message="from_date month must be less than to_date month"
                        data={
                            'message':message
                        }
                        return JsonResponse(data)
                elif((from_day>to_day and from_month<to_month)):
                    message="from_date day must be less than to_date day"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                else:
                    staff_id=request.session.get('staff_name')
                    with file.open(mode="rb") as f:
                        reads=f.read()
                    compressed=zlib.compress(reads)
                    saved=staff_up(staff_id=staff_id,title=event_name,journal=name,file_name=f"{datetime.now()}.pdf",file=compressed,from_date=from_date,to_date=to_date,host=host,student=staff_no,amount=0)
                    saved.save()
                    message="saved successfully"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
        if(event_name=="paper"):
                name=request.POST.get('journal')
                amount=request.POST.get('amount')
                host=request.POST.get('host')
                staff_id=request.session.get('staff_name')
                file=request.FILES.get('file_input')
                from_date=request.POST.get('subs')
                if not file.name.lower().endswith('.pdf'):
                    message="Only Pdf file only"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                with file.open(mode="rb") as f:
                    reads=f.read()
                compressed=zlib.compress(reads)
                saved=staff_up(staff_id=staff_id,title=event_name,journal=name,file_name=f"{datetime.now()}.pdf",file=compressed,from_date=from_date,to_date=from_date,host=host,amount=amount,student='-')
                saved.save()
                message="saved successfully"
                data={
                    'message':message
                }
                return JsonResponse(data)
        if(event_name=="project"):
                name=request.POST.get('journal')
                host=request.POST.get('host')
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')
                file=request.FILES.get('file_input')
                if not file.name.lower().endswith('.pdf'):
                    message="Only Pdf file only"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                from_obj = datetime.strptime(from_date, '%Y-%m-%d')
                to_obj=datetime.strptime(to_date,"%Y-%m-%d")
                year=from_obj.strftime("%Y")
                from_month=from_obj.strftime("%m")
                from_year=from_obj.strftime("%y")
                to_year=to_obj.strftime("%y")
                to_month=to_obj.strftime("%m")
                from_day=from_obj.strftime("%d")
                to_day=to_obj.strftime("%d")
                current_month = datetime.now().month
                current_year = datetime.now().year
                message="message"
                from_month=int(from_month)
                to_month=int(to_month)
                from_year=int(from_year)
                to_year=int(to_year)
                if(from_month>current_month and from_year==current_year):
                    message="from date month is greater than current month "
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                elif(from_month>to_month and from_year==to_year):
                        message="from_date month must be less than to_date month"
                        data={
                            'message':message
                        }
                        return JsonResponse(data)
                elif((from_day>to_day and from_month<to_month)):
                    message="from_date day must be less than to_date day"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                else:
                    staff_id=request.session.get('staff_name')
                    with file.open(mode="rb") as f:
                        reads=f.read()
                    compressed=zlib.compress(reads)
                    saved=staff_up(staff_id=staff_id,title=event_name,journal=name,file_name=f"{datetime.now()}.pdf",file=compressed,from_date=from_date,to_date=to_date,host=host,student="-",amount=0)
                    saved.save()
                    message="saved successfully"
                    data={
                        'message':message
                    }
                    return JsonResponse(data)
                    
                return render(request,'ll.html')
       
def prevs(request):
     if request.method=="POST":
        reg=request.POST.get('reg_nos')
        sub=request.POST.get('sub_name')
        marks = mark.objects.filter(roll_no=reg, subject=sub).values('mark1', 'mark2', 'mark3')
    
        data = {
            'success': True,
            'p': marks[0] if marks else None
        }
        return JsonResponse(data)
def prevsion(request):
     if request.method=="POST":
        reg=request.POST.get('reg_nos')
        sub=request.POST.get('sub_name')
        marks = mark.objects.filter(roll_no=reg, subject=sub).values('unit1', 'unit2', 'unit3')
        data = {
            'success': True,
            'p': marks[0] if marks else None
        }
        return JsonResponse(data)
def prevsion1(request):
     if request.method=="POST":
        reg=request.POST.get('reg_nos')
        sub=request.POST.get('sub_name')
        print(sub,reg)
        marks = mark.objects.filter(roll_no=reg, subject=sub).values('assessment1', 'assessment2', 'assessment3')
        print(marks)
        data = {
            'success': True,
            'p': marks[0] if marks else None
        }
        return JsonResponse(data)
def staff_reg(request):
     return render(request,'staff_reg.html')
def staff_download(request):
    name=request.POST.get('file_name')
    res=staff_up.objects.get(file_name=name)
    dcompress=zlib.decompress(res.file)
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{name}"'
    with BytesIO(dcompress) as f:
            response.write(f.read())
    return response
    return render(request,'ll.html')
def index2(request):
    if request.method == 'POST':
        
        try:
                stud=request.POST.get("student_name")
                request.session["stu_name"]=stud
                res=student_sign.objects.get(roll_no=stud)
                request.session["stu_dept"]=res.dept
                request.session["stu_year"]=res.year
                request.session["batch"]=res.school
                student_pass=request.POST.get("student_password")
            
                if(res.password!=student_pass):
                    message = 'enter the correct password'
                    data = {
                            'message': message,
                        
                            }
                    return JsonResponse(data)
                else:
                    message='success'
                    data={
                    'message':message,
                    }
                    return JsonResponse(data)
        except:
                    message='invalid username'
                    data={
                        'message':message,
                    }
                    return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

def photo(request):
    if(request.method=="POST"):
        event_name=request.POST.get('event-name')
        if(event_name==''):
              return JsonResponse({"success":False,"error":"username must be filled"})
        else:
             return JsonResponse({"success":True})
    return render(request,'student_upload.html')
def photo1(request):
   
    if request.method == 'POST':
            batch=request.session.get('batch')
            event_name=request.POST.get("event-name")
            dept=request.session.get("stu_dept")
            year1=request.session.get("stu_year")
            from_date=request.POST.get("fromdate")
            to_date=request.POST.get("todate")
            event_title=request.POST.get("title")
            event_org=request.POST.get("event-org")
            file=request.FILES.get("file_name")
            if not file.name.lower().endswith('.pdf'):
                message="Only Pdf file only"
                data={
                    'message':message
                }
                return JsonResponse(data)
            from_obj = datetime.strptime(from_date, '%Y-%m-%d')
            to_obj=datetime.strptime(to_date,"%Y-%m-%d")
            year=from_obj.strftime("%Y")
            ac_years=int(year)
            ac_year=f"{ac_years-1}-{ac_years}"
            from_month=from_obj.strftime("%m")
            from_year=from_obj.strftime("%y")
            to_year=to_obj.strftime("%y")
            to_month=to_obj.strftime("%m")
            from_day=from_obj.strftime("%d")
            to_day=to_obj.strftime("%d")
            current_month = datetime.now().month
            current_year = datetime.now().year
            message="message"
            from_month=int(from_month)
            to_month=int(to_month)
            from_year=int(from_year)
            to_year=int(to_year)
            if(from_month>current_month and from_year==current_year):
                message="from date month is greater than current month "
                data={
                    'message':message
                }
                return JsonResponse(data)
            elif(from_month>to_month and from_year==to_year):
                message="from_date month must be less than to_date month"
                data={
                    'message':message
                }
                return JsonResponse(data)
            elif((from_day>to_day and from_month<to_month)):
                message="from_date day must be less than to_date day"
                data={
                    'message':message
                }
                return JsonResponse(data)
            else:
                roll_no=request.session.get("stu_name")
                with file.open(mode='rb') as r:
                    read=r.read()
                
                compressed=zlib.compress(read)
            
                save_file=photo_p(file_name=f"{datetime.now()}.pdf",file=compressed,title=event_title,from_date=from_date,to_date=to_date,event_org=event_org,academic=ac_year,roll_no=roll_no,dept=dept,year=year1,batch=batch)
                save_file.save()
                message="success"
                data={
                'message':message            
                }
                return JsonResponse(data)
        
    return render(request,'student_upload.html')
def gets(request):
     from_date=request.POST.get("from-date")
     to_date=request.POST.get("to-date")
     data={
          'from':from_date,
          'to':to_date
     }
     return JsonResponse(data)
def display_data(request):
    from_value = request.GET.get('from')
    to_value=request.GET.get('to')
    from_value = datetime.strptime(from_value, '%Y-%m-%d').date()
    to_value = datetime.strptime(to_value, '%Y-%m-%d').date()
    from_value=photo_p.objects.filter(from_date__range=[from_value, to_value]).values("file_name","event_org","title","academic","from_date","to_date","ids")
    context = {'from': from_value}
    return render(request, 'sel.html', context)
def get_file(request):
     if request.method=="POST":
        name=request.POST.get('fileName')
        if name:
            roll_nos=request.session.get("stu_name")
            name=name.strip()
            res=photo_p.objects.get(file_name=name)
            compressed_data = zlib.decompress(res.file)
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{name}"'
            with BytesIO(compressed_data) as f:
                 response.write(f.read())
            return response

        return render(request,"ll.html")
def all_file(request):
    if request.method=="POST":
        name=request.POST.get('fileName')
        if name:
            roll_nos=request.session.get("stu_name")
            name=name.strip()
            res=photo_p.objects.get(file_name=name)
            compressed_data = zlib.decompress(res.file)
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{name}"'
            with BytesIO(compressed_data) as f:
                 response.write(f.read())
            return response
            
    return render(request,"ll.html")
def index3(request):
    if("certificate" in request.POST):
        return render( request,"student_upload.html")
    if('logout' in request.POST):
         return render(request,'l.html')
    if("download" in request.POST):
         return render(request,"download.html")
    if("res" in request.POST):
        roll_no=request.session.get('stu_name')
        get=mark.objects.filter(roll_no=roll_no).values("sem","subject","mark1","mark2","mark3")
        context={'form':get}
        return render(request,"dis_tab.html",context)
    if("attendance" in request.POST):
         return redirect("http://vcet.ac.in/vcetattendance/ParentsLogin.php")
    if("select_date" in request.POST):
         return render(request,"date.html")
    if("aca" in request.POST):
       return render(request,'goto.html')
    if("sem_mark" in request.POST):
        sem=request.POST.get('semester')
        type=request.POST.get('type')
        roll_no=request.session.get('stu_name')
        if type=="Internal":
            get=mark.objects.filter(roll_no=roll_no).filter(Q(sem=sem)).values("sem","subject","mark1","mark2","mark3")
            context={'form':get}
            return render(request,"int1.html",context)
        if type=="Assessment":
            get = mark.objects.filter(roll_no=roll_no, sem=sem).values("sem", "subject", "assessment1", "assessment2", "assessment3")
            context = {'forms': get}
            return render(request, "assess1.html", context)
        if type=="Unit Test":
            get=mark.objects.filter(roll_no=roll_no, sem=sem).values("sem","subject","unit1","unit2","unit3")
            context={'formss':get}
            return render(request,"unit1.html",context)
    if("select_all" in request.POST):
        roll_no=request.session.get('stu_name')
        res = photo_p.objects.filter(roll_no=roll_no).values("file_name","event_org","title","academic","from_date","to_date","ids")
        context = {"form": res}
        return render(request, "table2.html", context)
    return render(request,"Button.html")
def save_ass(request):
     if request.method == "POST":
        roll = request.POST.get('reg_nos')
        roll = roll.lower()
        staff_id = request.session.get("staff_name")
        sem = request.POST.get("semester")
        sub_name = request.POST.get('sub_name')
        a1 = request.POST.get('amark1')
        a2 = request.POST.get('amark2')
        a3 = request.POST.get('amark3')
        if(sub_name==" "):
            error_message="enter the subject name"
            data = {'message': error_message}
            return JsonResponse(data)
        # Check if assessment marks are valid (less than 100)
        if a1 and int(a1) > 100:
            error_message = "Invalid mark for Assessment 1. Marks should be less than 100."
            return render(request, "ll.html", {"error_message": error_message})
        if a2 and int(a2) > 100:
            error_message = "Invalid mark for Assessment 2. Marks should be less than 100."
            return render(request, "ll.html", {"error_message": error_message})
        if a3 and int(a3) > 100:
            error_message = "Invalid mark for Assessment 3. Marks should be less than 100."
            return render(request, "ll.html", {"error_message": error_message})

        existing_mark = mark.objects.filter(sem=sem, subject=sub_name, roll_no=roll, staff_id=staff_id).first()
        if existing_mark:
            # Update the existing mark
            if a1:
                existing_mark.assessment1 = a1
            if a2:
                existing_mark.assessment2 = a2
            if a3:
                existing_mark.assessment3 = a3
            existing_mark.save()
            print("Updated existing mark.")
            error_message="Saved new mark."
            data={
                     'message':error_message
                }
            return JsonResponse(data)
        else:
            # Create a new mark
            res = mark(
                sem=sem,
                subject=sub_name,
                staff_id=staff_id,
                roll_no=roll,
                mark1=None,
                mark2=None,
                mark3=None,
                assessment1=a1 or None,
                assessment2=a2 or None,
                assessment3=a3 or None,
                unit1=None,
                unit2=None,
                unit3=None
            )
            res.save()
            print("Saved new mark.")
            error_message = "Saved new mark."
            data = {'message': error_message}
            return JsonResponse(data)
        
        return render(request, "ll.html")
def saveinter(request):
      if request.method == "POST":
            roll = request.POST.get('reg_nos')
            staff_id = request.session.get("staff_name")
            roll = roll.lower()
            sem = request.POST.get("semester")
            sub_name = request.POST.get('sub_name')
            i1 = request.POST.get('mark1')
            i2 = request.POST.get('mark2')
            i3 = request.POST.get('mark3')
            print(sub_name=="")
            if(sub_name==""):
                error_message="enter the subject name"
                data = {'message': error_message}
                return JsonResponse(data)
            print(i1, i2, i3)
            if(i1==" " or i2==" " or i3==" "):
                error_message="fill required fields "
                data={
                     'message':error_message
                }
                return JsonResponse(data)
            # Check if marks are valid (less than 100)
            if i1 and int(i1) > 100:
                error_message = "Invalid mark for Mark 1. Marks should be less than 100."
                data={
                     'message':error_message
                }
                return JsonResponse(data)
                
            if i2 and int(i2) > 100:
                error_message = "Invalid mark for Mark 2. Marks should be less than 100."
                data={
                     'message':error_message
                }
                return JsonResponse(data)
            if i3 and int(i3) > 100:
                error_message = "Invalid mark for Mark 3. Marks should be less than 100."
                data={
                     'message':error_message
                }
                return JsonResponse(data)

            existing_mark = mark.objects.filter(sem=sem, subject=sub_name, roll_no=roll, staff_id=staff_id).first()
            if existing_mark:
                # Update the existing mark
                if i1:
                    existing_mark.mark1 = i1
                if i2:
                    existing_mark.mark2 = i2
                if i3:
                    existing_mark.mark3 = i3
                existing_mark.save()
                print("Updated existing mark.")
                error_message="Saved new mark."
                data={
                     'message':error_message
                }
                return JsonResponse(data)
            else:
                # Create a new mark
                res = mark(
                    sem=sem,
                    subject=sub_name,
                    staff_id=staff_id,
                    roll_no=roll,
                    mark1=i1,
                    mark2=i2 or None,
                    mark3=i3 or None,
                    assessment1=None,
                    assessment2=None,
                    assessment3=None,
                    unit1=None,
                    unit2=None,
                    unit3=None
                )
                res.save()
                error_message="Saved new mark."
                data={
                     'message':error_message
                }
                return JsonResponse(data)

            return render(request, "ll.html")


def saveunit(request):
     if request.method == "POST":
            roll = request.POST.get('reg_nos')
            print(roll)
            staff_id = request.session.get("staff_name")
            print(staff_id)
            sem = request.POST.get("semester")
            sub_name = request.POST.get('sub_name')
            un1 = request.POST.get('umark1')
            un2 = request.POST.get('umark2')
            un3 = request.POST.get('umark3')
            if(sub_name==" "):
                error_message="enter the subject name"
                data = {'message': error_message}
                return JsonResponse(data)
            # Check if unit marks are valid (less than or equal to 20)
            if un1 and int(un1) > 101:
                error_message = "Invalid mark for Unit 1. Marks should be less than or equal to 20."
                data = {'error_message': error_message}
                return JsonResponse(data)
            if un2 and int(un2) > 101:
                error_message = "Invalid mark for Unit 2. Marks should be less than or equal to 20."
                data = {'error_message': error_message}
                return JsonResponse(data)
            if un3 and int(un3) > 101:
                error_message = "Invalid mark for Unit 3. Marks should be less than or equal to 20."
                data = {'error_message': error_message}
                return JsonResponse(data)

            existing_mark = mark.objects.filter(sem=sem, subject=sub_name, roll_no=roll, staff_id=staff_id).first()
            if existing_mark:
                # Update the existing mark
                if un1:
                    existing_mark.unit1 = un1
                if un2:
                    existing_mark.unit2 = un2
                if un3:
                    existing_mark.unit3 = un3
                existing_mark.save()
                print("Updated existing mark.")
                error_message = "Saved new mark."
                data = {'message': error_message}
                return JsonResponse(data)
            else:
                # Create a new mark
                res = mark(
                    sem=sem,
                    subject=sub_name,
                    staff_id=staff_id,
                    roll_no=roll,
                    mark1=None,
                    mark2=None,
                    mark3=None,
                    assessment1=None,
                    assessment2=None,
                    assessment3=None,
                    unit1=un1 or None,
                    unit2=un2 or None,
                    unit3=un3 or None
                )
                res.save()
                error_message = "Saved new mark."
                data = {'message': error_message}
                return JsonResponse(data)
            

def tab(request):
    return redirect("dis_tab.html")
def tab1(request):
     return render(request,"dis_tab.html")
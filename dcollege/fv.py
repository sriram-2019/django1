from django.shortcuts import render
from django.http import HttpResponse
import sqlite3 as sq
from dcollege.models import MyTable
def index(request):
    if(request.method=="POST"):
        if "staff" in request.POST:
            names=(request.POST["adminpass"])
            passwords=(request.POST["adminid"])
            n=MyTable(name=names,password=passwords)
            n.save()
        elif("register" in request.POST):
            print(request.POST["studentid"])
            print(request.POST["stupass"])
        elif("user" in request.POST):
            print("pass")
    return render(request,'l.html')
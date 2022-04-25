from django.shortcuts import render

# Create your views here.

# from django.http import HttpResponse

from django.db import connection

def welcome(request):
    # with connection['website'].cursor() as cursor:
    #     cursor.execute(r"SELECT * FROM animal")
    #     row = cursor.fetchall()
    #
    # print(row)
    # sample = row;
    sample = range(1,10)
    sample = [[],[]]
    for i in range(1,10):
        for j in range(1,10):
            sample[0].append(j*i)
        sample[1].append(i)
    print(sample)
    return render(request,'index.html',{'numbers':sample})

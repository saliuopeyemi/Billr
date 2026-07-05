from django.shortcuts import render




def document(request):
    return render(request,"output.html")

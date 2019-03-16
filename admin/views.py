from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'latest_question_list': 1}
    return render(request, 'admin/homepage_index.html', context)

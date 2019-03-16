from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

def index(request):
    context = {'latest_question_list': 1}
    return render(request, 'transaction/index.html', context)
def paper_submit(request):
    context = {'latest_question_list': 1}
    return render(request, 'transaction/paper_submit.html', context)
def paper_submit_action(request):
    if request.method=="GET":
        paper_title = request.GET.get('paper_title',"paper_title not found"); 
        paper_author= request.GET.get('paper_author',"author not found")
        #return HttpResponse("paper_submit_action:" + paper_title + paper_author)
    if request.method=="POST":
        paper_title = request.POST.get('paper_title',"not found"); print(paper_title)
        paper_author= request.POST.get('paper_author',"not found")
        #return HttpResponse("paper_submit_action:" + paper_title + paper_author)

    post_object = {
        'paper_title' : paper_title,
        'paper_author': paper_author,
    }
    post_json = json.dumps(post_object)
 
    # Submit a transaction
    CONNECTED_NODE_ADDRESS = "http://127.0.0.1:99"
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    return HttpResponse("paper_submit_action: \n" + post_json)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})


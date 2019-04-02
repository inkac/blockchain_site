from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import base64
from hashlib import sha256

def index(request):
    context = {'latest_question_list': 1}
    return render(request, 'transaction/index.html', context)
def paper_submit(request):
    context = {'latest_question_list': 1}
    return render(request, 'transaction/paper_submit.html', context)
@csrf_exempt
def paper_submit_action(request):
    if request.method=="GET":
        paper_title = request.GET.get('paper_title',"paper_title not found"); 
        paper_author= request.GET.get('paper_author',"author not found")
        #return HttpResponse("paper_submit_action:" + paper_title + paper_author)
    if request.method=="POST":
        paper_title = request.POST.get('paper_title',"not found"); #print(paper_title)
        paper_author= request.POST.get('paper_author',"not found")
        pubkey_input = request.POST.get('pubkey',"not found").strip(" \r\n　"); #去掉开头结尾空格换行符
        prikey_input = request.POST.get('prikey',"not found").strip(" \r\n　"); #去掉开头结尾空格换行符
        #return HttpResponse("paper_submit_action:" + paper_title + paper_author)

    #priKey = RSA.importKey( base64.b64decode(prikey_input))
    priKey = RSA.importKey(prikey_input)
    contents_data = {
        'paper_title' : paper_title,
        'paper_author': paper_author,
    }
    nonce = 9999
    contents_json = json.dumps(contents_data, sort_keys=True)
    hash_data = {'type':"paper_submit", 'contents':contents_json, 'nonce':nonce}
    hash_json = json.dumps(hash_data, sort_keys=True)
    hash_obj = SHA256.new(hash_json.encode()); #print(hash_obj.hexdigest())
    transaction_hash = sha256(hash_json.encode()).hexdigest(); #print(transaction_hash)
    transaction_data = hash_data
    transaction_data['hash'] = transaction_hash
    signer = PKCS1_v1_5.new(priKey)
    signature_obj = base64.b64encode(signer.sign(hash_obj))
    transaction_data['signature'] = str(signature_obj,encoding = "utf-8")
    transaction_data['pubkey']    = pubkey_input
    transaction_json = json.dumps(transaction_data, sort_keys=True)
 
    # Submit a transaction
    CONNECTED_NODE_ADDRESS = "http://127.0.0.1:99"
    new_tx_address = "{}/transaction/new/".format(CONNECTED_NODE_ADDRESS)
    try:
        response  = requests.post(new_tx_address,
                  data=transaction_json,
                  headers={'Content-type': 'application/json'})
        result = response.text
    except:
        result = "\n Can't access the blockchain server! \n"
    context = json.loads(transaction_json)
    context["result"] = result
    return render(request, 'transaction/submit_result.html', context)
    # 注，context是一个transaction_data字典类型
    # template里面可以通过{{ type }}方式直接引用context里面key 'type' 对应的值



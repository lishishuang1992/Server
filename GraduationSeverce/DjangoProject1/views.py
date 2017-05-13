# coding=UTF-8
from django.db.transaction import TransactionManagementError
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.



import base64,random,os,string,operator
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError,transaction
from DjangoProject1 import  models
import json
from django.views.decorators.csrf import csrf_exempt



def login(request):
    getUserName = request.GET.get('username')
    getPassWord = request.GET.get('password')
    try:
        models.ball_user.objects.get(user_name = getUserName)
    except ObjectDoesNotExist:
        x = "用户不存在"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type = "application/json")
    userPassword = models.ball_user.objects.only('password').get(user_name = getUserName).password
    if userPassword == getPassWord:
        x = "登录成功"
        obj = models.ball_user.objects.get(user_name = getUserName,password = getPassWord)
        message = x.decode("UTF-8")
        data = {'status': '1006', 'message': message,'user_id':obj.user_id,'image':obj.image}
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        x = "密码错误"
        message = x.decode("UTF-8")
        data = {'status': '1004', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")


def register(request):
    getUserName = request.GET.get('username')
    getPassWord = request.GET.get('password')
    try:
        models.ball_user.objects.get(user_name = getUserName)
    except ObjectDoesNotExist:
        user_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        userMesssage = models.ball_user(user_name=getUserName, password=getPassWord,user_id=user_id)
        userMesssage.save()
        defaultImagePath = models.ball_user.objects.get(user_id=user_id)
        x = "注册成功"
        message = x.decode("UTF-8")
        data = {'status': '1006', 'message': message,'user_id':user_id,'image':defaultImagePath.image}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "用户名已经存在"
    message = x.decode("UTF-8")
    data = {'status': '1005', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def postUserImage(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    imageStr = received_json_data['image']
    imgdata = base64.b64decode(imageStr)
    num_Image = random.randint(10000000, 99999999)
    path = "%s/media/userImage/%d.jpg" % (os.path.dirname(os.path.dirname(__file__)), num_Image)
    file = open(path, "wb")
    file.write(imgdata)
    file.flush()
    file.close()
    try:
        ballUpdate = models.ball_user.objects.get(user_id=user_id)
        imagePath =  "userImage/%d.jpg" %(num_Image)
        ballUpdate.image = imagePath
        ballUpdate.save()
    except ObjectDoesNotExist:
        x = "用户id错误"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "上传成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def homeData(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    project = received_json_data['project']
    ball_object = received_json_data['ball_object']
    place = received_json_data['place']
    user_id = received_json_data['user_id']
    try:
        if project:
            data = models.ball_table.objects.filter(project = project)
        elif ball_object:
            data = models.ball_table.objects.filter(ball_object = ball_object)
        elif place:
            data = models.ball_table.objects.filter(place = place)
        elif user_id:
            data = models.about_ball.objects.filter(user_id=user_id)
        else:
            data = models.ball_table.objects.all()
        if data:
            listData = []
            if user_id:
                for obj in data:
                    userBall = models.ball_table.objects.get(ball_ID=obj.ball_id)
                    dictData = { 'ball_ID':userBall.ball_ID,'current_time': str(userBall.current_time), 'ball_object': userBall.ball_object,
                        'money': userBall.money, 'project': userBall.project, 'ball_format': userBall.ball_format, 'place': userBall.place,
                        'num_people': userBall.num_people, 'current_people': userBall.current_people,
                        'introduction': userBall.introduction}
                    listData.append(dictData)
            else:
                for obj in data:
                    aboutBall = models.about_ball.objects.filter(ball_id=obj.ball_ID)
                    userBall = models.ball_user.objects.filter(user_id=aboutBall[0].user_id)
                    dictData = {'user_name':userBall[0].user_name,'image':userBall[0].image,'current_time':str(obj.current_time),'ball_ID':obj.ball_ID,'ball_object':obj.ball_object,'money':obj.money,'project':obj.project,'ball_format':obj.ball_format,'place':obj.place,'num_people':obj.num_people,'current_people':obj.current_people,'introduction':obj.introduction}
                    listData.append(dictData)
            listData.sort(key=lambda x: x['current_time'].split('-'), reverse=True)
            listData.sort(key=lambda x: x['current_time'].split(':'), reverse=True)
            x = "查询到数据"
            message = x.decode("UTF-8")
            data = {'status': '1006', 'message': message,'result':listData}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            x = "没有查询到数据"
            message = x.decode("UTF-8")
            data = {'status': '1005', 'message': message}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except models.ball_table.DoesNotExist:
        x = "不存在类型"
        message = x.decode("UTF-8")
        data = {'status': '1004', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def allBallMessage(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    if user_id:
        aboutBall = models.about_ball.objects.filter(user_id = user_id)
        messageList = []
        for obj in aboutBall:
            if obj.ballMessage_id:
                messageData = models.ball_message.objects.get(message_id = obj.ballMessage_id)
                messageList.append(messageData)
    else:
        data = models.ball_message.objects.all()
    listData = []
    if user_id:
        data = messageList
    if data:
        for obj in data:
            aboutBall = models.about_ball.objects.filter(ballMessage_id=obj.message_id)
            userBall = models.ball_user.objects.filter(user_id=aboutBall[0].user_id)
            zanData = models.zan_message.objects.filter(message_id=obj.message_id)
            zanUserIdList = []
            if zanData:
                for zanObj in zanData:
                    zanUser = models.ball_user.objects.filter(user_id=zanObj.user_id)
                    zanDict = {'user_id': zanObj.user_id,'user_name':zanUser[0].user_name}
                    zanUserIdList.append(zanDict)
            dictData = {'user_id':userBall[0].user_id,'user_image':userBall[0].image,'user_name':userBall[0].user_name,'message_id':obj.message_id,'image':obj.image,'num':obj.num,'message':obj.message,'current_time':str(obj.current_time),'zan_userId':zanUserIdList}
            listData.append(dictData)
        listData.sort(key=lambda x: x['current_time'].split('-'), reverse=True)
        listData.sort(key=lambda x: x['current_time'].split(':'),reverse=True)
        x = "查询到数据"
        message = x.decode("UTF-8")
        data = {'status': '1006', 'message': message,'result':listData}
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        x = "无数据"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message, 'result': listData}
        return HttpResponse(json.dumps(data), content_type="application/json")




@csrf_exempt
def resertBallTable(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    ball_ID = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    user_id = received_json_data['user_id']
    end_time = received_json_data['end_time']
    ball_object = received_json_data['ball_object']
    money = received_json_data['money']
    project = received_json_data['project']
    ball_format = received_json_data['ball_format']
    num_people = received_json_data['num_people']
    introduction = received_json_data['introduction']
    place = received_json_data['place']
    try:
        ball_table = models.ball_table(ball_ID=ball_ID, end_time=end_time,ball_object=ball_object,money=money,project=project,ball_format=ball_format,num_people=num_people,place=place,introduction=introduction)
        ball_table.save()
        about_ball = models.about_ball(user_id = user_id,ball_id =ball_ID)
        about_ball.save()
    except TransactionManagementError:
        x = "插入数据失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "插入数据成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def resertBallMessage(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    message_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    imageStr = received_json_data['image']
    user_id = received_json_data['user_id']
    imgdata = base64.b64decode(imageStr)
    num_Image = random.randint(10000000,99999999)
    path = "%s/media/messageImage/%d.jpg"%(os.path.dirname(os.path.dirname(__file__)),num_Image)
    file = open(path, "wb")
    file.write(imgdata)
    file.flush()
    file.close()
    message = received_json_data['message']
    try:
        imagePath = "messageImage/%d.jpg"%(num_Image)
        ball_message = models.ball_message(message_id=message_id, image=imagePath, message=message)
        ball_message.save()
        about_ball = models.about_ball(user_id=user_id, ballMessage_id=message_id)
        about_ball.save()
    except TransactionManagementError:
        x = "插入数据失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "插入数据成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")



@csrf_exempt
def ballEnroll(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    ball_id = received_json_data['ball_id']
    user_id = received_json_data['user_id']
    try:
        ball_enroll = models.ball_enroll(ball_id=ball_id, user_id=user_id)
        ball_enroll.save()
    except TransactionManagementError:
        x = "报名失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "报名成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def searchBallEnroll(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    ball_id = received_json_data['ball_id']
    try:
        ball_enroll = models.ball_enroll.objects.filter(ball_id=ball_id)
        if ball_enroll:
            listData = []
            for obj in ball_enroll:
                userBall = models.ball_user.objects.get(user_id=obj.user_id)
                dictData = {"user_id":obj.user_id,'status': obj.status, 'image': userBall.image,'user_name':userBall.user_name}
                listData.append(dictData)
        else:
            x = "无人员报名"
            message = x.decode("UTF-8")
            data = {'status': '1008', 'message': message}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "报名人员查询成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message ,'result':listData}
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def cancelBallEnroll(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    ball_id = received_json_data['ball_id']
    user_id = received_json_data['user_id']
    try:
        ball_enroll = models.ball_enroll.objects.filter(ball_id=ball_id,user_id=user_id)
        ball_enroll.delete()
    except TransactionManagementError:
        x = "取消失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "取消成功"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def allAboutBall(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    try:
        allAboutMessage_id = models.about_ball.objects.filter(user_id=user_id)
        allData = []
        for obj in allAboutMessage_id:
            allAbout = models.ball_table.objects.filter(ball_id=obj.ball_id)
            listData = []
            for obj in allAbout:
                audioMessage = models.ball_enroll.objects.filter(ball_id=obj.ball_ID)
                audioMessageList = []
                for obj in audioMessage:
                    audioMessageData = {'user_id':obj.user_id,'status':obj.status}
                    audioMessageList.append(audioMessageData)
                dictData = {'audioMessage':audioMessageList,'ball_ID':obj.ball_ID,'ball_object':obj.ball_object,'money':obj.money,'project':obj.project,'ball_format':obj.ball_format,'place':obj.place,'num_people':obj.num_people,'current_people':obj.current_people}
                listData.append(dictData)
            allData.append(listData)
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "查询到数据"
    message = x.decode("UTF-8")
    data = {'status': '1006', 'message': message, 'result': allData}
    return HttpResponse(json.dumps(data), content_type="application/json")



@csrf_exempt
def deleteAboutBall(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    ball_ID = received_json_data['ball_ID']
    try:
        models.about_ball.objects.filter(user_id=user_id,ball_id=ball_ID).delete()
        models.ball_table.objects.filter(ball_ID=ball_ID).delete()
        models.ball_enroll.objects.filter(ball_id=ball_ID).delete()
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "删除成功"
    data = {'status': '1006', 'message': x.decode("UTF-8")}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def deleteBallMessage(request):
    request.method = 'POST'
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    message_id = received_json_data['message_id']
    try:
        models.ball_message.objects.filter(message_id = message_id).delete()
        models.zan_message.objects.filter(message_id = message_id).delete()
        models.about_ball.objects.filter(ballMessage_id = message_id,user_id = user_id).delete()
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1004', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "删除成功"
    data = {'status': '1006', 'message': x.decode("UTF-8")}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def auditAbout(request):
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    ball_id = received_json_data['ball_id']
    audio_status = received_json_data['audio_status']
    try:
        audioAbout = models.ball_enroll.objects.get(user_id=user_id,ball_id=ball_id)
        if audio_status == "4":
            audioAbout.delete()
            x = "删除成功"
        else:
            print (audio_status)
            audioAbout.status = audio_status
            audioAbout.save()
            x = "审核成功"
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {'status': '1006', 'message': x.decode("UTF-8")}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def zanMessage(request):
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    message_id = received_json_data['message_id']
    try:
        ball_Message = models.ball_message.objects.filter(message_id=message_id)
        if ball_Message:
            ball_Message.num = ball_Message.num +1
            ball_Message.update()
            models.zan_message(message_id=message_id, user_id=user_id).save()
            x = "点赞成功"
            data = {'status': '1006', 'message': x.decode("UTF-8")}
        else:
            x = "点赞失败"
            data = {'status': '1007', 'message': x.decode("UTF-8")}
        return HttpResponse(json.dumps(data), content_type="application/json")
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "点赞失败"
    message = x.decode("UTF-8")
    data = {'status': '1004', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")


def canleZanMessage(request):
    received_json_data = json.loads(request.body)
    user_id = received_json_data['user_id']
    message_id = received_json_data['message_id']
    try:
        ball_Message = models.ball_message.objects.filter(message_id=message_id)
        if ball_Message:
            ball_Message.num = ball_Message.num - 1
            ball_Message.update()
            models.zan_message(message_id=message_id, user_id=user_id).delete()
            x = "取消点赞成功"
            data = {'status': '1006', 'message': x.decode("UTF-8")}
        else:
            x = "取消点赞失败"
            data = {'status': '1007', 'message': x.decode("UTF-8")}
        return HttpResponse(json.dumps(data), content_type="application/json")
    except TransactionManagementError:
        x = "失败"
        message = x.decode("UTF-8")
        data = {'status': '1005', 'message': message}
        return HttpResponse(json.dumps(data), content_type="application/json")
    x = "取消点赞失败"
    message = x.decode("UTF-8")
    data = {'status': '1004', 'message': message}
    return HttpResponse(json.dumps(data), content_type="application/json")
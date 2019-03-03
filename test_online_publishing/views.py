import os
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import serializers
from django.views import View
from test_online_publishing import models
from rest_framework.views import APIView
from common.mypage import Pagination


class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        msg = ''
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/publish/tasklist/')

        elif username == '':
            msg = '账号不能为空！'
        elif username != request.user.first_name + request.user.first_name:
            msg = '账号不存在！'
        elif username == request.user.first_name + request.user.first_name and not request.user.check_password(password):
            msg = '密码错误！'
        else:
            msg = '未知错误，请联系管理员！'

        return render(request, 'login.html', {'msg': msg})


class Logout(APIView):
    def get(self, request):
        auth.logout(request)
        return redirect('/publish/login/')

class PasswordChange(APIView):
    def get(self, request):
        return render(request, 'password_change.html', {
            'user_name': request.user.last_name + request.user.first_name,
        })

    def post(self, request):
        msg = ''
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not new_password == confirm_password:
            msg = '两次密码'
            return render(request, 'password_change.html', {
                "msg":msg,
            })

        if request.user.check_password(old_password):
            return redirect('/publish/tasklist/')
        else:
            msg = '原密码不正确'
            return render(request, 'password_change.html', {
                "msg":msg,
            })


class TaskList(APIView):
    def get(self, request):
        try:
            if request.GET.get('page'):
                page = int(request.GET.get('page'))
                if page < 1:
                    page = 1
            else:
                page = 1
        except:
            return HttpResponse('请求出错')

        all_task = models.TaskList.objects.all()
        page_obj = Pagination(current_page=page, total_count=all_task.count(),
                              base_url='/publish/tasklist/',
                              per_page=10, max_page=20)
        task_list = all_task[page_obj.page_start:page_obj.page_end]
        page_html = page_obj.page_html

        return render(request, 'tasklist.html', {
            "tasks": task_list.values(),
            'page_html': page_html,
            'user_name': request.user.last_name + request.user.first_name,
        })

        # tasks = serializers.serialize("json", all_task)
        # return render(request, 'tasklist.html',{"tasks":tasks})

    def post(self, request):
        keyword = request.POST.get('keyword')
        tasks = models.TaskList.objects.filter(name__icontains=keyword)
        return render(request, 'tasklist.html', {
            "tasks": tasks.values(),
            'user_name': request.user.last_name + request.user.first_name,
        })

        # 返回搜索结果的任务列表不用分页了
        # try:
        # if request.GET.get('page'):
        #         page = int(request.GET.get('page'))
        #         if page < 1:
        #             page = 1
        #     else:
        #         page = 1
        # except:
        #     return HttpResponse('请求出错')
        # page_obj = Pagination(current_page=page, total_count=tasks.count(),
        #                       base_url='/publish/tasklist/',
        #                       per_page=10, max_page=20)
        # tasks = tasks[page_obj.page_start:page_obj.page_end]
        # page_html = page_obj.page_html
        #
        # return render(request, 'tasklist.html', {
        #     "tasks": tasks.values(),
        #     'page_html': page_html,
        # })


class AddTask(APIView):
    def get(self, request):
        return render(request, 'addtask.html', {
            'user_name': request.user.last_name + request.user.first_name,
        })

    def post(self, request):
        # print(request.POST)

        name = request.POST.get('name')
        repository = request.POST.get('repository')
        # repositorys = request.POST.getlist('repository')
        branch = request.POST.get('branch')
        # branchs = request.POST.getlist('branch')
        tag = request.POST.get('tag')
        # tags = request.POST.getlist('tag')
        developer = request.POST.get('developer')
        tester = request.POST.get('tester')
        system = request.POST.get('system')
        is_publish = request.POST.get('is_publish')
        notice_tester = request.POST.get('notice_tester')
        notice_operator = request.POST.get('notice_operator')
        sql = request.POST.get('sql')

        repository_obj = models.Repository.objects.create(
            name=repository,
            branch=branch,
            tag=tag,
        )

        envir_obj = models.Envir.objects.get(id=1)

        task_obj = models.TaskList.objects.create(
            name=name,
            envir=envir_obj,
            # repositorys=repository_obj,
            developer=developer,
            tester=tester,
            is_publish=is_publish,
            system=system,
            notice_tester=notice_tester,
            notice_operator=notice_operator,
            sql=sql,
            creator=1,
        )

        task_obj.repositorys.add(repository_obj)

        return redirect('/publish/tasklist')


class EditTask(APIView):
    def get(self, request):
        task_id = request.GET.get("id")
        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        repository_objs = task_obj.repositorys.all()
        log_objs = models.Log.objects.filter(task_id=task_id)
        return render(request, 'edittask.html', {
            "task": task_obj,
            "repositorys": repository_objs,
            "logs": log_objs,
            'user_name': request.user.last_name + request.user.first_name,
        })
        # task = serializers.serialize("json", task_obj)
        # return render(request, 'edittask.html',{"task":task})

    def post(self, request):
        task_id = request.GET.get("id")
        name = request.POST.get('name')
        repository = request.POST.get('repository')
        branch = request.POST.get('branch')
        tag = request.POST.get('tag')
        developer = request.POST.get('developer')
        tester = request.POST.get('tester')
        system = request.POST.get('system')
        is_publish = request.POST.get('is_publish')
        notice_tester = request.POST.get('notice_tester')
        notice_operator = request.POST.get('notice_operator')
        sql = request.POST.get('sql')

        repository_obj = models.Repository.objects.create(
            name=repository,
            branch=branch,
            tag=tag,
        )
        # print(models.Repository.objects.filter(id=repository_obj.id))

        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        task_obj.name = name
        # task_obj.envir=1
        # task_obj.repositorys = models.Repository.objects.filter(id=repository_obj.id)
        task_obj.developer = developer
        task_obj.tester = tester
        task_obj.is_publish = is_publish
        task_obj.system = system
        task_obj.notice_tester = notice_tester
        task_obj.notice_operator = notice_operator
        task_obj.sql = sql
        task_obj.creator = 1
        task_obj.save()

        task_obj.repositorys.set(models.Repository.objects.filter(id=repository_obj.id))

        return redirect('/publish/tasklist')


class AddLog(APIView):
    def get(self, request):
        pass

    def post(self, request):
        task_id = request.POST.get("task_id")
        operate_tpye_id = request.POST.get('operate_tpye_id')

        if operate_tpye_id == "5":
            update_detail = []
            exec_result = os.popen(r"cd D:/git/mywork/test").read()
            os.popen("d:")
            # update_detail = update_detail + r"cd D:/git/mywork/test" + '\n' + str(exec_result) + '\n'
            update_detail.append(r"执行命令：    cd D:/git/mywork/test")
            update_detail.append("执行结果：    " + str(exec_result))

            exec_result = os.popen("git pull").read()
            # update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
            update_detail.append("执行命令：    git pull")
            update_detail.append("执行结果：    " + str(exec_result))

            exec_result = os.popen("git checkout master").read()
            # update_detail = update_detail + "git checkout master" + '\n' + str(exec_result) + '\n'
            update_detail.append("执行命令：    git checkout master")
            update_detail.append("执行结果：    " + str(exec_result))

            exec_result = os.popen("git pull").read()
            # update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
            update_detail.append("执行命令：    git pull")
            update_detail.append("执行结果：    " + str(exec_result))
            # print(update_detail)

            log_obj = models.Log.objects.create(
                task=models.TaskList.objects.filter(id=task_id)[0],
                operator=1,
                operate_type=models.OperateType.objects.filter(id=operate_tpye_id)[0],
                detail=update_detail
            )

        return HttpResponse("更新成功")


class GetLogDetail(APIView):
    def get(self, request):
        log_id = request.GET.get('id')
        log_obj = models.Log.objects.filter(id=log_id)[0]
        log_detail = log_obj.detail

        return HttpResponse(log_detail)
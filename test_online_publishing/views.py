import os
import json
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import serializers
from django.views import View
from test_online_publishing import models
from rest_framework.views import APIView
from common.mypage import Pagination
from common.git_operate import GitOperate
from test_online_publishing.config import GitPath


# 登录
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        msg = ''
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/publish/tasklist/')

        elif username == '':
            msg = '账号不能为空！'
        elif not username == request.user.username:
            msg = '账号不存在！'
        elif username == request.user.first_name + request.user.first_name and not request.user.check_password(
                password):
            msg = '密码错误！'
        else:
            msg = '未知错误，请联系管理员！'

        return render(request, 'login.html', {'msg': msg})


# 注销
class Logout(APIView):
    def get(self, request):
        auth.logout(request)
        return redirect('/publish/login/')


# 修改密码
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
            msg = '两次密码不一致'
            return render(request, 'password_change.html', {
                "msg": msg,
            })
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            return redirect('/publish/tasklist/')
        else:
            msg = '原密码不正确'
            return render(request, 'password_change.html', {
                "msg": msg,
            })


# 任务列表
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

        all_task = models.TaskList.objects.all().order_by("-id")
        page_obj = Pagination(current_page=page, total_count=all_task.count(),
                              base_url='/publish/tasklist/',
                              per_page=10, max_page=20)
        task_list = all_task[page_obj.page_start:page_obj.page_end]
        page_html = page_obj.page_html

        return render(request, 'tasklist.html', {
            "tasks": task_list,
            'page_html': page_html,
            # 'user_name': request.user.last_name + request.user.first_name,
            # 'user_name': request.user.username,
        })

        # tasks = serializers.serialize("json", all_task)
        # return render(request, 'tasklist.html',{"tasks":tasks})

    def post(self, request):
        keyword = request.POST.get('keyword')
        tasks = models.TaskList.objects.filter(name__icontains=keyword).order_by("-id")
        return render(request, 'tasklist.html', {
            "tasks": tasks.values(),
            'user_name': request.user.last_name + request.user.first_name,
            'keyword': keyword,
        })

        # 返回搜索结果的任务列表不用分页了
        # try:
        # if request.GET.get('page'):
        # page = int(request.GET.get('page'))
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


# 添加任务
class AddTask(APIView):
    def get(self, request):
        return render(request, 'addtask.html', {
            'user_name': request.user.last_name + request.user.first_name,
        })

    def post(self, request):
        # print(request.POST)

        name = request.POST.get('name')
        # repository = request.POST.get('repository')
        repositorys = request.POST.getlist('repository')
        # branch = request.POST.get('branch')
        branchs = request.POST.getlist('branch')
        # tag = request.POST.get('tag')
        # tags = request.POST.getlist('tag')
        developer = request.POST.get('developer')
        tester = request.POST.get('tester')
        system = request.POST.get('system')
        is_publish = request.POST.get('is_publish')
        notice_tester = request.POST.get('notice_tester')
        notice_operator = request.POST.get('notice_operator')
        sql = request.POST.get('sql')

        repositorys_obj = []
        for i in range(len(repositorys)):
            repository_obj = models.Repository.objects.create(
                name=repositorys[i],
                branch=branchs[i],
                # tag=tags,
            )
            repositorys_obj.append(repository_obj)

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
            creator=request.user,
        )

        task_obj.repositorys.add(*repositorys_obj)

        models.Log.objects.create(
            task=task_obj,
            operator=request.user,
            operate_type=models.OperateType.objects.filter(id=1)[0],
            detail="新增新更新包"
        )

        return redirect('/publish/tasklist')


# 编辑任务
class EditTask(APIView):
    def get(self, request):
        task_id = request.GET.get("id")
        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        repository_objs = task_obj.repositorys.all()
        log_objs = models.Log.objects.filter(task_id=task_id).order_by("-id")
        return render(request, 'edittask.html', {
            "task": task_obj,
            "repositorys": repository_objs,
            "logs": log_objs,
            # 'user_name': request.user.last_name + request.user.first_name,
            'user_name': request.user.username,
        })
        # task = serializers.serialize("json", task_obj)
        # return render(request, 'edittask.html',{"task":task})

    def post(self, request):
        task_id = request.GET.get("id")
        name = request.POST.get('name')
        # repository = request.POST.get('repository')
        repositorys = request.POST.getlist('repository')
        # branch = request.POST.get('branch')
        branchs = request.POST.getlist('branch')
        # tag = request.POST.get('tag')
        # tags = request.POST.getlist('tag')
        developer = request.POST.get('developer')
        tester = request.POST.get('tester')
        system = request.POST.get('system')
        is_publish = request.POST.get('is_publish')
        notice_tester = request.POST.get('notice_tester')
        notice_operator = request.POST.get('notice_operator')
        sql = request.POST.get('sql')

        repositorys_obj = []
        for i in range(len(repositorys)):
            repository_obj = models.Repository.objects.create(
                name=repositorys[i],
                branch=branchs[i],
                # tag=tags,
            )
            repositorys_obj.append(repository_obj)

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
        task_obj.creator = request.user
        task_obj.save()

        task_obj.repositorys.set(repositorys_obj)

        models.Log.objects.create(
            task=models.TaskList.objects.filter(id=task_id)[0],
            operator=request.user,
            operate_type=models.OperateType.objects.filter(id=2)[0],
            detail="编辑更新包"
        )

        return redirect('/publish/tasklist')


# 任务操作记录
class Operate(APIView):
    def get(self, request):
        pass

    def post(self, request):
        task_id = request.POST.get("task_id")
        operate_tpye_id = request.POST.get('operate_tpye_id')
        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        repository_objs = task_obj.repositorys.all()

        response = "操作失败，请联系管理员"
        repository_path = ''
        # 更新到本地环境
        if operate_tpye_id == "5":
            repository_path = GitPath.local_env_path
            response = "本地环境更新成功"

        # 更新到开发环境
        elif operate_tpye_id == "10":
            repository_path = GitPath.develop_env_path
            response = "开发环境更新成功"

        # 更新到测试环境
        elif operate_tpye_id == "15":
            repository_path = GitPath.test_env_path
            response = "测试环境更新成功"

        # 更新到预生产环境
        elif operate_tpye_id == "20":
            repository_path = GitPath.preproduct_env_path
            response = "预生产环境更新成功"

        # 更新到生产环境
        elif operate_tpye_id == "25":
            repository_path = GitPath.product_env_path
            response = "生产环境更新成功"

        # 更新仓库代码
        if repository_path:
            update_detail = []
            for repository_obj in repository_objs:
                # print(repository_obj.id,repository_obj.name,repository_obj.branch)
                git_operate = GitOperate(repository_path=repository_path, repository_name=repository_obj.name,
                                         branch_name=repository_obj.branch)
                update_detail.extend(git_operate.run())
                # print(update_detail)

            models.Log.objects.create(
                task=models.TaskList.objects.filter(id=task_id)[0],
                operator=request.user,
                operate_type=models.OperateType.objects.filter(id=operate_tpye_id)[0],
                detail=update_detail
            )

        # 申请发版
        if operate_tpye_id == "100":
            # print(task_obj)
            task_obj.is_publish = 1
            task_obj.save()
            update_detail = '申请发版'
            models.Log.objects.create(
                task=models.TaskList.objects.filter(id=task_id)[0],
                operator=request.user,
                operate_type=models.OperateType.objects.filter(id=operate_tpye_id)[0],
                detail=update_detail
            )
            response = "申请发版成功"

        elif operate_tpye_id == "101":
            task_obj.is_publish = 0
            update_detail = '撤销申请发版'
            models.Log.objects.create(
                task=models.TaskList.objects.filter(id=task_id)[0],
                operator=request.user,
                operate_type=models.OperateType.objects.filter(id=operate_tpye_id)[0],
                detail=update_detail
            )
            response = "撤销申请发版成功"

        return HttpResponse(response)


# 获取任务操作日志
class GetLogDetail(APIView):
    def get(self, request):
        log_id = request.GET.get('id')
        log_obj = models.Log.objects.filter(id=log_id)[0]
        log_detail = log_obj.detail
        log_detail = log_detail.replace(r'[', '')
        log_detail = log_detail.replace(r']', '')
        log_detail = log_detail.replace(r'\n', ',')
        log_detail = log_detail.replace(r'\t', '    ')
        return HttpResponse(log_detail)


class Test(APIView):
    def get(self, request):
        data = [{
            "a1": 1,
            "a2": 2,
        }]

        return HttpResponse(json.dumps(data))
        # return HttpResponse("hello get ")

    def post(self, request):
        data = [{
            "a1":1,
            "a2":2,
        }]

        return HttpResponse(json.dumps(data))
        # return HttpResponse("hello post ")
import os
from django.shortcuts import render, HttpResponse, redirect
from django.core import serializers
from django.views import View
from test_online_publishing import models
from rest_framework.views import APIView


# Create your views here.
class TaskList(View):
    def get(self, request):
        all_task = models.TaskList.objects.all().values()
        return render(request, 'tasklist.html', {"tasks": all_task})

        # tasks = serializers.serialize("json", all_task)
        # return render(request, 'tasklist.html',{"tasks":tasks})

    def post(self, request):

        return render(request, 'tasklist.html')


class AddTask(View):
    def get(self, request):
        return render(request, 'addtask.html')

    def post(self, request):
        print(request.POST)

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


class EditTask(View):
    def get(self, request):
        task_id = request.GET.get("id")
        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        repository_objs = task_obj.repositorys.all()
        log_objs = models.Log.objects.filter(task_id=task_id)
        return  render(request, 'edittask.html', {"task":task_obj, "repositorys":repository_objs, "logs":log_objs})
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
        print(models.Repository.objects.filter(id=repository_obj.id))

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


class AddLog(View):
    def get(self, request):
        pass

    def post(self, request):
        task_id = request.POST.get("task_id")
        operate_tpye_id = request.POST.get('operate_tpye_id')

        if operate_tpye_id=="5":
            update_detail = []
            exec_result = os.popen(r"cd D:/git/mywork/test").read()
            os.popen("d:")
            # update_detail = update_detail + r"cd D:/git/mywork/test" + '\n' + str(exec_result) + '\n'
            update_detail.append(r"cd D:/git/mywork/test")
            update_detail.append(str(exec_result))

            exec_result = os.popen("git pull").read()
            # update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
            update_detail.append("git pull")
            update_detail.append(str(exec_result))

            exec_result = os.popen("git checkout master").read()
            # update_detail = update_detail + "git checkout master" + '\n' + str(exec_result) + '\n'
            update_detail.append("git checkout master")
            update_detail.append(str(exec_result))

            exec_result = os.popen("git pull").read()
            # update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
            update_detail.append("git pull")
            update_detail.append(str(exec_result))
            print(update_detail)


            log_obj = models.Log.objects.create(
                task = models.TaskList.objects.filter(id=task_id)[0],
                operator = 1,
                operate_type = models.OperateType.objects.filter(id=operate_tpye_id)[0],
                detail = update_detail
            )

        return HttpResponse("更新成功")


class GetLogDetail(View):
    def get(self, request):
        log_id = request.GET.get('id')
        log_obj = models.Log.objects.filter(id=log_id)[0]
        log_detail = log_obj.detail

        return HttpResponse(log_detail)
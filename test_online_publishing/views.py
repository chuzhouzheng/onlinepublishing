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

        envir_obj = models.Envir.objects.get(id=1)

        models.TaskList.objects.create(
            name=name,
            envir=envir_obj,
            repository_id=repository_obj,
            developer=developer,
            tester=tester,
            is_publish=is_publish,
            system=system,
            notice_tester=notice_tester,
            notice_operator=notice_operator,
            sql=sql,
            creator=1,
        )

        return redirect('/publish/tasklist')


class EditTask(View):
    def get(self, request):
        task_id = request.GET.get("id")
        task_obj = models.TaskList.objects.filter(id=task_id)[0]
        return  render(request, 'edittask.html', {"task":task_obj})
        # task = serializers.serialize("json", task_obj)
        # return render(request, 'edittask.html',{"task":task})

    def post(self, request):
        print(request.POST)
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

        task_obj = models.TaskList.objects.filter(id=task_id)
        task_obj.update(
            name=name,
            # envir=1,
            # repository_id=1,
            developer=developer,
            tester=tester,
            is_publish=is_publish,
            system=system,
            notice_tester=notice_tester,
            notice_operator=notice_operator,
            sql=sql,
            creator=1,
        )

        return redirect('/publish/tasklist')

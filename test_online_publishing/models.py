from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=256, null=False, help_text='更新包名称', verbose_name='更新包名称')
    envir = models.ForeignKey(to='Envir', on_delete=True, db_constraint=False, default=1, verbose_name='所在环境，对应envir.id')
    repositorys = models.ManyToManyField(to='Repository', db_constraint=False, default=None, verbose_name='代码仓库')
    developer = models.CharField(max_length=256, null=True, verbose_name='开发员')
    tester = models.CharField(max_length=256, null=True, verbose_name='测试员')
    is_publish = models.SmallIntegerField(null=True, default=0, verbose_name='是否申请发版（1：申请发版，0：不用申请发版）')
    system = models.CharField(max_length=64, null=True, verbose_name='所属项目')
    notice_tester = models.TextField(null=True, verbose_name='测试须知')
    notice_operator = models.TextField(null=True, verbose_name='运维须知')
    sql = models.TextField(null=True, verbose_name='需要执行的sql')
    creator = models.ForeignKey(to=User, on_delete=True, db_constraint=False, default=None, verbose_name='创建人，auth_user.id')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task'
        verbose_name_plural = '更新包列表'


class Repository(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=256, null=False, verbose_name='代码仓库')
    branch = models.CharField(max_length=256, null=True, default='develop', verbose_name='分支')
    tag = models.CharField(max_length=256, null=True, verbose_name='分支tag')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'repository'
        verbose_name_plural = '代码仓库'


class Log(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    task = models.ForeignKey(to='TaskList', on_delete=True, db_constraint=False, default=None, verbose_name='任务id')
    operator = models.ForeignKey(to=User, on_delete=True, db_constraint=False, default=None, verbose_name='操作人，auth_user.id')
    operate_type = models.ForeignKey(to='OperateType', on_delete=True, db_constraint=False, verbose_name='操作类型，对应operate_type.id')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    detail = models.TextField(null=True, verbose_name='操作详情')

    def __str__(self):
        return self.task

    class Meta:
        db_table = 'log'
        verbose_name_plural = '操作日志'


class OperateType(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=64, null=False, verbose_name='操作类型')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'operate_type'
        verbose_name_plural = '操作类型'


class Envir(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=64, null=False, verbose_name='操作类型')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'envir'
        verbose_name_plural = '代码所在环境'



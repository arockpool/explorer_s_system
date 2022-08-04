from django.db import models


class Admin(models.Model):
    '''
    管理员
    '''
    user_id = models.CharField('用户id', max_length=32, db_index=True)
    permissions = models.TextField('用户权限json字符串', null=True)
    is_super = models.IntegerField('是否超级管理员', default=0)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, null=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    objects = models.Manager()

    class Meta:
        ordering = ["-create_time", ]


class ChoiceModel(models.Model):
    key = models.CharField('键名', max_length=128)
    value = models.CharField('值', max_length=128)
    describe = models.CharField('描述', max_length=128, null=True)
    send = models.IntegerField(verbose_name="返回的值")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    objects = models.Manager()
    state = models.IntegerField(default=1)

    class Meta:
        ordering = ["-create_time"]


class Role(models.Model):
    '''角色'''
    name = models.CharField('角色名称', max_length=128)
    permissions = models.TextField('权限json字符串', null=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ["-create_time"]


class Permission(models.Model):
    '''权限'''
    code = models.CharField('权限code', max_length=128)
    name = models.CharField('权限名称', max_length=128)
    url = models.CharField('菜单对应的url', max_length=128)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ["-create_time"]


class Appinfo(models.Model):
    """Appid 管理"""
    app_id = models.CharField('app_id', max_length=16, unique=True, db_index=True)
    app_secret = models.CharField('app_secret', max_length=128)
    opt_user_id = models.CharField('最后修改人', max_length=128)
    status = models.BooleanField('status', default=True)
    remarks = models.CharField('remarks', max_length=128, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
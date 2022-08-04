from django.db import models


class Notice(models.Model):
    '''
    通知
    '''
    state_choices = ((-1, '无效'), (0, '草稿'), (1, '有效'))
    category_choices = ((0, '新闻'),)

    category = models.IntegerField('类别', default=0, choices=category_choices)
    title = models.CharField('通知标题', max_length=256)
    content = models.TextField('通知内容', null=True)
    publish_time = models.DateTimeField('发布时间', null=True)
    author = models.CharField('作者', max_length=64, null=True)

    sort = models.IntegerField('排序', default=0)
    state = models.IntegerField('状态', default=0, choices=state_choices)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ["-sort", "-publish_time", "-create_time"]


class Faq(models.Model):
    '''
    常见问题
    '''
    state_choices = ((0, '无效'), (1, '停用'))

    title = models.CharField('问题标题', max_length=256)
    content = models.TextField('通知内容', null=True)

    sort = models.IntegerField('排序', default=0)
    state = models.IntegerField('状态', default=1, choices=state_choices)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    objects = models.Manager()

    class Meta:
        ordering = ["-sort", "-create_time"]

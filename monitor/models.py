from django.db import models


class SlowRequest(models.Model):
    """慢url"""
    url = models.CharField('url', max_length=256, db_index=True)
    duration = models.FloatField("时长", db_index=True)
    ip = models.CharField('ip', max_length=32)
    post_data = models.TextField('post数据')
    record_date = models.DateField('记录日期', db_index=True)
    record_time = models.DateTimeField('记录时间', auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class SysError(models.Model):
    """系统错误"""
    service = models.CharField('服务模块', max_length=32, db_index=True)
    url = models.CharField('url', max_length=190, null=True, db_index=True)  # 非http请求中的报错可以为空
    detail = models.TextField('错误信息')
    record_date = models.DateField('记录日期', db_index=True)
    record_time = models.DateTimeField('发生时间', auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class RequestLog(models.Model):
    """请求日志"""
    url = models.CharField('url', max_length=256, db_index=True)
    post_data = models.TextField('post数据')
    res_data = models.TextField('返回数据')
    request_time = models.DateTimeField('请求时间', db_index=True)
    duration = models.FloatField("时长", db_index=True)
    app_id = models.CharField('app_id', max_length=32, null=True)
    ip = models.CharField('ip', max_length=32, null=True)
    create_time = models.DateTimeField('记录时间', auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)

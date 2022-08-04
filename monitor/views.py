import datetime

from explorer_s_common.decorator import common_ajax_response
from explorer_s_common.utils import format_return

from monitor.interface import SlowRequestBase, SysErrorBase, RequestLogBase

srb = SlowRequestBase()
seb = SysErrorBase()


def _format_end_date(end_date):
    # 查询的时候结束日期往后延迟一天
    if end_date and ":" not in end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    return end_date


def _format_sr(sr):
    return dict(url=sr.url, duration=sr.duration, ip=sr.ip, post_data=sr.post_data, record_time=sr.record_time.strftime("%Y-%m-%d %H:%M:%S"))


def _format_se(se):
    return dict(url=se.url, detail=se.detail, record_time=se.record_time.strftime("%Y-%m-%d %H:%M:%S"))


@common_ajax_response
def add_slow_request(request):
    '''
    添加慢请求
    '''
    url = request.POST.get('url')
    duration = request.POST.get('duration')
    ip = request.POST.get('ip')
    post_data = request.POST.get('post_data')

    return srb.add_slow_request(url=url, duration=duration, ip=ip, post_data=post_data)


@common_ajax_response
def get_slow_request_group(request):
    # 慢查询分组信息，展示：时间期限内的慢url、总次数、最大时长、最小时长、平均时长
    # [["/body_data/api/get_body_overview_for_homepage", 1, 5, 5, 5],["/body_data/api/get_body_overview", 3, 12, 6, 8.7]]

    start_date = request.POST.get("start_date")
    end_date = _format_end_date(request.POST.get("end_date"))

    srs = srb.get_slow_request(start_date, end_date)
    urls = {}
    for sr in srs:
        if sr.url not in urls:
            urls[sr.url] = [sr.duration, ]
        else:
            urls[sr.url].append(sr.duration)
    data = []
    for url in urls:
        data.append([url, len(urls[url]), max(urls[url]), min(urls[url]), float('%.1f' % (sum(urls[url]) / len(urls[url])))])

    data.sort(key=lambda x: x[1], reverse=True)

    return format_return(0, data=data)


@common_ajax_response
def get_slow_request(request):
    # 慢查询详情：{"url": "/body_data/api/get_body_overview", "duration": 12, "ip": "192.168.1.111",
    #                "post_data": "a=1&n=2", "record_time": "2017-11-07 14:41:50"}

    url = request.POST.get("url")
    start_date = request.POST.get("start_date")
    end_date = _format_end_date(request.POST.get("end_date"))

    srs = srb.get_slow_request(start_date, end_date, url)
    data = [_format_sr(sr) for sr in srs]

    return format_return(0, data=data)


@common_ajax_response
def add_sys_error(request):
    '''
    添加系统错误
    '''
    service = request.POST.get('service')
    url = request.POST.get('url')
    detail = request.POST.get('detail')

    return seb.add_sys_error(service=service, url=url, detail=detail)


@common_ajax_response
def get_sys_error_group(request):
    # 错误分组信息，展示：时间期限内的慢url、总次数
    # [["/body_data/api/get_body_overview_for_homepage", 1],["/body_data/api/get_body_overview", 3]]

    start_date = request.POST.get("start_date")
    end_date = _format_end_date(request.POST.get("end_date"))

    ses = seb.get_sys_error(start_date, end_date)
    urls = {}
    for se in ses:
        if se.url not in urls:
            urls[se.url] = 1
        else:
            urls[se.url] += 1
    data = list(urls.items())
    data.sort(key=lambda x: x[1], reverse=True)

    return format_return(0, data=data)


@common_ajax_response
def get_sys_error(request):
    # 错误详情：{"url": "/body_data/api/get_body_overview", "duration": 12, "ip": "192.168.1.111",
    #                "post_data": "a=1&n=2", "record_time": "'2017-11-07 14:41:50'"}

    url = request.POST.get("url")
    start_date = request.POST.get("start_date")
    end_date = _format_end_date(request.POST.get("end_date"))

    ses = seb.get_sys_error(start_date, end_date, url)
    data = [_format_se(se) for se in ses]

    return format_return(0, data=data)


@common_ajax_response
def add_request_log(request):

    url = request.POST.get('url')
    post_data = request.POST.get('post_data')
    res_data = request.POST.get('res_data')
    request_time = request.POST.get('request_time')
    duration = request.POST.get('duration')
    app_id = request.POST.get('app_id')
    ip = request.POST.get('ip')

    return RequestLogBase().add_request_log(
        url=url, post_data=post_data, res_data=res_data, request_time=request_time,
        duration=duration, app_id=app_id, ip=ip
    )

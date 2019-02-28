__author__ = 'Administrator'

'''
    封装一个分页的类:Pagination
'''

import math
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


class Pagination(object):

    def __init__(self, current_page, total_count, base_url, per_page=10, max_page=10 ):
        '''

        :param current_page: 当前页码
        :param total_count: 数据总数
        :param base_url: 分页的跳转路径
        :param per_page: 每页加载的数据量
        :param max_page: 每页的最大页码数
        :return:
        '''

        self.current_page = current_page
        self.total_count = total_count
        self.base_url = base_url
        self.per_page = per_page
        self.max_page = max_page


    def __str__(self):
        return "This is a pagination Object.base_url:{}".format(self.base_url)

    @property
    def page_start(self):
        return (self.current_page - 1) * self.per_page


    @property
    def page_end(self):
        return self.current_page * self.per_page


    @property
    def page_html(self):

        page_count = math.ceil(self.total_count / self.per_page)    # 总页数，向上取正
        page_start = 1      # 分页的开始页码
        page_end = page_count + 1   # 分页的结束页码

        # 分页功能
        max_page = self.max_page
        page = self.current_page
        half_max_page = max_page // 2
        if page_count > max_page:
            page_start = 1
            page_end = max_page +1
            if page > half_max_page + 1:
                page_start = page - half_max_page
                page_end = page + half_max_page
            if page_end > page_count - half_max_page:
                page_start = page_count - max_page
                page_end = page_count + 1
        # print('页码：',page,page_start,page_end)

        page_html_list = []
        #上一页
        if page <= 1:
            up_page = '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            up_page = '<li><a href="{}?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.base_url,page-1)
        page_html_list.append(up_page)

        # 首页：
        home_page = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
        page_html_list.append(home_page)

        for i in range(page_start, page_end):
            if i == page:
                li = '<li class="active"><a href="{}?page={}">{}</a></li>'.format(self.base_url,i,i)
            else:
                li = '<li><a href="{}?page={}">{}</a></li>'.format(self.base_url,i,i)
            page_html_list.append(li)

        # 尾页：
        end_page = '<li><a href="{}?page={}">尾页</a></li>'.format(self.base_url,page_count)
        page_html_list.append(end_page)

        #下一页
        if page >= page_count:
            down_page = '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            down_page = '<li><a href="{}?page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.base_url,page+1)
        page_html_list.append(down_page)

        page_html = "".join(page_html_list)     # 将page_html_list转换成str对象

        return page_html


class MyPageNumberPagination(PageNumberPagination):
    '''
        一般分页：每页条数，请求的页码
        page_size：默认每页显示多少条数据
        page_query_param：url参数，请求的页码

        page_size_query_param：url参数，请求的页码参数，临时使用的，优先级高于page_size
        max_page_size：每页显示最多显示多少条数据，配合page_size_query_param使用的
    '''
    page_size = 2
    page_query_param = 'page'

    page_size_query_param = 'size'
    max_page_size = 10


class MyLimitOffsetPagination(LimitOffsetPagination):
    '''
        偏移分页：从第几条数据开始查询，查询多少条数据
        default_limit：默认每页显示多少条数据
        limit_query_param：url参数，每页显示多少条数据
        offset_query_param：url参数，请求数据的偏移量
        max_limit：每页显示最多显示多少条数据
    '''
    default_limit = 2
    limit_query_param = 'limit'

    offset_query_param ='offset'
    max_limit = 10


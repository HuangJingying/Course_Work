# -*- coding: utf-8 -*-
# 使用时cookie需要更新
# 参考资料：
# https://github.com/yaochenkun/enterprise-info-spider
# https://blog.csdn.net/qq_38934189/article/details/79280255
# TODO: 缓存所有查询到的详情页
# TODO: 跳过香港公司

import os
from bs4 import BeautifulSoup
import requests
import xlrd
import xlwt
from xlutils.copy import copy
import time
import pandas as pd
from collections import defaultdict
# import lxml
# import winsound


# 企查查网站爬虫类
class EnterpriseInfoSpider:
    def __init__(self):

        # 文件相关
        self.excelPath = '爬取信息.xls'
        self.sheetName = 'details'
        self.workbook = None
        self.table = None
        self.beginRow = None

        # 目录页
        self.catalogUrl = "https://www.qichacha.com/search?key=%E4%BD%9B%E5%B1%B1%E5%B8%82%E6%B3%93%E6%B6%A6%E9%BE%99%E8%B4%A7%E8%BF%90%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"

        # 详情页（前缀+firm）
        self.detailsUrl = "http://www.qichacha.com/"
        self.cookie = input("请输入cookie:") # QCCSESSID=f9ung05iqpv3a4e9jo13qad7p6; UM_distinctid=166b4bad3b46f-0f6e64afcc4836-8383268-1fa400-166b4bad3b664; CNZZDATA1254842228=414356198-1540626200-%7C1540626200; zg_did=%7B%22did%22%3A%20%22166b4bad4122a-06946ce710e1b3-8383268-1fa400-166b4bad413a5%22%7D; acw_tc=6f3f319815406304469506525e8a4fb1df01a207fdf57406d346e984ff; _uab_collina=154063044832335314199152; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1540630450; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1540630464; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201540630434842%2C%22updated%22%3A%201540630484541%2C%22info%22%3A%201540630434853%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%222763db2ac8cfd4f3a73ba7025bbd47b5%22%7D
        self.host = "www.qichacha.com"
        self.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"

        self.headers = {
            "cookie": self.cookie,
            "host": self.host,
            "user-agent": self.userAgent
        }

        # 数据字段名
        # self.fields = ['QYMC', '公司名称', 'ZCZJ', 'JYFWMS', 'ZCSZSF']
        self.fields = ['企业名称', '公司名称', '注册资本', '实缴资本', '经营状态', '成立日期', '统一社会信用代码', '纳税人识别号', '注册号', '组织机构代码', '公司类型', '所属行业', '核准日期', '登记机关', '所属地区', '英文名', '曾用名', '参保人数', '人员规模', '营业期限', '企业地址', '经营范围']

    # 爬虫开始前的一些预处理
    def init(self):
        try:
            # 试探是否有该excel文件，#获取行数：workbook.sheets()[0].nrows
            readWorkbook = xlrd.open_workbook(self.excelPath)
            self.beginRow = readWorkbook.sheets()[0].nrows  # 获取行数
            self.workbook = copy(readWorkbook)
            self.table = self.workbook.get_sheet(0)

        except Exception as e:
            print(e)
            self.workbook = xlwt.Workbook(encoding='utf-8')
            self.table = self.workbook.add_sheet(self.sheetName)

            # 创建表头字段
            col = 0
            for field in self.fields:
                self.table.write(0, col, field)
                # self.table.write(0, col, field.decode('gbk').encode('utf-8'))
                col += 1

            self.workbook.save(self.excelPath)
            self.beginRow = 1
            print("已在当前目录下创建爬取信息.xls数据表")

    # 从keyword/1页 得到的html中获得总页码数
    def getTotalPage(self, catalogPageCode):
        soup = BeautifulSoup(catalogPageCode, "lxml")
        pagebar = soup.select("li #ajaxpage")
        if pagebar == None:
            return -1
        elif pagebar == []:
            return 1
        return len(pagebar) + 1

    # 从keyword/page页 得到html中的所有公司条目
    def getFirmIdDoms(self, catalogPageCode):
        soup = BeautifulSoup(catalogPageCode, "lxml")
        content = soup.find('section', id='searchlist')
        if content != None:
            company = content.find('tbody').find_all('tr')[0]
            FirmIdDoms = company.find('a', 'ma_h1')['href']
            name = company.find('a', 'ma_h1').get_text()  # 企业名称
        else:
            print('没有查询到相关信息')
            FirmIdDoms = 0
            name = ''
        return FirmIdDoms, name

    # 爬虫开始
    def start(self):
        # filename = input("请输入关键字：").decode("gbk").encode("utf-8")
        filename = input("请输入文件名(如：name-1.xlsx)：")
        # 读取企业名称
        # filename = "企业基本信息表.xlsx"
        f = open(filename, "rb")
        keywords = pd.read_excel(f)
        f.close()
        length = len(keywords)
        for i in range(length):
            # 先获取keyword第一页内容的页码
            keyword = keywords.loc[i, 'QYMC']
            # keyword="中铁国际多式联运"
            print("第{}项 {}".format(i + 1, keyword))
            self.table.write(self.beginRow, 0, keyword)
            self.workbook.save(self.excelPath)
            totalPage = self.getTotalPage(self.getCatalogPageCode(keyword, 1))
            if totalPage == -1:
                continue

            # 模拟翻页操作
            # for page in range(1, totalPage + 1):
            for page in range(1, 2):  # 只爬第一页
                print("正在爬取数据,请稍等...")
                # 获取第page页代码
                catalogPageCode = self.getCatalogPageCode(keyword, page)
                soup = BeautifulSoup(catalogPageCode, 'lxml')
                if soup.find('div', id='smartBox') is None:
                    input('请重新在页面验证后，按Enter键重试...')
                    catalogPageCode = self.getCatalogPageCode(keyword, page)
                firmIdDoms, name = self.getFirmIdDoms(catalogPageCode)
                if firmIdDoms != 0:
                    detailsPageCode = self.getDetailsPageCode(firmIdDoms)                        
                    self.writeDetailsToExcel(detailsPageCode, name)
                else:
                    self.beginRow += 1
                # time.sleep(2)  # 0.5s后再爬防止反爬虫机制

        print("爬虫已完全结束！")

    # 根据keyword和page构造查询串
    # 其中keyword中的空格换成+
    # 返回查询字符串构成的字典
    def getCatalogQueryString(self, keyword, page):
        keyword.replace(' ', '+')
        return {"key": keyword, "index": "0", "p": page}

    # 根据keyword关键字获取目录页代码
    def getCatalogPageCode(self, keyword, page):
        queryString = self.getCatalogQueryString(keyword, page)
        response = requests.request("GET", self.catalogUrl, headers=self.headers, params=queryString)
        if response.text.strip() == '':
            for i in range(5):
                print('网络错误: 目录页获取失败，第{}次重试...'.format(i + 1))
                response = requests.request("GET", self.catalogUrl, headers=self.headers, params=queryString)
                if response.text.strip != '':
                    break
        if response.status_code==405:
            # response.txt='cookie error'
            print('cookie error')
        return response.text

    # 根据firmId获取公司的详情页代码
    def getDetailsPageCode(self, firmId):
        response = requests.request("GET", self.detailsUrl + firmId.replace('firm','cbase'), headers=self.headers)
        if response.text.strip() == '':
            for i in range(5):
                print('网络错误: 详情页获取失败，第{}次重试...'.format(i + 1))
                response = requests.request("GET", self.detailsUrl + firmId.replace('firm','cbase'), headers=self.headers)
                if response.text.strip != '':
                    break
        if response.text.strip == '':
            with open('network_error_ids.log', 'a', encoding='utf-8') as f:
                f.writeline([firmId])
        return response.text

    # 抓取detailsPageCode页上该企业所有信息，并存入excel
    def writeDetailsToExcel(self, detailsPageCode, companyname):
        detailDoms = self.getDetailDoms(detailsPageCode)
        self.table.write(self.beginRow, 1, companyname)
        for col in range(2, len(self.fields)):
            key = self.fields[col]
            value = detailDoms[key]
            self.table.write(self.beginRow, col, value)  # 写入excel
        self.workbook.save(self.excelPath)  # 保存至文件
        self.beginRow += 1

    # 根据detailsPageCode获得它的所有detailDoms元素
    def getDetailDoms(self, detailsPageCode):
        soup = BeautifulSoup(detailsPageCode, "lxml")
        basic_list = defaultdict(lambda: '')
        if soup.find('section', id='Cominfo') != None:
            content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('td')
            for i in range(len(content) // 2):
                key = content[i * 2].get_text().strip().strip('：')
                value = content[i * 2 + 1].get_text().strip()
                basic_list[key] = value
            basic_list['企业地址'] = basic_list['企业地址'].split()[0]
        else:
            with open('debug.log', 'w', encoding='utf-8') as f:
                f.write(detailsPageCode)
            input('未找到相关信息，按任意键继续……')
        return basic_list


########
# 爬虫入口
########
spider = EnterpriseInfoSpider()
spider.init()
spider.start()

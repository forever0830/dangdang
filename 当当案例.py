import requests
from lxml import etree
import re
import openpyxl

wb=openpyxl.Workbook()
sheet = wb.active
sheet.title ='图书数据'
sheet['A1'] = '书名'
sheet['B1'] = '价格'
sheet['C1'] = '时间'
sheet['D1'] = '作者'
sheet['E1'] = '出版社'
sheet['F1'] = '链接'

print('开始爬取数据：')

def get_page(key):
    for page in range(1,5):
        url = 'http://search.dangdang.com/?key=%C6%B7%B8%F1%D1%F8%B3%C9&act=input&sort_type=sort_score_desc&page_index='+str(page+1)+'#J_tab'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = requests.get(url = url,headers = headers)
        parse_page(response)
        print('page %s over!!!' % page)

def parse_page(response):
    tree = etree.HTML(response.text)
    li_list = tree.xpath('//ul[@class="bigimg"]/li')
    # print(len(li_list))  # 测试
    for li in li_list:
        data = []
        try:
            # 获取书的标题,并添加到列表中
            title = li.xpath('./a/@title')[0].strip()
            #data.append(title)
            # 获取商品链接,并添加到列表中
            commodity_url = li.xpath('./p[@class="name"]/a/@href')[0]
            #data.append(commodity_url)
            # 获取价格,并添加到列表中
            price = li.xpath('./p[@class="price"]/span[1]/text()')[0]
            #data.append(price)
            # 获取作者,并添加到列表中
            author = ''.join(li.xpath('./p[@class="search_book_author"]/span[1]//text()')).strip()
            #data.append(author)
            # 获取出版时间,并添加到列表中
            time = li.xpath('./p[@class="search_book_author"]/span[2]/text()')[0]
            pub_time = re.sub('/','',time).strip()
            #data.append(pub_time)
            #commodity_detail = ''
            #获取出版社
            publis = ''.join(li.xpath('./p[@class="search_book_author"]/span[3]//text()')).strip()
            #data.append(publis)

            sheet.append([title,price,time,author,publis,commodity_url])

        except:
            pass

def main():
    # key = input('Please input key:')
    key = '品格养成'  
    get_page(key)
    
main()

print('爬取完毕，在同目录查找表格文件')
wb.save('品格养成.xlsx')

'''
#csv储存
import requests
from lxml import etree
import re
import csv

def get_page(key):
    for page in range(1,5):
        url = 'http://search.dangdang.com/?key=%C6%B7%B8%F1%D1%F8%B3%C9&act=input&sort_type=sort_score_desc&page_index='+str(page+1)+'#J_tab'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = requests.get(url = url,headers = headers)
        parse_page(response)
        print('page %s over!!!' % page)

def parse_page(response):
    tree = etree.HTML(response.text)
    li_list = tree.xpath('//ul[@class="bigimg"]/li')
    # print(len(li_list))  # 测试
    for li in li_list:
        data = []
        try:
            # 获取书的标题,并添加到列表中
            title = li.xpath('./a/@title')[0].strip()
            data.append(title)
            # 获取商品链接,并添加到列表中
            commodity_url = li.xpath('./p[@class="name"]/a/@href')[0]
            data.append(commodity_url)
            # 获取价格,并添加到列表中
            price = li.xpath('./p[@class="price"]/span[1]/text()')[0]
            data.append(price)
            # 获取作者,并添加到列表中
            author = ''.join(li.xpath('./p[@class="search_book_author"]/span[1]//text()')).strip()
            data.append(author)
            # 获取出版时间,并添加到列表中
            time = li.xpath('./p[@class="search_book_author"]/span[2]/text()')[0]
            pub_time = re.sub('/','',time).strip()
            data.append(pub_time)
            commodity_detail = ''
            #获取出版社
            publis = ''.join(li.xpath('./p[@class="search_book_author"]/span[3]//text()')).strip()
            data.append(publis)

        except:
            pass
        save_data(data)

def save_data(data):
    writer.writerow(data)


def main():
    key = '品格养成'  # input('Please input key:')
    get_page(key)

fp = open('品格养成.csv','w',encoding = 'utf-8-sig',newline = '')
writer = csv.writer(fp)
header = ['书名','链接','价格','作者','出版时间','出版社']
writer.writerow(header)
main()
fp.close()
'''
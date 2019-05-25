import requests
from lxml import etree
from useragent import UA
import pymysql
import time

used = []

def main():

    html = requests.get(url='http://www.goubanjia.com/', headers=UA, timeout=3)

    data = etree.HTML(html.text)

    tr = data.xpath('//tbody/tr')

    ip_list = []

    for td in tr:
        ip = ''
        isgaomi = td.xpath('td[2]/a/text()')[0]
        if isgaomi == '高匿':
            ip_temp = td.xpath('td[@class="ip"]//*[not(@style="display:none;")and(not(@style="display: none;"))and(not(not(text())))and(not(contains(@class,"port")))]/text()')
            for i in ip_temp:
                ip += i

            ip_list.append(ip)

    checkIP(ip_list, ':80')
    time.sleep(15)

def checkIP(ip_list, port):
    db = connect_db()

    for ip in ip_list:
        try:
            res = requests.get(url='http://ip.tool.chinaz.com/', headers=UA, proxies={'http':str(ip+port)}, timeout=3)
            if res.status_code == 200:
                html = etree.HTML(res.text)
                try:
                    ret_ip = html.xpath('//dl[@class="IpMRig-tit"]/dd[@class="fz24"]//text()')[0]
                    ret_pos = html.xpath('//dl[@class="IpMRig-tit"]/dd[2]//text()')[0]
                    db.insertData(ip=str(ret_ip), pos=str(ret_pos))
                except:
                    print('--fail--')
        except:
            print('fail')

class connect_db():

    def __init__(self):
        self.conn = pymysql.connect(host='192.168.2.170', user='root', password='123456', port=3306, charset='utf8', database='ips')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from ip_table')

    def insertData(self, pos, ip):
        print(pos, ip)
        sql = 'insert into ip_table (pos, ip) value ("%s", "%s")' % (pos, ip)
        self.cur.execute(sql)

    def getIp(self):
        data =  self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return data

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':

    main()
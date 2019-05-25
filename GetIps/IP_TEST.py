import requests
import json
import pymysql
def main():

    conn = pymysql.connect(user='root', password='123456', host='localhost', charset='utf8', database='ips', port=3306)

    cur = conn.cursor()

    cur.execute('select * from ip_table')

    file = open('ip.json', 'r', encoding='utf-8')

    ip_data = json.load(file)

    proxies = {}

    ua = {
        'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    sql = 'insert into ip_table (types, ip) value ("%s", "%s")'
    for i in ip_data:
        proxies[i['type']] = i['type'] +'://'+ i['ip'] + ':' + i['port']
        h = requests.get(url='https://www.baidu.com', headers=ua, proxies=proxies, timeout=3)

        if h.status_code == 200:
            print('%s:%s is success' % (i['type'], i['type'] +'://'+ i['ip'] + ':' + i['port']))
            cur.execute(sql % (i['type'], i['type'] +'://'+ i['ip'] + ':' + i['port']))
        else:
            print('%s:%s is fail' % (i['type'], i['type'] + '://' + i['ip'] + ':' + i['port']))

    conn.commit()
    cur.close()
    conn.close()
if __name__ == '__main__':
    main()
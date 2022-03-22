from requests_html import HTMLSession
import requests
import os

barkKey = str(os.environ['BARKKEY'])
session = HTMLSession()
header = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
url = "https://billing.virmach.com/index.php?rp=/store/special-offers"
req = session.get(url=url, headers=header)
# 取得产品名 product1 = Ryzen Special 384
product = req.html.xpath("//div[@id='product1']/header/span[@id='product1-name']/text()")[0]
# 取得产品余量
qty = req.html.xpath("//div[@id='product1']/header/span[@class='qty']/text()")[0]

if int(qty.split(' ')[0]) !=0:
    # bark 推送
    title = 'Vir 监控'
    body = product +' 补货了\n' + qty
    if barkKey !=' ':
        barkUrl = 'https://api.day.app/'+barkKey
        requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
    else:
        print('BARKKEY 未填写')
    print(body)
else:
    print('未补货')

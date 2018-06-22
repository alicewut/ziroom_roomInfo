import requests
from lxml import etree
from downloader import getProxyies, downloadFunc
from urllib import request
import time
import json

def main():
	base_url = 'http://www.ziroom.com/z/nl/z3.html?p={}'
	for i in range(1,51):
		full_url = base_url.format(i)
		proxy_list = getProxyies()
		rooms_info_html = downloadFunc(url=full_url,proxies=proxy_list)
		rooms_info_obj = etree.HTML(rooms_info_html)
		rooms_link_list = rooms_info_obj.xpath('//ul[@id="houseList"]/li[@class="clearfix"]/div[@class="txt"]/h3/a/@href')
		for room_link_url in rooms_link_list:
			try:
				room_link_url = "http:"+room_link_url
				print(room_link_url)
				room_info_html = downloadFunc(url=room_link_url,proxies=proxy_list)
				room_info_obj = etree.HTML(room_info_html)

				# 房屋标题：
				room_title = room_info_obj.xpath('//div[@class="room_name"]/h2/text()')[0]
				room_title = room_title.replace(' ','').replace('\n','')
				# 房屋地址：
				room_address = room_info_obj.xpath('//div[@class="room_name"]/p/span[@class="ellipsis"]/text()')[0]
				room_address = room_address.replace(" ","").replace("\n","")
				# 租金：
				room_rant = room_info_obj.xpath('//div[@class="room_name"]/p/span[@class="price"]/span[@id="room_price"]/text()')[0]
				# 租金方式：
				room_rant_moneyway = room_info_obj.xpath('//div[@class="room_name"]/p/span[@class="price"]/span[@class="gray-6"]/text()')[0]
				room_rant_moneyway = room_rant_moneyway.split('(')[-1].rstrip(')')
				# 住房面积
				room_area = room_info_obj.xpath('//ul[@class="detail_room"]/li[1]/text()')[0]
				room_area = room_area.replace(' ','').replace('\n','')
				# 住房朝向
				room_direct = room_info_obj.xpath('//ul[@class="detail_room"]/li[2]/text()')[0]
				# 户型
				room_style = room_info_obj.xpath('//ul[@class="detail_room"]/li[3]/text()')[0]
				room_style = room_style.replace(' ', '').replace('\n', '')
				# 楼层
				room_floor = room_info_obj.xpath('//ul[@class="detail_room"]/li[4]/text()')[0]
				# 房间照片
				room_img_list = room_info_obj.xpath('//div[@id="bigPhotShow"]//ul[@class="lof-main-wapper"]/li/a/img/@src')
				finallpath = ''
				for room_img in room_img_list:
					filepath = './ziru_img/'+room_img.split('/')[-1]
					request.urlretrieve(room_img, filepath)
					finallpath += "'"+filepath+"'"+','
				finallpath = finallpath.rstrip(',')

				detail = {
						"room_title": room_title,
						"room_address": room_address,
						"room_rant": room_rant,
						"room_rant_moneyway": room_rant_moneyway,
						"room_area": room_area,
						"room_direct": room_direct,
						"room_style": room_style,
						"room_floor": room_floor,
						"finallpath": finallpath
				}
				detail = json.dumps(detail, ensure_ascii=False)
				detail = detail + ',\n'
				with open('./ziruinfo.json', 'a', encoding='utf8') as f:
					f.write(detail)


				print("===========end============")
				time.sleep(10)
			except Exception as e:
				continue



if __name__ == '__main__':
    main()




import requests
import random
import time

def getProxyies():
	with open('./proxies.txt','r') as f:
		proxies = f.readlines()
	proxy = {

	}
	proxies_list = []
	for i in proxies:
		clear_url = i.split('\n')[0]
		proxy = {
			'http':clear_url,
			'https':clear_url
		}
		proxies_list.append(proxy)
	return proxies_list

def downloadFunc(url,proxies=None,timeout=5,retrytimes=5):
	header = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
	}
	# 使用代理
	if proxies:
		proxy = random.choice(proxies)
		try:
			response = requests.get(url=url,headers=header,proxies=proxy,timeout=timeout)
			response.encoding = response.apparent_encoding
			html = response.text
			return html
		except Exception as f:
			html = None
			if retrytimes>0:
				time.sleep(2)
				html = downloadFunc(url, proxies=None, timeout=5, retrytimes=retrytimes-1)
			return html
	# 不使用代理
	else:
		try:
			response = requests.get(url=url, headers=header)
			response.encoding = response.apparent_encoding
			html = response.text
			return html
		except Exception as e:
			html = None
			if retrytimes > 0:
				time.sleep(2)
				html = downloadFunc(url, proxies=None, timeout=5, retrytimes=retrytimes - 1)
			return html


if __name__ == '__main__':
	# getProxyies()
	# proxylist = [{'http': 'http://61.158.187.157:8080', 'https': 'http://61.158.187.157:8080'}, {'http': 'http://120.26.110.59:8080', 'https': 'http://120.26.110.59:8080'}, {'http': 'http://113.200.159.155:9999', 'https': 'http://113.200.159.155:9999'}, {'http': 'http://122.72.18.34:80', 'https': 'http://122.72.18.34:80'}, {'http': 'http://139.224.80.139:3128', 'https': 'http://139.224.80.139:3128'}, {'http': 'http://114.215.95.188:3128', 'https': 'http://114.215.95.188:3128'}, {'http': 'http://101.37.79.125:3128', 'https': 'http://101.37.79.125:3128'}, {'http': 'http://1.119.193.36:8080', 'https': 'http://1.119.193.36:8080'}, {'http': 'http://221.219.98.62:6666', 'https': 'http://221.219.98.62:6666'}, {'http': 'http://113.195.10.4:53281', 'https': 'http://113.195.10.4:53281'}, {'http': 'http://124.237.83.14:53281', 'https': 'http://124.237.83.14:53281'}, {'http': 'http://183.141.144.233:9000', 'https': 'http://183.141.144.233:9000'}]
	# print(downloadFunc(url='http://www.baidu.com/s?wd=ip', proxies=proxylist,timeout=5,retrytimes=5))
	print(downloadFunc(url='http://www.baidu.com/s?wd=ip'))



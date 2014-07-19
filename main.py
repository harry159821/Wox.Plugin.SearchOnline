#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json,sys,re
import webbrowser
true = True
null = None
false = False

def query(Allkey):
	Allkey = Allkey.encode('utf-8')
	key = Allkey.split(" ")[1]
	if not key:
		return ""
	results = []		
	if not Allkey.endswith(' '):	
		preKeyUrl = 'http://suggestion.baidu.com/su?json=1&zxmode=1&wd='+key
		html = requests(preKeyUrl).decode('gbk').encode('utf-8')
		html = json.loads(html[17:-2])
		if not html:
			return ''
		if html.has_key('tzx'):
			res = {}
			res["Title"] = html['tzx']['info']['site']
			res["SubTitle"] = html['tzx']['info']['showurl']
			res["ActionName"] = "openUrl"
			if(download(html['tzx']['info']['iconurl'],sys.path[0]+'\\'+key+'.png')):
				res["IcoPath"] = sys.path[0]+'\\'+key+'.png'
			else:
				res["IcoPath"] = "./icon.png"
			res["ActionPara"] = html['tzx']['info']['siteurl']
			results.append(res)
		for i in html['s']:
			res = {}
			res["Title"] = i
			res["IcoPath"] = "./baidu.png"
			results.append(res)
		return json.dumps(results)
	else:
		url = 'http://wap.baidu.com/s?word='+key
		html = requests(url)
		if not html:
			return ''		
		html = html.replace('<em>','')
		html = html.replace('</em>','')	
		html = html.replace('&#160;','')
		data = re.findall(r'''(resitem"([\w\W]*?)abs([\w\W]*?)</div>).*?''',html)
		for item in data:
			res = {}
			result = re.findall(r'''(href="([\w\W]*?)">([\w\W]*?)</a><div class="abs">([\w\W]*?)<br /><span class="site">([\w\W]*?)</span>([\w\W]*?)date">([\w\W]*?)</span>).*?''',item[0])
			if result:
				try:
					res["Title"] = result[0][2]
					res["SubTitle"] = result[0][3]
					res["ActionName"] = "openUrl2"
					res["IcoPath"] = "./icon.png"
					res["ActionPara"] = 'http://wap.baidu.com'+result[0][1].replace('amp;','')
					results.append(res)
				except Exception, e:
					print e			
		return json.dumps(results)

def requests(url,timeouts=4):
	header = {
			'Referer': 'http://www.baidu.com/',
			'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			}	
	request = urllib2.Request(url,headers=header)
	response = urllib2.urlopen(request,timeout=timeouts)
	html = response.read()
	if html:	
		return html
	return False

def getRealUrl(url):
	url = url.replace('amp;','')
	header = {
			'Referer': 'http://wap.baidu.com/',
			'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			}	
	request = urllib2.Request(url,headers=header)	
	html = urllib2.urlopen(request,timeout=8).read()	
	result = re.findall(r'''(url=([\w\W]*?)">原网页).*?''',html)
	if result:
		return result[0][1]
	return url


def download(url,path):
	File = requests(url)
	if not File:
		return False
	FILE = open(path,'wb')
	FILE.write(File)
	FILE.close()
	return True

def openUrl(context,url):
	webbrowser.open(url)

def openUrl2(context,url):
	webbrowser.open(getRealUrl(url))

if __name__ == '__main__':
	#print query(u"search xiami ")
	print getRealUrl("http://wap.baidu.com/ssid=0/from=0/bd_page_type=1/uid=0/baiduid=45075F32CD2672D6989AD5727F9582B4/pu=sz%40224_220%2Cta%40middle____/baiduid=45075F32CD2672D6989AD5727F9582B4/w=0_10_xiami/t=wap/l=0/tc?ref=www_colorful&lid=5167244119924064437&order=9&vit=osres&tj=www_normal_9_0_10&sec=40091&di=8099560a9bcc75e7&bdenc=1&nsrc=IlPT2AEptyoA_yixCFOxXnANedT62v3IHti2LC6N_8SxokDyqRLuFM2bXCP7Lny")

# 程序功能: 按关键字爬取微博清单
# 原创作者: 马哥python说

import os
import re  # 正则表达式提取文本
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用
import time
import random

# 请求头
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"cookie": "替换为自己的m端微博cookie"
}


def trans_time(v_str):
	"""转换GMT时间为标准格式"""
	GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
	timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
	ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
	return ret_time


def getLongText(v_id):
	"""爬取长微博全文"""
	# 请求头
	try:
		url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
		r = requests.get(url, headers=headers)
		json_data = r.json()
		long_text = json_data['data']['longTextContent']
		# print('long_text0:')
		# print(long_text)
		time.sleep(random.uniform(1, 2))
		# 微博内容-正则表达式数据清洗
		dr = re.compile(r'<[^>]+>', re.S)
		long_text2 = dr.sub('', long_text)
		return long_text2
	except Exception as e:
		print('getLongText ERR:', str(e))
		return ''


def get_weibo_list(v_keyword, v_max_page):
	"""
	爬取微博内容列表
	:param v_keyword: 搜索关键字
	:param v_max_page: 爬取前几页
	:return: None
	"""
	for page in range(1, v_max_page + 1):
		print('\n===开始爬取[{}]第[{}]页微博==='.format(v_keyword, page))
		time.sleep(random.uniform(1, 2))
		# 请求地址
		url = 'https://m.weibo.cn/api/container/getIndex'
		# 请求参数
		params = {
			"containerid": "100103type=1&q={}".format(v_keyword),
			"page_type": "searchall",
			"page": page
		}
		# 发送请求
		r = requests.get(url, headers=headers, params=params)
		print('响应码：', r.status_code)
		# print(r.json())
		# 解析json数据
		try:
			cards = r.json()["data"]["cards"]
		except:
			cards = []
		print('本页帖子数量:', len(cards))
		# print(cards)
		text2_list = []
		time_list = []
		author_list = []
		id_list = []
		reposts_count_list = []
		comments_count_list = []
		attitudes_count_list = []
		region_name_list = []
		status_city_list = []
		status_province_list = []
		status_country_list = []
		for card in cards:
			if str(card['card_type']) != '11':  # 非正常数据跳过
				continue
			# 如果没有正常的 mblog 数据，跳过该条卡片，避免写入空行
			try:
				card['card_group'][0]['mblog']
			except Exception:
				continue
			# 微博id
			try:
				id2 = card['card_group'][0]['mblog']['id']
				id_list.append(id2)
			except:
				id_list.append('')
			# 微博内容
			try:
				text  = card['card_group'][0]['mblog']['text']
				dr = re.compile(r'<[^>]+>', re.S)
				text2 = dr.sub('', text)
				isLongText = card['card_group'][0]['mblog']['isLongText']
				if isLongText:
					print('请求全文展开: {}'.format(id2))
					long_text = getLongText(id2)
					text2_list.append(long_text)
				else:
					text2_list.append(text2)
			except Exception as e:
				print('微博内容ERR:')
				print(str(e))
				text2_list.append('')
			# 微博创建时间
			try:
				time2 = card['card_group'][0]['mblog']['created_at']
				time2 = trans_time(time2)
				time_list.append(time2)
			except:
				time_list.append('')
			# 微博作者
			try:
				author = card['card_group'][0]['mblog']['user']['screen_name']
				author_list.append(author)
			except:
				author_list.append('')
			# 转发数
			try:
				reposts_count = card['card_group'][0]['mblog']['reposts_count']
				reposts_count_list.append(reposts_count)
			except:
				reposts_count_list.append('')
			# 评论数
			try:
				comments_count = card['card_group'][0]['mblog']['comments_count']
				comments_count_list.append(comments_count)
			except:
				comments_count_list.append('')
			# 点赞数
			try:
				attitudes_count = card['card_group'][0]['mblog']['attitudes_count']
				attitudes_count_list.append(attitudes_count)
			except:
				attitudes_count_list.append('')
			# 发布于
			try:
				region_name = card['card_group'][0]['mblog']['region_name']
				region_name_list.append(region_name)
			except:
				region_name_list.append('')
			# ip属地_城市
			try:
				status_city = card['card_group'][0]['mblog']['status_city']
				status_city_list.append(status_city)
			except:
				status_city_list.append('')
			# ip属地_省份
			try:
				status_province = card['card_group'][0]['mblog']['status_province']
				status_province_list.append(status_province)
			except:
				status_province_list.append('')
			#ip属地_国家
			try:
				status_country = card['card_group'][0]['mblog']['status_country']
				status_country_list.append(status_country)
			except:
				status_country_list.append('')

		# print(len(id_list))
		# print(len(author_list))
		# print(len(time_list))
		# print(len(text2_list))
		# print(len(reposts_count_list))
		# print(len(comments_count_list))
		# print(len(attitudes_count_list))
		# print(len(region_name_list))
		# print(len(status_city_list))
		# print(len(status_province_list))
		# print(len(status_country_list))

		# 把列表数据保存成DataFrame数据
		df = pd.DataFrame(
			{
				'页码': page,
				'微博id': id_list,
				'微博作者': author_list,
				'发布时间': time_list,
				'微博内容': text2_list,
				'转发数': reposts_count_list,
				'评论数': comments_count_list,
				'点赞数': attitudes_count_list,
				'发布于': region_name_list,
				'ip属地_城市': status_city_list,
				'ip属地_省份': status_province_list,
				'ip属地_国家': status_country_list,
			}
		)
		# 表头
		if os.path.exists(v_weibo_file):
			header = False
		else:
			header = True
		# 保存到csv文件
		df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
		print('csv保存成功:{}'.format(v_weibo_file))


if __name__ == '__main__':
	# 爬取前几页
	max_search_page = 5  # 爬前n页
	# 爬取关键字
	search_keyword = '小龙虾'
	# 保存文件名
	v_weibo_file = '微博清单_{}_前{}页.csv'.format(search_keyword, max_search_page)
	# 如果csv文件存在，先删除之
	if os.path.exists(v_weibo_file):
		os.remove(v_weibo_file)
		print('微博清单存在，已删除: {}'.format(v_weibo_file))
	# 调用爬取微博函数
	get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)
	# 数据清洗-去重
	df = pd.read_csv(v_weibo_file)
	# 删除重复数据
	df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
	# 再次保存csv文件
	df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
	print('数据清洗去重完成')

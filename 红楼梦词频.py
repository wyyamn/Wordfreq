# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:13:09 2020

@author: natuk
"""

'''
中文小说《红楼梦》的词频分析
统计人名“共现”情况
'''

import jieba
import jieba.posseg as pseg
import time

#import os
#import sys

txt_filename = "红楼梦.txt"

#打开文件和异常处理       
flag = False  # 标记文件是否打开成功
try_num = 5  # 设置尝试次数

while flag == False and try_num > 0:
    try:
        text_file = open(txt_filename, 'r', encoding='utf-8')
        print('文件打开成功')
    except:
        print('文件打开失败！！！')
        flag = False
        print('3秒钟后继续尝试……（还剩' + str(try_num) + '次）')
        time.sleep(3)
        try_num = try_num - 1
    else:
        print('未发生异常，已关闭文件')
        flag = True

if flag:
    text_file.close()
    print('已关闭文件')
else:
    print('没有已打开的文件')
    
print('完成打开文件，接下来读取文字')

#输入小说
content = text_file.readlines()
#for line in content:
#    print(line)
text_file.close()

print("完成读取文字，接下来分析关键字")

#自动创建输出文件
link_file_name = 'hlm_人物连接.csv'
node_file_name = 'hlm_人物节点.csv'

#测试打开输出文件
test = open(link_file_name, 'w')
test.close()
test = open(node_file_name, 'w')
test.close()

print('好了')

# ---第1步：词频分析

# 加载用户字典
jieba.load_userdict('红楼梦自定义词典.txt') #这个需要手动创建文件


#生成基础数据（一个列表，一个字典）
line_name_list = []  # 每个段落出现的人物列表
name_cnt_dict = {}  # 统计人物出现次数

#忽略词表
ignore_list = ['分节阅读', '施礼', '花柳','那僧笑','那玉','闻世','莫如','须眉','贺喜','和尚','通灵宝玉','金陵','荣华',
               '祖德','那丫头','从小儿','寿星','别信','子孙','贾府中','荣耀','冷笑','甄府','金刚','贾家','言语','宝贝',
               '田庄','恩赐','斯文','古董','云雨','桂花','隆恩','加恩','科第','荣府','陈设','杜撰','何曾','斯斯文文',
               '寻思','','胡闹','何必当初','巧遇','冷汗','翠墨','任凭','白操','子石','爱慕','张嘴','宁荣','贾府','盘桓',
               '谢恩','薛家','安富尊荣','宁府','宁府中','呼唤','道谢','明言','华丽','钱粮','母笑','天亮','鬼混','齐备',
               '藏躲','宁可','王夫','浮萍','有凤来仪','封锁','刁钻','那傅','安神','蒙圣恩','伏侍贾','宝鼎','张罗','都还没',
               '努嘴儿','天香楼','通灵玉','古人云','花香','钮子','别提','庄子','亦且','舍不得你','寿礼','关了门','宝贝儿',
               '老虎','齐声','清虚观','通今博古','迎宾','阴司里','香甜','和睦','洛神','孔雀','麻黄','玉石','盘金彩',
               '明白人','谢礼','安静','胡思','红香圃','柳絮','夏家','香熏','老东西','花梨','山子石','小学生',
               '帕子','那宝','比一比','那五儿','但凡','西风','柳枝','明白','老婆子','小丫头']

print('正在分段统计……')

# 用于计算进度条
progress = 0

for line in content: # 逐个段落循环处理
    word_gen = pseg.cut(line) # peseg.cut返回分词结果，“生成器”类型
    line_name_list.append([])
    
    for one in word_gen:
        word = one.word
        flag = one.flag
        
        if len(word) == 1:  # 跳过单字词
            continue
        
        if word in ignore_list:  # 跳过标记忽略的人名 
            continue
        
        # 对指代同一人物的名词进行合并
        if word == '宝二爷' or word == '怡红公子' or word == '绛洞花主' or word == '二哥哥' or word == '天魔星' \
                    or word == '宝玉':
            word = '贾宝玉'
        elif word == '颦颦' or word == '颦儿' or word == '林姑娘' or word == '林妹妹' or word == '潇湘妃子' \
                    or word == '黛玉':
            word = '林黛玉'
        elif word == '史太君' or word == '老太太' or word == '老祖宗' or word == '贾母说' or word == '贾母到' \
                    or word == '贾母笑':
            word = '贾母'
        elif word == '凤姐' or word == '琏二奶奶' or word == '凤辣子' or word == '凤哥儿' or word == '凤丫头' \
                    or word == '凤姐儿' or word == '熙凤':
            word = '王熙凤'
        elif word == '蘅芜君' or word == '宝姐姐' or word == '宝丫头' or word == '宝姑娘' or word == '宝钗':
            word = '薛宝钗'
        elif word == '贾政道' or word == '贾政说' or word == '贾政听' or word == '贾政笑':
            word == '贾政'
            
        if flag == 'nr': 
            line_name_list[-1].append(word) #把人名字放到list里
            if word in name_cnt_dict.keys():
                name_cnt_dict[word] = name_cnt_dict[word] + 1
            else:
                name_cnt_dict[word] = 1
                

        progress += 1
        print('\r' + '已处理' + str((progress/(len(content)*3.7))*100) + '%', end= '')

# 循环结束点        
print()
print('基础数据处理完成')
            

# 字典转成列表，按出现次数排序          
item_list = list(name_cnt_dict.items())
item_list.sort(key=lambda x:x[1], reverse=True) 

total_num = len(item_list)
print('经统计，共有' + str(total_num) + '个不同的人物')

num = input('您想查看前多少个人物？:')
if not num.isdigit() or num == '':
    num = 10
else:
    num = int(num)

result_filename = 'hlm_wordfreq.csv'
result_file = open(result_filename, 'w', encoding='gbk')   
result_file.write('人物,出现次数\n')
for i in range(num):
    word, cnt = item_list[i]
    message = str(i+1) + '. ' + word + '\t' + str(cnt)
    print(message)
    result_file.write(word + ',' + str(cnt) + '\n')
result_file.close()

print('已写入文件：' + result_filename)

##--- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}

# 只统计出现次数达到限制数的人名
name_cnt_limit = 100  

for line_name in line_name_list:
    for name1 in line_name:
        # 判断该人物name1是否在字典中
        if name1 in relation_dict.keys():
            pass  # 如果已经在字典中，继续后面的统计工作
        elif name_cnt_dict[name1] >= name_cnt_limit:  # 只统计出现较多的人物
            relation_dict[name1] = {}  # 添加到字典
            #print('add ' + name1)  # 测试点
        else:  # 跳过出现次数较少的人物
            continue
        
        # 统计name1与本段的所有人名（除了name1自身）的共现数量
        for name2 in line_name:
            if name2 == name1 or name_cnt_dict[name2] < name_cnt_limit:  
            # 不统计name1自身；不统计出现较少的人物
                continue
            
            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

print('共现统计完成，仅统计出现次数达到' + str(name_cnt_limit) + '及以上的人物')

## 导出节点文件
node_file = open(node_file_name, 'w', encoding='gbk') 
# 节点文件，格式：Name,Weight -> 人名,出现次数
node_file.write('Name,Weight\n')
node_cnt = 0  # 累计写入文件的节点数量
for name,cnt in item_list: 
    if cnt >= name_cnt_limit:  # 只输出出现较多的人物
        node_file.write(name + ',' + str(cnt) + '\n')
        node_cnt = node_cnt + 1
node_file.close()
print('人物数量：' + str(node_cnt))
print('已写入文件：' + node_file_name)

## 导出连接文件
# 共现数可以看做是连接的权重，只导出权重达到限制数的连接
link_cnt_limit = 10  
print('只导出数量达到' + str(link_cnt_limit) + '及以上的连接')

link_file = open(link_file_name, 'w', encoding='gbk')
# 连接文件，格式：Source,Target,Weight -> 人名1,人名2,共现数量
link_file.write('Source,Target,Weight\n')
link_cnt = 0  # 累计写入文件的连接数量
for name1,link_dict in relation_dict.items():
    for name2,link in link_dict.items():
        if link >= link_cnt_limit:  # 只输出权重较大的连接
            link_file.write(name1 + ',' + name2 + ',' + str(link) + '\n')
            link_cnt = link_cnt + 1
link_file.close()
print('连接数量：' + str(link_cnt))
print('已写入文件：' + link_file_name)  


#--- 第3步：根据共现表绘制人物关系图 
out_file_name = '关系图-红楼梦人物.html'

##--- 从文件读入节点和连接信息
node_file = open(node_file_name, 'r', encoding='gbk')
node_line_list = node_file.readlines()
node_file.close()
del node_line_list[0]  # 删除标题行

link_file = open(link_file_name, 'r', encoding='gbk')
link_line_list = link_file.readlines()
link_file.close()
del link_line_list[0]  # 删除标题行


from pyecharts import options as opts
from pyecharts.charts import Graph

##--- 解析读入的信息，存入列表
node_in_graph = []
for one_line in node_line_list:
    one_line = one_line.strip('\n')
    one_line_list = one_line.split(',')
    #print(one_line_list)  # 测试点
    node_in_graph.append(opts.GraphNode(
            name=one_line_list[0], 
            value=int(one_line_list[1]), 
            symbol_size=int(one_line_list[1])/20))  # 手动调整节点的尺寸
#print('-'*20)  # 测试点
link_in_graph = []
for one_line in link_line_list:
    one_line = one_line.strip('\n')
    one_line_list = one_line.split(',')
    print(one_line_list)  # 测试点
    link_in_graph.append(opts.GraphLink(
            source=one_line_list[0], 
            target=one_line_list[1], 
            value=int(one_line_list[2])))


##--- 画图
c = Graph()
c.add("", 
      node_in_graph, 
      link_in_graph, 
      edge_length=[10,50], 
      repulsion=5000,
      layout="force",  # "force"-力引导布局，"circular"-环形布局
      )
c.set_global_opts(title_opts=opts.TitleOpts(title="关系图-红楼梦人物"))
c.render(out_file_name)

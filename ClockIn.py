###############################################################
# 江西高校支付宝校园防疫自动签到程序
###############################################################
# @Author JetXi
# @Create 2021-02-21
# @Email  ShengJieXi233@gmail.com
###############################################################
# 请仔细阅读代码注释，修改必要的部分后直接运行即可
# 请在使用程序前仔细阅读代码注释，请不要将此程序用于学习交流以外的任何用途，否则由此引发的一切后果由使用者本人承担。
# 可以在Windows设定计划任务定时执行，也可在Linux使用crontab定时执行
###############################################################


import requests
import json

### 按照自己的实际情况配置以下数据即可
### 配置省市区时，不要只写省市区的名称，应写作：江西省 南昌市 红谷滩区
### 具体地址应与经纬度的转换结果基本一致，经纬度可由在线坐标拾取系统查询
### 默认为健康 非毕业生，若需更改这些参数，请修改signin函数中的data变量
uCode = ''            # 学校代码 README.md可查
stuID = ''            # 学号
province = ''         # 省
city = ''             # 市
county = ''           # 区/县
street = ''           # 具体地址
longitude = 0         # 经度
latitude = 0          # 纬度

# 登录页面，提交学校代码和学号，用于获取cookie，直接get请求
loginurl = f'https://fxgl.jx.edu.cn/{uCode}/public/homeQd?loginName={stuID}&loginType=0'
# 签到页面，需要使用cookie登录，post一系列参数实现签到
signinurl = f'https://fxgl.jx.edu.cn/{uCode}/studentQd/saveStu'

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'
}

# 签到函数
# 作用：将用户填写的参数post至签到api完成签到
def signin():
    # 使用session会话保持技术，可跨请求保留cookie
    session = requests.session()
    # 访问登陆界面，获取到用户的cookie，保持于session会话中
    session.get(loginurl, headers=headers)
    # 需要post的数据
    data = {
        'province':province,    # 省份
        'city':city,            # 市
        'district':county,      # 区/县
        'street':street,        # 具体地址
        'xszt':0,
        'jkzk':0,               # 健康状况 0:健康 1:异常
        'jkzkxq':'',            # 异常原因
        'sfgl':1,               # 是否隔离 0:隔离 1:未隔离
        'gldd':'',
        'mqtw':0,
        'mqtwxq':'',
        'zddlwz':province+city+county,    # 省市区
        'sddlwz':'',
        'bprovince':province,
        'bcity':city,
        'bdistrict':county,
        'bstreet':street,
        'sprovince':province,
        'scity':city,
        'sdistrict':county,
        'lng':longitude,          # 经度
        'lat':latitude,           # 纬度
        'sfby':1                  # 是否为毕业生 0:是 1:否
    }
    result = session.post(url=signinurl, data=data, headers=headers).text
    # 访问接口返回的数据是json字符串，使用loads方法转换为python字典
    statusCode = json.loads(result)['code']
    # 根据状态码判断签到状态
    if statusCode == 1001: print("签到成功")
    elif statusCode == 1002: print("今日已签")
    else: print("签到状态异常，请尝试重新运行程序")



if __name__ == '__main__':
    signin()

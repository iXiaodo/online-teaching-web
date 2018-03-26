# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-3-26   

#日期：上午12:46   

#：IDE：PyCharm
import string
import random


def get_captcha(number):
    source = list(string.letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source,number))  # number是生成验证码的位数


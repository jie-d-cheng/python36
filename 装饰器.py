#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2018/7/26 10:49
# Version: 0.1
# __author__: Jie Cheng D <jie.d.cheng@outlook.com>


def outer(func):
    def inner(*args, **kwargs):
        print("{} function starts running here.".format(func.__name__))
        func(*args,**kwargs)
        print("{} function finished here.".format(func.__name__))
    return inner

@outer
def inner(a, b):
    print("{} + {} = {}".format(a,b,a+b))

inner(9,8)


@outer
def blade():
    print("I don't know who I am...")

blade()
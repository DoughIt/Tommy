#!/usr/bin/env python3
# -*- utf-8 -*-


import random
import functools


def _check_value(value):
    """返回一个有效状态值"""
    if value < 0:
        return 0
    elif value > 100:
        return 100
    else:
        return value


def _log(func):
    """输出猫咪当前状态"""

    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        res = func(self, *args, **kw)
        print(self.STATUSES[self.get_status()])
        return res

    return wrapper


class Cat(object):
    WALK, PLAY, FEED, SEEDOCTOR, SLEEP, WAKING = "WALK", "PLAY", "FEED", "SEEDOCTOR", "SLEEP", "WAKING"
    NAME, STATUS, HAPPINESS, HUNGRY, HEALTH = "NAME", "STATUS", "HAPPINESS", "HUNGRY", "HEALTH"
    STATUSES = {
        WALK: "我在散步……",
        PLAY: "我在玩耍……",
        FEED: "我在吃饭……",
        SEEDOCTOR: "我在看医生……",
        SLEEP: "我在睡觉……",
        WAKING: "我醒着但很无聊……"
    }

    def __init__(self, name="Tommy", status=SLEEP, hungry=random.randint(0, 100), happy=random.randint(0, 100),
                 health=random.randint(0, 100)):
        self.__status = status
        self.__name = name
        self.__hungry = hungry
        self.__happy = happy
        self.__health = health

    def reload(self, name, status, hungry, happy, health):
        self.__init__(name, status, hungry, happy, health)

    def __set_hungry(self, hungry):
        self.__hungry = _check_value(hungry)

    def __set_happy(self, happy):
        self.__happy = _check_value(happy)

    def __set_health(self, health):
        self.__health = _check_value(health)

    def __set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def unhappy(self):
        """如果在睡觉状态， 你要带它去活动， 需要提醒，如果你坚持要带它去活动，幸福指数将减去 4。"""
        self.__set_happy(self.__happy - 4)

    def update(self, hours):
        """更新状态及状态值"""
        if self.__status == Cat.WAKING:  # 在醒着，什么事都不做的情况下，每个滴答，饥饿指数增加 2，幸福指数减少 1
            self.__set_hungry(self.__hungry + 2)
            self.__set_happy(self.__happy - 1)
        elif self.__status == Cat.SLEEP:  # 在睡着状态，每个滴答，饥饿指数增加 1
            self.__set_hungry(self.__hungry + 1)
        elif self.__status == Cat.WALK:  # 在陪它散步状态，每个滴答，饥饿指数增加 3, 健康指数加 1
            self.__set_hungry(self.__hungry + 3)
            self.__set_health(self.__health + 1)
        elif self.__status == Cat.PLAY:  # 在陪它玩耍状态，每个滴答，饥饿指数增加 3，幸福指数增加 1
            self.__set_hungry(self.__hungry + 3)
            self.__set_happy(self.__happy + 1)
        elif self.__status == Cat.FEED:  # 在喂食状态：每个滴答，饥饿指数则减少 3
            self.__set_hungry(self.__hungry - 3)
        elif self.__status == Cat.SEEDOCTOR:  # 带它去看医生，则每个滴答，健康指数将增加 4
            self.__set_health(self.__health + 4)

        if self.__hungry < 20 or self.__hungry > 80:  # 如果饥饿指数在大于 80，或低于 20 即过饱，则每个滴答，健康指数将减去 2
            self.__set_health(self.__health - 2)
        if self.__happy < 20:  # 如果幸福指数低于 20，则每个滴答，健康指数将减去 1
            self.__set_health(self.__health - 1)

        if hours == 0:  # 在0点开始睡觉
            self.__status = Cat.SLEEP  # 如果当前状态是“在睡觉中”，并且当前时间是8点，则醒来
        elif hours == 8 and self.__status == Cat.SLEEP:
            self.__status = Cat.WAKING

    @_log
    def play(self):
        self.__status = Cat.PLAY

    @_log
    def walk(self):
        self.__status = Cat.WALK

    @_log
    def feed(self):
        self.__status = Cat.FEED

    @_log
    def see_doctor(self):
        self.__status = Cat.SEEDOCTOR

    @_log
    def let_alone(self, hours):
        """根据当前的时刻（几点），它将返回醒着什么都不做，或者睡觉状态"""
        if 0 <= hours <= 8:
            self.__status = Cat.SLEEP
        else:
            self.__status = Cat.WAKING

    def get_msg(self):
        return {
            Cat.NAME: self.__name,
            Cat.STATUS: self.__status,
            Cat.HAPPINESS: self.__happy,
            Cat.HUNGRY: self.__hungry,
            Cat.HEALTH: self.__health
        }

    @staticmethod
    def bye():
        print("记得来找我！ Bye……")

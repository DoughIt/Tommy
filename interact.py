#!/usr/bin/env python3
# -*- utf-8 -*-


import threading
import time
import json
from cat import Cat

tommy = Cat()
HOURS = "HOURS"


def fun_timer():
    """计时器"""
    global timer, hours
    hours += 1
    if hours > 23:
        hours = 0
    tommy.update(hours)  # 每个滴答更新宠物猫状态值
    timer = threading.Timer(5.0, fun_timer)  # 5s执行一次fun_timer
    timer.start()


def init():
    """读档"""
    global hours
    config_file = None
    try:
        config_file = open("./config.json", "r")
        msg = json.load(config_file)
        hours = msg[HOURS]
        tommy.reload(msg[Cat.NAME], msg[Cat.STATUS], msg[Cat.HUNGRY], msg[Cat.HAPPINESS], msg[Cat.HEALTH])
        print("读档成功～")
    except IOError as e:    # 不存在存档，则初始化新宠物猫
        hours = 0
        tommy.set_name(input("我是机器猫Tommy，主人要帮我取个新名字么～： "))
    finally:
        if config_file:
            config_file.close()


def archive():
    """存档"""
    msg = tommy.get_msg()
    msg[HOURS] = hours
    with open("./config.json", "w") as config_file:
        json.dump(msg, config_file)
        print("存档成功～")


def print_help():
    """打印帮助信息"""
    print("Commands:", "1. walk: 散步", "2. play: 玩耍", "3. feed: 喂我", "4. seedoctor: 看医生", "5. letalone: 让我一个人",
          "6. status: 查看我的状态", "7. bye: 不想看见我", "8. help: 获取帮助信息", "……", sep="\n")


def print_status():
    """打印猫咪状态信息"""
    print("当前时间: %-2d点" % hours)
    msg = tommy.get_msg()
    print("%s%s" % ("我当前的状态:", tommy.STATUSES[msg[Cat.STATUS]]), sep="\t")
    s = "{:<10}{:>5}{:^52}{:<8}({:03d})\n" * 3
    print(s.format("Happiness", "Sad", ("*" * (msg[Cat.HAPPINESS] // 2) + "-" * ((100 - msg[Cat.HAPPINESS] + 1) // 2)),
                   "Happy", msg[Cat.HAPPINESS],
                   "Hungry", "Full", ("*" * (msg[Cat.HUNGRY] // 2) + "-" * ((100 - msg[Cat.HUNGRY] + 1) // 2)),
                   "Hungry", msg[Cat.HUNGRY],
                   "Health", "Sick", ("*" * (msg[Cat.HEALTH] // 2) + "-" * ((100 - msg[Cat.HEALTH] + 1) // 2)),
                   "Healthy", msg[Cat.HEALTH]))


def bye():
    """存档并关掉计时器"""
    tommy.bye()
    archive()
    timer.cancel()


COMMAND_HANDLES = {
    "walk": tommy.walk,
    "play": tommy.play,
    "feed": tommy.feed,
    "seedoctor": tommy.see_doctor,
    "letalone": tommy.let_alone,
    "status": print_status,
    "bye": bye,
    "help": print_help
}


def main():
    init()
    print("我的名字叫%s，一只可爱的猫咪……" % tommy.get_name(), "你可以和我一起散步，玩耍，你也需要给我好吃的东西，带我去看病，也可以让我发呆……")
    print_help()
    fun_timer()  # 启动计时器

    while True:
        command = input("\n你想: ")
        if command in ("walk", "play", "feed", "seedoctor"):
            if tommy.get_status() == "SLEEP":
                if input("你确定要吵醒我吗？我在睡觉，你要是坚持吵醒我，我会不高兴的！（y表示是/其他表示不是）: ") == "y":
                    tommy.unhappy()
                    COMMAND_HANDLES[command]()
            else:
                COMMAND_HANDLES[command]()
        elif command in ("status", "help"):
            COMMAND_HANDLES[command]()
        elif command == "bye":
            COMMAND_HANDLES[command]()
            break
        elif command == "letalone":
            COMMAND_HANDLES[command](hours)
        else:
            print("我不知道你在说什么")


if __name__ == '__main__':
    main()

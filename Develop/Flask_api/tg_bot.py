#-*-coding: utf-8-*-
# 创建时间: 2021/2/5

import telebot

TOKEN = '1693960412:AAEzPGakWSuqShcacJDxE849etNu-NAdrsA'
tb = telebot.TeleBot(TOKEN)
text = "我是第一个电报机器人通知"
tb.send_message(808721783, text)
# -*- coding: utf-8 -*-

import pyttsx3  # pip3 install pyttsx3
import datetime
import speech_recognition as sr  # pip3 install SpeechRecognition
import wikipedia  # pip3 install wikipedia
import smtplib
import webbrowser as wb
import psutil  # pip3 install psutil
import pyjokes  # pip3 install pyjokes
import os
import pyautogui  # pip3 install pyautogui
import random
import json
from urllib.request import urlopen
import wolframalpha  # pip3 install wolframalpha
import time
import sys
import getpass
from config import wolframalpha_app_id


engine = pyttsx3.init()
wikipedia.set_lang("zh-TW")
username = getpass.getuser()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time_():
    # Time = datetime.datetime.now().strftime("%H:%M:%S")  # For 24 hour clock
    Time = datetime.datetime.now().strftime("%I:%M:%S")  # For 12 hour clock
    speak("現在時間是:")
    speak(Time)


def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speak("今天日期是: %d年, %d月, %d日" % (year, month, day))


def wishme():
    speak("歡迎回來!")
    time_()
    date_()

    # Greeting
    hour = datetime.datetime.now().hour
    if hour > 6 and hour <= 12:
        speak("早安!")
    elif hour > 12 and hour <= 18:
        speak("午安!")
    else:
        speak("晚安!")

    speak("請問您需要我幫忙做什麼事?")


def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("接收指令中......")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("辨識指令中......")
        query = r.recognize_google(audio, language="zh-TW")
        print(query)
    except Exception as e:
        print(e)
        print("請再次說明指令, 謝謝!")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # For this function, we must enable low security in sender's gmail
    server.login("username@gmail.com", "password")
    server.sendmail("username@gmail.com", to, content)
    server.close()


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU的使用率為百分之" + usage)
    battery = psutil.sensors_battery().percent
    speak("電池的剩餘率為百分之%.1f" % battery)


def joke():
    speak(pyjokes.get_joke(language="en"))


def screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")


if __name__ == "__main__":
    wishme()

    while True:
        query = TakeCommand().lower()

        if "時間" in query:  # Tell us time when asked
            time_()

        elif "日期" in query:  # Tell us date when asked
            date_()

        elif "維基百科" in query:
            speak("搜尋中")
            query = query.replace("維基百科", '')
            result = wikipedia.summary(query, sentences=3)
            speak("根據維基百科")
            print(result)
            speak(result)

        elif "寄信" in query:
            try:
                speak("請說出寄出信件的內容")
                content = TakeCommand().lower()
                speak("請寫出收信者的信箱")
                receiver = input("收信者的信箱是: ")
                sendEmail(receiver, content)
                speak(content)
                speak("信件已成功寄出")
            except Exception as e:
                print(e)
                speak("信件無法寄出")

        elif "打開網頁" in query:
            speak("請問我應該打開什麼網頁?")
            safaripath = "/Users/" + username + "/Applications/Safari.app"
            search = TakeCommand().lower()
            wb.open_new_tab("http://" + search + ".com")  # Only open websites with .com

        elif "youtube搜尋" in query:
            speak("請問我應該搜尋什麼?")
            search_term = TakeCommand().lower()
            search_term_utf8 = str(search_term.encode("utf-8"))[2:-1].replace("\\x", "%")
            speak("打開YouTube中")
            wb.open_new_tab("http://www.youtube.com/results?search_query=%s" % search_term_utf8)

        elif "google搜尋" in query:
            speak("請問我應該搜尋什麼?")
            search_term = TakeCommand().lower()
            search_term_utf8 = str(search_term.encode("utf-8"))[2:-1].replace("\\x", "%")
            speak("打開估狗中")
            wb.open_new_tab("http://www.google.com/search?q=%s" % search_term_utf8)

        elif "cpu" in query:
            cpu()

        elif "笑話" in query:
            joke()

        elif "結束" in query:
            speak("結束程式中, 再見!")
            sys.exit()

        elif "word" in query:
            speak("打開Microsoft Word中")
            ms_word = "Microsoft Word"
            os.system("open -n -a \"%s\"" % ms_word)

        elif "寫入筆記" in query:
            speak("請問我應該記錄下什麼訊息?")
            notes = TakeCommand()
            file = open("notes.txt", 'w')
            speak("請問您想要留下當前的時間嗎?")
            ans = TakeCommand()
            if "不" not in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(": ")
            file.write(notes)
            speak("您的訊息已經寫入筆記了")

        elif "讀取筆記" in query:
            speak("正在讀取您的筆記中")
            file = open("notes.txt", 'r')
            line = file.readline()
            print(line)
            speak(line)

        elif "截圖" in query:
            screenshot()

        elif "音樂" in query:
            songs_dir = "/Users/" + username + "/Music/音樂"
            music = os.listdir(songs_dir)
            speak("請問我應該播放第幾首音樂? 請說一個數字")
            ans = TakeCommand().lower()
            while not (ans.isnumeric() or "隨便" in ans or "隨機" in ans or "都可以" in ans):
                speak("很抱歉, 我無法了解您的回應, 請再說一個數字")
                ans = TakeCommand().lower()
            if ans.isnumeric():
                no = int(ans)
            elif "隨便" in ans or "隨機" in ans or "都可以" in ans:
                no = random.randint(0, len(music))
            os.system("open \"%s\"" % os.path.join(songs_dir, music[no]))

        elif "提醒我" in query:
            speak("您想要我提醒您什麼事?")
            memory = TakeCommand()
            speak("您想要我提醒您" + memory)
            remember = open("memory.txt", 'w')
            remember.write(memory)
            remember.close()

        elif "記不記得" in query:
            remember = open("memory.txt", 'r')
            speak("您稍早提醒我要告訴您" + remember.readline())

        elif "新聞" in query:
            try:
                jsonObj = urlopen("https://newsapi.org/v2/everything?q=apple&from=2021-03-22&to=2021-03-22&sortBy=popularity&apiKey=b670a84573044f76878fb5d4ab6e6f0a")
                data = json.load(jsonObj)
                i = 1
                speak("以下為一些與蘋果相關的新聞")
                print("------ 蘋果頭條新聞 ------")
                for item in data["articles"]:
                    print(str(i) + ". " + item["title"] + '\n')
                    print(item["description"] + '\n')
                    speak(item["title"])
                    i += 1
            except Exception as e:
                print(e)

        elif "哪裡" in query:
            query = query.replace("在哪裡",  "")
            speak("打開Google地圖中, 搜尋" + query + "的位置")
            query_utf8 = str(query.encode("utf-8"))[2:-1].replace("\\x", "%")
            wb.open_new_tab("http://www.google.com/maps/place/" + query_utf8)

        elif "計算" in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            query = query[2:].replace("加", " + ").replace("減", " - ").replace("乘以", " * ").replace("除以", " / ")
            res = client.query(query)
            answer = next(res.results).text
            print("計算結果為: " + answer)
            speak("計算結果為" + answer)

        elif "什麼是" in query or "誰是" in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            query = query.replace("什麼是", "What is ").replace("誰是", "Who is ")
            res = client.query(query)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("無法找到任何答案, 抱歉")

        elif "休息" in query:
            speak("請問您希望我休息幾秒鐘? 請說一個數字")
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif "睡眠" in query:
            os.system("pmset sleepnow")

        elif "重新開機" in query:
            os.system("sudo shutdown -r now")

        elif "關機" in query:
            os.system("sudo shutdown -h now")
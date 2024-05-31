from calculation_f import claculation_f
from data_preparation import FileToList
import threading
import datetime
from datetime import timedelta
import math

class update_calculation:
    def __init__(self,main_window):
        self.main_window = main_window
        self.calculation = claculation_f(self.main_window)
        self.period = 1

    def trigger_timer(self,period):
        self.period = int(period)
        if self.period > 0:
            self.start_timer()
    def start_timer(self):
        self.timer = threading.Timer(self.period, self.start_timer)
        self.timer.start()
        self.period_update()
    def period_update(self):
        self.calculation.cnx = self.calculation.connect_to_mysql1(self.calculation.config)
        self.calculation.extractFunction_fromDB()
        time = self.calculation.doCal_all()
        f = 1
        for t in time:
            if t != None:
                if datetime.datetime.now().timestamp() - t.timestamp() > (self.period + 2):
                    self.stop_timer()
                    f = 1
                    time_delta = timedelta(seconds=self.period)
                    p = (datetime.datetime.now() - time_delta).replace(microsecond=0)
                    self.main_window.print_message(f"<font color = 'red'>ERROR, No value was update between{p} and {datetime.datetime.now().replace(microsecond=0)}")
                    break
        if f:
            self.main_window.print_message(f"--{datetime.datetime.now().replace(microsecond=0)}-- Value updated")
        print(self.calculation.valueTable)

    def stop_timer(self):
        try:
            self.timer.cancel()
            self.main_window.print_message("Calculation stopped.")
        except:
            self.main_window.print_message("<font color = 'red'>ERROR, Calculation wasn't started")
        



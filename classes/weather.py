
class Weather:

    def __init__(self):
        self.temp_now = 0
        self.max_temp = 0
        self.min_temp = 0
        self.condition = ""
        self.city = ""
        self.humidity = 0
        self.wind = 0
        self.sunrise = ""
        self.sunset = ""
        self.state = ""

    def set_condition(self, con):
        self.condition = con

    def set_temp_now(self, tmp):
        self.temp_now = tmp

    def set_low_temp(self, tmp):
        self.min_temp = tmp

    def set_high_temp(self, tmp):
        self.max_temp = tmp

    def set_city(self, c):
        self.city = c

    def set_humidity(self, h):
        self.humidity = h

    def set_wind(self, w):
        self.wind = w

    def set_sunrise(self, s):
        self.sunrise = s

    def set_sunset(self, s):
        self.sunset = s

    def set_state(self, s):
        self.state = s



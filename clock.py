import datetime, time
import ledcontroller
import language
import config

# RGB_RED = 'red'
# RGB_GREEN = 'green'
# RGB_BLUE = 'blue'

OFF_COLOR = 0x00 # black
DEFAULT_COLOR = 0x00 # black

class WordClock:

    """ ### WordClock
    """

    def __init__(self):

        """ ### WordClock init
        """
        
        self.lc = ledcontroller.LEDController()
        self.lang = language.De()
        self.status = -1
        self.colorset = [0xaaaaaa for _ in range(config.LED_COUNT)]

    def start(self):

        """ ### WordClock start
        """

        # use periodic timer instead of infinite loop (?)
        while(True):
            time.sleep(2)
            self.update_time()

    def parse_time_to_words(self, status, hour):

        """ ### WordClock parse_time_to_words
        """

        words = self.lang.time_base + self.lang.steps[status] + [(self.lang.numbers[hour][:-1] if hour == 1 and status == 0 else self.lang.numbers[hour])]
        return words

    def update_time(self):

        """ ### WordClock update_time

                - Get current time
                - Transform current time to words
                - Update leds using LedController accordingly

        """

        now = datetime.datetime.now() + datetime.timedelta(minutes=2) # shift (11:58 - 12:03 -> Es ist Zwölf)
        status = now.minute // 5

        if status is not self.status:
            self.status = status
            hour = (now.hour if self.status < 5 else (now.hour + 1)) % 12
            words = self.parse_time_to_words(status, hour)
            indices = set()
            for w in words:
                indices.update({i for i in range(self.lang.char_layout.index(w), self.lang.char_layout.index(w) + len(w))})
                
            self.lc.update_colors([self.colorset[x] if x in indices else DEFAULT_COLOR for x in range(config.LED_COUNT)])
            
    def test(self):
        
        for h in range(12):
            for status in range(12):
                hour = (h if status < 5 else (h + 1)) % 12
                print('hour', h, 'status', status, 'adjusted hour', hour)
                
                words = self.parse_time_to_words(status, hour)
                indices = set()
                for w in words:
                    indices.update({i for i in range(self.lang.char_layout.index(w), self.lang.char_layout.index(w) + len(w))})
                
                self.lc.update_colors([self.colorset[x] if x in indices else None for x in range(config.LED_COUNT)])
                
                time.sleep(1)

clock = WordClock()
clock.test()

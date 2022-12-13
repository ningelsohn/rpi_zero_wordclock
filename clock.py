from rpi_ws281x import *
import time

LED_ROWS = 10
LED_COLUMNS = 11
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_INVERT = False
LED_BRIGHTNESS = 255
LED_CHANNEL = 0

RGB_RED = 'red'
RGB_GREEN = 'green'
RGB_BLUE = 'blue'

DEFAULT_COLOR = 0x000000 # black

class WordClock:

    def __init__(self):
        
        self.strip = PixelStrip(LED_ROWS*LED_COLUMNS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.led_layout = self.init_led_layout()
        self.char_layout = 'eskistlfünfzehnzwanzigdreivierteltgnachvorjmhalbqZWÖLFpZWEINSIEBENkDREIrhFÜNFELFNEUNVIERwACHTZEHNrsbSECHSfmuhr'
        self.time_base = ['es', 'ist']
        self.numbers = [
            'ZWÖLF',
            'EINS',
            'ZWEI',
            'DREI',
            'VIER',
            'FÜNF',
            'SECHS', 
            'SIEBEN',
            'ACHT',
            'NEUN',
            'ZEHN',
            'ELF'
        ]
        self.steps = {
            0: ['uhr'],
            1: ['fünf', 'nach'],
            2: ['zehn', 'nach'],
            3: ['viertel', 'nach'],
            4: ['zwanzig', 'nach'], 
            5: ['fünf', 'vor', 'halb'],
            6: ['halb', ],
            7: ['fünf', 'nach', 'halb'],
            8: ['zwanzig', 'vor'], 
            9: ['viertel', 'vor'],
            10: ['zehn', 'vor'],
            11: ['fünf', 'vor']
        }
        self.status = -1
        self.colorset = [DEFAULT_COLOR for _ in range(LED_ROWS * LED_COLUMNS)]
        
    # create map for zig zag wiring of leds to standard 2d matrix ordering
    def init_led_layout(self):
        #: Create all rows in ascending order (current state similar to above shown conventional matrix order)
        num = [[x for x in range(LED_COLUMNS*y, LED_COLUMNS*y + LED_COLUMNS)] for y in range(LED_ROWS)]

        #: Reverse every other sublist
        rev = [list(reversed(l)) if l[0]%2 == 0 else l for l in num]

        #: Flatten two-dimensional list into one-dimensional and reverse the whole list for a descending sort of zig-zag order
        return list(reversed([x for y in rev for x in y]))

    def start(self):

        # use periodic timer instead of infinite loop (?)
        while(True):
            time.sleep(2)
            self.update_time()

    def parse_time_to_words(self, status, hour):
        words = self.time_base + self.steps[status] + [(self.numbers[hour][:-1] if hour == 1 and status == 0 else self.numbers[hour])]
        return words
            
    def update_colors(self, colors):
        
        """ Light LED-Strip based on Color-Matrix
            colors: rows*columns Color-Matrix consisting of HEX-Color-Values as string
                    Falsy values are skipped, first element sets color of upper left led
                    Example: ['#121212', '#232323', '#000', None, None, ...]
                             10 rows, 11 columns -> 110 items
        """

        #: Method expects a list of the length of the led count
        assert len(colors) == self.rows * self.columns

        #: Reset display before updating with new colors
        self.reset()

        #: Iterate color-list with index
        for i, color in enumerate(colors):

            #: Set color only if color is truthy and of type string
            if color and isinstance(color, str):

                #: led-matrix is not ordered as color-matrix due to wiring
                #: transforming from color-matrix index to led-matrix index
                led = self.led_layout[i]

                #: For operations with colors hex is convinient, but the led-strip needs rgb
                self.strip.setPixelColor(led, int(color.replace('#', '0x'), base=16))

        #: Now actually show the set colors on led strip
        self.strip.show()

    def update_time(self):
        now = time.gmtime()
        hour = now[3]
        minute = now[4] + 2 # shift (11:58 - 12:03 -> Es ist Zwölf)
        status = (minute // 5) % 12
        #status = 0 # test wegen bug
        if status != self.status:
            self.status = status
            hour = (hour if self.status < 5 else (hour + 1)) % 12
            words = self.parse_time_to_words(status, hour)
            indices = set()
            for w in words:
                indices.update({i for i in range(self.char_layout.index(w), self.char_layout.index(w) + len(w))})
            #TODO set_colors also updates display, maybe change name or method
            self.update_colors([self.colorset[x] if x in indices else None for x in range(LED_ROWS * LED_COLUMNS)])
            #self.show(colors)
            
    def test(self):
        
        for h in range(12):
            for status in range(12):
                hour = (h if status < 5 else (h + 1)) % 12
                print('hour', h, 'status', status, 'adjusted hour', hour)
                
                words = self.parse_time_to_words(status, hour)
                indices = set()
                for w in words:
                    indices.update({i for i in range(self.char_layout.index(w), self.char_layout.index(w) + len(w))})
                #TODO set_colors also updates display, maybe change name or method
                self.update_colors([self.colorset[x] if x in indices else None for x in range(LED_ROWS * LED_COLUMNS)])
                #self.show(colors)
                time.sleep(1)

clock = WordClock()
clock.start()

#: Run Configuration

#: Mode

class Mode:
    DEBUG ='debug'
    DEVELOP='develop'
    PRODUCTION='production'

mode: Mode = Mode.DEBUG

#: PixelStrip

LED_ROWS = 10
LED_COLUMNS = 11
LED_COUNT = LED_ROWS * LED_COLUMNS
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_INVERT = False
LED_BRIGHTNESS = 255
LED_CHANNEL = 0

# create map for zig zag wiring of leds to standard 2d matrix ordering
def init_led_layout():
    #: Create all rows in ascending order (current state similar to above shown conventional matrix order)
    num = [[x for x in range(LED_COLUMNS*y, LED_COLUMNS*y + LED_COLUMNS)] for y in range(LED_ROWS)]

    #: Reverse every other sublist
    rev = [list(reversed(l)) if l[0]%2 == 0 else l for l in num]

    #: Flatten two-dimensional list into one-dimensional and reverse the whole list for a descending sort of zig-zag order
    return list(reversed([x for y in rev for x in y]))

LED_LAYOUT = init_led_layout()
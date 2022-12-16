import config
import logging
from typing import List

#: Import module only in production mode
#: Module is only available on Raspberry Pi due to its GPIO usage
if config.mode is config.Mode.PRODUCTION:
    try:
        from rpi_ws281x import *
    except Exception as e:
        logging.fatal('Unable to start in production mode: %s \nExiting ...', str(e))
        exit()

class PixelStripMock:

    """ PixelStripMock

            - Mocks rpi_ws281x.PixelStrip
    """

    def __init__(self):

        """ PixelStripMock init

                - Create led list for colors
        """

        #: Init leds
        self.leds: List[int] = [0x0] * config.LED_COUNT

        self.mapping = {
            'a': '🅐',
            'b': '🅑',
            'c': '🅒',
            'd': '🅓',
            'e': '🅔',
            'f': '🅕',
            'g': '🅖',
            'h': '🅗',
            'i': '🅘',
            'j': '🅙',
            'k': '🅚',
            'l': '🅛',
            'm': '🅜',
            'n': '🅝',
            'o': '🅞',
            'p': '🅟',
            'q': '🅠',
            'r': '🅡',
            's': '🅢',
            't': '🅣',
            'u': '🅤',
            'v': '🅥',
            'w': '🅦',
            'x': '🅧',
            'y': '🅨',
            'z': '🅩'
        }

        self.layout = 'eskistlfunfzehnzwanzigdreivierteltgnachvorjmhalbqzwolfpzweinsiebenkdreirhfunfelfneunvierwachtzehnrsbsechsfmuhr'

        self.active = [self.mapping[c] for c in self.layout]
        self.inactive = '.'


    def setPixelColor(self, index: int, color: int) -> None:

        """ PixelStripMock setPixelColor

                - Mocks rpi_ws281x.PixelStrip.setPixelColor
                - Following PEP8 naming conventions, function names should follow the snake case scheme
                  For the sake of compatibilty with the mock, camelCase is used
                - The led controller is mapping the indices to the actual hardwired indices
                  While mocking, this mapping is not to be considered anymore, which is why it is reversed
        """

        #: Set color after reversing index-mapping (needed to consider for hardware-wiring)
        self.leds[config.LED_LAYOUT.index(index)] = color
        

    #: Mock PixelStrip.show
    def show(self) -> None:

        """ PixelStripMock show

                - Mocks rpi_ws281x.PixelStrip.show
                - Led states are simly printed in the terminal
                  For simplicity, only on and off is distinguished
        """

        #: Print basic text representation
        repr = '\n'
        for i in range(config.LED_ROWS):
            for k in range(config.LED_COLUMNS):
                # repr += '● ' if self.leds[i * config.LED_COLUMNS + k] else '○ '
                repr += self.active[i * config.LED_COLUMNS + k] if self.leds[i * config.LED_COLUMNS + k] else self.inactive
                repr += ' '
            repr += '\n'
        print(repr)


class LEDController:

    """ LEDController

            - Wraps access to WS2812B led strip
            - Provides debug functionality for non-GPIO-capable devices
            - Allows setting single pixels and full led-strip

    """

    def __init__(self):

        """ LEDController init

                - Create PixelStrip, Mock when not in Production

        """

        #: Use GPIO pixelstrip when in production
        if config.mode is config.Mode.PRODUCTION:
            self.strip = PixelStrip(config.LED_ROWS*config.LED_COLUMNS, config.LED_PIN, config.LED_FREQ_HZ, config.LED_DMA, config.LED_INVERT, config.LED_BRIGHTNESS, config.LED_CHANNEL)
        #: Otherwise use mock
        else:
            self.strip = PixelStripMock()


    def set_pixel_color(self, index: int, color: int) -> None:

        """ ### LEDController set_pixel_color

                index: int -> index of led \\
                color: int -> color, given in hex format: 0xAA00BB
                
                - Set single pixel color

        """

        #: Check for valid index
        assert index in range(config.LED_COUNT)
        #: Delegate to pixelstrip after considering hardware-wiring 
        self.strip.setPixelColor(config.LED_LAYOUT[index], color)


    def update_pixel_color(self, index: int, color: int) -> None:

        """ ### LEDController update_pixel_polor

                index: int -> index of led \\
                color: int -> color, given in hex format: 0xAA00BB
                
                - Set pixel color
                - Refresh pixelstrip

        """

        #: Set color
        self.set_pixel_color(index, color)
        #: Update pixelstrip
        self.show()


    def set_colors(self, colors: List[int]) -> None:

        """ ### LEDController set_colors

                colors: List[int] -> list of colors, each given in hex format: 0xAA00BB

                - Set all colors

        """

        #: Check for valid color count
        assert len(colors) is config.LED_COUNT

        #: Set colors
        for index, color in enumerate(colors):
            if color:
                self.set_pixel_color(index, color)
            else: 
                self.set_pixel_color(index, config.LED_DEFAULT_COLOR)

    #: Set all pixel colors and show immediately
    def update_colors(self, colors: List[int]) -> None:

        """ ### LEDController update_colors

                colors: List[int] -> list of colors, each given in hex format: 0xAA00BB

                - Set all colors
                - Refresh pixelstrip
        """

        #: Set colors
        self.set_colors(colors)
        #: Update pixelstrip
        self.show()


    def show(self) -> None:

        """ ### LEDController show

                - Refresh pixelstrip
        """

        #: Delegate to pixelstrip
        self.strip.show()


if __name__ == '__main__':

    lc = LEDController()

    # lc.update_pixel_color(0, 0x33)

    indices = {0, 1, 3, 4, 5, 77, 78, 79, 26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 38}
    l = [0xaabbcc if x in indices else 0 for x in range(config.LED_COUNT)]
    print(l)
    lc.update_colors(l)


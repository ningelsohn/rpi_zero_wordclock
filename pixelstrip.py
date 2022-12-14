import config
from typing import List

#: Import module only in production mode
#: Module is only available on Raspberry Pi due to its GPIO usage
if config.mode is config.Mode.PRODUCTION:
    from rpi_ws281x import *

#: Mock Class for rpi_ws281x PixelStrip
#: which is not available outside of Raspberry Pi
class PixelStripMock:

    #: Init
    def __init__(self):


        self.leds: List[int] = [0x0] * config.LED_COUNT


    #: Mock PixelStrip.setPixelColor
    def setPixelColor(self, index: int, color: int) -> None:

        #: Reverse index-mapping (needed to consider for hardware-wiring)
        self.leds[config.LED_LAYOUT.index(index)] = color
        

    #: Mock PixelStrip.show
    def show(self) -> None:

        #: print basic text representation
        print()
        for i in range(config.LED_ROWS):
            for k in range(config.LED_COLUMNS):
                print('● ' if self.leds[i * config.LED_COLUMNS + k] else '○ ', end='')
            print()
        print()


#: LEDController wraps access to the PixelStrip 
class LEDController:

    #: Init Controller
    def __init__(self):

        #: Use GPIO PixelStrip when in production
        if config.mode is config.Mode.PRODUCTION:
            self.strip = PixelStrip(config.LED_ROWS*config.LED_COLUMNS, config.LED_PIN, config.LED_FREQ_HZ, config.LED_DMA, config.LED_INVERT, config.LED_BRIGHTNESS, config.LED_CHANNEL)
        #: Otherwise use mock
        else:
            self.strip = PixelStripMock()

    #: set pixel color
    def setPixelColor(self, index: int, color: int) -> None:

        #: check for valid index
        assert index in range(config.LED_COUNT)
        #: delegate to strip itself after considering hardware-wiring 
        self.strip.setPixelColor(config.LED_LAYOUT[index], color)

    #: set single pixel and show immediately
    def updatePixelColor(self, index: int, color: int) -> None:

        self.setPixelColor(index, color)
        self.show()

    #: set all pixel colors 
    def setColors(self, colors: List[int]) -> None:

        #: check for valid color count
        assert len(colors) is config.LED_COUNT

        for index, color in colors:
            self.strip.setPixelColor(index, color)

    #:
    def updateColors(self, colors: List[int]) -> None:

        self.setColors(colors)
        self.show()

    #:
    def show(self) -> None:

        self.strip.show()


if __name__ == '__main__':

    lc = LEDController()
    lc.updatePixelColor(4, 0x220055)
    lc.updatePixelColor(7, 0x220055)


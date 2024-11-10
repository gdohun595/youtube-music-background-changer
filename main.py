import os
import ctypes
import webview

from PIL import Image
from urllib import request

#################################### VARIABLES ####################################
ICON_RESOLUTION = (500, 500)
SCREEN_RESOLUTION = (2560, 1440)
###################################################################################

#################################### CONSTANTS ####################################
CENTER = (SCREEN_RESOLUTION[0] // 2 - ICON_RESOLUTION[0] // 2), (SCREEN_RESOLUTION[1] // 2 - ICON_RESOLUTION[1] // 2) 
ALBUM_IMAGE_SELECTOR = '#layout > ytmusic-player-bar > div.middle-controls.style-scope.ytmusic-player-bar > div.thumbnail-image-wrapper.style-scope.ytmusic-player-bar > img'

SPI_SETDESKWALLPAPER = ctypes.c_uint(0x0014)
SPIF_UPDATEINIFILE_OR_SPIF_SENDWININICHANGE = ctypes.c_uint(0x01 | 0x02)

SystemParametersInfoW = ctypes.windll.user32.SystemParametersInfoW
SystemParametersInfoW.argtypes = (ctypes.c_uint, ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_uint)
SystemParametersInfoW.restype = ctypes.c_bool
###################################################################################

def invoke():
    '''Invokes a function fired when changing the album photo.'''

    element = window.dom.get_element(ALBUM_IMAGE_SELECTOR)

    def handler(event):
        del event 

        source: str = element.attributes.get('src')
        source = source.split('=', 1)
        source = source[0] + '=' + source[1].replace('60', str(ICON_RESOLUTION[0]), 2)

        image = request.urlopen(source)
        image = Image.open(image)
        
        colors = image.getcolors(image.width * image.height)
        color = max(colors, key=lambda color: color[0])[1]

        base = Image.new('RGB', SCREEN_RESOLUTION, color)
        base.paste(image, CENTER)
        base.save('background.png')

        path = os.path.abspath('background.png')
        path = ctypes.c_wchar_p(path)
        return SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE_OR_SPIF_SENDWININICHANGE)

    return element.on('load', handler)

if __name__ == '__main__':
    window = webview.create_window('YouTube Music', 'https://music.youtube.com')
    webview.start(invoke, private_mode=False)

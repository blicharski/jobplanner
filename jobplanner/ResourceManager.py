
from os import path
from PyQt4.QtCore import QSize 
from PyQt4.QtGui import QFontMetrics


# to jest komentarz do tego jak kod dziala
class ResourceManager:
    """This class manages various resources like images.
    """

    __instance = None
    images_root_dir = "img" #path.join(path.pardir, 'img')
    icon_image_max_size = QSize(25, 25)

    def __init__(self):
        pass

    def __new__(classtype, *argds, **kwargs):
        if classtype != type(classtype.__instance):
            classtype.__instance = object.__new__(classtype, *args, **kwargs)
        return classtype.__instance

    def get_icon_image_max_size(self):
        return self.icon_image_max_size
    
    def get_image(self, name):
        return self.translate_to_path(name) + ".png"

    def translate_to_path(self, name):
        return path.join(self.images_root_dir, name)

    def get_widthest_char_size(self,  widget):
        font = widget.font()
        return QFontMetrics(font).maxWidth()


resourceManager = ResourceManager()
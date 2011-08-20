

class ResourceManager:
    __instance = None
    images_root_dir = './img/'

    def __init__(self, root_path):
        self.images_root_dir = root_path

    def __new__(classtype, *args, **kwargs):
        if classtype != type(classtype.__instance):
            classtype.__instance = object.__new__(classtype, *args, **kwargs)
        return classtype.__instance

    def get_image(self, name):
        return self.translate_to_path(name)

    def translate_to_path(self, name):
        pass
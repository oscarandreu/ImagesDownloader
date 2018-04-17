from classes.imageHelper import ImageHelper
from os.path import join, dirname, abspath, exists


pathName = "serpentine_belt"

if __name__ == "__main__":
    path  = join(dirname(abspath(__file__)), join("images", pathName))
    img = ImageHelper()
    img.cleanDuplicates(path)
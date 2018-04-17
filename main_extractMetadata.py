from classes.imageHelper import ImageHelper
from os.path import join, dirname, abspath


pathName = "officetest"

if __name__ == "__main__":
    path  = join(dirname(abspath(__file__)), pathName)
    img = ImageHelper()
    img.extracMetadataFromFiles(path)
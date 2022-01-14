from tempfile import NamedTemporaryFile

from PIL import Image


def create_image():
    """Create in-memory PNG image and return it as byte stream. Required field: image name"""
    fp = NamedTemporaryFile()
    img = Image.new(mode="RGB", size=(100, 100), color=(255, 255, 255))
    img.save(fp, 'png')
    fp.name= "invokust_image.png"
    fp.seek(0)
    return fp
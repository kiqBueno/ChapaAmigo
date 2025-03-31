import logging
from io import BytesIO
from PIL import Image

def cropImage(imgBytes):
    """
    Crop 10% from the top and bottom of an image.
    """
    logging.info("Cropping image")
    img = Image.open(imgBytes)
    width, height = img.size
    cropHeight = int(height * 0.09)
    croppedImg = img.crop((0, cropHeight, width, height - cropHeight))
    croppedImgBytes = BytesIO()
    croppedImg.save(croppedImgBytes, format='PNG')
    croppedImgBytes.seek(0)
    return croppedImgBytes

def addTransparency(imagePath, transparency):
    """
    Add transparency to an image.
    """
    logging.info("Adding transparency to image")
    img = Image.open(imagePath).convert("RGBA")
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * transparency)
    img.putalpha(alpha)
    imgBytes = BytesIO()
    img.save(imgBytes, format='PNG')
    imgBytes.seek(0)
    return imgBytes
import pytesseract
from PIL import Image

print(pytesseract.image_to_string(Image.open('../../../Downloads/Transshipment-photo-1-1.jpg')))
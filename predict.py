from ssd import SSD
from PIL import Image
import cv2


def map_clear(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    cl1 = clahe.apply(gray)
    out_image = cv2.cvtColor(cl1, cv2.COLOR_GRAY2RGB)
    return out_image


img = r"E:\research\SSD\ssd-keras-master\img\cataract_0064.jpg"
image = cv2.imread(img)
image = map_clear(image)

image_new = Image.fromarray(image.astype('uint8')).convert('RGB')
ssd = SSD()
r_image = ssd.detect_image(image_new)
r_image.show()
r_image.save(r"D:/result2.jpg")
mc = 1

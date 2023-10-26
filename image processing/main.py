import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("/Users/nikodembartnik/Documents/git/StarTrckr/docs/edit4.jpg")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
assert img is not None, "file could not be read, check with os.path.exists()"
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
img = cv.normalize(img, None, 0, 1.0, cv.NORM_MINMAX, dtype=cv.CV_32F)
plt.hist(img.ravel(), 1, [0, 1])
plt.show()

cv.imshow("original", img)
cv.imshow("processed", thresh1)

titles = ["Original Image", "BINARY"]
images = [img, thresh1]
for i in range(2):
    plt.subplot(1, 2, i + 1), plt.imshow(images[i], "gray", vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("/Users/nikodembartnik/Documents/git/StarTrckr/docs/edit4.jpg")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
assert img is not None, "file could not be read, check with os.path.exists()"
ret, thresholded_image = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
# img = cv.normalize(img, None, 0, 1.0, cv.NORM_MINMAX, dtype=cv.CV_32F)
thresholded_image = cv.convertScaleAbs(thresholded_image)
cv.imshow("processed", thresholded_image)
# plt.hist(img.ravel(), 1, [0, 1])
# plt.show()

contours, _ = cv.findContours(
    thresholded_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
)
# print(contours)
contours = sorted(contours, key=cv.contourArea, reverse=True)


result_image = np.zeros_like(img)

# Draw all the blobs (contours) on the result_image
for contour in contours[:10]:
    M = cv.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv.circle(result_image, (cX, cY), 20, (255, 0, 0), -1)
    # mask = np.zeros_like(thresholded_image)
    # cv.drawContours(mask, [contour], 0, 255, -1)

# calculate and print center points for each blob
for contour in contours[:10]:
    M = cv.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print(f"center point: ({cX}, {cY})")

result_image = cv.addWeighted(img, 0.8, result_image, 0.7, 0)
# Display the result image with all blobs
cv.imshow("All Blobs", result_image)


cv.imshow("original", img)
cv.imshow("processed", thresholded_image)
cv.waitKey(0)
cv.destroyAllWindows()

# titles = ["Original Image", "BINARY"]
# images = [img, thresholded_image]
# for i in range(2):
#     plt.subplot(1, 2, i + 1), plt.imshow(images[i], "gray", vmin=0, vmax=255)
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()

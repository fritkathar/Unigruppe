import cv2

attrib_image_names = ["cashewkerne.tif","makadamia.tif","mandeln.tif","paranuss.tif","pekanuesse.tif"]
test_image_names = ["StichproeMix1.tif","StichproeMix2.tif","StichproeMix3.tif"]
veri_image_names = ["verifizierung1.tif","verifizierung2.tif","verifizierung3.tif"]

attrib_images = [cv2.imread(i) for i in attrib_image_names]
test_images = [cv2.imread(i) for i in test_image_names]
veri_image_names = [cv2.imread(i) for i in veri_image_names]

threshold_attrib = [cv2.threshold(i,120,255,cv2.THRESH_BINARY) for i in attrib_images]
bin_attrib_image = threshold_attrib[:][1]


cv2.imshow("image",bin_attrib_image[0])
cv2.waitKey(0)
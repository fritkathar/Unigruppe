from operator import concat

import cv2
import numpy as np
from shapely.geometry import Polygon

#attrib_image_names = ["cashewkerne.tif","makadamia.tif","mandeln.tif","paranuss.tif","pekanuesse.tif"]
#test_image_names = ["StichproeMix1.tif","StichproeMix2.tif","StichproeMix3.tif"]
#veri_image_names = ["verifizierung1.tif","verifizierung2.tif","verifizierung3.tif"]

#attrib_images = [cv2.imread(i) for i in attrib_image_names]
#test_images = [cv2.imread(i) for i in test_image_names]
#veri_image_names = [cv2.imread(i) for i in veri_image_names]

#for image in attrib_images:
 #   cv2.imshow("image", attrib_images[image])


#threshold_attrib = [cv2.threshold(i,120,255,cv2.THRESH_BINARY) for i in attrib_images]
#bin_attrib_image = threshold_attrib[:][1]
def load_image(image_path):
    image = cv2.imread(image_path)
    return image
def prepareImages(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #threshhold erstellen
    thresh = cv2.threshold(image_gray, 120, 255, cv2.THRESH_BINARY)

    #konturen finden
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_circularity(image, thresh):

    contours = prepareImages(image)

    #nach circularity filtern
    circular_contours = []

    for cnt in contours:
        # Fläche und Umfang der Kontur berechnen
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # Division durch 0 verhindern
        if perimeter == 0:
            continue

        # Rundheit berechnen
        circularity = 4 * np.pi * (area / (perimeter ** 2))

        # Filter-Bedingung: nur Objekte, die Runder als der Threshhold sind (1 = maximal rund)
        if circularity >= thresh:
            circular_contours.append(cnt)

        return circular_contours
def filter_rectangularity(image, thresh):

    contours = prepareImages(image)

    # filtern nach Rechteckigkeit
    rectangular_contours = []
    for cnt in contours:
        # 1. Fläche der eigentlichen Kontur berechnen
        area = cv2.contourArea(cnt)

        # 2. Das minimal umschließende Rechteck ermitteln
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int64(box)

        # 3. Fläche des umschließenden Rechtecks berechnen
        rect_area = cv2.contourArea(box)

         # 4. Rechteckigkeit berechnen (Extent)
        rectent = area / rect_area if rect_area > 0 else 0

        # 5. Filtern:  nur Konturen mit mindestens thresh % Rechteckigkeit
        if rectent >= thresh:
            rectangular_contours.append(cnt)
        return rectangular_contours
def filter_bulkiness(image, thresh):
    contours = prepareImages(image)
    #nach Bulkiness filtern
    bulkiness_contours = []
    min_area = 500  # Minimale Objektgröße in Pixeln
    mask = np.zeros_like(thresh)

    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
           bulkiness_contours.append(cnt)
    return bulkiness_contours

def filter_convexdeficit(image, thresh):
    contours = prepareImages(image)

    convexdeficit_contours = []
    for cnt in contours:
        convexityhull = cv2.convexityDefects(contours, thresh)
        convexdeficit = Polygon([convexityhull])
        convexdeficitSize = convexdeficit.area
        #falls die größe des Convexen Defiziets größer als der übergebene Threshhold ist
        if(convexdeficitSize > thresh):
            convexdeficit_contours.append(cnt)

    return convexdeficit_contours


# Gefilterte Konturen zeichnen und Bilder Filtern - testen Fehlgeschlagen, da Bild nicht lädt - Auswertung und Reihenfolge noch unfertig
image1 = load_image('StichproeMix1.tif')
#filtere nach Bulkiness für Pekanüsse
image2 = cv2.drawContours(image1, filter_bulkiness(image1, 1.01), -1, (0, 255, 0), 3)
#filtere nach Rechteckigkeit/Rectangularity für Pekanüsse
image3 = cv2.drawContours(image2, filter_rectangularity(image2, 0.815), -1, (0, 255, 0), 3)
#filtere nach Rundheit/circularity für Macadamia
image4 = cv2.drawContours(image3, filter_circularity(image3, 0.710), -1, (0, 255, 0), 3)
#filtere nach convexemDefizit/convexityDefizit für cashews
image5 = cv2.drawContours(image4, filter_convexdeficit(image4, 0.91), -1, (0, 255, 0), 3)

cv2.imshow('Ergebnis', image5)
cv2.waitKey(0)
cv2.destroyAllWindows()

#cv2.imshow("image",image)
#cv2.waitKey(0)

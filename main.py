import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 2000:
            # cv2.drawContours(imageContour, cnt , -1 , (0,255,0),2)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.005 * peri, True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imageContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imageContour,"Kvetinac",(x+(w//2), y+h+15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255),2)

kernel = np.ones((5,5),np.uint8)
# print("Package hereee!")
# image = cv2.imread("Resources/Woooman.png")
# cv2.imshow("Output", image)
# cv2.waitKey(0)
image = cv2.imread("Resources/Screen3.jpg")
image = cv2.resize(image,(700,950))
imgC1 = image[140:340,140:350]
imgC2 = image[140:340,375:585]
imgC3 = image[380:580,140:350]
imgC4 = image[380:580,375:585]
imageStackCropp = stackImages(1,([imgC1, imgC2], [imgC3, imgC4]))
imageContour = imageStackCropp.copy()

imgCMerged = cv2.cvtColor(imageStackCropp, cv2.COLOR_BGR2GRAY)
imgCMerged = cv2.GaussianBlur(imgCMerged, (7,7),4)
imgCMergedCanny = cv2.Canny(imgCMerged, 45,45)
imgCMergedDill = cv2.dilate(imgCMergedCanny, kernel, iterations = 1)

# imgC1 = cv2.cvtColor(imgC1, cv2.COLOR_BGR2GRAY)
# imgC2 = cv2.cvtColor(imgC2, cv2.COLOR_BGR2GRAY)
# imgC3 = cv2.cvtColor(imgC3, cv2.COLOR_BGR2GRAY)
# imgC4 = cv2.cvtColor(imgC4, cv2.COLOR_BGR2GRAY)
# imgC1 = cv2.GaussianBlur(imgC1, (7,7),2)
# imgC2 = cv2.GaussianBlur(imgC2, (7,7),2)
# imgC3 = cv2.GaussianBlur(imgC3, (7,7),2)
# imgC4 = cv2.GaussianBlur(imgC4, (7,7),2)
# imgC1Canny = cv2.Canny(imgC1, 45,45)
# imgC2Canny = cv2.Canny(imgC2, 45,45)
# imgC3Canny = cv2.Canny(imgC3, 45,45)
# imgC4Canny = cv2.Canny(imgC4, 45,45)
# imgC1Dill = cv2.dilate(imgC1Canny, kernel, iterations = 1)
# imgC2Dill = cv2.dilate(imgC2Canny, kernel, iterations = 1)
# imgC3Dill = cv2.dilate(imgC3Canny, kernel, iterations = 1)
# imgC4Dill = cv2.dilate(imgC4Canny, kernel, iterations = 1)
#
# imageC1Erod = cv2.erode(imgC1Dill, kernel, iterations=3)
# imageC2Erod = cv2.erode(imgC2Dill, kernel, iterations=3)
# imageC3Erod = cv2.erode(imgC3Dill, kernel, iterations=3)
# imageC4Erod = cv2.erode(imgC4Dill, kernel, iterations=3)
# cv2.imshow("Output1", imageCanny)
# cv2.imshow("OutputC1", imgC1Dill)
# cv2.imshow("OutputC2", imgC2Dill)
# cv2.imshow("OutputC3", imgC3Dill)
# cv2.imshow("OutputC4", imgC4Dill)
getContours(imgCMergedDill)

# imageStack1 = stackImages(1,([imgC1Canny, imgC2Canny], [imgC3Canny, imgC4Canny]))
# imageStack2 = stackImages(1,([imgC1, imgC2], [imgC3, imgC4]))
# imageStack3 = stackImages(1,([imgC1Dill, imgC2Dill], [imgC3Dill, imgC4Dill]))
# imageStack4 = stackImages(1,([imageC1Erod, imageC2Erod], [imageC3Erod, imageC4Erod]))
cv2.imshow("Output_Edges", imgCMergedCanny)
# cv2.imshow("OutputC2", imageStack2)
# cv2.imshow("OutputC3", imageStack3)
# cv2.imshow("OutputC4", imageStack4)
cv2.imshow("Output_BoundBoxes", imageContour)
cv2.imshow("Output_MergedDill", imgCMergedDill)
cv2.waitKey(0)
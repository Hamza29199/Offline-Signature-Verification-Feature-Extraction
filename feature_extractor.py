import cv2
import math

"""
import pathlib
#making and opening directories and files
try:
    pathlib.Path('/centroid').mkdir(parents = False, exist_ok = False)
    pathlib.Path('/ratio').mkdir(parents = False, exist_ok = False)
    pathlib.Path('/transitions').mkdir(parents = False, exist_ok = False)
except:
    print("failed to create directories")
    exit()
"""

filename = "AAK.txt"
try:
    centFile = open("centroid/" + filename, "w")
    ratioFile = open("ratio/" + filename, "w")
    transFile = open("transitions/" + filename, "w")

    blacksFile = open("blacks/" + filename, "w")
    normSizeFile = open("normSize/" + filename, "w")
    centAnglesFile = open("centAngles/" + filename, "w")
    normCentAngleFile = open("normCentAngles/" + filename, "w")
    
except:
    print("failed to create text files")
    exit()


"""
CONVERTING THE IMAGE
AND TRIMMING BORDER WHITESPACES
"""

signature = 0

#Opening the image here
try:
    signature = cv2.imread("signSample.jpeg")
except IOError:
    print("Could not find/open signature file!")
finally:
    if signature is None:
        print("Image was not read from the file")
        exit()

#Setting the default window name for image display
defaultWindow = "Signature"

#showing the opened image
print("Opening read image file")
cv2.imshow(defaultWindow, signature)
cv2.waitKey()

#Converting the image to grayscale
converted = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)

#displaying the grayscale converted image
print("Displaying grayscale converted image")
cv2.imshow(defaultWindow, converted)
cv2.waitKey()

#image original resolution
print("\n",converted.shape,"\n")

#grayscale to black and white using binary thresholding
#threshold = 220 (trial and error)
(thresh, blackAndWhiteImage) = cv2.threshold(converted, 220, 255, cv2.THRESH_BINARY)

#show the converted image
print("Displaying black and white converted image")
cv2.imshow(defaultWindow, blackAndWhiteImage)
cv2.waitKey()

print("\nRunning boundary calculation")
#finding the boundaries of greyscale image for extraction
#using existing algorithm
res_y, res_x = converted.shape      #image resolution, returned as (height,width)
top = res_y
right = 0
left = res_x
bottom = 0

#image array is traversed as image columns(array rows) x image rows(array columns)
for y in range(res_y):
    for x in range(res_x):
        if blackAndWhiteImage[y][x] == 0:
            if y < top:
                top = y
            if y > bottom:
                bottom = y
            if x < left:
                left = x
            if x > right:
                right = x
            

#crop image to boundary values
trimmed = blackAndWhiteImage[top:bottom, left:right]

#show the cropped image with added border
print("Displaying cropped image")
cv2.imshow(defaultWindow ,cv2.copyMakeBorder(trimmed, 2,2,2,2 , cv2.BORDER_CONSTANT))
cv2.waitKey()

#closing all image windows
cv2.destroyAllWindows()




#Using segment boxes numpy array to store 64 image segments
blocks = []
ratios = []
transitions = []

"""
LOCATING THE CENTROID (mean of all the points in a shape)
(center of mass of image)
Dividing the image at centroid creating 4 segments and adding to segments
Calculating the ratio of each segment and adding to ratios
Finding black to white transitions in each segment and adding to transitions
"""

def centroid(cropped):
    

    #algorithm to calculate centroid
    res_y, res_x = cropped.shape
    concentration_X = 0
    concentration_Y = 0
    points = 0

    for y in range(res_y):
        for x in range(res_x):
            if cropped[y][x] == 0:
                concentration_X += x
                concentration_Y += y
                points += 1
    try:            
        concentration_X = int(concentration_X / points)
        concentration_Y = int(concentration_Y / points)
    except ZeroDivisionError:
        pass

    #print("\nCentroid x: ",concentration_X,"Centroid y: ",concentration_Y,"\n")
    return [concentration_Y, concentration_X]

def transitions(segment):
    transitions = 0
    if segment.size > 0:
        previousPixel = segment[0][0]
        for y in range(1,segment.shape[0]):
            for x in range(1,segment.shape[1]):
                if segment[y][x] == 255 and previousPixel == 0:
                    transitions += 1
                previousPixel = segment[y][x]
    return transitions
    

def ratio(image):
    if image.size > 0:
        return image.shape[1]/image.shape[0]
    else:
        return 0

#for finding the number of black cells
def numberBlacks(cells):
    black = 0

    if cells.size > 0:
        for y in range(1, cells.shape[0]):
            for x in range(1, cells.shape[1]):

                if cells[y][x] == 0:
                    black += 1
    return black

#for finding the normalized size for each cell
def findNormSize(cells):

    numBlacks = numberBlacks(cells)

    if cells.size > 0 and numBlacks != 0:
    
        normalSize = ((cells.shape[0]) * (cells.shape[1]))/numBlacks

        return normalSize

    else:

        return 0


#for finding the cnetroid angles for each cell
def findCentAngle(cells):

    cx, cy = centroid(cells)
    a = 0.0

    if cells.size > 0:

        dx = cx - left
        dy = bottom - cy

        a = math.atan(dx/dy)

        return a

    else:
        return 0.0

#for finding the normalized sum of centroid angles

def findNormAngle(cells):

    sumAngles = 0.0
    numBlacks = numberBlacks(cells)
    
    a = 0.0
    

    if cells.size > 0:

        a = findCentAngle(cells)

        sumAngles += a

        
    if numBlacks != 0:
        
        return (sumAngles / numBlacks)

    else:

        return 0.0
    

def split(image, centroidp, depth = 0):
    #splitting
    if depth < 3:
        topLeft = image[top:centroidp[0], left:centroidp[1]]
        split(topLeft,centroid(topLeft), depth + 1)
        
        topRight = image[top:centroidp[0], centroidp[1]:right]
        split(topRight,centroid(topRight), depth + 1)

        bottomLeft = image[centroidp[0]:bottom, left:centroidp[1]]
        split(bottomLeft,centroid(bottomLeft), depth + 1)

        bottomRight = image[centroidp[0]:bottom, centroidp[1]:right]
        split(bottomRight,centroid(bottomRight), depth + 1)
        
    else:
        t = transitions(image)
        print("\nNumber of transitions is ", t)
        r = ratio(image)
        print("\nAspect ratio is ", r)
        c = centroid(image)
        print("\nCentroid is ", c)

        #for task 5 additions

        b = numberBlacks(image)
        print("\nNumber of black cells is ", b)
        
        s = findNormSize(image)
        
        print("\nNorm size is ", s)
        a = findCentAngle(image)

        print("\nCentrodi angle is ", a)

        A = findNormAngle(image)
        print("\nNormalized Angle for black pixels is ", A)

        centFile.write(str(c[1])+":"+str(c[0]) + "\n")
        ratioFile.write(str(r)+ "\n")
        transFile.write(str(t) + "\n")

        blacksFile.write(str(b) + "\n")
        normSizeFile.write(str(s)+ "\n")
        centAnglesFile.write(str(a) + "\n")
        normCentAngleFile.write(str(A) + "\n")
        

split(trimmed,centroid(trimmed),0)

#dumping the values for the cells to their respective text files

centFile.close()
ratioFile.close()
transFile.close()

blacksFile.close()
normSizeFile.close()
centAnglesFile.close()
normCentAngleFile.close()

input("\nPress enter to exit")



from PIL import Image
import numpy
import scipy
import math
from scipy.misc import toimage

i = Image.open('Bridge.jpg')
width, height = i.size

#Reading image
im = numpy.array(Image.open('Bridge.jpg'))

#DoG filter
convdogf = numpy.array([[0, 0, -1, -1, -1, 0, 0],
                     [0, -2, -3, -3, -3, -2, 0],
                     [-1, -3, 5, 5, 5, -3, -1],
                     [-1, -3, 5, 16, 5, -3, -1],
                     [-1, -3, 5, 5, 5, -3, -1],
                     [0, -2, -3, -3, -3, -2, 0],
                     [0, 0, -1, -1, -1, 0, 0]])
                     

#LoG filter
convlogf = numpy.array([[0, 0, 1, 0, 0],
                     [0, 1, 2, 1, 0],
                     [1, 2, -16, 2, 1],
                     [0, 1, 2, 1, 0],
                     [0, 0, 1, 0, 0]])



#Creating image with buffer for DoG convolution
image = numpy.zeros(shape=(width + 6, height + 6), dtype=int)
image1 = numpy.array(image)

for m in range(0, width - 1):
    for n in range(0, height - 1):
        image1[m + 3, n + 3] = im[m, n]


#DoG Convolution
def convdog(w, h, image, conv):
    image2 = numpy.zeros(shape=(width, height), dtype=int)
    image2 = numpy.array(image2)
    for x in range(3, w - 4):
        for y in range(3, h - 4):
            v=0
            for a in range(0, 6):
                for b in range(0, 6):
                    v = v+image[x+a-3,y+b-3]*conv[a,b]
            
            image2[x-3, y-3]=v

    toimage(image2).show()
    return image2



dog=convdog(width + 6, height + 6, image1, convdogf)


#Creating null image to save zero crossing
image = numpy.zeros(shape=(width, height), dtype=int)
image3 = numpy.array(image)

#DoG zero crossing
for x in range(1, width - 2):
    for y in range(1, height - 2):
        count=0
        if ((dog[x,y-1] >0 and dog[x,y] <0) or (dog[x,y-1] <0 and dog[x,y] >0)):
            count=count+1
        elif ((dog[x-1,y] >0 and dog[x,y] <0) or (dog[x-1,y] <0 and dog[x,y] >0)):
            count=count+1
        elif ((dog[x,y+1] >0 and dog[x,y] <0) or (dog[x,y+1] <0 and dog[x,y] >0)):
            count=count+1
        elif ((dog[x+1,y] >0 and dog[x,y] <0) or (dog[x+1,y] <0 and dog[x,y] >0)):
            count=count+1
        
        if (count>0):
            image3[x,y]=1
        else:
            image3[x,y]=0
            
toimage(image3).show()


#Creating null image for thresholding zero crossing
image = numpy.zeros(shape=(width, height), dtype=int)
image4 = numpy.array(image)

#Thresholding zero crossing to remove weak edges
for x in range(1, width - 2):
    for y in range(1, height - 2):
        maxdiff=0
        if ((dog[x,y-1] >0 and dog[x,y] <0) or (dog[x,y-1] <0 and dog[x,y] >0)):
            if (maxdiff<abs(dog[x,y-1])+abs(dog[x,y])):
                maxdiff=abs(dog[x,y-1])+abs(dog[x,y])
        elif ((dog[x-1,y] >0 and dog[x,y] <0) or (dog[x-1,y] <0 and dog[x,y] >0)):
            if (maxdiff<abs(dog[x-1,y])+abs(dog[x,y])):
                maxdiff=abs(dog[x-1,y])+abs(dog[x,y])
        elif ((dog[x,y+1] >0 and dog[x,y] <0) or (dog[x,y+1] <0 and dog[x,y] >0)):
            if (maxdiff<abs(dog[x,y+1])+abs(dog[x,y])):
                maxdiff=abs(dog[x,y+1])+abs(dog[x,y])
        elif ((dog[x+1,y] >0 and dog[x,y] <0) or (dog[x+1,y] <0 and dog[x,y] >0)):
            if (maxdiff<abs(dog[x+1,y])+abs(dog[x,y])):
                maxdiff=abs(dog[x+1,y])+abs(dog[x,y])
        #Thresholding criteria is difference of 450 between negative and positive values
        if (maxdiff>450):
            image4[x,y]=1
        else:
            image4[x,y]=0

toimage(image4).show()

#Creating image with buffer for LoG convolution
image = numpy.zeros(shape=(width + 4, height + 4), dtype=int)
image5 = numpy.array(image)

for m in range(0, width - 1):
    for n in range(0, height - 1):
        image5[m + 2, n + 2] = im[m, n]


#LoG convolution
def convlog(w, h, image, conv):
    image6 = numpy.zeros(shape=(width, height), dtype=int)
    image6 = numpy.array(image6)
    for x in range(2, w - 3):
        for y in range(2, h - 3):
            v=0
            for a in range(0, 4):
                for b in range(0, 4):
                    v = v+image[x+a-2,y+b-2]*conv[a,b]
            
            image6[x-2, y-2]=v

    toimage(image6).show()
    return image6



log=convlog(width + 4, height + 4, image5, convlogf)

#Creating null image for zero crossing on LoG
image = numpy.zeros(shape=(width, height), dtype=int)
image7 = numpy.array(image)

#LoG zero crossing
for x in range(1, width - 2):
    for y in range(1, height - 2):
        count=0
        if ((log[x,y-1] >0 and log[x,y] <0) or (log[x,y-1] <0 and log[x,y] >0)):
            count=count+1
        elif ((log[x-1,y] >0 and log[x,y] <0) or (log[x-1,y] <0 and log[x,y] >0)):
            count=count+1
        elif ((log[x,y+1] >0 and log[x,y] <0) or (log[x,y+1] <0 and log[x,y] >0)):
            count=count+1
        elif ((log[x+1,y] >0 and log[x,y] <0) or (log[x+1,y] <0 and log[x,y] >0)):
            count=count+1
        
        if (count>0):
            image7[x,y]=1
        else:
            image7[x,y]=0
            
toimage(image7).show()



toimage(image3).save('zcDoG.bmp')
toimage(image4).save('WeakEdgeZcDoG.bmp')
toimage(image7).save('zcLoG.bmp')
toimage(dog).save('dog.jpeg')
toimage(log).save('log.jpeg')









import os, sys
import Image
import math

def entropy(image):
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    pixel = list()
    entropylist = list()
    for j in pixels:
        s = sum((j.count(i)/(len(j)+0.0))*math.log(1/(j.count(i)/(len(j)+0.0))) for i in set(j))
        entropylist.append(s)
    print sum(entropylist[:3])
    
image = Image.open('flower.jpg') 
entropy(image)
"""image = Image.open('flower1.jpg')
entropy(image)
image = Image.open('white.jpg')
entropy(image)
"""

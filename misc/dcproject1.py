import os, sys
import Image
import math
from numpy import array
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import *

def compare(codebook, pixel):
    avg = 0
    returning = codebook[0]
    for index, code in enumerate(codebook):
        diff = sum(abs(x-y) for x in code for y in pixel)/3.0
        if index == 0:
            avg = diff
            returning = code
        elif diff <= avg:
            avg = diff
            returning = code
    return returning


def entropy(image):
    pixels = list(image.getdata())
    #width, height = image.size
    #pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    #pixel = list()
    #entropylist = list()
    #for j in pixels:
    #    s = sum((j.count(i)/(len(j)+0.0))*math.log(1/(j.count(i)/(len(j)+0.0))) for i in set(j))
    #    entropylist.append(s)
    #obs = array(entropylist)   
    #print obs
    #print pixels,
    obs1 = array(pixels)
    codebook,distortion = kmeans(obs1, 7)#, minit='points')
    #print codebook
    newcodebook = [tuple(x) for x in codebook]
    print newcodebook
    for index, pixel in enumerate(pixels):
        closest = compare(newcodebook, pixel)
        #print closest
        pixels[index] = closest
    newimage = Image.new(image.mode, image.size)
    newimage.putdata(pixels)
    newimage.save('sample1.png', "PNG")
    #newimage.show()
        

image = Image.open('girl.jpg') 
entropy(image)
'''image = Image.open('white.jpg') 
entropy(image)
image = Image.open('flower1.jpg') 
entropy(image)
'''

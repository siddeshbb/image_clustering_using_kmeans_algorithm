from Tkinter import *
import re
import tkFileDialog
import os
from tkFileDialog import askopenfilename
import sys
import Image, ImageTk
import math
from numpy import array
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import *


def browse():
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=top, initialdir=currdir, title='Please select a directory')
    content.set(tempdir)
        
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

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def entropy(image, k):
    pixels = list(image.getdata())
    obs1 = array(pixels)
    codebook,distortion = kmeans(obs1, k)#, minit='points')
    #print codebook
    newcodebook = [tuple(x) for x in codebook]
    for index, pixel in enumerate(pixels):
        closest = compare(newcodebook, pixel)
        #print closest
        pixels[index] = closest
    root = Toplevel()
    newimage = Image.new(image.mode, image.size)
    newimage.putdata(pixels)
    newimage.save('sample1.png', "PNG")
    im = Image.open('sample1.png')
    tkimage = ImageTk.PhotoImage(im)
    panel = Label(root, image=tkimage)
    panel.pack()
    qb = Button(root, text='QUIT', command=combine_funcs(root.destroy, root.quit))
    qb.pack()
    root.mainloop()


def execute():
    clusters=int(content2.get())    
    s=content.get()
    dirlist = os.listdir(s)
    for x in dirlist:
        y = Image.open(x)
        entropy(y,clusters)
        print 'Clustering is done'
                 
top =Tk()
top.geometry("500x500+100+100")
text=Text(top,height='1',padx='75')
text.insert(INSERT,"Image Clustering in Python")
text.insert(END,"")
text.pack()
L1 = Label(top, text="Select the input folder/single image").pack()
content=StringVar()
E1 = Entry(top,textvariable=content).pack()
B =Button(top, text ="Browse", command = browse)
B.pack()
L2 = Label(top, text="No of Clusters you want").pack()
content2=StringVar()
E2 = Entry(top,textvariable=content2).pack()
B2 =Button(top, text ="OK", command = execute)
B2.pack()
top.mainloop()

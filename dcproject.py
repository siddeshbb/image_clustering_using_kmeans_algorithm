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

codelist = dict()

def browse():
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=top, initialdir=currdir, title='Please select a directory')
    content.set(tempdir)
        
def browsefile():
    filename = askopenfilename(parent=top)
    f = open(filename)
    content3.set(filename)
    
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

number = 0

def cluster(image, k):
    global number
    pixels = list(image.getdata())
    obs1 = array(pixels)
    codebook,distortion = kmeans(obs1, k)
    newcodebook = [tuple(x) for x in codebook]
    for index, pixel in enumerate(pixels):
        closest = compare(newcodebook, pixel)
        pixels[index] = closest
    root = Toplevel()
    newimage = Image.new(image.mode, image.size)
    newimage.putdata(pixels)
    path = 'output\op' + str(number) + '.png'
    number = number + 1
    codelist[path] = newcodebook
    newimage.save(path, "PNG")
    l1=Label(root,text="Clustered Image")
    l1.pack()
    root.geometry("+100+100")
    im = Image.open(path)
    tkimage = ImageTk.PhotoImage(im)
    panel = Label(root, image=tkimage)
    panel.pack()
    qb = Button(root, text='QUIT',fg='#CC0000',bg='#3399FF', command=combine_funcs(root.destroy, root.quit))
    qb.pack()
    root.mainloop()
    
def compare_images(orig_path, clus_path, t):
    show = Toplevel()
    show.title(t)
    im = Image.open(orig_path)
    w, h = im.size
    tkimage = ImageTk.PhotoImage(im)
    panel = Label(show, image=tkimage)
    panel.pack()
    clus_path.replace('\\\\', '\\')
    orig_path.replace('\\\\', '\\')
    im1 = Image.open(clus_path)
    w1, h1 = im1.size
    tkimage1 = ImageTk.PhotoImage(im1)
    panel1 = Label(show, image=tkimage1)
    panel1.place(x=h1)
    panel1.pack()
    qb = Button(show, text='QUIT',fg='#CC0000',bg='#3399FF', command=combine_funcs(show.destroy, show.quit))
    qb.pack()
    show.mainloop()

def findclosest(codebook, k):
    code = codelist.values()
    code = [x for x in code if len(x) == k]
    returning = code[0]
    for index, x in enumerate(code):
        s1,s2 = 0,0
        for a,b in zip(x,codebook):
            s1 += sum(a)
            s2 += sum(b)
        if index == 0:
            avg = abs(s1-s2)
            returning = x
        else:
            if abs(s1-s2) < avg:
                avg = abs(s1-s2)
                returning = x
    return returning, avg
            
def check():
    ss=content3.get()
    ss.replace('\\\\', "\\")
    image = Image.open(ss)
    pixels = list(image.getdata())
    pixels = array(pixels)
    k = int(content2.get())
    codebook,_ = kmeans(pixels, k)
    codebook = [tuple(x) for x in codebook]
    out=Toplevel()
    closest,distortion = findclosest(codebook, k)
    if distortion < k*10:
        L=Label(out,text="Image Found")
        L.pack()
        path = codelist.keys()[codelist.values().index(closest)]
        compare_images(ss, path, 'Image Display')
    else:
        L=Label(out,text="Image Not Found")
        L.pack()
    qb = Button(out, text='QUIT', command=combine_funcs(out.destroy, out.quit),fg='#CC0000',bg='#3399FF')
    qb.pack()
    out.mainloop()
    
    
def execute():
    clusters=int(content2.get())    
    s = content.get()
    s = s + '/'
    dirlist = os.listdir(s)
    dirlist = [s+x for x in dirlist]
    folder = 'output'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            os.unlink(file_path)
        except Exception, e:
            print e
    for x in dirlist:
        y = Image.open(x)
        cluster(y,clusters)
        print 'Image is Clustered'

top =Tk()
top.title('Image Clustering')
top.geometry("300x350+100+100")
img = Image.open("label.png")
photoImg = ImageTk.PhotoImage(img)
text=Label(top,padx='33',font="TimesNewRoman",text="Image Clustering Using Kmeans",image=photoImg)
text.image = photoImg
text.pack()
L1 = Label(top, text="Select the Image folder to be used as Database",fg='brown').pack()
content=StringVar()
E1 = Entry(top,textvariable=content).pack()
B =Button(top, text ="Browse", command = browse,fg='#CC0000',bg='#3399FF')
B.pack()
L2 = Label(top, text="No of Clusters you want",fg='brown').pack()
content2=StringVar()
E2 = Entry(top,textvariable=content2).pack()
B2 =Button(top, text ="OK", command = execute,fg='#CC0000', bg='#3399FF')
B2.pack()
L3 = Label(top, text="Enter the input image",fg='brown').pack()
content3=StringVar()
E3 = Entry(top,textvariable=content3).pack()
B3 =Button(top, text ="Browse file", command = browsefile,fg='#CC0000', bg='#3399FF')
B3.pack()
B4 =Button(top, text ="Check whether the Image is present in the Database", command = check,fg='#CC0000', bg='#3399FF')
B4.pack()
qb = Button(top, text='QUIT', command=combine_funcs(top.destroy, top.quit),fg='#CC0000',bg='#3399FF')
qb.pack()
top.mainloop()

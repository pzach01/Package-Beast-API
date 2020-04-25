import os


os.chdir("C:\\Users\\lucas\\Desktop")
os.chdir("Box Stuff Core Python Only")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import box_stuff2
import rendering
import random

r=random.Random()






class BoxClicker(object):
    ind = 0
    
    
    def __init__(self):
        self.bins=[]
        self.boxes=[]
        bins=['96x80x52' for ele in range(0,1)]
        boxes=['82x50x35']+['54x41x12']+['21x6x7']
        cost=None


        self.binList,self.packageList=box_stuff2.master_calculate_optimal_solution(bins,boxes,costList=[10,10,1000])
        print(str(len(self.binList))+' bins.')
        print('-----------------------------')
    '''
    def hide_button(self,button):
        button.ax.patch.set_visible(False)
        button.label.set_visible(False)
        button.ax.axis('off')
        button.set_active(False)
    def hide_axis(self):
        ax.set_visible(not ax.get_visible())
    def show_button(self,button):
        button.ax.patch.set_visible(True)
        button.label.set_visible(True)
        button.ax.axis('on')
        button.set_active(True)
    
    '''

    def clear_figure(self):
        fig = plt.figure(num=1, clear=True)   #clear contents of window

    # currently  renders and calculates optimal solution
    def special(self, event):   
      
        ### calculate the result for an arrangment of a bin that is 10x10x10 and 2 objects that are 5x5x5

        
        
        #rendering.render_bin(binList[0],packageList[0])        
        
        bin=self.binList[self.ind]
        boxes=self.packageList[self.ind]
        
        
        print("Bin "+str(self.ind))        
        print(bin)
        print('Contains '+str(len(boxes))+ ' boxes.')
        print(boxes)
        print('---------------------------------')  
        
        # This import registers the 3D projection, but is otherwise unused.
        supportedColors=['red','blue','green','magenta','cyan','yellow']
        x, y, z = np.indices((bin.length,bin.width ,bin.heigth))   
        cubeList=[]
        for key in boxes.keys():
            upperZ=key[0]+(boxes[key].heigth/2)
            lowerZ=key[0]-(boxes[key].heigth/2) 
            upperY=key[1]+(boxes[key].width/2)
            lowerY=key[1]-(boxes[key].width/2)
            
            upperX=key[2]+(boxes[key].length/2)
            lowerX=key[2]-(boxes[key].length/2)
    
    
            cube = ((x>lowerX)&(x < upperX)) & (((y>lowerY)& (y<upperY)) & ((z>lowerZ)& (z<upperZ)))
            cubeList.append(cube)
        voxels=cubeList[0]
        for element in cubeList:
            voxels=voxels|element
            
        colors = np.empty(voxels.shape, dtype=object)
        for element in cubeList:
            colors[element]=supportedColors[random.randint(0,5)]
        
        # and plot everything
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.voxels(voxels, facecolors=colors, edgecolor='k')        
        
        
        
        

        
        plt.draw()   

    def to_graphs(self, event):
        self.clear_figure()
        
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(callback.next)
        
        
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(callback.prev)
        
        axspec = plt.axes([0.59, 0.05, 0.1, 0.075])
        bspec = Button(axspec, 'Render')
        bspec.on_clicked(callback.special)
        
        
        axtoui = plt.axes([0.41, 0.05, 0.1, 0.075])
        btoui = Button(axtoui, 'New Arrangment')
        btoui.on_clicked(callback.to_ui)  
        
        
        plt.draw()        


        
    def next(self, event):
        self.ind += 1
        bin=self.binList[self.ind]
        boxes=self.packageList[self.ind]

        plt.draw()

    def prev(self, event):
        self.ind -= 1
        bin=self.binList[self.ind]
        boxes=self.packageList[self.ind]   
   
        
        
        
    def to_ui(self,event):
        #self.hide_button(bnext)
        #self.hide_button(bprev)
        #self.hide_button(bspec)
        #self.hide_axis()
        self.clear_figure()

        
        
        plt.draw()        
        
        

    


    def up(self, event):
        pass
    def down(self, event):
        pass
        
freqs = np.arange(2, 20, 3)
        
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
t = np.arange(0.0, 1.0, 0.001)
s = np.sin(2*np.pi*freqs[0]*t)
l, = plt.plot(t, s, lw=2)
plt.axis('off')


callback = BoxClicker()
#axprev=plt.axes([1,1,1,1])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)


axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

axspec = plt.axes([0.59, 0.05, 0.1, 0.075])
bspec = Button(axspec, 'Render')
bspec.on_clicked(callback.special)




# get rid of other ui renderings










plt.draw()



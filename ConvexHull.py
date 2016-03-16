# -*- coding: cp936 -*-
'''
Javis March
'''

import sys
import numpy as np
import os
import math

# Function to know if we have a CCW turn
def CCW(p1, p2, p3):
        if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
                return True
        return False

# Main function:
def GiftWrapping(S):
        n = len(S)
        P = [None] * n
        l = np.where(S[:,0] == np.min(S[:,0]))
        pointOnHull = S[l[0][0]]
        i = 0
        while True:
                P[i] = pointOnHull
                P[i] = list(P[i]) #array to list
                endpoint = S[0]
                for j in range(1,n):
                        if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not CCW(S[j],P[i],endpoint):
                                endpoint = S[j]
                i += 1
                pointOnHull = endpoint
                if endpoint[0] == P[0][0] and endpoint[1] == P[0][1]:
                        break
        for i in range(n):
                if P[-1] == None:
                        del P[-1]
        return P

''' Compute the polygonal area. '''

def GetAreaOfTri(a, b ,c):     
        vec1 = [(a[0]-b[0])*55.66,(a[1]-b[1])*110.94]#1 longtitude = 55.66km, 1 latitude = 110.94km
        vec2 = [(b[0]-c[0])*55.66,(b[1]-c[1])*110.94]
        vec = [vec1, vec2]
        return abs(np.linalg.det(vec)/2)

def GetAreaOfCH(points):
        if len(points) < 3:
                Exception('at least 3 points')
        area = 0
        recordp=[]#to record the original vertices' coordinates
        for i in range(len(points)-2):
                area +=GetAreaOfTri(points[0], points[1], points[2])
                recordp.append(points[1])
                del points[1]
        recordp.insert(0,points[0])
        recordp.append(points[1])
        return area,recordp

def GetDistance(a,b):
    vec1 = [(a[0]-b[0])*55.66,(a[1]-b[1])*110.94]
    return math.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
    
#-----data computing--------------------------
class cluster:
    def __init__(self,name,points,area,hotindex):
        self.name=name
        self.points=points
        self.area=area
        self.hotindex=hotindex
    def __repr__(self):
      #  return repr((self.name,self.points,self.area,self.hotindex))
        return repr((self.hotindex))
    def center(self):
        cp=[0,0]
        number=0
        for point in self.points:
            cp[0]+=point[0]
            cp[1]+=point[1]
            number+=1
        for p in cp:
            p=p/number
        return cp

def dm(pointdir,index):
    mapdir={}
    for i in range(36*index+1):
        mapdir.setdefault(i,{})
        for j in range(22*index+1):
            mapdir[i].setdefault(j,[]) 
            mapdir[i][j]=0
            
    a=0
    b=0
    for point in pointdir:
        x=int((round(point[0]*2,2)/2-121.31)/(0.01/index))
        y=int((round(point[1]*2,2)/2-31.1)/(0.01/index))
        if x<=(36*index) and y<=(22*index) and x>=0 and y>=0:
            mapdir[x][y]+=1
            a+=1
        else:
            b+=1
    print 'fitted:'+str(a)+' dropped:'+str(b)
    
    file_object=open('densitymap.txt','w')
    lat=floatrange(121.31,121.67,36*index+1)
    longt=floatrange(31.1,31.32,22*index+1)
    sum=0
    number=0
    for i in lat:
        for j in longt:
            x=int((i-121.31)/(0.01/index))
            y=int((j-31.1)/(0.01/index))
            line=str(i)+' '+str(j)+' '+str(mapdir[x][y])+'\n'
            number+=1
            sum+=mapdir[x][y]
            file_object.write(line)
    print sum,number
    file_object.close()    
    

def floatrange(start,stop,steps):
        return [round(start+(float(i)*(stop-start)/(float(steps)-1)),3) for i in range(steps)]

def isinvertex(x,y,points,res):
    checkpoint=[x,y]
    area=0
    area+=GetAreaOfTri(points[0], points[-1], checkpoint)
    for i in range(len(points)-1):
        area+=GetAreaOfTri(points[i], points[i+1], checkpoint)
    if area<res+0.001:
        return True
    else:
        return False

def localgi(cluses):
    clusteres=[]
    avex=0
    number=0
    for clus in cluses:
        avex+=clus.hotindex
        number+=1
    avex=avex/number

    xj2sum=0
    for clus in cluses:
        xj2sum+=clus.hotindex*clus.hotindex
    s=math.sqrt(xj2sum/number-avex*avex)

    for clus in cluses:
        wijxjsum=0
        wijsum=0
        wij2sum=0
        for clus2 in cluses:
            if GetDistance(clus.center(),clus2.center())>0:
                wij=1/GetDistance(clus.center(),clus2.center())
            else:
                wij=0   
            wijxjsum+=wij*clus2.hotindex
            wijsum+=wij
            wij2sum+=wij*wij
        gi=(wijxjsum-avex*wijsum)/(math.sqrt((number*wij2sum-wijsum*wijsum)/(number-1))*s)
        clusteres.append(cluster(clus.name,clus.points,clus.area,gi))
    return clusteres

def mapgrading(dailycluster,filename,precision):
        x=floatrange(121.31,121.67,precision)
        y=floatrange(31.1,31.32,precision)
        dailycluster=sorted(dailycluster,key=lambda cluster:abs(cluster.hotindex),reverse=True)
        mapdir={}
        maptxt=str(filename)+'.txt'
        file_object=open(maptxt,'w')
        number=0
        for i in range(precision-1):
                mapdir.setdefault(i,{})
                for j in range(precision-1):
                        mapdir[i].setdefault(j,[]) 
                        mapdir[i][j]=0
                        for c in dailycluster:
                            boolv=isinvertex(x[i],y[j],c.points,c.area)
                            if boolv==True:
                                mapdir[i][j]=c.hotindex
                                number+=1
                                print number
                                break
                        line=str(x[i])+' '+str(y[j])+' '+str(mapdir[i][j])+'\n'
                        file_object.write(line)
        file_object.close()
        mom=precision*precision
        print str(number)+' points have been matched in '+str(mom)+' points'
        return mapdir
        
def avegrade(mapdir,precision):
    file_object=open('hotmap.txt','w')
    avemap={}
    x=floatrange(121.31,121.67,precision)
    y=floatrange(31.1,31.32,precision)
    for i in range(precision-1):
                avemap.setdefault(i,{})
                for j in range(precision-1):
                        avemap[i].setdefault(j,[]) 
                        avemap[i][j]=0
    for dailymap in mapdir:
        for i in range(precision-1):
            for j in range(precision-1):
                if mapdir[dailymap][i][j]==0:
                    pass
                else:
                    avemap[i][j]+=mapdir[dailymap][i][j]
    dirlength=len(mapdir)
    for i in range(precision-1):
        for j in range(precision-1):
            if avemap[i][j]==0:
                pass
            else:
                avemap[i][j]=avemap[i][j]/dirlength 
            line=str(x[i])+' '+str(y[j])+' '+str(avemap[i][j])+'\n'
            file_object.write(line)       
    file_object.close()
    return avemap

def main(precision): 
    file_path=os.path.dirname(__file__)
    daydirs=os.listdir(file_path)
    datadir={}
    hotmap={}
    for d in daydirs:
        if d.startswith('Origin'):
            fullroot=os.path.join(file_path,d)
            ox,oy  = np.loadtxt(fullroot, delimiter=',', usecols=(1,2), unpack=True)
            P = np.column_stack((ox, oy))#ox,oy are 1 colume vector, this to be a 2D array
            print len(P)
            dm(P,2)
        '''
        if d.startswith('11'):
            subdir=os.path.join(file_path,d)
            if os.path.isdir(subdir):
                datadir.setdefault(d,[])
                hotmap.setdefault(d,{})
                for root,dirs,files in os.walk(subdir):
                        sum=0
                        for file  in files:
                                areaname=file.split('.')[0]
                                fullroot=os.path.join(root,file)
                                ox,oy  = np.loadtxt(fullroot, delimiter=',', usecols=(0,1), unpack=True)
                                P = np.column_stack((ox, oy))#ox,oy are 1 colume vector, this to be a 2D array
                                if len(P)>3:
                                    points = GiftWrapping(P)
                                    res,recordp = GetAreaOfCH(points)
                                    hotindex=len(P)/res
                                    datadir[d].append(cluster(areaname,recordp,res,hotindex))
                datadir[d]=localgi(datadir[d])
                hotmap[d]=mapgrading(datadir[d],d,precision)
                print [str(d),'finished']
        '''
    #avemap=avegrade(hotmap,precision)
         
if __name__ == '__main__':
  main(100)



import numpy
import pandas
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

sbi=pandas.read_csv("sbi1.csv", parse_dates=True, index_col=0)
sbi= sbi['Close']
pos=0
profit=0
lstpos=0
diff=0
prf=[]
n = len(sbi)
for i in range(0,n-5):
    u=sbi[i:i+5]
    sbi1=[]
    sbi2=[]
    sbi3=[]
    sbi4=[]
    sbi5=[]
    
    for k in range(i,i+5):
        x=sbi[k+1]-sbi[k]
        sbi1.append(x)
    for l in range(4):
        y=sbi1[l+1]-sbi1[l]
        sbi2.append(y)
    for m in range(3):
        z=sbi2[m+1]-sbi2[m]
        sbi3.append(z)
    for n in range(2):
        t=sbi3[n+1]-sbi3[n]
        sbi4.append(t)
    for o in range(1):
        h=sbi4[o+1]-sbi4[o]
        sbi5.append(h)
    last= sbi[i] + 5*sbi1[0]+ 10*sbi2[0]+ 10*sbi3[0]+ 5*sbi4[0]+ sbi5[0]
    xyz= numpy.mean(u)
    temp=sbi[i+5]
    if (last>xyz):
        print ("Buy")
        if (pos==(-1)):
            pos=pos+2
            diff=lstpos-sbi[i]
            profit=(profit+diff)-(0.02*lstpos)
            lstpos=sbi[i]
            
        elif (pos==0):
            pos=pos+1
            profit=(profit+diff)
            lstpos=sbi[i]
    else :
        print ("Sell")
        if (pos==1):
            pos=pos-2
            diff=sbi[i]-lstpos - (0.02*lstpos)
            profit=(profit+diff)
            lstpos=(sbi[i])
        elif (pos==0):
            pos=pos-1
            profit=(profit+diff)
            lstpos=(sbi[i])
    print (sbi[i])
    print (profit)
    prf.append(profit)



plt.plot(prf)

plt.show()

    

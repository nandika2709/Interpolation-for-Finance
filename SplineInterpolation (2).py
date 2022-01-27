#!/usr/bin/env python
# coding: utf-8

# Q1) A)

# In[158]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta, MO
from datetime import datetime, timedelta 
from dateutil.relativedelta import relativedelta
get_ipython().run_line_magic('matplotlib', 'inline')
from gekko import GEKKO


# In[159]:


df = pd.read_excel("/Users/NANDIKA/DTU/semester 4/SC/project/yieldcurve_interpolation/Cublic_Spline.xlsx")


# In[160]:


df


# In[120]:


m= GEKKO()
xm=[1,2,3,6,12,24,36,60,84,120,240,360]
for i in range(1,79):
    ym = df.iloc[i-1:i, 1:13]
    ym = ym.values.tolist()[0]
    m= GEKKO()
    m.x = m.Param(value= np.linspace(0,360))
    m.y = m.Var()
    m.cspline(m.x,m.y,xm,ym)
    m.options.IMODE=2
    m.solve(disp=False)
    

    plt.plot(xm,ym,'bo',label='data')
    plt.plot(m.x,m.y,'r--',label='cubic spline')
    print(i)
    plt.show()


# Q1) B) 

# End of the Months Yield (31 Jan 2020, 28 Feb 2020, 31 March 2020 )

# In[122]:


xm=[1,2,3,6,12,24,36,60,84,120,240,360]
row_end=[21,40,62]
for i in row_end:
    ym = df.iloc[i-1:i, 1:13]
    ym = ym.values.tolist()[0]
    m= GEKKO()
    m.x = m.Param(value= np.linspace(0,360))
    m.y = m.Var()
    m.cspline(m.x,m.y,xm,ym)
    m.options.IMODE=2
    m.solve(disp=False)
    print(ym)

    plt.plot(xm,ym,'bo',label='data')
    plt.plot(m.x,m.y,'r--',label='cubic spline')
    print(i)
    plt.show()


# 

# In[123]:


#Spot Rates
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
xm=[1,2,3,6,12,24,36,60,84,120,240,360]
row_end=[21,40,62]
for i in row_end:
    ym = df.iloc[i-1:i, 1:13]
    ym = ym.values.tolist()[0]
    tenor= np.array(xm)
    yields= np.array(ym)
    cs= CubicSpline(tenor, yields, bc_type='natural')
    curvepoints=np.linspace(min(tenor),max(tenor),10000)
    plt.plot(curvepoints,cs(curvepoints),label="Spot Rates")
   


# In[124]:


#Instantaneous Forward Rates
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
xm=[1,2,3,6,12,24,36,60,84,120,240,360]
row_end=[21,40,62]
for i in row_end:
    ym = df.iloc[i-1:i, 1:13]
    ym = ym.values.tolist()[0]
    tenor= np.array(xm)
    yields= np.array(ym)
    cs= CubicSpline(tenor, yields, bc_type='natural')
    curvepoints=np.linspace(min(tenor),max(tenor),10000)

    plt.plot(curvepoints,(cs(curvepoints)+cs(curvepoints,1)*curvepoints),label="Instantaneous Forward Rates")
    


# Q1) c)
# Daily Yield Curve: (Analysis)
# During the months of January and February, partial inversion of yield curves are nooticed towards the left end of the spectrum. That is the short term rates are higher than the long term rates. Historically speaking a inversion of a yield curve is supposed to be a strongly correlated indicator of bare markets or a recession. However, the most common indicator used by investors which influences their investing decisions or to predict recession, is the SPREAD between the 10YR treasuries and 2YR treasuries in order to check for the inversion. As we can see from the discrete data as well as the cubic spline fitted graph, the curve is NORMAL in the spread between 2YR and 10YR. So the investors would not be fearing a recession. 
# By the end of March however, we notice that the yield curve is completely normal between 1month and 30YR.

# Q2) a)

# In[349]:


df2 = pd.read_excel("/Users/NANDIKA/DTU/semester 4/SC/project/yieldcurve_interpolation/m.xlsx")


# In[350]:


df2


# In[351]:


df_date = pd.to_datetime(df['Date'], format='%d%b%Y:%H:%M:%S.%f')


# In[352]:


df2 = pd.read_excel("/Users/meetshah/Desktop/Final/m.xlsx")
df2_cp = pd.to_datetime(df2['First Coupon'], format='%d%b%Y:%H:%M:%S.%f')
df2_mt = pd.to_datetime(df2['Maturity'], format='%d%b%Y:%H:%M:%S.%f')
df2_cp.head()


# In[353]:


df2_mt = pd.to_datetime(df2['Maturity'], format='%d%b%Y:%H:%M:%S.%f')
df2_mt[0]


# In[ ]:





# In[371]:


xm=[1,2,3,6,12,24,36,60,84,120,240,360]
final_eq=[]
for q in range(78):
    df2 = pd.read_excel("/Users/NANDIKA/DTU/semester 4/SC/project/yieldcurve_interpolation/m.xlsx")
    df2_cp = pd.to_datetime(df2['First Coupon'], format='%d%b%Y:%H:%M:%S.%f')
    df2_mt = pd.to_datetime(df2['Maturity'], format='%d%b%Y:%H:%M:%S.%f')
    ym = df.iloc[q:q+1,1:13]
    ym = ym.values.tolist()[0]
    tenor= np.array(xm)
    yields= np.array(ym)
    cs= CubicSpline(tenor, yields, bc_type='natural')
    curvepoints=np.linspace(min(tenor),max(tenor),10000)
    result=[]
    ytm=[]
    rb365=[]
    eq=[]
    cp= df2_cp
    mt = df2_mt
    for i in range(17):
        temp =[]
        tempytm=[]
        temprb_arr=[]
        temp_sum=0
        tempcs =0
        while mt[i]>=cp[i]: 

            temp.append((cp[i]-df_date[q]).days)
            cs_val=((cp[i]-df_date[q]).days)/30
            tempcs = cs(cs_val)
            tempcs_1 = 1+(float(tempcs)/100)
            temprb = ((cp[i]-df_date[q]).days)/365
            tempcspower= (tempcs_1)**temprb
            re_tempcspower = tempcspower**-1
            temp_sum+=re_tempcspower
            tempytm.append(tempcs)
            temprb_arr.append(temprb)
            cp[i] = cp[i] + relativedelta(months=+6)
        temp_sum*= (df2['Coupon'][i])/2
        temp_sum += (re_tempcspower*100)
        result.append(temp)
        ytm.append(tempytm)
        eq.append(temp_sum)
        rb365.append(temprb)
    
    final_eq.append(eq)
print(final_eq)


# In[374]:


print(final_eq)


# ##Q2) b)

# In[375]:


fin = []
for i in range(len(final_eq)-1):
    for j in range(len(final_eq[i])):
        value = (final_eq[i+1][j]-final_eq[i][j])/final_eq[i][j]
        fin.append(value)
print(fin)


# In[ ]:





# Q2) c)
# Instantaneous Forward Rate: (Analysis)
# We do observe that the interest rates during these times are fluctuating rather harshly. From the Instantaneous Forward Rate curve, which is essentially the slope of the spot rates, we could see that the forward rate curve keeps dropping as the time progresses. However, the curve also indicates that the longer maturity bond yields are still higher than the shorter maturity bonds. This shows that the investors could cash in by riding the yield curve, that is, buy longer maturity bonds and selling them before they mature so as to profit from the declining yields.

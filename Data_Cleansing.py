import pandas as pd
import numpy as np
df=pd.read_csv('dirty_data.csv')
print(df.columns)
df.rename(columns={"Unnamed: 0":'Id'},inplace=True)
for i,j in df.iterrows():
    if j['Id'][2:3]=='1':
        df.loc[i,'Uber Type']=0
    elif j['Id'][2:3]=='3':
        df.loc[i,'Uber Type']=1
    elif j['Id'][2:3]=='5':
        df.loc[i,'Uber Type']=2
print(df)
# plt.hist(df['Origin Region'],bins=20)
for i,j in df.iterrows():
    if j['Origin Latitude'] > 0:
        df.loc[i,'Origin Latitude']=-j['Origin Latitude']
    if j['Destination Latitude'] > 0:
        df.loc[i,'Destination Latitude']=-j['Destination Latitude']
year=[]
month=[]
day=[]
for i,j in df.iterrows():
    q=j['Departure Date'].split('-')
    if int(q[1])>12:
        q[1],q[2]=q[2],q[1]
    df.loc[i,'Departure Date']='-'.join(q)
    year.append(q[0])
    month.append(q[1])
    day.append(q[2])
for i in range(283):
    if month[i]=='2' and int(day[i])>28:
        day[i]='28'
    elif (int(month[i])==2 or int(month[i])==4 or int(month[i])==6 or int(month[i])==9 or int(month[i])==11) and int(day[i])>30:
        day[i]='30'
    elif (int(month[i])==1 or int(month[i])==3 or int(month[i])==5 or int(month[i])==7 or int(month[i])==8 or int(month[i])==10 or int(month[i])==12) and int(day[i])>31:
        day[i]='31'
list=[]
for i in range(283):
    l=[day[i],month[i],year[i]]
    list.append(l)
for i in range(283):
    df.loc[i,'Departure Date']='-'.join(list[i])
hour=[]
min=[]
sec=[]
for i,j in df.iterrows():
    q=j['Departure Time'].split(':')
    hour.append(q[0])
    min.append(q[1])
    sec.append(q[2])
for i in range(283):
    if int(hour[i])>23:
        hour[i]=='23'
    elif int(min[i])>59:
        min[i]='59'
    elif int(sec[i])>59:
        sec[i]='59'
hour1=[]
min1=[]
sec1=[]
for i,j in df.iterrows():
    q=j['Arrival Time'].split(':')
    hour1.append(q[0])
    min1.append(q[1])
    sec1.append(q[2])
for i in range(283):
    if int(hour1[i])>23:
        hour1[i]=='23'
    elif int(min1[i])>59:
        min1[i]='59'
    elif int(sec1[i])>59:
        sec1[i]='59'
for i in range(283):
    if int(hour[i])>int(hour1[i]):
        hour1[i]=str(24+int(hour1[i]))
at_sec=[]
dp_sec=[]
for i in range(283):
    dp_sec.append(int(hour[i])*3600+int(min[i])*60+int(sec[i]))
    at_sec.append(int(hour1[i])*3600+int(min1[i])*60+int(sec1[i]))
cal_time=[]
for i in range(283):
    cal_time.append(abs(at_sec[i]-dp_sec[i]))
speed_given=[]
speed_calc=[]
for i,j in df.iterrows():
    q=(j['Journey Distance(m)']/j['Travel Time(s)'])
    speed_given.append(q)
    w=cal_time[i]
    speed_calc.append(j['Journey Distance(m)']/w)
sg=np.array(speed_given)
sg=sg*(18/5)
sc=np.array(speed_calc)
sc=sc*(18/5)
df.to_csv('Undirty Data.csv',index=False)
gf=pd.read_csv('outliers.csv')
olan_mean=gf['Origin Latitude'].mean()
olon_mean=gf['Origin Longitude'].mean()
dlan_mean=gf['Destination Latitude'].mean()
dlon_mean=gf['Destination Longitude'].mean()
olan_std=np.std(gf['Origin Latitude'])
olon_std=np.std(gf['Origin Longitude'])
dlan_std=np.std(gf['Destination Latitude'])
dlon_std=np.std(gf['Destination Longitude'])
a=0
b=0
c=0
d=0
for i,j in gf.iterrows():
    if abs(j['Origin Latitude']-olan_mean)> olan_std*2:
        gf=gf.drop(i)
        a+=1
    elif abs(j['Origin Longitude']-olon_mean)> olon_std*2:
        gf=gf.drop(i)
        b+=1
    elif abs(j['Destination Latitude']-dlan_mean)> dlan_std*2:
        gf=gf.drop(i)
        c+=1
    elif abs(j['Destination Longitude']-dlon_mean)> dlon_std*2:
        gf=gf.drop(i)
        d+=1
ff=pd.read_csv('missing_value.csv')
ff.rename(columns={"Unnamed: 0":'Id'},inplace=True)
for i,j in ff.iterrows():
    if j['Id'][2:3]=='1':
        ff.loc[i,'Uber Type']=0
    elif j['Id'][2:3]=='3':
        ff.loc[i,'Uber Type']=1
    elif j['Id'][2:3]=='5':
        ff.loc[i,'Uber Type']=2
a=[]
b=[]
l=ff['Fare$'].isna()
for i in range(l.__len__()):
    if l[i]:
        a.append(ff.loc[i,'Journey Distance(m)'])
        b.append(ff.loc[i,'Uber Type'])
c=[]
d=[]
e=[]
for i in range(l.__len__()):
    if not l[i]:
        c.append(ff.loc[i,'Journey Distance(m)'])
        d.append(ff.loc[i,'Uber Type'])
        e.append(ff.loc[i,'Fare$'])
ff1=pd.DataFrame({'Journey Distance(m)':c,'Uber Type':d,'Fare$':e})
from sklearn import linear_model
find=[]
for i in range(a.__len__()):
    rg=linear_model.LinearRegression()
    rg.fit(ff1[['Journey Distance(m)','Uber Type']],ff1['Fare$'])
    find.append(*rg.predict([[a[i],b[i]]]))
find=list(find)
k=0
m=0
fare=[]
for i in range(l.__len__()):
    if l[i]:
        fare.append(find[k])
        k+=1
    else:
        fare.append(e[m])
        m+=1
ff.drop('Fare$',axis=1)
ff['Fare$']=fare
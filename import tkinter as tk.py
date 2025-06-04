from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error


# Obtenir la date et l'heure actuelles
lt = datetime.now().date()
lts = datetime.now().time()

print(lt)
res=[]
for i in range(20):
    new_time = (datetime.combine(datetime.now().date(), lts) + timedelta(hours=i)).time()
    r =str(new_time)
    if int(r[0:2]) >6 and int(r[0:2]) <= 18 :
        res.append(r[0:8])
    
# # Afficher la date et la nouvelle heure
# print(new_time)

# print(res)
li="je"
lid=[li,li,li,li,li,li,li,li,li,li]
lit=[1,2,3,4]
for i, j in zip(lid, lit):
    print(f"{i}: {j}")
    
ch= str(datetime.now())[:10] 

print(str(lts)[:2]>str(new_time)[:2])

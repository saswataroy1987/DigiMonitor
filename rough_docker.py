myclient = [ pymongo.MongoClient("mongodb://localhost:2017/"),pymongo.MongoClient("mongodb://localhost:2018/"),pymongo.MongoClient("mongodb://localhost:2019/"),pymongo.MongoClient("mongodb://localhost:2020/"),pymongo.MongoClient("mongodb://localhost:2021/") ]

mydb = []

for temp in myclient:
    mydb.append(temp["RealData"])



cursor.close()

#<------------2hour--------------->
sum_2hour =0
for i in range(5):
	mycol2hour=mydb[i]["test2hour"]
	sum_2hour = sum_2hour + mycol2hour.count()

cursor = []
for i in range(5):
	mycol2hour=mydb[i]["test2hour"]
	cursor2hour = list(mycol2hour.find(no_cursor_timeout=True))
	cursor.extend(cursor2hour)

for i in range(5):
	mycol2hour=mydb[i]["test2hour"]
	result_del=mycol2hour.delete_one(ele)

for i in range(5):
	mycol2hour=mydb[i]["test2hour"]
	mycol2hour.remove({})


#<------------10min--------------->
sum_10min =0
for i in range(5):
	mycol10min=mydb[i]["test10min"]
	sum_10min = sum_10min + mycol10min.count()

cursor = []
for i in range(5):
	mycol10min=mydb[i]["test10min"]
	cursor10min = list(mycol10min.find(no_cursor_timeout=True))
	cursor.extend(cursor10min)

for i in range(5):
	mycol10min=mydb[i]["test10min"]
	result_del=mycol10min.delete_one(ele)


for i in range(5):
	mycol10min=mydb[i]["test10min"]
	mycol10min.remove({})

#<------------ve--------------->
sum_ve =0
for i in range(5):
	mycol_ve=mydb[i]["ve"]
	sum_ve = sum_ve + mycol_ve.count()

cursor = []
for i in range(5):
	mycol_ve=mydb[i]["ve"]
	cursor_ve = list(mycol_ve.find(no_cursor_timeout=True))
	cursor.extend(cursor_ve)

for i in range(5):
	mycol_ve=mydb[i]["ve"]
	result_del=mycol_ve.delete_one(ele)

for i in range(5):
	mycol_ve=mydb[i]["ve"]
	mycol_ve.remove({})

#<------------nve--------------->
sum_nve =0
for i in range(5):
	mycol_nve=mydb[i]["nve"]
	sum_nve = sum_nve + mycol_nve.count()

cursor = []
for i in range(5):
	mycol_nve=mydb[i]["nve"]
	cursor_nve = list(mycol_nve.find(no_cursor_timeout=True))
	cursor.extend(cursor_nve)

for i in range(5):
	mycol_nve=mydb[i]["nve"]
	result_del=mycol_nve.delete_one(ele)

for i in range(5):
	mycol_nve=mydb[i]["nve"]
	mycol_nve.remove({})


#<------------rv--------------->
sum_rv =0
for i in range(5):
	mycol_rv=mydb[i]["rv"]
	sum_rv = sum_rv + mycol_rv.count()

cursor = []
for i in range(5):
	mycol_rv=mydb[i]["rv"]
	cursor_rv = list(mycol_rv.find(no_cursor_timeout=True))
	cursor.extend(cursor_rv)

for i in range(5):
	mycol_rv=mydb[i]["rv"]
	result_del=mycol_rv.delete_one(ele)

for i in range(5):
	mycol_rv=mydb[i]["rv"]
	mycol_rv.remove({})

#<------------nrv--------------->
sum_nrv =0
for i in range(5):
	mycol_nrv=mydb[i]["nrv"]
	sum_nrv = sum_nrv + mycol_nrv.count()

cursor = []
for i in range(5):
	mycol_nrv=mydb[i]["nrv"]
	cursor_nrv = list(mycol_nrv.find(no_cursor_timeout=True))
	cursor.extend(cursor_nrv)

for i in range(5):
	mycol_nrv=mydb[i]["nrv"]
	result_del=mycol_rv.delete_one(ele)

for i in range(5):
	mycol_nrv=mydb[i]["nrv"]
	mycol_nrv.remove({})

#-------------------------------------------------




cursor_ve = []
for i in range(5):
	mycol_ve=mydb[i]["ve"]
	cursor_veL = list(mycol_ve.find(no_cursor_timeout=True))
	cursor_ve.extend(cursor_veL)


cursor_nve = []
for i in range(5):
	mycol_nve=mydb[i]["nve"]
	cursor_nveL = list(mycol_nve.find(no_cursor_timeout=True))
	cursor_nve.extend(cursor_nveL)



cursor_rv = []
for i in range(5):
	mycol_rv=mydb[i]["rv"]
	cursor_rvL = list(mycol_rv.find(no_cursor_timeout=True))
	cursor_rv.extend(cursor_rvL)




cursor_nrv = []
for i in range(5):
	mycol_nrv=mydb[i]["nrv"]
	cursor_nrvL = list(mycol_nrv.find(no_cursor_timeout=True))
	cursor_nrv.extend(cursor_nrvL)
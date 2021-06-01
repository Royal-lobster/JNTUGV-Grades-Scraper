import requests
from bs4 import BeautifulSoup
import csv
##################################################
sem_codes = [1,2,12]
##################################################
class_rolls = ["19VV1A1201","19VV1A1202","19VV1A1203","19VV1A1204","19VV1A1205","19VV1A1206","19VV1A1207","19VV1A1208","19VV1A1209","19VV1A1210","19VV1A1211","19VV1A1212","19VV1A1213","19VV1A1214","19VV1A1215","19VV1A1216","19VV1A1217","19VV1A1218","19VV1A1219","19VV1A1220","19VV1A1221","19VV1A1222","19VV1A1223","19VV1A1224","19VV1A1225","19VV1A1226","19VV1A1227","19VV1A1228","19VV1A1229","19VV1A1230","19VV1A1231","19VV1A1232","19VV1A1233","19VV1A1234","19VV1A1235","19VV1A1236","19VV1A1237","19VV1A1238","19VV1A1239","19VV1A1240","19VV1A1241","19VV1A1242","19VV1A1243","19VV1A1244","19VV1A1245","19VV1A1246","19VV1A1247","19VV1A1248","19VV1A1249","19VV1A1250","19VV1A1251","19VV1A1252","19VV1A1253","19VV1A1254","19VV1A1255","19VV1A1256","19VV1A1257","19VV1A1258","19VV1A1259","19VV1A1260","19VV1A1261","19VV1A1262","19VV1A1263","18VV1A1250","20VV5A1267","20VV5A1268","20VV5A1269","20VV5A1270","20VV5A1271 ","20VV5A1272","20VV5A1273","20VV5A1274","20VV5A1275"]
url = 'https://results.jntukucev.ac.in/helper.php?jntuhcehpayOne=getResult'
extracted_data = []
for roll in class_rolls:
    cgpa = 0.0
    sgpa_arr = []
    sem_count = 0
    print("Currently Running " + roll)
    for sem_code in sem_codes:
        try:
            response = requests.post(url, data = {'hallticket': roll, "result" : sem_code})
            soup = BeautifulSoup(response.text, features="lxml")
            sgpa = soup.find("div", {"data-title": "SGPA"}).getText()
            try:
                sgpa_arr.append(float(sgpa))
            except:
                sgpa_arr.append("FAIL")
            try:
                cgpa = cgpa + float(sgpa)
            except:
                cgpa = "BACKLOG"
            sem_count = sem_count + 1
        except:
            sgpa_arr.append("NO DATA")
    if cgpa != "BACKLOG": cgpa = round(cgpa/sem_count,3)
    extracted_data.append({"ROLL" : roll, "CGPA" : cgpa, "SEM 1 (SGPA)" : sgpa_arr[0], "SEM 2 (SGPA)": sgpa_arr[1], "SEM 3 (SGPA)": sgpa_arr[2]})

field_names = ['ROLL', 'CGPA', 'SEM 1 (SGPA)', 'SEM 2 (SGPA)', 'SEM 3 (SGPA)']
with open('Results.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(extracted_data)
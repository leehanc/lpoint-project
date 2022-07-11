import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='asdf123', db='lpointv2', charset='utf8')
cur = conn.cursor()
custData, dateData, meanData, maxData, minData, num, lastdateData, meanbuyData, buyData = [], [], [], [], [], [], [], [], []
#custData, dateData, buyData : mysql 데이터 가져오기
# num : 이용일수 df 만들기 위한 list
# lastdateData : 마지막날 df 만들기 위한 list
# meanbuyData : 평균 일 이용액 df 만들기 위한 list
#  meanData, maxData, minData : 재구매기간 산정 df 만들기 위한 list
# checking = []
# # 하루에 두번 산 사람을 체킹하기 위한 list
cur.execute("SELECT cust, de_dt, buy_am FROM 엘페이이용 ORDER BY cust, de_dt DESC;")
while True:
    column = cur.fetchone()
    if column == None:
        break
    custData.append(column[0])
    dateData.append(column[1])
    buyData.append(column[2])
custData.append("zzzzzzz")
cust = []
for v in custData:
    if v not in cust:
        cust.append(v)
# print(len(cust))
cust_date_data = []
cal_data = []
cal_buy_data = [] # 고객이 한번에 이용한 이용액들의 list ( 평균을 구하기 위한 list)
# print(f"custdata : {len(custData)}, dataData {len(dateData)}")
for i in range(len(custData)-1):
    if custData[i] == custData[i+1]:
        cust_date_data.append(dateData[i])
        cal_buy_data.append(buyData[i])
    else:
        cust_date_data.append(dateData[i])
        cal_buy_data.append(buyData[i])
        # cust_date_data1 = cust_date_data
        lastdateData.append(cust_date_data[0])
        cust_date_data = list(set(cust_date_data))
        #이용날짜 겹치는 cust
        # if len(cust_date_data1) != len(cust_date_data):
        #     checking.append(custData[i])
        num.append(len(cust_date_data))
        cust_date_data.sort()
        print(cust_date_data)
        # print(cust_date_data)
        if len(cust_date_data) != 1:
            for i in range(len(cust_date_data)-1):
                cal_data.append([cust_date_data[i+1] - cust_date_data[i]][0].days)
            # print("여기")
            # print(cal_data)
            minData.append(min(cal_data))
            maxData.append(max(cal_data))
            avg = sum(cal_data) / len(cal_data)
            meanData.append(avg)
            meanbuyData.append(sum(cal_buy_data)/num[0])
        else:
            # print("두루와")
            minData.append(0)
            maxData.append(0)
            meanData.append(0)
            meanbuyData.append(cal_buy_data[0])
            # print(len(cust_date_data))
        cust_date_data = []
        cal_data = []
        cal_buy_data = []
# con.commit()
# con.close()
# print(meanData, maxData, minData)
# df=pd.DataFrame(custData, maxData, minData, meanData)
# print(df)
cust = cust[0:len(cust)-1]
print(f"cust : {len(cust)} \nmaxData : {len(maxData)} \nminData : {len(minData)} \nmeanData : {len(meanData)}\n{len(lastdateData)}\n{len(meanbuyData)}")
dict = {'cust' : cust, 'maxData' : maxData, 'minData' : minData, 'meanData' : meanData,
        'last_de_dt' : lastdateData ,'이용일수' : num, '평균 일 이용액' : meanbuyData}
df = pd.DataFrame(dict)
# df = pd.DataFrame([cust, maxData, minData, meanData], columns = ['cust', 'maxData', 'minData', 'meanData'])

print(df)
# print(f"cust : {len(cust)} \nmaxData : {sum(maxData)/len(cust)} \nminData : {sum(minData)/len(cust)} \nmeanData : {sum(meanData)/len(cust)}")
# df_dic = {'restID': custData, 'mean': meanData, 'max': maxData, 'min': minData}
# print(checking)
# print(len(checking))
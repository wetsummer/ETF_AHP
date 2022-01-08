# It requires 'pandas_datareader' and 'openpyxl'
from pandas.core.indexes.base import Index
from download_ETF_data import dt_down
from AHP_cal import return_val_date, AHP, AHP_score, AHP_const, AHP_const_index, AHP_const_ratio, AHP_random_const_index, AHP_random_const_index_inside
import pandas_datareader.data as web
import FinanceDataReader as fdr
import pandas, numpy, datetime, calendar, os, glob, random, multiprocessing, threading, math
from time import sleep

dt_down()
etf_list = pandas.read_excel(str(max(glob.iglob('data_*.xlsx'), key=os.path.getctime)), index_col=0)
# 0: 표준코드 1: 단축코드 2: 한글종목명 3: 한글종목약명 4: 영문종목명 5: 상장일 6: 기초지수명 7: 지수산출기관 8: 추적배수 9: 복제방법 10: 기초시장분류 11: 기초자산분류 12: 상장좌수 13: 운용사 14: CU수량 15: 총보수 16: 과세유형

etf_list = etf_list.drop(etf_list[etf_list['추적배수'] != '일반 (1)'].index) # 1배 추종 이외 제거
etf_list = etf_list.drop(etf_list[(etf_list['기초자산분류'] == '원자재') | (etf_list['기초자산분류'] == '통화')].index) # 1배 추종 이외 제거

# 상장된지 5년 지난 것만 남기기 시작
now_date = datetime.date.today() # 오늘 날짜
if now_date.month > 1:
    start_date_years = now_date.year - 5
    start_date_months = now_date.month - 1
else:
    start_date_years = now_date.year - 6
    start_date_months = 12

start_date = datetime.datetime.strptime(str(start_date_years) + '-' + str(start_date_months) + '-' + '1', '%Y-%m-%d').date()

untimed = etf_list[pandas.to_datetime(etf_list['상장일'], format='%Y-%m-%d') > pandas.to_datetime(start_date, format='%Y-%m-%d')].index
etf_list = etf_list.drop(untimed)
etf_list = etf_list.reset_index()
# 상장된지 5년 지난 것만 남기기 끝
#etf_list = etf_list[:5] #시험 운전용 개수 조절
#etf_list.sort_values(by=["상장좌수"], axis=0, ascending=False, inplace=True)
# 주가 가져오기 시작
code_list = etf_list['단축코드'].tolist() # 부호 얻기
#print(code_list)

(x, last_day) = calendar.monthrange(start_date.year + 5, start_date.month)
end_date = datetime.datetime.strptime(str(start_date.year + 5) + '-' + str(start_date.month) + '-' + str(last_day), '%Y-%m-%d').date()

etf_num = len(code_list)
save = numpy.empty(shape=(etf_num,6))
for code, num in zip(code_list, range(etf_num)):
    price = fdr.DataReader(str(code), start_date, end_date)

    # 거래일로 범위 조정 시작
    (year, month, day) = return_val_date(price, start_date.year, start_date.month, start_date.day)
    if numpy.logical_not(numpy.isnan(year)):
        start_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d').date()
        (year, month, day) = return_val_date(price, start_date.year + 5, start_date.month, last_day, 'back')
        if numpy.logical_not(numpy.isnan(year)):
            end_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d').date()
            # 거래일로 범위 조정 끝
        
            last_price = int(price['Close'][str(end_date)])

            (year, month, day) = return_val_date(price, start_date.year, start_date.month)
            save[num][0] = last_price / int(price['Close'][str(year) + '-' + str(month) + '-' + str(day)]) - 1 # 5년 수익률
            years_period = price['Close'][(str(year) + '-' + str(month) + '-' + str(day)):]
            save[num][1] = numpy.std((numpy.array(years_period[:-1].astype(int))/numpy.array(years_period[1:].astype(int))).reshape(-1) - 1) # 5년 표준편차

            (year, month, day) = return_val_date(price, start_date.year + 2, start_date.month)
            save[num][2] = last_price / int(price['Close'][str(year) + '-' + str(month) + '-' + str(day)]) - 1 # 3년 수익률
            years_period = price['Close'][(str(year) + '-' + str(month) + '-' + str(day)):]
            save[num][3] = numpy.std((numpy.array(years_period[:-1].astype(int))/numpy.array(years_period[1:].astype(int))).reshape(-1) - 1) # 3년 표준편차

            (year, month, day) = return_val_date(price, start_date.year + 4, start_date.month)
            save[num][4] = last_price / int(price['Close'][str(year) + '-' + str(month) + '-' + str(day)]) - 1 # 1년 수익률
            years_period = price['Close'][(str(year) + '-' + str(month) + '-' + str(day)):]
            save[num][5] = numpy.std((numpy.array(years_period[:-1].astype(int))/numpy.array(years_period[1:].astype(int))).reshape(-1) - 1) # 1년 표준편차

        else:
            save[num][0] = numpy.nan
            save[num][1] = numpy.nan
            save[num][2] = numpy.nan
            save[num][3] = numpy.nan
            save[num][4] = numpy.nan
            save[num][5] = numpy.nan
            
    else:
        save[num][0] = numpy.nan
        save[num][1] = numpy.nan
        save[num][2] = numpy.nan
        save[num][3] = numpy.nan
        save[num][4] = numpy.nan
        save[num][5] = numpy.nan
        
    
    print("{0} 완료".format(num + 1))
    sleep(5)
    #print('{0}: 5년 수익률 {1: .4f} 5년 표준편차 {2: .4f} 3년 수익률 {3: .4f} 3년 표준편차 {4: .4f} 1년 수익률 {5: .4f} 1년 표준편차 {6: .4f}'.format(code, save[num][0], save[num][1], save[num][2], save[num][3], save[num][4], save[num][5]))

row_nan = numpy.where(numpy.isnan(save))[0].tolist()
#print(row_nan)
if len(row_nan) >= 1:
    save = numpy.delete(save, row_nan, axis = 0)
    etf_list = etf_list.drop(row_nan, axis = 0)


five_year_earning_rate = AHP(save[:,0])
five_year_sdt = AHP(save[:,1], way='small')
three_year_earning_rate = AHP(save[:,2])
three_year_sdt = AHP(save[:,3], way='small')
one_year_earning_rate = AHP(save[:,4])
one_year_sdt = AHP(save[:,5], way='small')

'''pandas.DataFrame(five_year_earning_rate).to_excel("a.xlsx", index = False)
pandas.DataFrame(five_year_sdt).to_excel("b.xlsx", index = False)
pandas.DataFrame(three_year_earning_rate).to_excel("c.xlsx", index = False)
pandas.DataFrame(three_year_sdt).to_excel("d.xlsx", index = False)
pandas.DataFrame(one_year_earning_rate).to_excel("e.xlsx", index = False)
pandas.DataFrame(one_year_sdt).to_excel("f.xlsx", index = False)'''

five_year_earning_rate_score = AHP_score(five_year_earning_rate)
five_year_sdt_score = AHP_score(five_year_sdt)
three_year_earning_rate_score = AHP_score(three_year_earning_rate)
three_year_sdt_score = AHP_score(three_year_sdt)
one_year_earning_rate_score = AHP_score(one_year_earning_rate)
one_year_sdt_score = AHP_score(one_year_sdt)

#RI = AHP_random_const_index(etf_num)
'''RI = 1.59

a = AHP_const_ratio(AHP_const_index(AHP_const(five_year_earning_rate, five_year_earning_rate_score)), RI)
b = AHP_const_ratio(AHP_const_index(AHP_const(five_year_sdt, five_year_sdt_score)), RI)
c = AHP_const_ratio(AHP_const_index(AHP_const(three_year_earning_rate, three_year_earning_rate_score)), RI)
d = AHP_const_ratio(AHP_const_index(AHP_const(three_year_sdt, three_year_sdt_score)), RI)
e = AHP_const_ratio(AHP_const_index(AHP_const(one_year_earning_rate, one_year_earning_rate_score)), RI)
f = AHP_const_ratio(AHP_const_index(AHP_const(one_year_sdt, one_year_sdt_score)), RI)'''

#기준별 가중치
earn = [[1,3,5],[1/3,1,3],[1/5,1/3,1]]
sdt = [[1,3,5],[1/3,1,3],[1/5,1/3,1]]

earn = AHP_score(earn)/2
sdt = AHP_score(sdt)/2

#최종점수 산출
one_year_earning_rate_score = one_year_earning_rate_score * earn[0]
three_year_earning_rate_score = three_year_earning_rate_score * earn[1]
five_year_earning_rate_score = five_year_earning_rate_score * earn[2]

one_year_sdt_score = one_year_sdt_score * sdt[0]
three_year_sdt_score = three_year_sdt_score * sdt[1]
five_year_sdt_score = five_year_sdt_score * sdt[2]


#종목 구하기
etf_list["최종 점수"] = one_year_earning_rate_score + one_year_sdt_score + three_year_earning_rate_score + three_year_sdt_score + five_year_earning_rate_score + five_year_sdt_score
etf_list["수익성 점수"] = one_year_earning_rate_score + three_year_earning_rate_score + five_year_earning_rate_score
etf_list["표준편차 점수"] = one_year_sdt_score + three_year_sdt_score + five_year_sdt_score
#etf_list.sort_values(by=["score"], axis=0, ascending=False, inplace=True)

final_dt = etf_list[["단축코드", "한글종목약명", "최종 점수", "수익성 점수", "표준편차 점수"]]
final_dt.to_excel("result\end.xlsx")


'''with pandas.ExcelWriter('result\AHP2.xlsx') as writer:
    pandas.DataFrame(five_year_earning_rate).to_excel(writer, sheet_name='sheet1', index=False, header=False)
    pandas.DataFrame(five_year_sdt).to_excel(writer, sheet_name='sheet2', index=False, header=False)
    pandas.DataFrame(three_year_earning_rate).to_excel(writer, sheet_name='sheet3', index=False, header=False)
    pandas.DataFrame(three_year_sdt).to_excel(writer, sheet_name='sheet4', index=False, header=False)
    pandas.DataFrame(one_year_earning_rate).to_excel(writer, sheet_name='sheet5', index=False, header=False)
    pandas.DataFrame(one_year_sdt).to_excel(writer, sheet_name='sheet6', index=False, header=False)'''

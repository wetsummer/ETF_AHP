### 개요
분석적 계층화 과정(AHP; Analytic Hierarchy Process)을 사용하여 1년 수익률, 3년 수익률, 5년 수익률, 1년 일 수익률 표준편차, 3년 일 수익률 표준편차, 5년 일 수익률 표준편차를 기준으로 상장 지수 기금(ETF; Exchanged Traded Fund)의 점수를 도출하는 도구입니다.

상장 지수 기금이 아니더라도 선호도 분석을 한 표가 있다면,   
+ 점수 얻기
  + AHP_score(※선호도표※)
+ 일관성 검증
  + AHP_const_ratio(AHP_const_index(AHP_const(AHP_score(※선호도표※), ※선호도표※)), AHP_RI(len(※선호도표※))) <= 0.1   

로 손쉽게 분석적 계층화 과정를 진행할 수 있습니다.

### 내용물
+ main.py
  + : 주 함수입니다. 정보를 받아와 엑셀로 내보냅니다.

+ AHP_cal.py
  + return_val_date(): 증권 정보, 연도, 월을 입력 받아 가까운 거래일을 찾아냅니다. 가인수 way에 인수 go를 주면 미래 날짜를, 인수 back을 주면 과거 날짜를 찾습니다.
  + AHP(): 증권 정보, 방식을 입력 받아 종가로 선호도를 셈합니다. 가인수 way에 인수 big을 주면 큰 수를 선호하고, 인수 small을 주면 작은 수를 선호합니다.
  + AHP_score(): 함수 AHP()로 만든 선호도 표를 입력 받아 점수를 셈합니다.
  + get_smallest_num_biggrt_then_zero(): 0보다 큰 가장 작은 양수를 구합니다. 대안 개수가 너무 많아 0 나눗셈이 발생할 여지를 없앱니다.
  + AHP_const(): 함수 AHP()로 만든 선호도 표와 함수 AHP_score()로 만든 점수표를 입력 받아 일관성 척도를 구합니다.
  + AHP_const_index(): 일관성 척도를 입력 받아 일관성 지수(CI; Consistency Index)를 구합니다.
  + AHP_const_ratio(): 일관성 지수와 무작위 일관성 지수(RI; Random Consistency Index)로 일관성 비율(CI; Consistency Ratio)를 구합니다.
  + AHP_RI():  대안 개수를 입력 받아 무작위 일관성 지수를 구합니다.
  + AHP_random_const_index(): 무작위 일관성 지수 계산 병렬 처리를 관리합니다.
  + AHP_random_const_index_inside(): 무작위 일관성 계산을 병렬 처리하는 함수입니다.

+ download_ETF_data.py
  + dt_down(): 한국거래소에서 상장 지수 기금 정보를 엑셀로 내려받는 함수입니다. 셀레니움(selenium)에서 구글 크롬(Google Chrome)을 사용합니다.

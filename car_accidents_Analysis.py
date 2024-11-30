import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
from datetime import datetime

# 파일 열기
fp = open('traffic.csv', 'r', encoding='cp949')
data = csv.reader(fp)

# 첫 번째 행(헤더)을 건너뜀
next(data)

# 데이터를 저장할 딕셔너리 생성
yearly_data = defaultdict(lambda: {'accident': 0, 'death': 0})  # 연도별 사고, 사망
monthly_data = defaultdict(lambda: {'accident': 0, 'death': 0})  # 월별 사고, 사망
daily_data = defaultdict(lambda: {'accident': 0, 'death': 0, 'btc': 0})  # 일자별 사고, 사망, 비트코인

# 데이터 읽기 및 저장
for row in data:
    date = datetime.strptime(row[0], '%Y-%m-%d')  # 날짜 변환
    accident, death, injury, btc_price = map(float, row[1:5])  # 숫자로 변환

    # 연도별 사고와 사망 합계
    yearly_data[date.year]['accident'] += accident
    yearly_data[date.year]['death'] += death

    # 월별 사고와 사망 합계
    monthly_data[(date.year, date.month)]['accident'] += accident
    monthly_data[(date.year, date.month)]['death'] += death

    # 일자별 사고, 사망, 비트코인 가격
    daily_data[(date.year, date.month, date.day)]['accident'] += accident
    daily_data[(date.year, date.month, date.day)]['death'] += death
    daily_data[(date.year, date.month, date.day)]['btc'] += btc_price

# 사용자 입력 받기
user_input = input("전체기간, 특정년도(2005~2023), 특정 월(월-년도) 입력 : ")
print()

##추가한 코드(1)
# 월을 계절로 매핑
season_mapping = {
    1: '겨울', 2: '겨울', 12: '겨울',
    3: '봄', 4: '봄', 5: '봄',
    6: '여름', 7: '여름', 8: '여름',
    9: '가을', 10: '가을', 11: '가을'
}
##

try:
    # 1) 전체 기간에 대한 그래프 출력
    if user_input == "전체기간":
        years = sorted(yearly_data.keys())
        accidents = [yearly_data[year]['accident'] for year in years]
        deaths = [yearly_data[year]['death'] for year in years]

        # 가장 사고가 많은 연도 및 사망자 수
        max_accidents = max(accidents)
        max_accidents_years = [year for year in years if yearly_data[year]['accident'] == max_accidents]

        # 가장 사망자가 많은 연도 및 사망자 수
        max_deaths = max(deaths)
        max_deaths_years = [year for year in years if yearly_data[year]['death'] == max_deaths]

        # 월별 사고 및 사망 데이터에서 가장 많은 사고와 사망자를 찾음
        max_accidents_monthly = max(monthly_data.items(), key=lambda x: x[1]['accident'])
        max_deaths_monthly = max(monthly_data.items(), key=lambda x: x[1]['death'])

         ##추가한 코드
        # 가장 사고가 많았던 월의 계절 찾기
        max_accident_month_str = f"{max_accidents_monthly[0][1]:02}-{max_accidents_monthly[0][0]}"
        max_accident_season = season_mapping[max_accidents_monthly[0][1]]
        #가장 사망자가 많았던 월의 계절 찾기
        max_death_year, max_death_month = max_deaths_monthly[0]
        max_death_season = season_mapping[max_deaths_monthly]
        ##

        print(f"가장 많은 사고가 발생한 년도: {', '.join(map(str, max_accidents_years))} - 사고 수: {max_accidents}")
        print(f"가장 많은 사망자가 발생한 년도: {', '.join(map(str, max_deaths_years))} - 사망자 수: {max_deaths}")

        # 월 정보를 추출하여 출력
        max_accidents_month_str = f"{max_accidents_monthly[0][1]:02}-{max_accidents_monthly[0][0]}"
        max_deaths_month_str = f"{max_deaths_monthly[0][1]:02}-{max_deaths_monthly[0][0]}"

        print(f"가장 많은 사고가 발생한 월: {max_accidents_month_str} - 사고 수: {max_accidents_monthly[1]['accident']}")
        print(f"가장 많은 사망자가 발생한 월: {max_deaths_month_str} - 사망자 수: {max_deaths_monthly[1]['death']}")
        print()

        # 서브플롯 생성 (3x2 구조)
        plt.figure(figsize=(12, 24))

        # 첫 번째 서브플롯: 전체 기간에 대한 사고 및 사망자 수
        plt.subplot(5, 1, 1)
        plt.bar(years, accidents, color='skyblue', label='Accidents')
        plt.xlabel('Year')
        plt.ylabel('Number of Accidents', color='skyblue')
        plt.title('Total period Accidents and Deaths (2005-2023)')
        plt.xticks(rotation=45)

        # X축의 간격을 1로 설정
        plt.xticks(years, rotation=45)  # years를 직접 사용하여 간격을 1로 설정

        # 두 번째 Y축 생성
        ax2 = plt.gca().twinx()  # 현재 Axes 객체에 대해 두 번째 Y축 생성
        ax2.plot(years, deaths, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # 범례 설정
        plt.legend(loc='upper left')  # 사고에 대한 범례 위치
        ax2.legend(loc='upper right')  # 사망자에 대한 범례 위치

        # 세 번째 서브플롯: 가장 사고가 많은 해의 월별 데이터 (사고: bar, 사망: plot)
        plt.subplot(5, 1, 2)
        max_accident_year = max_accidents_years[0]  # 가장 사고가 많았던 연도
        months = [month for month in range(1, 13)]
        accidents_month = [monthly_data[(max_accident_year, month)]['accident'] for month in months]
        deaths_month = [monthly_data[(max_accident_year, month)]['death'] for month in months]

        # 두 개의 축을 사용하여 사고는 bar로, 사망은 plot으로 출력
        ax1 = plt.gca()
        ax1.bar(months, accidents_month, color='skyblue', label='Accidents')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(months, deaths_month, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most monthly Accidents : {max_accident_year}')
        plt.xticks(rotation=45)

        # 네 번째 서브플롯: 가장 사망자가 많은 해의 월별 데이터 (사고: bar, 사망: plot)
        plt.subplot(5, 1, 3)
        max_death_year = max_deaths_years[0]  # 가장 사망자가 많았던 연도
        accidents_month = [monthly_data[(max_death_year, month)]['accident'] for month in months]
        deaths_month = [monthly_data[(max_death_year, month)]['death'] for month in months]

        # 두 개의 축을 사용하여 사고는 bar로, 사망은 plot으로 출력
        ax1 = plt.gca()
        ax1.bar(months, accidents_month, color='skyblue', label='Accidents')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(months, deaths_month, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most monthly Deaths : {max_death_year}')
        plt.xticks(rotation=45)

        # 다섯 번째 서브플롯: 전체 기간 중에서 가장 사고가 많았던 월의 일자별 데이터 (사고: bar, 사망: plot)
        plt.subplot(5, 1, 4)

        # 가장 사고가 많았던 월을 찾음
        max_accident_month = max(monthly_data, key=lambda x: monthly_data[x]['accident'])
        max_accident_year, max_accident_month = max_accident_month  # 해당 월과 연도

        days = [day for day in range(1, 32) if (max_accident_year, max_accident_month, day) in daily_data]
        accidents_day = [daily_data[(max_accident_year, max_accident_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(max_accident_year, max_accident_month, day)]['death'] for day in days]

        # 두 개의 축을 사용하여 사고는 bar로, 사망은 plot으로 출력
        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most daily Accidents : {max_accident_year}-{max_accident_month:02}')
        plt.xticks(rotation=45)

        # 여섯 번째 서브플롯: 전체 기간 중에서 가장 사망자가 많았던 월의 일자별 데이터 (사고: bar, 사망: plot)
        plt.subplot(5, 1, 5)
        # 가장 사망자가 많았던 월을 찾음
        max_death_month = max(monthly_data, key=lambda x: monthly_data[x]['death'])
        max_death_year, max_death_month = max_death_month  # 해당 월과 연도

        days = [day for day in range(1, 32) if (max_death_year, max_death_month, day) in daily_data]
        accidents_day = [daily_data[(max_death_year, max_death_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(max_death_year, max_death_month, day)]['death'] for day in days]

        # 두 개의 축을 사용하여 사고는 bar로, 사망은 plot으로 출력
        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most daily Deaths : {max_death_year}-{max_death_month:02}')
        plt.xticks(rotation=45)

        # 서브플롯 간격 조정
        plt.subplots_adjust(hspace=0.5, wspace=0.3)  # 높이와 너비 간격 조정

        # 레이아웃 조정 및 그래프 출력
        plt.tight_layout()
        plt.show()


    # 2) 특정 년도에 대한 월별 그래프 출력
    # 특정 년도에 대한 월별 그래프 출력
    elif user_input.isdigit() and 2005 <= int(user_input) <= 2023:
        year = int(user_input)
        months = [month for month in range(1, 13)]
        accidents = [monthly_data[(year, month)]['accident'] for month in months]
        deaths = [monthly_data[(year, month)]['death'] for month in months]

        # 가장 사고가 많은 월 및 사망자 수
        max_accidents = max(accidents)
        max_accidents_month = months[accidents.index(max_accidents)]

        max_deaths = max(deaths)
        max_deaths_month = months[deaths.index(max_deaths)]

        # 가장 사고가 적은 월 및 사망자 수
        min_accidents = min(accidents)
        min_accidents_month = months[accidents.index(min_accidents)]

        min_deaths = min(deaths)
        min_deaths_month = months[deaths.index(min_deaths)]

         # 가장 사고가 많았던 월의 계절 찾기
        max_accident_season = season_mapping[max_accidents_month]
        max_death_season = season_mapping[max_deaths_month]

        print(f"{year}년에서 가장 많은 사고가 발생한 월: {max_accidents_month} 월 - 사고 수: {max_accidents}")
        print(f"그 월의 계절: {max_accident_season}")##추가한 코드##
        print(f"{year}년에서 가장 많은 사망자가 발생한 월: {max_deaths_month} 월 - 사망자 수: {max_deaths}")
        print(f"{year}년에서 가장 적은 사고가 발생한 월: {min_accidents_month} 월 - 사고 수: {min_accidents}")
        print(f"그 월의 계절: {max_death_season}")##추가한 코드##
        print(f"{year}년에서 가장 적은 사망자가 발생한 월: {min_deaths_month} 월 - 사망자 수: {min_deaths}")
        print()

        # 서브플롯 생성 (3x2 구조)
        plt.figure(figsize=(12, 24))

        # 1번째 서브플롯: 해당 년도의 월별 사고 및 사망
        plt.subplot(5, 1, 1)
        ax1 = plt.gca()
        ax1.bar(months, accidents, color='skyblue', label='Accidents')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')

        # 오른쪽 y축에 사망자 수 표시
        ax2 = ax1.twinx()
        ax2.plot(months, deaths, color='red', marker='o', label='Deaths')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        plt.title(f'{year} Monthly Accidents and Deaths')

        # 3번째 서브플롯: 가장 사고가 많은 월의 일자별 데이터
        plt.subplot(5, 1, 2)
        days = [day for day in range(1, 32) if (year, max_accidents_month, day) in daily_data]
        accidents_day = [daily_data[(year, max_accidents_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(year, max_accidents_month, day)]['death'] for day in days]

        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most Accidents Month ({max_accidents_month})')

        # 4번째 서브플롯: 가장 사망이 많은 월의 일자별 데이터
        plt.subplot(5, 1, 3)
        days = [day for day in range(1, 32) if (year, max_deaths_month, day) in daily_data]
        accidents_day = [daily_data[(year, max_deaths_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(year, max_deaths_month, day)]['death'] for day in days]

        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Most Deaths Month ({max_deaths_month})')

        # 5번째 서브플롯: 가장 사고가 적은 월의 일자별 데이터
        plt.subplot(5, 1, 4)
        days = [day for day in range(1, 32) if (year, min_accidents_month, day) in daily_data]
        accidents_day = [daily_data[(year, min_accidents_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(year, min_accidents_month, day)]['death'] for day in days]

        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Least Accidents Month ({min_accidents_month})')

        # 6번째 서브플롯: 가장 사망이 적은 월의 일자별 데이터
        plt.subplot(5, 1, 5)
        days = [day for day in range(1, 32) if (year, min_deaths_month, day) in daily_data]
        accidents_day = [daily_data[(year, min_deaths_month, day)]['accident'] for day in days]
        deaths_day = [daily_data[(year, min_deaths_month, day)]['death'] for day in days]

        ax1 = plt.gca()
        ax1.bar(days, accidents_day, color='skyblue', label='Accidents')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Number of Accidents', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2 = ax1.twinx()
        ax2.plot(days, deaths_day, color='red', label='Deaths', marker='o')
        ax2.set_ylabel('Number of Deaths', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title(f'Least Deaths Month ({min_deaths_month})')

        plt.tight_layout()
        plt.show()

    # 3) 특정 년도의 특정 월에 대한 일자별 그래프 출력
    elif '-' in user_input:
        try:
            # 월과 년도가 올바른 순서로 들어왔는지 확인
            parts = user_input.split('-')
            if len(parts) != 2:  # '-'로 정확히 두 부분으로 나눠져 있어야 함
                raise ValueError

            month, year = map(int, parts)

            # 월과 연도의 범위 확인 (월은 1~12, 연도는 2005~2023이어야 함)
            if not (1 <= month <= 12) or not (2005 <= year <= 2023):
                raise ValueError

            # 정상적으로 입력된 경우 그래프 그리기 처리
            days = [day for day in range(1, 32) if (year, month, day) in daily_data]
            accidents = [daily_data[(year, month, day)]['accident'] for day in days]
            deaths = [daily_data[(year, month, day)]['death'] for day in days]
            btc_prices = [daily_data[(year, month, day)]['btc'] for day in days]

            # 가장 사고가 많은 일자 및 사망자 수
            max_accidents = max(accidents)
            max_accidents_days = [day for day in days if daily_data[(year, month, day)]['accident'] == max_accidents]

            max_deaths = max(deaths)
            max_deaths_days = [day for day in days if daily_data[(year, month, day)]['death'] == max_deaths]

            print(f"{year}-{month:02} 에서 가장 많은 사고가 발생한 일자: {', '.join(map(str, max_accidents_days))}일 - 사고 수: {max_accidents}")
            print(f"{year}-{month:02} 에서 가장 많은 사망자가 발생한 일자: {', '.join(map(str, max_deaths_days))}일 - 사망자 수: {max_deaths}")

            # 비트코인 가격이 가장 높은 일자 및 낮은 일자
            max_btc_day = days[btc_prices.index(max(btc_prices))]
            min_btc_day = days[btc_prices.index(min(btc_prices))]

            print(f"{year}-{month:02} 에서 가장 높은 비트코인 가격: {daily_data[(year, month, max_btc_day)]['btc']} ({year}-{month:02}-{max_btc_day})")
            print(f"{year}-{month:02} 에서 가장 낮은 비트코인 가격: {daily_data[(year, month, min_btc_day)]['btc']} ({year}-{month:02}-{min_btc_day})")
            print()

            # 그래프 그리기
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax1.bar(days, accidents, color='skyblue', label='Accidents')
            ax1.set_xlabel('Day')
            ax1.set_ylabel('Number of Accidents', color='skyblue')
            ax1.tick_params(axis='y', labelcolor='skyblue')
            ax2 = ax1.twinx()
            ax2.plot(days, deaths, color='red', label='Deaths')
            ax2.set_ylabel('Number of Deaths', color='red')
            ax2.tick_params(axis='y', labelcolor='red')

            # 비트코인 가격은 0이 아닌 경우에만 Plot 형태로 추가
            if any(btc_prices):
                btc_days = [day for day, price in zip(days, btc_prices) if price > 0]
                btc_prices_filtered = [price for price in btc_prices if price > 0]
                ax3 = ax1.twinx()
                ax3.plot(btc_days, btc_prices_filtered, color='green', label='BTC Price', linestyle='dashed')
                ax3.set_ylabel('BTC Price', color='green')
                ax3.tick_params(axis='y', labelcolor='green')
                ax3.spines['right'].set_position(('outward', 60))  # 세 번째 축을 오른쪽으로 이동

            # 범례 설정
            fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
            plt.title(f'Daily Accidents, Deaths, and BTC Price in {year}-{month:02}')
            plt.tight_layout()
            plt.show()

        except ValueError:
            print("잘못된 입력입니다. 올바른 형식은 '월-년도'입니다. 예: '3-2020'.")

    else:
        print("올바른 입력을 해주세요.")

except Exception as e:
    print(f"예기치 않은 오류가 발생했습니다: {e}")

# 파일 닫기
fp.close()

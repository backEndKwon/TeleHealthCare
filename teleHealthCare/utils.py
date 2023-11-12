from datetime import datetime, timedelta, time
#시간을 24시간 형식으로 변환
#ex) 1시 -> 13, 2시 -> 14, 3시 -> 15, 4시 -> 16, 5시 -> 17, 6시 -> 18, 7시 -> 19, 8시 -> 20, 9시 -> 21, 10시 -> 22, 11시 -> 23, 12시 -> 24
def convertTimeFormat(time):
    time = time.replace('시', '')
    if '오후' in time:
        hour = int(time.replace('오후', '').strip()) + 12
    else:
        hour = int(time.replace('오전', '').strip())
    return hour

#입력한 시간이 의사의 영업시간 내에 있는지 확인
def isWithinWorkingHours1(user_time, working_hours, lunch_hours):
    if '휴무' in working_hours:
        return '휴무입니다.'

    working_start, working_end = [int(convertTimeFormat(t)) for t in working_hours.split('~')]
    lunch_start, lunch_end = [int(convertTimeFormat(t)) for t in lunch_hours.split('~')]
    if not (working_start <= user_time < lunch_start or lunch_end <= user_time < working_end):
        return '의사선생님의 영업시간이 아닙니다.'
    return user_time

#treatment api에 사용
def isWithinWorkingHours(user_time, working_hours, lunch_hours):
    if '휴무' in working_hours:
        return '의사선생님의 영업시간이 아닙니다.'
    else:
        working_start, working_end = [int(convertTimeFormat(t)) for t in working_hours.split('~')]
        lunch_start, lunch_end = [int(convertTimeFormat(t)) for t in lunch_hours.split('~')]
        if not (working_start <= user_time < lunch_start or lunch_end <= user_time < working_end):
            return '의사선생님의 영업시간이 아닙니다.'
    return user_time


#진료요청 만료시간 계산
def calculateExpirationDate(rez_date, doctor):
    # 의사의 영업시간과 점심시간을 시간 형태로 변환
    working_days = doctor.time_business.split('/')
    for i in range(7):  # 최대 7일 동안만 확인
        working_hours = working_days[(rez_date.weekday()+i)%7].split('~')
        if '휴무' not in working_hours:  # 휴무가 아닌 날을 찾으면 그 날의 working_hours를 사용
            break
    else:  # 모든 날이 휴무일 경우
        return None  # 또는 적절한 에러 메시지 반환

    working_hours = [convertTimeFormat(t) for t in working_hours]
    lunch_hours = [convertTimeFormat(t) for t in doctor.time_lunch.split('~')]

    # 진료요청 시간이 의사의 근무시간 내인 경우
    if working_hours[0] <= rez_date.time().hour < working_hours[1]:
        # 진료요청 시간이 점심시간 이전인 경우
        if rez_date.time().hour < lunch_hours[0]:
            expiration_date = rez_date + timedelta(minutes=20)
        # 진료요청 시간이 점심시간 이후인 경우
        elif rez_date.time().hour >= lunch_hours[1]:
            expiration_date = rez_date + timedelta(minutes=20)
        # 진료요청 시간이 점심시간 동안인 경우
        else:
            expiration_date = datetime(rez_date.year, rez_date.month, rez_date.day, lunch_hours[1], 15)
    # 진료요청 시간이 의사의 근무시간 외인 경우
    else:
        # 다음 근무일을 계산
        next_working_day = (rez_date + timedelta(days=1)).replace(hour=working_hours[0], minute=15)
        expiration_date = next_working_day

    return expiration_date



#treatment api에 사용
def parseDateString(date_str):
    # 요일 제거
    date_str = date_str.replace("토요일", "").replace("일요일", "").replace("월요일", "").replace("화요일", "").replace("수요일", "").replace("목요일", "").replace("금요일", "")

    # 날짜 및 시간 분리
    date_str, time_str = date_str.rsplit(maxsplit=1)

    # AM/PM 및 시간 분리
    am_pm = time_str[:-2]
    hour_str = time_str[-2:]

    # 시간 파싱
    hour = int(hour_str.replace("시", ""))

    # 오후 시간 변환
    if "오후" in am_pm and hour != 12:
        hour += 12

    # 날짜와 시간 합치기
    date = datetime.strptime(date_str, "%Y년 %m월 %d일").replace(hour=hour)
    return date





# def parseDateString(date_str):
#     date_str = date_str.replace("년", "-").replace("월", "-").replace("일", "")
#     date_str, am_pm, time_str = date_str.split()

#     # 날짜 파싱
#     date = datetime.strptime(date_str, "%Y-%m-%d").date()

#     # 시간 파싱
#     hour_minute = time_str[:-1]  # '시' 제거
#     hour, minute = map(int, hour_minute.split(":"))

#     # 오후 시간 변환
#     if am_pm == "오후" and hour != 12:
#         hour += 12

#     return datetime.combine(date, time(hour, minute))

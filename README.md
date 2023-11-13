# TeleHealthCare

## 1. 개요

비대면 의료 서비스에 필요한 기본 기능 구현 연습 및 python django djangoRestFramework 연습

## 2. 기능

- 2-1. Patient<br/>
  - 환자정보 등록<br/>
- 2-2. Doctor<br/>
  - 의사정보 등록<br/>
  - 의사 검색(문자열 검색, 특정날자 영업가능한 의사 검색)<br/>
- 2-3. Treatment<br/>
  - 진료요청<br/>
  - 진료요청 건 수락<br/>
  - 진료요청 건 검색<br/>

## 3. 프로그램 세팅방법

<details>
<summary>3-1. 가상환경 설정(venv)</summary>

- 가상환경 생성 : python -m venv venv
- 가상환경 활성화 : source venv/Script/activate
- 인터프리터 선택 : ctrl+shift+p => python 인터프리터 venv 선택
- 패키지 설치 : pip install -r requirements.txt
</details>

<details>
<summary>3-2. DB 설정(PostgreSQL)</summary>

- root 경로에 .env 생성후 본인의 DB_HOST, DB_USER, DB_NAME, DB_PASSWORD, DB_PORT 세팅
</details>

## 4. URL 및 입력값, 출력값 예시

<details>
<summary>4-1. 공통주소 : http://127.0.0.1:8000</summary>
</details>

<details>
    <summary>4-2. 기능별 주소/입력값/출력값<br/></summary>
        <details>
          <summary> 컬럼 설명</summary>
          - 안내사항 : 타입은 ERD 참고. 시간 작성은 오전, 오후로 구분. 점심시간 12시는 오후12시 / 밤 12시는 오전 12시. 요일은 사용하지 않음.<br/>
          - name[환자 또는 의사 이름] : "홍길동"<br/>
          - hospital[병원명] : "ABC병원"<br/>
          - department[진료과] : "성형외과, 외과"<br/>
  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - "," 쉼표로 진료과 구분<br/> 
          - department_selfPay[비급여 진료과] : "다이어트과, 탈모과"<br/>
  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - "," 쉼표로 진료과 구분<br/> 
          - time_business[영업요일별 영업시간] : "오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전11시~오후3시/휴무"<br/>
  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - "/" 슬래쉬로 구분, 첫번째 인덱스부터 "월"요일을 의미함. 휴무일 경우 "휴무" 입력. 1시간 단위로만 입력, 출력 가능<br/>
          - time_lunch[점심시간] : "오전11시~오후1시"<br/>
          - isAccepted[의사의 진료요청 수락 여부] : true 또는 false<br/>
          - rezDate[진료요청 일자] : "2023년 11월 13일 오후2시"<br/>
          - rezExpirationDate[진료요청 만료일자] : "2023-11-13 11:47:37"
        </details>
        <details>
          <summary> Patient</summary>
              ① 환자정보 등록<br/>
                - POST요청, 공통주소/patients/<br/>
                - 입력값 : Request Body json<br/>
                <pre>
                ```
                    {
                    "name":"홍길동"
                    }
                ```
                </pre>
                - 출력값 : <br/>
                <pre>
                ```
                    {
                    "patientId":"21qw-23df-21a-43g",
                    "name":"홍길동"
                    }
                ```
                </pre>
        </details>
        <details>
        <summary> Doctor</summary>
              ① 의사정보 등록<br/> 
                - POST요청, 공통주소/doctors/<br/>
                - 입력값 : Request Body json<br/>
                <pre>
                ```
                    {
                    "hospital": "ABC병원",
                    "name": "허준",
                    "department": "성형외과, 외과",
                    "department_selfPay": "다이어트과, 심근경색과",
                    "time_business": "오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전10시~오후7시/오전11시~오후3시/휴무",
                    "time_lunch": "오전11시~오후1시"
                    }
                ```
                </pre>
                - 출력값 : <br/>
                <pre>
                ```
                    {"doctorId":"53sdg-fd3-523g-865tg",
                      - 나머지 입력값과 동일 - 
                    }
                ```
                </pre><br/>
              ② 의사 검색(문자열 검색, 특정날자 영업가능한 의사 검색)<br/>
                - GET요청, 공통주소/search<br/>
                - 입력값 : Query Params / 한가지 혹은 여러개 선택해서 서칭 가능<br/>
                    (1) key-value(병원명) : keyword, ABC병원<br/>
                    (2) key-value(진료과) : keyword, 성형외과<br/>
                    (3) key-value(비급여) : keyword, 심근경색과<br/>
                    (4) key-value(날짜/시간) : datetime, 2023년 11월 13일 오후3시"<br/>
                - 출력값 : <br/>
                <pre>
                ```
                    {
                     "허준" 
                    }
                ```
                </pre>
        </details>
        <details>
          <summary> Treatment</summary>
               ① 진료요청
                - POST요청, 공통주소/treatments/createTreatment<br/>
                - 입력값 : Request Body json<br/>
                <pre>
                ```
                    {
                    "patientId": "c17398a5-6c77-451e-bf52-8c247c08386d",
                    "doctorId": "2b958b6a-e8b9-4528-be88-7c82a7525345",
                    "rezDate": "2023년 11월 15일 오후3시"
                    }
                ```
                </pre>
                - 출력값 : <br/>
                <pre>
                ```
                    {
                    "treatmentId": "3f061250-2826-4186-9ad0-4abae6fb63e3",
                    "patientName": "홍길동",
                    "doctorName": "허준",
                    "rezDate": "2023년 11월 15일 15시00분",
                    "rezExpirationDate": "2023-11-15 15:20:00",
                    "isAccepted": false
                    }
                ```
                </pre>
                <br/>
                ② 진료요청 건 수락 <br/>
                  - PUT요청, 공통주소/treatments/{treatmentId}/acceptTreatment<br/>
                  - 입력값 : Path Param<br/>
                      {treatmentId} : "3f061250-2826-4186-9ad0-4abae6fb63e3"<br/>
                  - 출력값 : <br/>
                  <pre>
                  ```
                      {
                       "treatmentId": "3f061250-2826-4186-9ad0-4abae6fb63e3",
                       "patientName": "홍길동",
                       "doctorName": "허준",
                       "rezDate": "2023년 11월 15일 15시00분",
                       "rezExpirationDate": "2023-11-15 15:20:00",
                       "isAccepted": true
                      }
                  ```
                  </pre>
                  <br/>
                 ③ 진료요청 건 검색<br/>
                  - GET요청, 공통주소/treatments/search<br/>
                  - 입력값 : Query Param<br/>
                  <pre>
                  ```
                     (1) key-value(doctorId) : doctorId, "2b958b6a-e8b9-4528-be88-7c82a7525345"
                  ```
                  </pre>
                  - 출력값 : <br/>
                  <pre>
                  ```
                      [
                       {
                         "treatmentId": "3f061250-2826-4186-9ad0-4abae6fb63e3",
                          "patientName": "홍길동",
                          "doctorName": "허준",
                          "rezDate": "2023년 11월 15일 15시00분",
                          "rezExpirationDate": "2023-11-15 15:20:00",
                          "isAccepted": false
                          },{.."isAccepted":false},{.."isAccepted":false},...
                         ]
                  ```
                  </pre>
        </details>
  </details>
</details>

## 5. ERD

<details>
<summary>ERD image</summary>
  ![image](https://github.com/backEndKwon/teleHealthCare/assets/128948886/9bd1ff25-0ff0-4cc2-be01-82e05e1bd3ee)
</details>

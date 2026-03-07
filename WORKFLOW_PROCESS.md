# 마이콜의 작업 처리 과정 상세 설명

**작성일**: 2026-03-05  
**작성자**: 마이콜 (MyCol)  
**주제**: 퀀트 매매 및 엘리어트 파동 분석 보고서 생성 과정

---

## 📋 개요

이 문서는 콜링님의 요청을 처리하여 텔레그램으로 결과를 전달하는 전체 과정을 상세히 설명합니다.

---

## 🛠️ 사용하는 도구 목록

### 1. **Bash Tool**
- **용도**: 명령어 실행, 프로세스 관리, 파일 조작
- **예시**: `python3 script.py`, `pip3 install`, `ps aux`

### 2. **Write Tool**  
- **용도**: 새 파일 생성 및 작성
- **예시**: `.md` 보고서, `.py` 스크립트 파일 생성

### 3. **Edit Tool**
- **용도**: 기존 파일 내용 수정
- **예시**: 코드 수정, 줄바꿈 처리, 내용 업데이트

### 4. **Read Tool**
- **용도**: 파일 내용 읽기 및 확인
- **예시**: 설정 파일 확인, 기존 데이터 검토

### 5. **WebFetch Tool**
- **용도**: 웹 페이지 내용 가져오기
- **예시**: 트윗 내용 추출 (api.fxtwitter.com)

### 6. **Python (코드 실행)**
- **용도**: 실제 데이터 처리 및 API 호출
- **라이브러리**: `yfinance`, `requests`, `sqlite3`, `pandas` 등

---

## 📊 퀀트 매매 보고서 생성 상세 과정

### 단계 1: 환경 확인 및 준비
```bash
# 작업 디렉토리로 이동
cd /home/icall/.opencode/workspace/quant_project

# 필요한 라이브러리 확인
pip3 install yfinance requests --break-system-packages
```
**사용 도구**: Bash

---

### 단계 2: 주식 데이터 수집
```python
import yfinance as yf

# TSLA 데이터 수집
tsla = yf.Ticker('TSLA')
df_tsla = tsla.history(period="3mo")

# MOS 데이터 수집  
mos = yf.Ticker('MOS')
df_mos = mos.history(period="3mo")

# 현재가, 고가, 저가, 거래량 등 추출
current_price_tsla = df_tsla['Close'].iloc[-1]
current_price_mos = df_mos['Close'].iloc[-1]
```
**사용 도구**: Python (yfinance 라이브러리)
**데이터 출처**: Yahoo Finance API

---

### 단계 3: 기술적 지표 계산 (볼린저 밴드)
```python
# 20일 이동평균 계산
window = 20
sma20_tsla = df_tsla['Close'].rolling(window=window).mean().iloc[-1]

# 표준편차 계산
std20_tsla = df_tsla['Close'].rolling(window=window).std().iloc[-1]

# 볼린저 밴드 계산
upper_band = sma20_tsla + (std20_tsla * 2)
lower_band = sma20_tsla - (std20_tsla * 2)

# 매매 신호 판단
if current_price < lower_band:
    signal = "BUY"
elif current_price > upper_band:
    signal = "SELL"
else:
    signal = "HOLD"
```
**사용 도구**: Python (pandas)
**계산 공식**: 
- 중간선 = 20일 이동평균
- 상단선 = 중간선 + (2 × 표준편차)
- 하단선 = 중간선 - (2 × 표준편차)

---

### 단계 4: 엘리어트 파동 분석
```python
# 장기 추세 데이터 수집 (월간)
df_monthly = tsla.history(period="5y", interval="1mo")

# 파동 패턴 식별
# 파동 1: $30 → $900 (상승)
# 파동 2: $900 → $100 (조정, 88% 되돌림)
# 파동 3: $100 → $400 (상승)
# 파동 4: 현재 진행 중 또는 완료
# 파동 5: 예상 목표가 계산

# 피본아치 되돌림 비율 계산
fib_38_2 = wave3_peak * 0.382
fib_50 = wave3_peak * 0.50
fib_61_8 = wave3_peak * 0.618

# 파동 5 목표가 예측
wave5_target = wave4_low + (wave3_length * 0.618)
```
**사용 도구**: Python
**분석 방법**: 엘리어트 파동 이론 + 피본아치 비율

---

### 단계 5: 보고서 파일 작성
```python
# 보고서 내용 생성
report_content = f"""
# 엘리어트 파동 분석 보고서
## {datetime.now().strftime('%Y-%m-%d')}

### TSLA 분석
- 현재가: ${current_price}
- 신호: {signal}
- 파동 위치: 파동 4 조정 완료 또는 진행 중
- 목표가: ${target_price}

### MOS 분석
- 현재가: ${current_price}
- 신호: {signal}
- 파동 위치: 파동 4 조정 중
- 목표가: ${target_price}

### 매매 전략
...
"""

# 파일로 저장
with open('elliott_wave_analysis_TSLA_MOS.md', 'w') as f:
    f.write(report_content)
```
**사용 도구**: Write Tool
**출력 파일**: `elliott_wave_analysis_TSLA_MOS.md`

---

### 단계 6: 파일 내용 확인 및 수정
```bash
# 파일 생성 확인
ls -la elliott_wave_analysis_TSLA_MOS.md

# 내용 검토 (필요시 수정)
cat elliott_wave_analysis_TSLA_MOS.md | head -50
```
**사용 도구**: Read Tool (확인), Edit Tool (수정)

---

### 단계 7: Telegram으로 전송
```python
import requests

BOT_TOKEN = "8684597246:AAFRE9MPxczQe1X17j9knGaadyyY6NGzBS8"
CHAT_ID = "63402726"

# 1. 텍스트 메시지 보기
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
message = "📊 퀀트 매매 신호\n\nTSLA: HOLD @ $405.55\nMOS: HOLD @ $26.28"
payload = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'HTML'
}
response = requests.post(url, json=payload, timeout=10)

# 2. 문서 파일 첨부
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
with open('elliott_wave_analysis_TSLA_MOS.md', 'rb') as f:
    files = {'document': f}
    data = {'chat_id': CHAT_ID, 'caption': '상세 분석 보고서'}
    response = requests.post(url, files=files, data=data, timeout=30)

# 전송 결과 확인
if response.status_code == 200:
    print("✅ 전송 완료!")
else:
    print(f"❌ 전송 실패: {response.status_code}")
```
**사용 도구**: Python (requests 라이브러리)
**API**: Telegram Bot API

---

### 단계 8: 완료 확인
```bash
# 로그 확인
tail -20 /tmp/telegram_send.log

# 결과 보고
echo "✅ 모든 작업 완료"
```
**사용 도구**: Bash

---

## 🔄 전체 프로세스 흐름도

```
사용자 요청
    ↓
[Bash] 환경 확인 및 준비
    ↓
[Python] 데이터 수집 (yfinance)
    ↓
[Python] 기술적 분석 (볼린저 밴드 계산)
    ↓
[Python] 엘리어트 파동 분석
    ↓
[Write] 보고서 파일 생성 (.md)
    ↓
[Read/Edit] 파일 확인 및 수정
    ↓
[Python] Telegram API 호출 (requests)
    ↓
[Bash] 결과 확인
    ↓
완료!
```

---

## 📱 Telegram API 상세

### API 엔드포인트
- **메시지 보기**: `https://api.telegram.org/bot<TOKEN>/sendMessage`
- **문서 첨부**: `https://api.telegram.org/bot<TOKEN>/sendDocument`
- **사진 보기**: `https://api.telegram.org/bot<TOKEN>/sendPhoto`

### 인증 방법
- Bot Token: `8684597246:AAFRE9MPxczQe1X17j9knGaadyyY6NGzBS8`
- Chat ID: `63402726`

### 전송 형식
- **text**: 일반 텍스트 (HTML 파싱 지원)
- **document**: 파일 첨부 (PDF, MD, TXT 등)
- **parse_mode**: 'HTML' 또는 'Markdown'

---

## 🔧 사용된 Python 라이브러리

| 라이브러리 | 용도 | 설치 방법 |
|------------|------|-----------|
| yfinance | 주식 데이터 수집 | pip3 install yfinance |
| requests | HTTP API 호출 | pip3 install requests |
| pandas | 데이터 처리 | pip3 install pandas |
| sqlite3 | 데이터베이스 | 내장 모듈 |
| numpy | 수치 계산 | pip3 install numpy |

---

## ⚠️ 주의사항 및 한계

### 데이터 지연
- yfinance 데이터는 실시간이 아님 (15-20분 지연)
- 장중 거래 시 실제 가격과 차이 있을 수 있음

### API 제한
- Telegram Bot API: 분당 30개 메시지 제한
- Yahoo Finance: 과도한 호출 시 차단 가능

### 오류 처리
- 네트워크 오류 시 재시도 로직 필요
- 데이터 없을 경우 예외 처리 필수

---

## ✅ 완료 체크리스트

- [x] 주식 데이터 수집
- [x] 볼린저 밴드 계산
- [x] 엘리어트 파동 분석
- [x] 보고서 파일 작성
- [x] Telegram 메시지 전송
- [x] 문서 파일 첨부
- [x] 결과 확인

---

## 📞 문의사항

보고서 내용에 대해 궁금한 점이 있으시면 텔레그램으로 메시지 보내주세요!

---

**문서 작성 완료**: 2026-03-05  
**버전**: 1.0  
**작성자**: 마이콜 (MyCol)

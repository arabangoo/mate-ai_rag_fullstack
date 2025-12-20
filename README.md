# 💕 MATE.AI - AI Romance Simulator

**영화 "Her" 스타일 AI 연애 시뮬레이터**

MATE.AI는 사용자가 자신만의 AI 캐릭터를 생성하고, 감정적으로 깊이 있는 대화를 나눌 수 있는 로맨틱 AI 플랫폼입니다. Google Gemini의 File Search RAG 기술을 활용하여 캐릭터가 모든 대화를 기억하고, 시간이 지남에 따라 관계가 자연스럽게 발전합니다.

---

## 📋 목차

- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [빠른 시작](#-빠른-시작)
- [프로젝트 구조](#-프로젝트-구조)
- [상세 설명](#-상세-설명)
- [RAG 비용 및 서버리스 아키텍처 장점](#-rag-비용-및-서버리스-아키텍처-장점)
- [개발 가이드](#-개발-가이드)
- [트러블슈팅](#-트러블슈팅)

---

## ✨ 주요 기능

### 🎨 캐릭터 커스터마이징 시스템

#### 4단계 캐릭터 생성 프로세스
1. **기본 정보 설정**
   - 캐릭터 이름, 성별, 나이 입력
   - **성별**: AI의 정체성 (대화 스타일, 성격에 영향)
   - 자유로운 커스터마이징

2. **외형 디자인** (2가지 옵션)
   - 🎮 **MATE.AI 3D 아바타 생성**
     - MMORPG 수준의 고품질 3D 캐릭터 커스터마이징
     - 아바타 에디터 내에서 성별, 얼굴 모양, 헤어스타일, 의상, 액세서리 등 자유롭게 선택
     - 셀카로 얼굴 인식 생성 가능
     - Web 기반 실시간 3D 미리보기
     - **참고**: 1단계 성별과 무관하게 원하는 외형 선택 가능
   - 🖼️ **이미지 업로드**
     - 원하는 캐릭터 이미지 업로드 (PNG, JPG, GIF 지원)
     - 간편하고 빠른 설정

3. **성격 & 말투 선택**
   - 다중 선택 가능한 성격 특성
     - 친절함, 장난기, 지적, 감성적, 활발함, 차분함
   - 말투 스타일 선택
     - 친근하고 다정함
     - 공손하고 정중함
     - 쿨하고 직설적

4. **배경 스토리 작성** (최소 100자)
   - 캐릭터의 과거, 성장 배경
   - 가치관, 꿈, 인생 철학
   - AI의 행동 원칙이 되는 핵심 요소

### ❤️ 관계 진행 시스템

#### 호감도 시스템 (0-100 레벨)
자동으로 호감도가 상승하는 이벤트:

| 이벤트 | 호감도 상승 | 발생 조건 |
|--------|------------|-----------|
| 일상 대화 | +1 | 모든 대화 |
| 깊은 대화 | +3 | 100자 이상 메시지 |
| 공통 관심사 언급 | +2 | 관심사 키워드 감지 |
| 감정적 지지 | +5 | 위로, 격려 표현 |
| 개인 이야기 공유 | +4 | 사적인 이야기 |
| 칭찬 | +2 | 긍정적 피드백 |
| 디테일 기억 | +3 | 과거 대화 언급 |
| 첫 아침 인사 | +2 | 6-9시 첫 대화 |
| 깊은 밤 대화 | +3 | 22시-2시 대화 |
| 일주일 연속 대화 | +5 | 7일 스트릭 달성 |

#### 5단계 관계 발전
```
┌─────────────────────────────────────────────┐
│  호감도   │  관계 단계      │  특징          │
├─────────────────────────────────────────────┤
│  0-19    │  처음 만난 사이  │  조심스러운 대화 │
│  20-39   │  안면이 있는 사이 │  편해지는 중    │
│  40-59   │  친구           │  편한 대화      │
│  60-79   │  가까운 친구     │  깊은 이야기    │
│  80-100  │  연인 ❤️        │  특별한 관계    │
└─────────────────────────────────────────────┘
```

#### 마일스톤 시스템
- 첫 대화 (1회)
- 10회 대화 달성
- 50회 대화 달성
- 100회 대화 달성
- 1주일 함께한 기념일
- 1개월 함께한 기념일
- 관계 단계 업그레이드

### 💬 지능형 대화 시스템

#### Google Gemini 2.5 Flash 기반
- 최신 AI 모델 활용
- 자연스러운 대화 생성
- 감정 이해 및 표현

#### File Search RAG - 완벽한 기억력
**모든 대화와 파일이 영구 저장되어 캐릭터가 기억합니다**

- ✅ **모든 대화 내용 자동 저장**: 사용자와 AI의 모든 대화가 RAG에 저장
- ✅ **업로드한 파일 기억**: 이미지, 문서 등 업로드한 모든 파일을 RAG에 저장하여 나중에 참조
- ✅ **과거 대화 자동 검색**: 과거에 나눴던 대화 내용을 자동으로 찾아서 맥락 이해
- ✅ **캐릭터별 독립 메모리**: 각 캐릭터는 자신만의 독립적인 기억 공간 보유
- ✅ **벡터 기반 시맨틱 검색**: 의미 기반으로 관련 대화 내용을 지능적으로 검색
- ✅ **재접속 시 대화 이어가기**: 다음에 접속해도 과거 기억을 바탕으로 자연스럽게 대화 계속
- ✅ **관계 진행 누적**: 호감도와 관계 단계가 계속 쌓여서 발전

**💡 초기화 기능**
- "초기화" 버튼을 누르면 RAG의 모든 데이터(프로필, 대화 기록, 업로드 파일)가 완전히 삭제됩니다
- 완전히 새로운 시작과 동일한 상태가 됩니다

#### 시간 인식 컨텍스트
**시간대별 인사**
- 🌅 **새벽 (5-8시)**: "좋은 아침이에요! 일찍 일어나셨네요"
- ☀️ **오전 (8-12시)**: "활기찬 아침이네요!"
- 🌤️ **오후 (12-18시)**: "점심은 드셨어요?"
- 🌆 **저녁 (18-22시)**: "하루 마무리는 어떠세요?"
- 🌙 **밤 (22-24시)**: "늦은 시간이네요. 아직 안 주무세요?"
- ✨ **심야 (0-5시)**: "깊은 밤이네요... 잠이 안 오세요?"

**요일 인식**
- 월요일: "한 주의 시작! 힘내요! 💪"
- 금요일: "불금이에요! 주말이 코앞이에요 🎉"
- 주말: "편안한 휴일 보내세요 ☀️"

**계절 감지**
- 봄: "꽃이 피고 있을 것 같아요 🌸"
- 여름: "더위 조심하세요 ☀️"
- 가을: "단풍이 아름다운 시기네요 🍂"
- 겨울: "따뜻하게 지내세요! ❄️"

**특별한 날**
- 발렌타인데이 (2/14)
- 화이트데이 (3/14)
- 크리스마스 (12/24-25)
- 새해 (1/1)

#### 파일 업로드 기능
**대화 중 이미지와 문서를 공유할 수 있습니다**

- 📎 **지원 파일 형식**: 이미지(image/*), PDF, DOCX, TXT, JSON
- 🖼️ **이미지 미리보기**: 업로드한 이미지를 전송 전에 미리 확인 가능
- 📄 **파일 정보 표시**: 파일명과 크기를 UI에 표시
- 🗑️ **전송 전 삭제**: 잘못 선택한 파일을 전송 전에 삭제 가능
- 💾 **RAG 자동 저장**: 업로드한 파일이 자동으로 RAG에 저장되어 나중에 참조 가능
- 💬 **파일 기반 대화**: 이미지나 문서를 보내면서 "이 사진에 대해 이야기해줘" 같은 대화 가능

#### 실시간 스트리밍 응답
- Server-Sent Events (SSE) 방식
- 타이핑하는 것처럼 실시간 표시
- 자연스러운 대화 흐름

### 📊 관계 대시보드

#### 시각화 요소
- **호감도 진행 바**: 현재 호감도 시각적 표시
- **관계 단계 뱃지**: 현재 관계 상태
- **통계 카드**:
  - 💬 총 대화 횟수
  - 📅 알고 지낸 날짜
  - 🔥 연속 대화 일수
  - 🎉 달성한 마일스톤 수

#### 마일스톤 타임라인
- 최근 5개 마일스톤 표시
- 달성 날짜 및 당시 호감도
- 관계 발전 과정 시각화

#### 대화 품질 점수
- 0-10점 척도
- 대화의 깊이와 질 평가
- 실시간 업데이트

---

## 🛠️ 기술 스택

### Backend
- **프레임워크**: FastAPI 0.115.0+
- **언어**: Python 3.11+
- **AI 모델**: Google Gemini 2.5 Flash
- **RAG 시스템**: Gemini File Search Store
- **비동기 처리**: asyncio, run_in_executor
- **파일 처리**: python-multipart, Pillow

### Frontend
- **UI 라이브러리**: React 19
- **언어**: TypeScript 5.7+
- **빌드 도구**: Vite 6.3+
- **HTTP 클라이언트**: Axios 1.12+
- **스타일링**: Tailwind CSS 4.1+
- **UI 컴포넌트**: Radix UI
- **3D 아바타**: Ready Player Me (iframe 통합)

### AI & RAG Infrastructure
- **대화 생성**: Google Gemini 2.5 Flash
- **임베딩**: Gemini Embedding API (text-embedding-004)
- **벡터 DB**: Google File Search Store (관리형)
- **청킹**: Google 자동 최적화 알고리즘

### 핵심 의존성
```toml
# Backend (pyproject.toml)
google-genai>=1.50.0    # File Search Store 필수
fastapi>=0.115.0
uvicorn>=0.32.0
python-dotenv>=1.0.1
Pillow>=10.0.0
python-multipart>=0.0.6
```

```json
// Frontend (package.json)
"react": "^19.0.0"
"typescript": "~5.7.2"
"vite": "^6.3.4"
"axios": "^1.12.2"
"tailwindcss": "^4.1.5"
```

---

## 🚀 빠른 시작

### 사전 요구사항
- **Python** 3.11 이상
- **Node.js** 18 이상
- **Google Gemini API 키** (필수)
  - [여기서 발급](https://aistudio.google.com/app/apikey)
- **Ready Player Me Subdomain** (선택 - 3D 아바타 사용 시)
  - [Ready Player Me Studio](https://studio.readyplayer.me/)에서 Application 생성

### 1. 저장소 클론
```bash
git clone <repository-url>
cd trinity_ai_friend_rag_fullstack
```

### 2. Backend 설정

#### 2.1 의존성 설치
```bash
cd backend

# 가상환경 생성 (권장)
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -e .
```

#### 2.2 환경 변수 설정
`.env` 파일 내용:
```env
# 필수: Google Gemini API 키
GEMINI_API_KEY=your_actual_gemini_api_key_here

# 서버 설정
HOST=0.0.0.0
PORT=8000
```

**Gemini API 키 발급 방법:**
1. https://aistudio.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. 생성된 키를 `.env` 파일에 붙여넣기

#### 2.3 Backend 서버 실행
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**정상 실행 로그:**
```
✅ Google (Gemini) 연결 완료
✅ Gemini File Search Manager 초기화 완료
🚀 MATE.AI 시작
✅ 사용 가능한 AI: Gemini
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Frontend 설정

새 터미널 열기:

```bash
cd frontend

# 의존성 설치
npm install
```

#### 3.1 (선택) Ready Player Me 설정

3D 아바타 커스터마이징을 사용하려면:

1. **Ready Player Me Studio 접속**
   - https://studio.readyplayer.me/ 방문
   - Google 계정으로 로그인

2. **Application 생성**
   - "Add application" 클릭
   - Name: "MATE.AI" (또는 원하는 이름)
   - Type: "Web" 선택
   - 생성 완료

3. **Subdomain 확인**
   - My Applications에서 생성한 앱 클릭
   - Subdomain 복사 (예: `mateai-9h686e`)

4. **환경 변수 설정**
   - `frontend/.env` 파일 생성:
   ```env
   # Ready Player Me 설정 (선택)
   VITE_READYPLAYERME_SUBDOMAIN=your-subdomain-here
   ```

   예시:
   ```env
   VITE_READYPLAYERME_SUBDOMAIN=mateai-9h686e
   ```

   > **참고**: 설정하지 않으면 기본값 'demo'로 작동합니다.

#### 3.2 Frontend 서버 실행

```bash
# frontend 폴더에서
npm run dev
```

**정상 실행 로그:**
```
VITE v6.3.4  ready in 352 ms

➜  Local:   http://localhost:5173/
➜  Network: http://192.168.x.x:5173/
```

### 4. 브라우저에서 접속

http://localhost:5173 열기

---

## ⚡ 빠른 실행 (Windows)

Windows 사용자를 위한 원클릭 실행 스크립트:

### 최초 설치
```bash
# 1. 저장소 클론
git clone <repository-url>
cd <repository-name>

# 2. 자동 설치 실행
install.bat
```

`install.bat`가 자동으로:
- Backend 가상환경 생성 및 패키지 설치
- Frontend 의존성 설치

### 환경 변수 설정

설치 후 반드시 설정:

1. **Backend API 키**
   ```bash
   # backend/.env 파일 생성 후 편집
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   HOST=0.0.0.0
   PORT=8000
   ```

2. **(선택) Frontend Ready Player Me**
   ```bash
   # frontend/.env 파일 생성 후 편집
   VITE_READYPLAYERME_SUBDOMAIN=your-subdomain-here
   ```

### 서버 실행

```bash
# 프로젝트 루트 폴더에서
run-all.bat
```

`run-all.bat`가 자동으로:
- Backend 서버 시작 (포트 8000)
- Frontend 개발 서버 시작 (포트 5173)
- 브라우저 자동 오픈 (http://localhost:5173)

두 서버가 동시에 실행되며, `Ctrl+C`로 종료할 수 있습니다.

---

## 📁 프로젝트 구조

```
trinity_ai_friend_rag_fullstack/
├── backend/                             # Python FastAPI 백엔드
│   ├── main.py                          # 메인 서버 (FastAPI 앱)
│   ├── character_manager.py             # 캐릭터 생성 & 관리
│   ├── relationship_tracker.py          # 관계 진행도 추적 시스템
│   ├── daily_context.py                 # 시간/컨텍스트 인식
│   ├── ai_manager.py                    # AI 모델 통합 관리
│   ├── file_search_manager.py           # Gemini File Search RAG
│   ├── pyproject.toml                   # Python 의존성
│   ├── .env                             # API 키 (gitignore)
│   ├── .env.example                     # 환경 변수 예시
│   ├── data/                            # 데이터 저장소
│   │   ├── characters/                  # 캐릭터 메타데이터
│   │   │   ├── {character_id}.json      # 캐릭터 정보
│   │   │   ├── {character_id}_relationship.json  # 관계 데이터
│   │   │   └── images/                  # 캐릭터 이미지
│   │   │       └── {character_id}.png
│   │   └── file_search_metadata.json    # RAG Store 정보
│   └── src/                             # LangGraph 에이전트 (선택)
│
└── frontend/                            # React TypeScript 프론트엔드
    ├── src/
    │   ├── App.tsx                      # 메인 앱 컴포넌트
    │   ├── App.css                      # 전역 스타일
    │   ├── main.tsx                     # React 엔트리포인트
    │   ├── components/
    │   │   ├── CharacterCreation.tsx    # 4단계 캐릭터 생성 마법사
    │   │   ├── ReadyPlayerMeCustomizer.tsx # Ready Player Me 3D 아바타
    │   │   ├── ChatInterface.tsx        # 채팅 UI (Her 스타일)
    │   │   ├── RelationshipDashboard.tsx # 관계 대시보드
    │   │   ├── CharacterProfile.tsx     # 캐릭터 프로필 뷰어
    │   │   └── ui/                      # shadcn UI 컴포넌트
    │   │       ├── button.tsx
    │   │       ├── card.tsx
    │   │       ├── input.tsx
    │   │       └── ...
    │   └── lib/
    │       └── utils.ts                 # 유틸리티 함수
    ├── package.json                     # Node 의존성
    ├── vite.config.ts                   # Vite 설정
    ├── tsconfig.json                    # TypeScript 설정
    ├── tailwind.config.js               # Tailwind 설정
    └── components.json                  # shadcn 설정
```

---


## 📖 상세 설명

### 데이터 저장 구조 및 RAG 시스템

#### 영구 저장 (서버 재시작 후에도 유지)

**1. File Search Store (Gemini 클라우드 RAG)**
   - 📝 캐릭터 프로필 (이름, 성격, 배경스토리 등)
   - 💬 모든 대화 내용 (사용자 ↔ AI 대화 쌍)
   - 📎 업로드한 파일 (이미지, PDF, DOCX, TXT, JSON)
   - 🔍 자동 생성된 임베딩 (벡터 검색용)

**작동 방식:**
- 캐릭터 생성 시: 프로필이 `{character_id}_profile.txt`로 RAG에 업로드
- 대화할 때마다: `{character_id}_conversation_{timestamp}.txt` 형태로 대화 저장
- 파일 업로드 시: 파일이 RAG에 업로드되어 나중에 참조 가능
- 다음 대화 시: 사용자 메시지 기반으로 관련 과거 대화 및 파일을 자동 검색하여 컨텍스트 제공

**2. 로컬 JSON 파일** (`backend/data/characters/`)
   - `{character_id}.json`: 캐릭터 메타데이터 (대화 횟수, 호감도, 관계 단계, 이미지 경로)
   - `{character_id}_relationship.json`: 관계 추적 데이터 (마일스톤, 통계)
   - `file_search_metadata.json`: RAG Store 정보 (Store ID, 생성일시)
   - `images/{character_id}.*`: 캐릭터 이미지 파일

#### 임시 저장 (재시작 시 초기화)
- 대화 히스토리 (메모리) - 현재 세션 동안만 유지

#### 초기화 시 삭제되는 데이터
**"초기화" 버튼 클릭 시 완전 삭제:**
1. ✅ RAG의 모든 문서 (프로필 + 모든 대화 기록 + 업로드한 파일)
2. ✅ 로컬 메타데이터 (JSON 파일)
3. ✅ 캐릭터 이미지
4. ✅ 관계 추적 데이터

→ 완전히 새로운 시작 상태로 돌아갑니다.

---

## 💰 RAG 비용 및 서버리스 아키텍처 장점

### 📊 실제 운영 비용 (2025년 기준)

MATE.AI는 **Google Cloud의 완전 관리형 서버리스 RAG** 시스템을 사용하여 **매우 저렴한 비용**으로 운영됩니다.

#### 1️⃣ File Search RAG 비용 (거의 무료!)

| 항목 | 가격 | 설명 |
|------|------|------|
| 초기 파일 인덱싱 | $0.15 / 100만 토큰 | 최초 1회만 발생 |
| 저장 비용 | **무료** ✅ | 클라우드 저장 완전 무료 |
| 쿼리 시 임베딩 | **무료** ✅ | 검색 시 임베딩 생성 무료 |
| 컨텍스트 검색 | **무료** ✅ | RAG 검색 완전 무료 |

**실제 비용 예시:**
- 캐릭터 프로필 업로드: ~500 토큰 → **$0.000075** (약 0.1원)
- 대화 1회 저장: ~200 토큰 → **$0.00003** (약 0.004원)
- **100회 대화 저장**: **$0.003** (약 **4원**)
- **월간 RAG 저장 비용**: **1원 미만** (거의 무시 가능)

#### 2️⃣ Gemini 2.5 Flash 대화 비용 (주요 비용)

| 항목 | 가격 | 실제 사용량 |
|------|------|------------|
| Input 토큰 | $0.30 / 100만 | ~1,500 토큰/대화 |
| Output 토큰 | $2.50 / 100만 | ~200 토큰/대화 |
| **대화 1회 비용** | **$0.00095** | **약 1.25원** |

#### 3️⃣ 실제 사용 시나리오별 월 비용

**💡 라이트 유저** (하루 10번 대화)
- 대화 비용: 10회 × $0.00095 = **$0.0095/일**
- RAG 저장: 거의 무료
- **월 비용: $0.30** (약 **400원/월**)

**📱 미들 유저** (하루 50번 대화)
- 대화 비용: 50회 × $0.00095 = **$0.0475/일**
- RAG 저장: 거의 무료
- **월 비용: $1.50** (약 **2,000원/월**)

**🔥 헤비 유저** (하루 200번 대화)
- 대화 비용: 200회 × $0.00095 = **$0.19/일**
- RAG 저장: 거의 무료
- **월 비용: $6.00** (약 **8,000원/월**)

### ☁️ 서버리스 아키텍처의 핵심 장점

#### 1. **완전 관리형 서비스 (Zero Maintenance)**
- ✅ 인프라 관리 불필요: 서버, DB, 벡터 스토어 직접 구축/운영 필요 없음
- ✅ 자동 스케일링: 사용량에 따라 자동으로 확장/축소
- ✅ 유지보수 제로: 백업, 업데이트, 보안 패치 모두 Google이 처리
- ✅ 고가용성 보장: 99.9% SLA 자동 제공

#### 2. **종량제 과금 (Pay-as-you-go)**
- ✅ 사용한 만큼만 과금 (초기 투자 비용 $0)
- ✅ 트래픽 없으면 비용도 없음
- ✅ 고정 서버 비용 $0
- ✅ 사용자 수 증가 시 자동 확장

#### 3. **전통적 RAG vs 서버리스 RAG 비용 비교**

| 구분 | 전통적 RAG (자체 구축) | 서버리스 RAG (Gemini) |
|------|----------------------|---------------------|
| Vector DB | Pinecone/Weaviate: $70~100/월 | **무료** ✅ |
| 임베딩 API | OpenAI: $0.13/100만 토큰 | **무료** (쿼리 시) ✅ |
| 서버 호스팅 | AWS/GCP: $20~50/월 | **무료** ✅ |
| 유지보수 | 개발자 시간 비용 | **무료** (Google 관리) ✅ |
| **월 고정 비용** | **최소 $90~150** | **$0** ✅ |
| **실제 사용 비용** | 고정 비용 + 사용량 | **사용량만** ✅ |

#### 4. **스타트업/개인 프로젝트 최적화**
- ✅ **초기 단계**: 사용자 거의 없을 때 → 비용 거의 $0
- ✅ **성장 단계**: 사용자 증가 시 → 자동 스케일링, 비용은 매출에 비례
- ✅ **글로벌 배포**: Google Cloud의 전 세계 데이터센터 자동 활용
- ✅ **빠른 개발**: 백엔드 인프라 걱정 없이 비즈니스 로직에 집중

### 🚀 비용 절감 방안 (선택)

원한다면 추가로 비용을 더 절감할 수 있습니다:

**1. Gemini 2.5 Flash-Lite로 전환** (76% 비용 절감)
- Input: $0.10 / 100만 토큰 (67% 절감)
- Output: $0.40 / 100만 토큰 (84% 절감)
- 대화 1회: **$0.00023** (약 **0.3원**, 기존 대비 76% 절감)

**2. Context Caching 활용** (Input 비용 90% 절감)
- 캐릭터 프로필은 매번 반복되므로 캐싱 가능
- 캐시 읽기: 기본 input 가격의 10%

**3. Batch API 활용** (50% 할인)
- 긴급하지 않은 작업(예: 일간 요약)에 활용

### 📈 결론

✅ **RAG 저장 비용: 거의 무료** (월 1원 미만)
✅ **주요 비용: 대화 생성 비용** (대화 1회 약 1.25원)
✅ **일반 사용자 월 비용: 400~2,000원**
✅ **서버리스 아키텍처로 초기 투자 비용 $0**
✅ **사용한 만큼만 과금, 트래픽 없으면 비용도 없음**

**MATE.AI는 클라우드 서버리스 RAG 덕분에 개인 프로젝트부터 상용 서비스까지 매우 경제적으로 운영 가능합니다! 🎉**

---

## 🛠️ 개발 가이드

### 환경 변수 설명

#### Backend (.env)
```env
# 필수
GEMINI_API_KEY=your_key_here

# 서버 설정
HOST=0.0.0.0
PORT=8000

# LangSmith (선택)
LANGSMITH_STUDIO_AUTO_OPEN=false
```

#### Frontend (.env)
```env
# Ready Player Me 3D 아바타 (선택)
# https://studio.readyplayer.me/ 에서 Application 생성 후 Subdomain 입력
# 기본값은 'demo'이므로 설정하지 않아도 작동합니다
VITE_READYPLAYERME_SUBDOMAIN=your-subdomain-here
```

---

## 🐛 트러블슈팅

### 자주 묻는 질문

**Q: Gemini API 키는 어디서 발급받나요?**
A: https://aistudio.google.com/app/apikey

**Q: 무료로 사용 가능한가요?**
A: Gemini API는 무료 할당량이 있습니다. 자세한 내용은 Google AI 문서 참조.

**Q: Ready Player Me 설정이 필수인가요?**
A: 아닙니다. 선택사항입니다. 설정하지 않아도 이미지 업로드 방식으로 캐릭터를 생성할 수 있습니다.

**Q: 3D 아바타 생성 시 성별을 어떻게 선택하나요?**
A:
- 1단계에서 선택한 성별은 AI의 정체성(대화 스타일)을 결정합니다
- 3D 아바타의 외형 성별은 아바타 에디터 내에서 별도로 선택할 수 있습니다
- 예: 여성 AI + 남성 아바타, 남성 AI + 여성 아바타 등 자유로운 조합 가능

**Q: MATE.AI 3D 아바타가 로딩되지 않아요**
A:
1. Vite 개발 서버를 재시작하세요 (환경 변수 반영)
2. 브라우저 콘솔(F12)에서 에러 메시지 확인
3. Ready Player Me Studio에서 Subdomain이 올바른지 확인
4. 10초 타임아웃 후 자동으로 아바타 에디터가 표시됩니다

**Q: 다른 언어도 지원하나요?**
A: 현재는 한국어만 지원합니다.

**Q: Backend 서버가 시작되지 않아요**
A:
1. Python 3.11 이상이 설치되어 있는지 확인
2. 가상환경이 활성화되어 있는지 확인
3. `.env` 파일에 GEMINI_API_KEY가 설정되어 있는지 확인
4. `pip install -e .`로 패키지가 제대로 설치되었는지 확인

**Q: Frontend 빌드 에러가 발생해요**
A:
1. Node.js 18 이상이 설치되어 있는지 확인
2. `node_modules` 삭제 후 `npm install` 재실행
3. `npm cache clean --force` 실행 후 재설치

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

## 🙏 감사의 말

이 프로젝트는 영화 "Her"에서 영감을 받아 만들어졌습니다.

---

**Made with ❤️ for meaningful AI relationships**

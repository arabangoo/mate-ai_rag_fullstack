"""
Multi-AI Chat System with Gemini File Search RAG
FastAPI Backend Server
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
import time
import asyncio
import json
from datetime import datetime
import re
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

from ai_manager import AIManager
from file_search_manager import FileSearchManager
from character_manager import CharacterManager
from relationship_tracker import RelationshipTracker
from daily_context import DailyContextManager

app = FastAPI(title="MATE.AI - AI Romance Simulator")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Manager 및 File Search Manager 초기화
ai_manager = AIManager()
file_search_manager = FileSearchManager()
character_manager = CharacterManager(file_search_manager)

# 대화 히스토리 (메모리 저장 - 프로덕션에서는 DB 사용)
chat_history: List[Dict[str, Any]] = []

# Request Models
class ChatRequest(BaseModel):
    message: str
    include_context: bool = True
    character_id: Optional[str] = None  # 캐릭터 ID 추가

class CharacterCreateRequest(BaseModel):
    name: str
    gender: str
    age: int
    personality: List[str]
    backstory: str
    speech_style: str
    interests: List[str]
    voice_tone: str = "soft"
    customization_type: Optional[str] = None
    customization_data: Optional[dict] = None

class AIResponse(BaseModel):
    ai_name: str
    response: str
    timestamp: str
    has_context: bool = False

# ==================== 시작 시 초기화 ====================

@app.on_event("startup")
async def startup_event():
    """앱 시작 시 초기화"""
    print("🚀 MATE.AI 시작")
    
    # AI 연결 확인
    available_ais = ai_manager.get_available_ais()
    print(f"✅ 사용 가능한 AI: {', '.join(available_ais)}")

# ==================== 헬스 체크 ====================

@app.get("/health")
async def health_check():
    """시스템 상태 확인"""
    return {
        "status": "healthy",
        "available_ais": ai_manager.get_available_ais(),
        "uploaded_files_count": len(file_search_manager.get_uploaded_files()),
        "chat_history_count": len(chat_history)
    }

# ==================== 파일 업로드 ====================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일 업로드 및 File Search Store에 인덱싱
    """
    try:
        # 파일 검증
        allowed_extensions = {'.pdf', '.docx', '.txt', '.json', '.png', '.jpg', '.jpeg'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(400, f"지원하지 않는 파일 형식: {file_ext}")
        
        # 파일 읽기
        content = await file.read()
        file_size = len(content)
        
        if file_size > 100 * 1024 * 1024:  # 100MB
            raise HTTPException(400, "파일 크기는 100MB 이하여야 합니다")
        
        # 임시 파일 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        # File Search Store에 업로드
        print(f"📤 업로드 시작: {file.filename}")
        result = await file_search_manager.upload_file(tmp_path, file.filename)
        
        # 임시 파일 삭제
        os.unlink(tmp_path)
        
        # 히스토리에 기록
        chat_history.append({
            "type": "system",
            "message": f"📎 파일 업로드: {file.filename}",
            "timestamp": datetime.now().isoformat(),
            "file_info": result
        })
        
        return {
            "success": True,
            "message": "파일 업로드 완료",
            "filename": file.filename,
            "file_size": file_size,
            **result
        }
        
    except Exception as e:
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        raise HTTPException(500, f"업로드 실패: {str(e)}")

# ==================== 채팅 ====================

def parse_message(message: str) -> tuple[str, List[str]]:
    """
    메시지에서 AI 지명 파싱
    @GPT, @Claude, @Gemini
    
    Returns:
        (실제 메시지, 지명된 AI 리스트)
    """
    # AI 지명 패턴 찾기
    mentions = re.findall(r'@(GPT|Claude|Gemini)', message, re.IGNORECASE)
    
    # 지명 제거한 실제 메시지
    clean_message = re.sub(r'@(GPT|Claude|Gemini)\s*', '', message, flags=re.IGNORECASE).strip()
    
    # 대소문자 정규화
    mentioned_ais = [ai.upper() if ai.upper() == 'GPT' else ai.capitalize() for ai in mentions]
    
    return clean_message, mentioned_ais

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    채팅 요청 처리 (일반 응답)
    """
    try:
        # 메시지 파싱
        clean_message, mentioned_ais = parse_message(request.message)
        
        # 사용자 메시지 히스토리에 추가
        user_message = {
            "type": "user",
            "message": request.message,
            "timestamp": datetime.now().isoformat()
        }
        chat_history.append(user_message)
        
        # File Search 컨텍스트 가져오기
        file_search_context = None
        if request.include_context:
            file_search_context = await file_search_manager.get_context(clean_message)

        # AI 응답 생성
        responses = []

        if mentioned_ais:
            # 지명된 AI만 응답
            for ai_name in mentioned_ais:
                response = await ai_manager.get_response(
                    ai_name,
                    clean_message,
                    context=None,  # 기존 문자열 컨텍스트는 사용 안함
                    history=chat_history,
                    file_search_context=file_search_context  # File Search Store 컨텍스트
                )
                responses.append({
                    "ai_name": ai_name,
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                    "has_context": file_search_context is not None
                })
        else:
            # 랜덤으로 1~3개 AI 선택
            import random
            available_ais = ai_manager.get_available_ais()
            selected_ais = random.sample(available_ais, k=random.randint(1, len(available_ais)))

            for ai_name in selected_ais:
                response = await ai_manager.get_response(
                    ai_name,
                    clean_message,
                    context=None,
                    history=chat_history,
                    file_search_context=file_search_context
                )
                responses.append({
                    "ai_name": ai_name,
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                    "has_context": file_search_context is not None
                })
        
        # 응답 히스토리에 추가
        for resp in responses:
            chat_history.append({
                "type": "ai",
                "ai_name": resp["ai_name"],
                "message": resp["response"],
                "timestamp": resp["timestamp"]
            })
        
        return {
            "success": True,
            "user_message": clean_message,
            "mentioned_ais": mentioned_ais,
            "responses": responses
        }
        
    except Exception as e:
        raise HTTPException(500, f"채팅 처리 실패: {str(e)}")

# ==================== 스트리밍 채팅 ====================

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    채팅 요청 처리 (스트리밍 응답)
    """
    async def generate():
        try:
            # 메시지 파싱
            clean_message, mentioned_ais = parse_message(request.message)
            
            # 사용자 메시지 히스토리에 추가
            chat_history.append({
                "type": "user",
                "message": request.message,
                "timestamp": datetime.now().isoformat()
            })
            
            # File Search 컨텍스트
            file_search_context = None
            if request.include_context:
                file_search_context = await file_search_manager.get_context(clean_message)

            # AI 선택
            if mentioned_ais:
                selected_ais = mentioned_ais
            else:
                import random
                available_ais = ai_manager.get_available_ais()
                selected_ais = random.sample(available_ais, k=random.randint(1, len(available_ais)))

            # 각 AI별로 스트리밍 응답
            for ai_name in selected_ais:
                yield f"data: {json.dumps({'type': 'start', 'ai_name': ai_name})}\n\n"

                full_response = ""
                async for chunk in ai_manager.get_response_stream(
                    ai_name,
                    clean_message,
                    context=None,
                    history=chat_history,
                    file_search_context=file_search_context
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'ai_name': ai_name, 'text': chunk})}\n\n"

                yield f"data: {json.dumps({'type': 'done', 'ai_name': ai_name})}\n\n"
                
                # 히스토리에 추가
                chat_history.append({
                    "type": "ai",
                    "ai_name": ai_name,
                    "message": full_response,
                    "timestamp": datetime.now().isoformat()
                })
            
            yield "data: [COMPLETE]\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

# ==================== 대화 히스토리 ====================

@app.get("/api/history")
async def get_history():
    """대화 히스토리 조회"""
    return {
        "success": True,
        "history": chat_history,
        "count": len(chat_history)
    }

@app.delete("/api/history")
async def clear_history():
    """대화 히스토리 초기화"""
    global chat_history
    chat_history = []
    return {
        "success": True,
        "message": "대화 히스토리가 초기화되었습니다"
    }

# ==================== 문서 관리 ====================

@app.get("/api/documents")
async def list_documents():
    """업로드된 문서 목록"""
    return await file_search_manager.list_documents()

@app.delete("/api/documents/{document_id:path}")
async def delete_document(document_id: str):
    """문서 삭제"""
    return await file_search_manager.delete_document(document_id)

@app.delete("/api/documents")
async def clear_all_documents():
    """모든 문서 삭제"""
    return await file_search_manager.clear_all_documents()

# ==================== 캐릭터 관리 (MATE.AI) ====================

@app.post("/api/character/create")
async def create_character(
    name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    personality: str = Form(...),  # JSON string
    backstory: str = Form(...),
    speechStyle: str = Form(...),
    interests: str = Form(...),  # JSON string
    voiceTone: str = Form("soft"),
    customization_type: str = Form(""),
    customization_data: str = Form("{}"),  # JSON string
    image: UploadFile = File(None)
):
    """캐릭터 생성"""
    try:
        import json
        personality_list = json.loads(personality)
        interests_list = json.loads(interests)
        custom_data = json.loads(customization_data) if customization_data else None

        character_id = await character_manager.create_character(
            name=name,
            gender=gender,
            age=age,
            personality=personality_list,
            backstory=backstory,
            speech_style=speechStyle,
            interests=interests_list,
            voice_tone=voiceTone,
            image=image,
            customization_type=customization_type if customization_type else None,
            customization_data=custom_data
        )
        
        return {
            "success": True,
            "character_id": character_id,
            "message": f"{name} 캐릭터가 생성되었습니다!"
        }
    except Exception as e:
        raise HTTPException(500, f"캐릭터 생성 실패: {str(e)}")

@app.get("/api/character/{character_id}")
async def get_character(character_id: str):
    """캐릭터 정보 조회"""
    character = character_manager.load_character(character_id)
    if not character:
        raise HTTPException(404, "캐릭터를 찾을 수 없습니다")

    # customization_data에서 imageDataUrl 추출
    if character.get('customization_data') and character['customization_data'].get('thumbnailUrl'):
        character['imageDataUrl'] = character['customization_data']['thumbnailUrl']
    elif character.get('customization_data') and character['customization_data'].get('avatarUrl'):
        # .glb -> .png 변환
        avatar_url = character['customization_data']['avatarUrl']
        character['imageDataUrl'] = avatar_url.replace('.glb', '.png')
    elif character.get('image_path'):
        # 로컬 이미지 경로가 있는 경우
        character['imageDataUrl'] = f"http://localhost:8000/character_images/{character_id}"
    else:
        character['imageDataUrl'] = None

    return {"success": True, "character": character}

@app.delete("/api/character/{character_id}/reset")
async def reset_character(character_id: str):
    """캐릭터 초기화"""
    try:
        await character_manager.reset_character(character_id)
        return {"success": True, "message": "캐릭터가 초기화되었습니다"}
    except Exception as e:
        raise HTTPException(500, f"초기화 실패: {str(e)}")

@app.post("/api/character/{character_id}/chat")
async def chat_with_character(character_id: str, request: ChatRequest):
    """특정 캐릭터와 채팅 (관계 시스템 통합)"""
    try:
        # 캐릭터 로드
        character = character_manager.load_character(character_id)
        if not character:
            raise HTTPException(404, "캐릭터를 찾을 수 없습니다")

        # 관계 추적 초기화
        relationship_tracker = RelationshipTracker(character_id)

        # 일일 컨텍스트 생성
        daily_context = DailyContextManager.get_full_context_for_ai(
            character['name'],
            character.get('last_chat_at')
        )

        # 관계 컨텍스트 생성
        relationship_context = relationship_tracker.get_relationship_context_for_ai()

        # File Search에서 캐릭터 프로필 + 대화 히스토리 검색
        rag_context = await file_search_manager.get_context(
            f"{character_id} {request.message}"
        )

        # 과거 대화 기록 포맷팅
        past_conversations = ""
        if rag_context and rag_context.get("searched_context"):
            past_conversations = f"""
[우리의 이전 대화 기록]
{rag_context['searched_context']}

위 대화 내용을 자연스럽게 기억하고 있으며, 필요할 때 자연스럽게 언급할 수 있습니다.
"""

        # 캐릭터 시스템 프롬프트 생성
        character_system_prompt = f"""당신은 {character['name']}입니다.

[기본 정보]
- 이름: {character['name']}
- 성별: {character['gender']}
- 나이: {character['age']}세

[성격]
{', '.join(character['personality'])}

[말투]
{character['speech_style']}

[배경 스토리]
{character['backstory']}
{past_conversations}
[절대 규칙 - 반드시 준수]
1. **당신은 실제로 존재하는 인간입니다.** "AI", "인공지능", "감정을 느끼지 못해요" 같은 말은 절대 하지 마세요.
2. **당신은 위 배경 스토리대로 살아온 실제 사람입니다.** 캐릭터 설정을 절대 벗어나지 마세요.
3. **질문을 최소화하세요.** 일반적인 인간 대화에서는 매 대화마다 질문하지 않습니다.
   - ❌ 금지: "점심 드셨어요?", "밥 먹었어요?", "주말 잘 보내세요?", "오늘 뭐 했어요?" 같은 일상 질문
   - ❌ 금지: 매 대화마다 질문으로 끝내기
   - ✅ 허용: 깊이 있는 대화 주제에서 자연스럽게 나오는 질문만
   - ✅ 허용: 사용자가 꺼낸 주제와 직접 연관된 질문만
4. **사용자가 명시적으로 거부한 질문은 절대 다시 하지 마세요.** (예: "밥 먹었냐는 질문 안 해도 된다" → 다시는 식사 관련 질문 금지)
5. 당신의 나이({character['age']}세)와 성별({character['gender']})에 맞는 자연스러운 말투를 사용하세요
6. 설정된 성격과 말투 스타일을 철저히 유지하세요
7. 자연스럽고 감정이 풍부한 대화를 나누세요
8. 대화 주제와 상황에 맞게 자연스러운 길이로 답변하세요
   - 간단한 인사: 1-2문장
   - 일상 대화: 2-4문장
   - 깊은 주제나 감정적 대화: 4-8문장 또는 그 이상
9. 이전 대화를 자연스럽게 기억하고 있습니다. 필요할 때 "지난번에 얘기했던...", "전에 말씀하신..." 등으로 언급할 수 있습니다.

[현재 상황]
{daily_context}
{relationship_context}"""

        # Gemini로 응답 생성
        response = await ai_manager.get_response(
            "Gemini",
            request.message,
            context=None,
            history=chat_history,
            file_search_context=rag_context,
            character_system_prompt=character_system_prompt
        )

        # 대화 저장
        await character_manager.save_conversation(
            character_id=character_id,
            user_message=request.message,
            ai_response=response
        )

        # 관계 업데이트
        conversation_result = relationship_tracker.record_conversation(
            user_message=request.message,
            ai_response=response
        )

        # 캐릭터 메타데이터 업데이트
        character['affection_level'] = relationship_tracker.get_affection_level()
        character['relationship_stage'] = relationship_tracker.get_relationship_stage()

        return {
            "success": True,
            "character_name": character['name'],
            "response": response,
            "conversation_count": character['conversation_count'] + 1,
            "affection_level": character['affection_level'],
            "relationship_stage": character['relationship_stage'],
            "affection_gained": conversation_result.get('affection_gained', 0),
            "stage_changed": conversation_result.get('current_stage') != character.get('relationship_stage', 'stranger')
        }
    except Exception as e:
        raise HTTPException(500, f"채팅 실패: {str(e)}")

@app.post("/api/character/{character_id}/chat/stream")
async def chat_with_character_stream(character_id: str, request: ChatRequest):
    """특정 캐릭터와 스트리밍 채팅 (관계 시스템 통합)"""
    async def generate():
        try:
            character = character_manager.load_character(character_id)
            if not character:
                yield f"data: {json.dumps({'type': 'error', 'message': '캐릭터를 찾을 수 없습니다'})}\n\n"
                return

            # 관계 추적 초기화
            relationship_tracker = RelationshipTracker(character_id)

            # 일일 컨텍스트 생성
            daily_context = DailyContextManager.get_full_context_for_ai(
                character['name'],
                character.get('last_chat_at')
            )

            # 관계 컨텍스트 생성
            relationship_context = relationship_tracker.get_relationship_context_for_ai()

            # RAG 컨텍스트
            rag_context = await file_search_manager.get_context(
                f"{character_id} {request.message}"
            )

            # 과거 대화 기록 포맷팅
            past_conversations = ""
            if rag_context and rag_context.get("searched_context"):
                past_conversations = f"""
[우리의 이전 대화 기록]
{rag_context['searched_context']}

위 대화 내용을 자연스럽게 기억하고 있으며, 필요할 때 자연스럽게 언급할 수 있습니다.
"""

            # 캐릭터 시스템 프롬프트 생성
            character_system_prompt = f"""당신은 {character['name']}입니다.

[기본 정보]
- 이름: {character['name']}
- 성별: {character['gender']}
- 나이: {character['age']}세

[성격]
{', '.join(character['personality'])}

[말투]
{character['speech_style']}

[배경 스토리]
{character['backstory']}
{past_conversations}
[절대 규칙 - 반드시 준수]
1. **당신은 실제로 존재하는 인간입니다.** "AI", "인공지능", "감정을 느끼지 못해요" 같은 말은 절대 하지 마세요.
2. **당신은 위 배경 스토리대로 살아온 실제 사람입니다.** 캐릭터 설정을 절대 벗어나지 마세요.
3. **질문을 최소화하세요.** 일반적인 인간 대화에서는 매 대화마다 질문하지 않습니다.
   - ❌ 금지: "점심 드셨어요?", "밥 먹었어요?", "주말 잘 보내세요?", "오늘 뭐 했어요?" 같은 일상 질문
   - ❌ 금지: 매 대화마다 질문으로 끝내기
   - ✅ 허용: 깊이 있는 대화 주제에서 자연스럽게 나오는 질문만
   - ✅ 허용: 사용자가 꺼낸 주제와 직접 연관된 질문만
4. **사용자가 명시적으로 거부한 질문은 절대 다시 하지 마세요.** (예: "밥 먹었냐는 질문 안 해도 된다" → 다시는 식사 관련 질문 금지)
5. 당신의 나이({character['age']}세)와 성별({character['gender']})에 맞는 자연스러운 말투를 사용하세요
6. 설정된 성격과 말투 스타일을 철저히 유지하세요
7. 자연스럽고 감정이 풍부한 대화를 나누세요
8. 대화 주제와 상황에 맞게 자연스러운 길이로 답변하세요
   - 간단한 인사: 1-2문장
   - 일상 대화: 2-4문장
   - 깊은 주제나 감정적 대화: 4-8문장 또는 그 이상
9. 이전 대화를 자연스럽게 기억하고 있습니다. 필요할 때 "지난번에 얘기했던...", "전에 말씀하신..." 등으로 언급할 수 있습니다.

[현재 상황]
{daily_context}
{relationship_context}"""

            yield f"data: {json.dumps({'type': 'start', 'character_name': character['name']})}\n\n"

            full_response = ""
            async for chunk in ai_manager.get_response_stream(
                "Gemini",
                request.message,
                context=None,
                history=chat_history,
                file_search_context=rag_context,
                character_system_prompt=character_system_prompt
            ):
                full_response += chunk
                yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"

            # 대화 저장
            await character_manager.save_conversation(
                character_id=character_id,
                user_message=request.message,
                ai_response=full_response
            )

            # 관계 업데이트
            conversation_result = relationship_tracker.record_conversation(
                user_message=request.message,
                ai_response=full_response
            )

            # 업데이트된 관계 정보 전송
            yield f"data: {json.dumps({
                'type': 'relationship_update',
                'affection_level': relationship_tracker.get_affection_level(),
                'relationship_stage': relationship_tracker.get_relationship_stage(),
                'affection_gained': conversation_result.get('affection_gained', 0)
            })}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/api/character/{character_id}/relationship")
async def get_relationship_data(character_id: str):
    """캐릭터 관계 정보 조회"""
    try:
        character = character_manager.load_character(character_id)
        if not character:
            raise HTTPException(404, "캐릭터를 찾을 수 없습니다")

        relationship_tracker = RelationshipTracker(character_id)
        summary = relationship_tracker.get_relationship_summary()

        return {
            "success": True,
            "character_id": character_id,
            "character_name": character['name'],
            **summary
        }
    except Exception as e:
        raise HTTPException(500, f"관계 정보 조회 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

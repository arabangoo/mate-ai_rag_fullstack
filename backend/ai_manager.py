"""
AI Manager - Gemini AI 관리
"""

import os
from typing import List, Optional, AsyncGenerator, Dict
import asyncio

# Google Gemini
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIManager:
    """Gemini AI 관리자"""

    def __init__(self):
        # API 키 로드
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        # 클라이언트 초기화
        self.gemini_client = None

        if GEMINI_AVAILABLE and self.gemini_key:
            self.gemini_client = genai.Client(api_key=self.gemini_key)
            print("✅ Google (Gemini) 연결 완료")
        else:
            raise RuntimeError("Gemini API를 사용할 수 없습니다. GEMINI_API_KEY를 확인해주세요.")

    def get_available_ais(self) -> List[str]:
        """사용 가능한 AI 목록"""
        return ["Gemini"] if self.gemini_client else []
    
    def format_context(self, context: Optional[str], files: Optional[List[Dict]] = None) -> str:
        """컨텍스트 포맷팅"""
        parts = []
        
        if context:
            parts.append(f"<업로드된 파일 정보>\n{context}\n</업로드된 파일 정보>")
        
        if files:
            file_list = "\n".join([f"- {f['display_name']}" for f in files])
            parts.append(f"<참고 파일 목록>\n{file_list}\n</참고 파일 목록>")
        
        if parts:
            return "\n\n" + "\n\n".join(parts) + "\n\n위 정보를 참고하여 답변해주세요."
        
        return ""
    
    def format_history(self, history: List[dict], limit: int = 5) -> str:
        """대화 히스토리 포맷팅"""
        if not history:
            return ""
        
        recent_history = history[-limit*3:]  # 최근 N개 대화
        formatted = []
        
        for msg in recent_history:
            if msg["type"] == "user":
                formatted.append(f"User: {msg['message']}")
            elif msg["type"] == "ai":
                formatted.append(f"{msg['ai_name']}: {msg['message']}")
        
        if formatted:
            return "\n\n<이전 대화>\n" + "\n".join(formatted) + "\n</이전 대화>\n"
        return ""
    
    async def get_response(
        self,
        ai_name: str,
        message: str,
        context: Optional[str] = None,
        history: Optional[List[dict]] = None,
        file_search_context: Optional[dict] = None,
        character_system_prompt: Optional[str] = None
    ) -> str:
        """AI 응답 생성"""

        # 프롬프트 구성
        full_message = message

        # 캐릭터 채팅이 아닐 때만 RAG 컨텍스트를 메시지에 추가
        # (캐릭터 채팅은 character_system_prompt에 이미 포함되어 있음)
        if not character_system_prompt and file_search_context and file_search_context.get("searched_context"):
            rag_context = file_search_context["searched_context"]
            full_message = f"""<참고 문서 내용>
{rag_context}
</참고 문서 내용>

사용자 질문: {message}

**중요 지침:**
- 위 문서 내용은 참고용입니다. 사용자의 질문이 문서 내용과 관련이 있을 때만 활용하세요.
- 질문이 일반적인 내용(인사, 날씨, 일상 대화 등)이라면 문서 내용을 무시하고 자연스럽게 답변하세요.
- 사용자가 명시적으로 "문서에서", "파일에서", "업로드한 자료에서" 등의 표현을 사용하거나, 문서 내용과 명확히 관련된 질문일 때만 문서를 참조하세요.
- 문서를 참조할 때는 출처를 명시해주세요."""

        if context:
            full_message += self.format_context(context)
        if history:
            full_message = self.format_history(history) + full_message

        if ai_name == "Gemini":
            return await self._get_gemini_response(full_message, file_search_context, character_system_prompt)
        else:
            raise ValueError(f"Gemini만 지원됩니다. 요청된 AI: {ai_name}")
    
    async def get_response_stream(
        self,
        ai_name: str,
        message: str,
        context: Optional[str] = None,
        history: Optional[List[dict]] = None,
        file_search_context: Optional[dict] = None,
        character_system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """AI 응답 스트리밍"""

        # 프롬프트 구성
        full_message = message

        # 캐릭터 채팅이 아닐 때만 RAG 컨텍스트를 메시지에 추가
        # (캐릭터 채팅은 character_system_prompt에 이미 포함되어 있음)
        if not character_system_prompt and file_search_context and file_search_context.get("searched_context"):
            rag_context = file_search_context["searched_context"]
            full_message = f"""<참고 문서 내용>
{rag_context}
</참고 문서 내용>

사용자 질문: {message}

**중요 지침:**
- 위 문서 내용은 참고용입니다. 사용자의 질문이 문서 내용과 관련이 있을 때만 활용하세요.
- 질문이 일반적인 내용(인사, 날씨, 일상 대화 등)이라면 문서 내용을 무시하고 자연스럽게 답변하세요.
- 사용자가 명시적으로 "문서에서", "파일에서", "업로드한 자료에서" 등의 표현을 사용하거나, 문서 내용과 명확히 관련된 질문일 때만 문서를 참조하세요.
- 문서를 참조할 때는 출처를 명시해주세요."""

        if context:
            full_message += self.format_context(context)
        if history:
            full_message = self.format_history(history) + full_message

        if ai_name == "Gemini":
            async for chunk in self._get_gemini_response_stream(full_message, file_search_context, character_system_prompt):
                yield chunk
        else:
            yield f"Gemini만 지원됩니다. 요청된 AI: {ai_name}"

    # ==================== Gemini ====================

    async def _get_gemini_response(self, message: str, file_search_context: Optional[dict] = None, character_system_prompt: Optional[str] = None) -> str:
        """Gemini 응답 (일반) - File Search Store 지원"""
        if not self.gemini_client:
            return "Gemini를 사용할 수 없습니다. API 키를 확인해주세요."

        max_retries = 3
        retry_delay = 2  # 초

        for attempt in range(max_retries):
            try:
                loop = asyncio.get_event_loop()

                # 캐릭터 시스템 프롬프트 사용 (제공되지 않으면 기본값)
                system_instruction = character_system_prompt if character_system_prompt else "당신은 친절하고 도움이 되는 AI 어시스턴트입니다."

                # File Search Store 활용 여부 판단
                if file_search_context and file_search_context.get("store_name"):
                    store_name = file_search_context["store_name"]
                    print(f"🔍 File Search Store 사용: {store_name}")

                    # File Search Tool 설정
                    response = await loop.run_in_executor(
                        None,
                        lambda: self.gemini_client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=message,
                            config=types.GenerateContentConfig(
                                temperature=0.7,
                                max_output_tokens=3000,
                                system_instruction=system_instruction,
                                tools=[
                                    types.Tool(
                                        file_search=types.FileSearch(
                                            file_search_store_names=[store_name]
                                        )
                                    )
                                ]
                            )
                        )
                    )
                else:
                    # File Search 미사용 (일반 모드)
                    response = await loop.run_in_executor(
                        None,
                        lambda: self.gemini_client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=message,
                            config=types.GenerateContentConfig(
                                temperature=0.7,
                                max_output_tokens=3000,
                                system_instruction=system_instruction
                            )
                        )
                    )

                return response.text
            except Exception as e:
                error_msg = str(e)
                # Rate limit, quota, 서버 오류 등에 대해 재시도
                if any(keyword in error_msg.lower() for keyword in ["rate_limit", "quota", "timeout", "503", "502", "500", "429", "resource_exhausted"]):
                    if attempt < max_retries - 1:
                        print(f"⚠️ Gemini API 오류, {retry_delay}초 후 재시도 ({attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # 지수 백오프
                        continue
                return f"Gemini 오류: {error_msg}"

        return "Gemini가 현재 응답할 수 없습니다. 잠시 후 다시 시도해주세요."
    
    async def _get_gemini_response_stream(self, message: str, file_search_context: Optional[dict] = None, character_system_prompt: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Gemini 응답 (스트리밍) - File Search Store 지원"""
        if not self.gemini_client:
            yield "Gemini를 사용할 수 없습니다."
            return

        max_retries = 3
        retry_delay = 2  # 초

        for attempt in range(max_retries):
            try:
                loop = asyncio.get_event_loop()

                # 캐릭터 시스템 프롬프트 사용 (제공되지 않으면 기본값)
                system_instruction = character_system_prompt if character_system_prompt else "당신은 친절하고 도움이 되는 AI 어시스턴트입니다."

                # File Search Store 활용 여부 판단
                if file_search_context and file_search_context.get("store_name"):
                    store_name = file_search_context["store_name"]
                    print(f"🔍 File Search Store 사용 (스트리밍): {store_name}")

                    # File Search Tool 설정
                    stream = await loop.run_in_executor(
                        None,
                        lambda: self.gemini_client.models.generate_content_stream(
                            model="gemini-2.5-flash",
                            contents=message,
                            config=types.GenerateContentConfig(
                                temperature=0.7,
                                max_output_tokens=3000,
                                system_instruction=system_instruction,
                                tools=[
                                    types.Tool(
                                        file_search=types.FileSearch(
                                            file_search_store_names=[store_name]
                                        )
                                    )
                                ]
                            )
                        )
                    )
                else:
                    # File Search 미사용 (일반 모드)
                    stream = await loop.run_in_executor(
                        None,
                        lambda: self.gemini_client.models.generate_content_stream(
                            model="gemini-2.5-flash",
                            contents=message,
                            config=types.GenerateContentConfig(
                                temperature=0.7,
                                max_output_tokens=3000,
                                system_instruction=system_instruction
                            )
                        )
                    )

                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
                        await asyncio.sleep(0.01)
                return  # 성공 시 종료
            except Exception as e:
                error_msg = str(e)
                # Rate limit, quota, 서버 오류 등에 대해 재시도
                if any(keyword in error_msg.lower() for keyword in ["rate_limit", "quota", "timeout", "503", "502", "500", "429", "resource_exhausted"]):
                    if attempt < max_retries - 1:
                        print(f"⚠️ Gemini API 오류, {retry_delay}초 후 재시도 ({attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # 지수 백오프
                        continue
                yield f"Gemini 오류: {error_msg}"
                return

        yield "Gemini가 현재 응답할 수 없습니다. 잠시 후 다시 시도해주세요."

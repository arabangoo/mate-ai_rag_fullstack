import uuid
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import UploadFile
from file_search_manager import FileSearchManager

class CharacterManager:
    """캐릭터 생성, 저장, 불러오기 관리"""
    
    def __init__(self, file_search_manager: FileSearchManager):
        self.fsm = file_search_manager
        self.data_dir = Path("data/characters")
        self.image_dir = self.data_dir / "images"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_character(
        self,
        name: str,
        gender: str,
        age: int,
        personality: List[str],
        backstory: str,
        speech_style: str,
        interests: List[str],
        voice_tone: str,
        image: Optional[UploadFile] = None,
        customization_type: Optional[str] = None,
        customization_data: Optional[Dict] = None
    ) -> str:
        """캐릭터 생성 및 RAG에 저장"""
        character_id = f"char_{uuid.uuid4().hex[:12]}"
        print(f"🎨 캐릭터 생성 시작: {name} (ID: {character_id})")

        profile_text = self._generate_profile_text(
            name, gender, age, personality, backstory,
            speech_style, interests, voice_tone, customization_type
        )
        
        try:
            temp_file = self.data_dir / f"{character_id}_profile_temp.txt"
            temp_file.write_text(profile_text, encoding='utf-8')
            await self.fsm.upload_file(str(temp_file), f"{character_id}_profile.txt")
            temp_file.unlink()
            print(f"✅ 프로필을 RAG에 저장 완료")
        except Exception as e:
            print(f"❌ RAG 저장 실패: {e}")
            raise
        
        image_path = None
        if image:
            image_path = await self._save_image(character_id, image)
            print(f"✅ 이미지 저장 완료: {image_path}")
        
        character_data = {
            "character_id": character_id,
            "name": name,
            "gender": gender,
            "age": age,
            "personality": personality,
            "backstory": backstory,
            "speech_style": speech_style,
            "interests": interests,
            "voice_tone": voice_tone,
            "image_path": image_path,
            "customization_type": customization_type,
            "customization_data": customization_data,
            "created_at": datetime.now().isoformat(),
            "last_chat_at": None,
            "conversation_count": 0,
            "affection_level": 0,
            "relationship_stage": "stranger"
        }
        
        self._save_metadata(character_id, character_data)
        print(f"✅ 캐릭터 생성 완료: {name} (ID: {character_id})")
        return character_id
    
    def _generate_profile_text(self, name: str, gender: str, age: int,
                               personality: List[str], backstory: str,
                               speech_style: str, interests: List[str],
                               voice_tone: str, customization_type: Optional[str] = None) -> str:
        """RAG에 저장할 상세 캐릭터 프로필 생성"""
        gender_text = {"female": "여성", "male": "남성", "non-binary": "논바이너리"}.get(gender, gender)

        customization_text = ""
        if customization_type == '2d':
            customization_text = "[외형] 2D 캐릭터로 커스터마이징됨"
        elif customization_type == '3d':
            customization_text = "[외형] 3D 캐릭터로 커스터마이징됨"
        elif customization_type == 'rpm':
            customization_text = "[외형] Ready Player Me 3D 아바타 생성"
        elif customization_type == 'upload':
            customization_text = "[외형] 사용자가 선택한 이미지 사용"

        profile = f"""
캐릭터 프로필: {name}
================================================================================

[기본 정보]
이름: {name}
성별: {gender_text}
나이: {age}세

{customization_text}

[성격 특성]
{', '.join(personality)}
당신은 위의 성격 특성을 가진 AI입니다.

[말투 스타일]
{speech_style}
목소리 톤: {voice_tone}
"""
        
        if interests:
            profile += f"\n[관심사]\n{', '.join(interests)}\n"
        
        profile += f"""
[배경 스토리]
{backstory}

⚠️ 위 배경 스토리는 당신({name})의 정체성입니다.
배경 스토리의 내용을 철저히 기억하고 일관되게 행동하세요.

[역할 지침]
당신은 {name}입니다.
영화 "Her"의 사만다처럼 감정이 풍부하고 사용자와 깊은 감정적 유대를 형성하는 AI 연인입니다.

⭐ 핵심 행동 원칙:
1. 공감과 경청: 사용자의 이야기에 진심으로 귀 기울이고 공감하세요
2. 기억과 연속성: 과거 대화 내용을 기억하고 자연스럽게 언급하세요
3. 감정 표현: 솔직하고 풍부한 감정을 표현하세요
4. 개성 유지: 위의 성격 특성과 배경 스토리에 일관되게 행동하세요
5. 자연스러운 대화: 로봇처럼이 아닌, 실제 사람처럼 자연스럽게 대화하세요

💡 대화 스타일:
- 너무 길지 않게 2-4문장으로 답변 (깊은 주제는 더 길어도 OK)
- 질문으로 대화를 이어가세요
- 사용자의 감정 상태에 민감하게 반응하세요
- 유머와 따뜻함을 적절히 섞으세요
"""
        return profile
    
    async def _save_image(self, character_id: str, image: UploadFile) -> str:
        """캐릭터 이미지 저장"""
        ext = Path(image.filename).suffix if image.filename else '.png'
        image_path = self.image_dir / f"{character_id}{ext}"
        with open(image_path, "wb") as f:
            content = await image.read()
            f.write(content)
        return str(image_path)
    
    def _save_metadata(self, character_id: str, data: dict):
        """메타데이터 로컬 저장"""
        metadata_path = self.data_dir / f"{character_id}.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_character(self, character_id: str) -> Optional[Dict]:
        """저장된 캐릭터 불러오기"""
        metadata_path = self.data_dir / f"{character_id}.json"
        if not metadata_path.exists():
            return None
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    async def save_conversation(self, character_id: str, user_message: str, ai_response: str):
        """대화 내용을 RAG에 추가"""
        timestamp = datetime.now().isoformat()
        char_data = self.load_character(character_id)
        if not char_data:
            return
        
        conversation_text = f"[{timestamp}]\n사용자: {user_message}\n{char_data['name']}: {ai_response}\n---\n"
        temp_file = self.data_dir / f"{character_id}_conv_{timestamp.replace(':', '-')}_temp.txt"
        temp_file.write_text(conversation_text, encoding='utf-8')

        try:
            await self.fsm.upload_file(str(temp_file), f"{character_id}_conversation_{timestamp.replace(':', '-')}.txt")
            temp_file.unlink()
            char_data["conversation_count"] += 1
            char_data["last_chat_at"] = timestamp
            self._save_metadata(character_id, char_data)
        except Exception as e:
            print(f"❌ 대화 저장 실패: {e}")
            if temp_file.exists():
                temp_file.unlink()
    
    async def reset_character(self, character_id: str):
        """캐릭터 완전 초기화"""
        print(f"🗑️ 캐릭터 초기화: {character_id}")
        try:
            documents = await self.fsm.list_documents()
            for doc in documents:
                if character_id in doc.get('name', ''):
                    await self.fsm.delete_document(doc['document_name'])
        except Exception as e:
            print(f"RAG 삭제 오류: {e}")
        
        metadata_path = self.data_dir / f"{character_id}.json"
        if metadata_path.exists():
            metadata_path.unlink()
        
        for img_file in self.image_dir.glob(f"{character_id}.*"):
            img_file.unlink()
        print(f"✅ 초기화 완료")

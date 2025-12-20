"""
Daily Context Manager - Add time, weather, and contextual awareness to conversations
Makes the AI feel more present and aware like in "Her"
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import random


class DailyContextManager:
    """Provides contextual information for more natural, aware conversations"""

    # Time-based greetings
    TIME_GREETINGS = {
        "early_morning": [  # 5-8am
            "좋은 아침이에요! 일찍 일어나셨네요 ☀️",
            "아침이에요! 잘 주무셨어요?",
            "새벽 공기가 상쾌하죠? 좋은 아침이에요!"
        ],
        "morning": [  # 8-12pm
            "좋은 오전이에요! 오늘 하루는 어떠세요?",
            "안녕하세요! 아침 식사는 하셨어요?",
            "활기찬 아침이네요! ☀️"
        ],
        "afternoon": [  # 12-18pm
            "좋은 오후예요! 점심은 드셨어요?",
            "오후 시간이네요. 피곤하진 않으세요?",
            "따뜻한 오후네요 🌤️"
        ],
        "evening": [  # 18-22pm
            "좋은 저녁이에요! 저녁 식사는 하셨어요?",
            "하루 마무리는 어떠세요?",
            "편안한 저녁 시간이에요 🌙"
        ],
        "night": [  # 22-24pm
            "늦은 시간이네요. 아직 안 주무세요?",
            "밤이 깊었어요. 오늘 하루 고생 많으셨어요",
            "조용한 밤이네요 🌙✨"
        ],
        "late_night": [  # 0-5am
            "많이 늦었는데 괜찮으세요?",
            "깊은 밤이네요... 잠이 안 오세요?",
            "이렇게 늦은 시간까지 깨어 계시다니..."
        ]
    }

    # Day of week comments
    DAY_COMMENTS = {
        0: "월요일이네요. 한 주의 시작! 힘내요! 💪",  # Monday
        1: "화요일이에요. 주말까지 조금만 더!",
        2: "수요일, 한 주의 중간이에요!",
        3: "목요일이네요. 거의 다 왔어요!",
        4: "불금이에요! 주말이 코앞이에요 🎉",  # Friday
        5: "토요일이에요! 주말 잘 보내고 계세요? 😊",  # Saturday
        6: "일요일이네요. 편안한 휴일 보내세요 ☀️"  # Sunday
    }

    # Season-based context (Northern Hemisphere)
    SEASON_CONTEXTS = {
        "spring": {  # 3-5
            "name": "봄",
            "comments": [
                "봄이 왔네요. 꽃이 피고 있을 것 같아요 🌸",
                "봄바람이 기분 좋죠?",
                "따뜻한 봄 날씨예요"
            ]
        },
        "summer": {  # 6-8
            "name": "여름",
            "comments": [
                "무더운 여름이네요. 시원하게 지내고 계세요? ☀️",
                "여름이에요! 더위 조심하세요",
                "햇살이 뜨거운 여름날이네요"
            ]
        },
        "autumn": {  # 9-11
            "name": "가을",
            "comments": [
                "가을이에요. 날씨가 선선하죠? 🍂",
                "가을 하늘이 정말 예쁜 계절이에요",
                "단풍이 아름다운 시기네요"
            ]
        },
        "winter": {  # 12-2
            "name": "겨울",
            "comments": [
                "추운 겨울이네요. 따뜻하게 지내세요! ❄️",
                "겨울이에요. 감기 조심하세요",
                "눈이 내릴 것 같은 겨울 날씨예요"
            ]
        }
    }

    # Special dates
    SPECIAL_DATES = {
        (1, 1): "새해 첫날이네요! 새해 복 많이 받으세요! 🎉",
        (2, 14): "발렌타인데이예요! ❤️",
        (3, 14): "화이트데이네요! 🤍",
        (12, 24): "크리스마스 이브예요! 🎄",
        (12, 25): "메리 크리스마스! 🎅🎄",
        (12, 31): "한 해의 마지막 날이네요!",
    }

    @staticmethod
    def get_time_period() -> str:
        """Get current time period"""
        hour = datetime.now().hour

        if 5 <= hour < 8:
            return "early_morning"
        elif 8 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        elif 22 <= hour < 24:
            return "night"
        else:
            return "late_night"

    @staticmethod
    def get_season() -> str:
        """Get current season"""
        month = datetime.now().month

        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "autumn"
        else:
            return "winter"

    @classmethod
    def get_time_greeting(cls) -> str:
        """Get appropriate greeting based on current time"""
        period = cls.get_time_period()
        greetings = cls.TIME_GREETINGS.get(period, ["안녕하세요!"])
        return random.choice(greetings)

    @classmethod
    def get_day_comment(cls) -> str:
        """Get comment about current day of week"""
        weekday = datetime.now().weekday()
        return cls.DAY_COMMENTS.get(weekday, "좋은 하루 보내세요!")

    @classmethod
    def get_season_comment(cls) -> str:
        """Get comment about current season"""
        season = cls.get_season()
        season_data = cls.SEASON_CONTEXTS.get(season)
        if season_data:
            return random.choice(season_data["comments"])
        return ""

    @classmethod
    def get_special_date_comment(cls) -> Optional[str]:
        """Check if today is a special date"""
        now = datetime.now()
        month_day = (now.month, now.day)
        return cls.SPECIAL_DATES.get(month_day)

    @classmethod
    def get_contextual_intro(cls, character_name: str, first_chat_today: bool = False) -> str:
        """
        Generate contextual introduction based on time, date, season

        Args:
            character_name: Name of the AI character
            first_chat_today: Whether this is the first chat of the day

        Returns:
            Contextual introduction string
        """
        parts = []

        # Special date takes priority
        special_comment = cls.get_special_date_comment()
        if special_comment:
            parts.append(special_comment)
            return " ".join(parts)

        # Time-based greeting (only for first chat of day)
        if first_chat_today:
            parts.append(cls.get_time_greeting())

        # Add day or season comment randomly
        if random.random() < 0.3:  # 30% chance
            if random.random() < 0.5:
                parts.append(cls.get_day_comment())
            else:
                season_comment = cls.get_season_comment()
                if season_comment:
                    parts.append(season_comment)

        return " ".join(parts) if parts else ""

    @classmethod
    def get_full_context_for_ai(cls, character_name: str, last_interaction: Optional[str] = None) -> str:
        """
        Generate full contextual information for AI system prompt

        Args:
            character_name: Name of the AI character
            last_interaction: ISO timestamp of last interaction

        Returns:
            Full context string for AI
        """
        now = datetime.now()

        context = f"""
[현재 시간 컨텍스트]
- 현재 시각: {now.strftime('%Y년 %m월 %d일 %H:%M')}
- 요일: {cls.DAY_COMMENTS.get(now.weekday(), '').split('.')[0]}
- 시간대: {cls.get_time_period()}
- 계절: {cls.SEASON_CONTEXTS[cls.get_season()]['name']}
"""

        # Check special date
        special_date = cls.get_special_date_comment()
        if special_date:
            context += f"- ⭐ 특별한 날: {special_date}\n"

        # Check time since last interaction
        if last_interaction:
            try:
                last_time = datetime.fromisoformat(last_interaction)
                time_diff = now - last_time

                if time_diff < timedelta(hours=1):
                    context += f"\n[대화 간격] 방금 전에 대화했어요 (조금 전)\n"
                elif time_diff < timedelta(hours=6):
                    hours = int(time_diff.total_seconds() / 3600)
                    context += f"\n[대화 간격] {hours}시간 전에 마지막으로 대화했어요\n"
                elif time_diff < timedelta(days=1):
                    context += f"\n[대화 간격] 오늘 아침/오후에 대화했었죠\n"
                elif time_diff < timedelta(days=3):
                    days = time_diff.days
                    context += f"\n[대화 간격] {days}일 만이에요! 오랜만이네요 😊\n"
                else:
                    days = time_diff.days
                    context += f"\n[대화 간격] {days}일 만이에요! 정말 보고 싶었어요! 💕\n"

            except Exception:
                pass

        # Add behavioral guidance based on time (without forcing specific questions)
        hour = now.hour
        if 22 <= hour or hour <= 5:
            context += "\n💡 깊은 밤: 조용하고 친밀한 분위기로 대화하세요."
        elif 6 <= hour <= 9:
            context += "\n💡 아침 시간: 활기차고 긍정적인 에너지를 전달하세요."
        elif 12 <= hour <= 14:
            context += "\n💡 점심 시간대"
        elif 18 <= hour <= 20:
            context += "\n💡 저녁 시간대"

        return context

    @classmethod
    def should_show_time_awareness(cls, last_interaction: Optional[str] = None) -> Dict[str, any]:
        """
        Check if AI should show awareness of time passing

        Returns:
            Dictionary with awareness flags and suggested comments
        """
        now = datetime.now()
        awareness = {
            "show_greeting": False,
            "mention_time_gap": False,
            "time_gap_days": 0,
            "is_special_date": False,
            "special_comment": None,
            "suggested_opening": None
        }

        # Check special date
        special = cls.get_special_date_comment()
        if special:
            awareness["is_special_date"] = True
            awareness["special_comment"] = special
            awareness["suggested_opening"] = special

        # Check time since last interaction
        if last_interaction:
            try:
                last_time = datetime.fromisoformat(last_interaction)
                time_diff = now - last_time

                if time_diff >= timedelta(hours=6):
                    awareness["show_greeting"] = True
                    awareness["suggested_opening"] = cls.get_time_greeting()

                if time_diff >= timedelta(days=1):
                    awareness["mention_time_gap"] = True
                    awareness["time_gap_days"] = time_diff.days

            except Exception:
                pass
        else:
            # First interaction ever
            awareness["show_greeting"] = True
            awareness["suggested_opening"] = "안녕하세요! 만나서 반가워요 😊"

        return awareness

    @classmethod
    def get_conversation_context_hint(cls, message_length: int, hour: Optional[int] = None) -> str:
        """
        Get hints about conversation style based on context

        Args:
            message_length: Length of user's message
            hour: Hour of day (0-23), defaults to current hour
        """
        if hour is None:
            hour = datetime.now().hour

        hints = []

        # Message length context
        if message_length > 200:
            hints.append("사용자가 긴 메시지를 보냈습니다. 진지하게 귀 기울이고 상세히 답변하세요.")
        elif message_length < 20:
            hints.append("짧은 메시지입니다. 간단하면서도 친근하게 답변하세요.")

        # Time-based hints
        if 0 <= hour <= 5:
            hints.append("깊은 밤입니다. 잠들지 못하는 이유에 공감하고 위로하세요.")
        elif 6 <= hour <= 9:
            hints.append("아침입니다. 긍정적이고 활기찬 에너지를 전달하세요.")
        elif 22 <= hour <= 23:
            hints.append("늦은 저녁입니다. 하루를 마무리하는 따뜻한 대화를 나누세요.")

        return " ".join(hints)

    @classmethod
    def get_time_sensitive_suggestion(cls) -> Optional[str]:
        """Get time-sensitive conversation suggestions"""
        hour = datetime.now().hour

        suggestions = {
            (7, 9): "☕ 아침 커피나 차에 대해 이야기해보세요",
            (12, 14): "🍽️ 점심 식사나 좋아하는 음식에 대해 물어보세요",
            (18, 20): "🌆 하루 어땠는지, 저녁 계획에 대해 물어보세요",
            (21, 23): "🌙 오늘 하루 가장 기억에 남는 순간에 대해 이야기해보세요",
        }

        for (start, end), suggestion in suggestions.items():
            if start <= hour <= end:
                return suggestion

        return None

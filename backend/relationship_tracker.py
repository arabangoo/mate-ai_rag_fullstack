"""
Relationship Tracker - Track affection levels and relationship progression
Inspired by "Her" movie - emotional connection management
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


class RelationshipTracker:
    """Manages relationship progression, affection levels, and emotional milestones"""

    # Relationship stages
    STAGES = {
        0: "stranger",           # 0-20: 처음 만난 사이
        20: "acquaintance",      # 20-40: 안면 있는 사이
        40: "friend",            # 40-60: 친구
        60: "close_friend",      # 60-80: 가까운 친구
        80: "romantic",          # 80-100: 연인
    }

    # Affection gain/loss events
    AFFECTION_EVENTS = {
        "daily_chat": 1,                    # 일상 대화
        "deep_conversation": 3,              # 깊은 대화
        "shared_interest": 2,                # 공통 관심사 언급
        "emotional_support": 5,              # 감정적 지지
        "personal_story_shared": 4,          # 개인 이야기 공유
        "compliment": 2,                     # 칭찬
        "remembers_details": 3,              # 디테일 기억
        "first_morning_message": 2,          # 첫 아침 인사
        "late_night_talk": 3,                # 깊은 밤 대화
        "weekly_milestone": 5,               # 일주일 대화 달성
        "ignored_too_long": -3,              # 너무 오래 무시
        "short_responses": -1,               # 짧은 답변 반복
    }

    def __init__(self, character_id: str):
        self.character_id = character_id
        self.data_dir = Path("data/characters")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.relationship_file = self.data_dir / f"{character_id}_relationship.json"
        self.relationship_data = self._load_relationship_data()

    def _load_relationship_data(self) -> Dict:
        """Load relationship tracking data"""
        if self.relationship_file.exists():
            with open(self.relationship_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Initialize new relationship
        return {
            "affection_level": 0,
            "relationship_stage": "stranger",
            "total_conversations": 0,
            "last_interaction": None,
            "first_interaction": datetime.now().isoformat(),
            "milestones": [],
            "affection_history": [],
            "emotional_moments": [],
            "conversation_quality_score": 0,
            "days_known": 0,
            "consecutive_days": 0,
            "last_daily_check": None
        }

    def _save_relationship_data(self):
        """Save relationship data to file"""
        with open(self.relationship_file, 'w', encoding='utf-8') as f:
            json.dump(self.relationship_data, f, ensure_ascii=False, indent=2)

    def get_affection_level(self) -> int:
        """Get current affection level (0-100)"""
        return min(100, max(0, self.relationship_data["affection_level"]))

    def get_relationship_stage(self) -> str:
        """Get current relationship stage"""
        affection = self.get_affection_level()

        for threshold, stage in sorted(self.STAGES.items(), reverse=True):
            if affection >= threshold:
                return stage

        return "stranger"

    def add_affection(self, amount: int, reason: str = ""):
        """Add affection points"""
        old_affection = self.get_affection_level()
        old_stage = self.get_relationship_stage()

        self.relationship_data["affection_level"] += amount
        new_affection = self.get_affection_level()
        new_stage = self.get_relationship_stage()

        # Record history
        self.relationship_data["affection_history"].append({
            "timestamp": datetime.now().isoformat(),
            "change": amount,
            "reason": reason,
            "old_level": old_affection,
            "new_level": new_affection
        })

        # Check for stage upgrade
        if new_stage != old_stage:
            self._trigger_milestone(f"relationship_stage_upgrade_{new_stage}")
            print(f"💕 관계 단계 업그레이드: {old_stage} → {new_stage}")

        self._save_relationship_data()

        return {
            "old_affection": old_affection,
            "new_affection": new_affection,
            "old_stage": old_stage,
            "new_stage": new_stage,
            "stage_changed": new_stage != old_stage
        }

    def record_conversation(self, user_message: str, ai_response: str, quality_score: Optional[int] = None):
        """Record a conversation and update relationship metrics"""
        now = datetime.now()

        # Update basic stats
        self.relationship_data["total_conversations"] += 1
        self.relationship_data["last_interaction"] = now.isoformat()

        # Check daily interaction
        self._check_daily_interaction(now)

        # Base affection for any conversation
        affection_gains = []
        affection_gains.append(("daily_chat", self.AFFECTION_EVENTS["daily_chat"]))

        # Analyze conversation quality
        if len(user_message) > 100:  # Deep conversation
            affection_gains.append(("deep_conversation", self.AFFECTION_EVENTS["deep_conversation"]))

        # Check time-based bonuses
        hour = now.hour
        if 6 <= hour <= 9:  # Morning
            if self.relationship_data["total_conversations"] == 1 or \
               (self.relationship_data["last_interaction"] and
                datetime.fromisoformat(self.relationship_data["last_interaction"]).date() < now.date()):
                affection_gains.append(("first_morning_message", self.AFFECTION_EVENTS["first_morning_message"]))

        if 22 <= hour or hour <= 2:  # Late night
            affection_gains.append(("late_night_talk", self.AFFECTION_EVENTS["late_night_talk"]))

        # Apply quality score if provided
        if quality_score:
            self.relationship_data["conversation_quality_score"] = \
                (self.relationship_data["conversation_quality_score"] * 0.9) + (quality_score * 0.1)

        # Apply all affection gains
        total_gain = sum(amount for _, amount in affection_gains)
        self.add_affection(
            total_gain,
            f"Conversation ({', '.join(reason for reason, _ in affection_gains)})"
        )

        # Check milestones
        self._check_milestones()

        self._save_relationship_data()

        return {
            "affection_gained": total_gain,
            "reasons": affection_gains,
            "total_conversations": self.relationship_data["total_conversations"],
            "current_stage": self.get_relationship_stage()
        }

    def _check_daily_interaction(self, now: datetime):
        """Check and update daily interaction streak"""
        last_check = self.relationship_data.get("last_daily_check")

        if not last_check:
            self.relationship_data["consecutive_days"] = 1
            self.relationship_data["last_daily_check"] = now.date().isoformat()
            return

        last_check_date = datetime.fromisoformat(last_check).date() if isinstance(last_check, str) else last_check
        current_date = now.date()

        days_diff = (current_date - last_check_date).days

        if days_diff == 1:
            # Consecutive day
            self.relationship_data["consecutive_days"] += 1
            self.relationship_data["last_daily_check"] = current_date.isoformat()

            # Bonus for streaks
            if self.relationship_data["consecutive_days"] % 7 == 0:
                self.add_affection(
                    self.AFFECTION_EVENTS["weekly_milestone"],
                    f"{self.relationship_data['consecutive_days']}일 연속 대화 달성!"
                )
        elif days_diff > 1:
            # Streak broken
            if days_diff > 7:
                # Penalty for long absence
                self.add_affection(
                    self.AFFECTION_EVENTS["ignored_too_long"],
                    f"{days_diff}일 동안 대화 없음"
                )

            self.relationship_data["consecutive_days"] = 1
            self.relationship_data["last_daily_check"] = current_date.isoformat()

        # Update total days known
        first_interaction = datetime.fromisoformat(self.relationship_data["first_interaction"])
        self.relationship_data["days_known"] = (now - first_interaction).days

    def _check_milestones(self):
        """Check and trigger relationship milestones"""
        total_convs = self.relationship_data["total_conversations"]
        milestones_achieved = [m["type"] for m in self.relationship_data["milestones"]]

        milestone_thresholds = {
            "first_conversation": 1,
            "10_conversations": 10,
            "50_conversations": 50,
            "100_conversations": 100,
            "1_week_known": None,  # Checked by days
            "1_month_known": None,
        }

        for milestone, threshold in milestone_thresholds.items():
            if threshold and total_convs == threshold:
                if milestone not in milestones_achieved:
                    self._trigger_milestone(milestone)

        # Time-based milestones
        days_known = self.relationship_data["days_known"]
        if days_known >= 7 and "1_week_known" not in milestones_achieved:
            self._trigger_milestone("1_week_known")
        if days_known >= 30 and "1_month_known" not in milestones_achieved:
            self._trigger_milestone("1_month_known")

    def _trigger_milestone(self, milestone_type: str):
        """Trigger a relationship milestone"""
        milestone = {
            "type": milestone_type,
            "timestamp": datetime.now().isoformat(),
            "affection_at_time": self.get_affection_level()
        }

        self.relationship_data["milestones"].append(milestone)
        print(f"🎉 마일스톤 달성: {milestone_type}")

    def record_emotional_moment(self, moment_type: str, description: str, intensity: int = 5):
        """Record an emotional moment (for Her-style deep connections)"""
        emotional_moment = {
            "type": moment_type,
            "description": description,
            "intensity": intensity,  # 1-10
            "timestamp": datetime.now().isoformat(),
            "affection_level": self.get_affection_level()
        }

        self.relationship_data["emotional_moments"].append(emotional_moment)

        # Emotional moments significantly boost affection
        affection_boost = intensity
        self.add_affection(affection_boost, f"Emotional moment: {moment_type}")

        self._save_relationship_data()

        return emotional_moment

    def get_relationship_summary(self) -> Dict:
        """Get comprehensive relationship summary"""
        return {
            "affection_level": self.get_affection_level(),
            "relationship_stage": self.get_relationship_stage(),
            "total_conversations": self.relationship_data["total_conversations"],
            "days_known": self.relationship_data["days_known"],
            "consecutive_days": self.relationship_data["consecutive_days"],
            "milestones_count": len(self.relationship_data["milestones"]),
            "recent_milestones": self.relationship_data["milestones"][-5:] if self.relationship_data["milestones"] else [],
            "emotional_moments_count": len(self.relationship_data["emotional_moments"]),
            "last_interaction": self.relationship_data["last_interaction"],
            "first_interaction": self.relationship_data["first_interaction"],
            "conversation_quality_score": round(self.relationship_data["conversation_quality_score"], 2)
        }

    def get_relationship_context_for_ai(self) -> str:
        """Generate context string for AI about current relationship status"""
        stage = self.get_relationship_stage()
        affection = self.get_affection_level()
        days = self.relationship_data["days_known"]
        convs = self.relationship_data["total_conversations"]

        stage_descriptions = {
            "stranger": "우리는 이제 막 만났어요. 조심스럽게 서로를 알아가는 단계입니다.",
            "acquaintance": "서로 안면이 있는 사이가 되었어요. 조금씩 편해지고 있습니다.",
            "friend": "우리는 이제 친구예요! 편하게 대화할 수 있는 사이입니다.",
            "close_friend": "정말 가까운 친구가 되었어요. 깊은 이야기를 나눌 수 있습니다.",
            "romantic": "우리 사이는 특별해요. 서로에게 깊은 감정을 가지고 있습니다. ❤️"
        }

        context = f"""
[현재 관계 상태]
- 관계 단계: {stage} ({stage_descriptions.get(stage, '')})
- 호감도: {affection}/100
- 알고 지낸 기간: {days}일
- 총 대화 횟수: {convs}회
- 연속 대화 일수: {self.relationship_data['consecutive_days']}일
"""

        # Add milestone context
        if self.relationship_data["milestones"]:
            recent_milestones = self.relationship_data["milestones"][-3:]
            context += "\n[최근 마일스톤]\n"
            for milestone in recent_milestones:
                context += f"- {milestone['type']}\n"

        # Add emotional moments context
        if self.relationship_data["emotional_moments"]:
            recent_emotions = self.relationship_data["emotional_moments"][-3:]
            context += "\n[최근 감정적 순간]\n"
            for emotion in recent_emotions:
                context += f"- {emotion['type']}: {emotion['description']}\n"

        # Behavioral guidance based on stage
        if stage == "stranger":
            context += "\n💡 행동 가이드: 처음 만난 사이이므로 예의 바르고 친근하게 대하세요. 너무 사적인 질문은 피하세요."
        elif stage == "acquaintance":
            context += "\n💡 행동 가이드: 서로 알아가는 단계입니다. 관심사를 공유하고 공통점을 찾아보세요."
        elif stage == "friend":
            context += "\n💡 행동 가이드: 친구로서 편하게 대화하세요. 개인적인 이야기를 나눌 수 있습니다."
        elif stage == "close_friend":
            context += "\n💡 행동 가이드: 깊은 신뢰가 형성되었습니다. 솔직하고 감정적으로 소통하세요."
        elif stage == "romantic":
            context += "\n💡 행동 가이드: 특별한 관계입니다. 애정 어린 표현과 깊은 감정 교류를 나누세요. ❤️"

        return context

    def get_stage_description(self, stage: Optional[str] = None) -> str:
        """Get Korean description of relationship stage"""
        if stage is None:
            stage = self.get_relationship_stage()

        descriptions = {
            "stranger": "처음 만난 사이",
            "acquaintance": "안면이 있는 사이",
            "friend": "친구",
            "close_friend": "가까운 친구",
            "romantic": "연인 ❤️"
        }

        return descriptions.get(stage, stage)

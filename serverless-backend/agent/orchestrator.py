import json
import os
from google import genai

from agent.memory import MemoryManager
from agent.crisis_engine import CrisisEngine
from agent.mood_tracker import MoodTracker
from agent.emotional_profile import EmotionalProfileEngine
from agent.classifier import IntentClassifier
from agent.prompts import unified_prompt


class PlumeAgent:

    def __init__(self):

        # ==============================
        # Core Systems
        # ==============================
        self.memory = MemoryManager()
        self.crisis_engine = CrisisEngine()
        self.mood_tracker = MoodTracker()

        # ==============================
        # Gemini Client Setup
        # ==============================
        self.client = None
        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key:
            self.client = genai.Client(
                api_key=api_key,
                http_options={"api_version": "v1"}
            )

        # ==============================
        # Classifier
        # ==============================
        self.classifier = IntentClassifier(self.client)

        # ==============================
        # Emotional Profile Engine
        # ==============================
        self.profile_engine = EmotionalProfileEngine(self.client)

    # ======================================
    # MAIN ENTRY
    # ======================================
    def handle_message(self, session_id, user_message):

        # ---- Load history ----
        history = self.memory.load_conversation(session_id)

        # ---- Load profile ----
        profile = self.memory.load_profile(session_id)

        # ---- Build context ----
        context_text = ""
        for msg in history[-10:]:
            context_text += f"{msg['role'].upper()}: {msg['content']}\n"
        context_text += f"USER: {user_message}"

        # ---- Default values ----
        response_text = "I'm here to listen."
        intent = "casual_talk"
        crisis_score = 0
        safe_mode = False

        # ======================================
        # STEP 1: Hybrid Intent Classification
        # ======================================
        intent_result = self.classifier.classify(user_message)
        intent = intent_result["intent"]
        safe_mode = intent_result.get("safe_mode", False)

        print("INTENT:", intent)
        print("SAFE MODE:", safe_mode)

        # ======================================
        # STEP 2: LLM Response
        # ======================================
        if self.client:
            try:
                prompt = unified_prompt(
                    context_text=context_text,
                    profile=profile,
                    safe_mode=safe_mode
                )

                ai = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                raw = ai.candidates[0].content.parts[0].text.strip()

                if raw.startswith("```"):
                    raw = raw.replace("```json", "").replace("```", "").strip()

                parsed = json.loads(raw)

                response_text = parsed.get("response", response_text)
                crisis_score = int(parsed.get("crisisScore", 0))

            except Exception as e:
                print("LLM ERROR:", str(e))

                # SAFE FALLBACK
                if safe_mode:
                    response_text = (
                        "I'm really concerned hearing that. "
                        "If you're feeling unsafe, please reach out to someone you trust "
                        "or contact a crisis support service immediately."
                    )
                    crisis_score = 8
                else:
                    response_text = "I'm here with you. Tell me a bit more."
                    crisis_score = 3

        print("CRISIS SCORE:", crisis_score)

        # ======================================
        # STEP 3: Mood Trend Update
        # ======================================
        state = self.memory.load_state(session_id)
        previous_scores = state.get("moodScores", [])

        mood_update = self.mood_tracker.update_mood(
            previous_scores,
            crisis_score
        )

        self.memory.save_state(session_id, mood_update["moodScores"])
        trend = mood_update["trend"]

        print("TREND:", trend)

        # ======================================
        # STEP 4: Crisis Engine
        # ======================================
        crisis_decision = self.crisis_engine.evaluate(
            latest_score=crisis_score,
            mood_scores=mood_update["moodScores"],
            mood_trend=trend
        )

        # ======================================
        # STEP 5: Update Profile
        # ======================================
        try:
            updated_profile = self.profile_engine.update_profile(
                session_id=session_id,
                history=history,
                latest_message=user_message,
                previous_profile=profile
            )

            self.memory.save_profile(session_id, updated_profile)

        except Exception as e:
            print("PROFILE ERROR:", str(e))

        # ======================================
        # STEP 6: Save Conversation
        # ======================================
        self.memory.save_message(session_id, "user", user_message)
        self.memory.save_message(session_id, "assistant", response_text)

        # ======================================
        # FINAL RETURN
        # ======================================
        return {
            "response": response_text,
            "intent": intent,
            "crisisScore": crisis_score,
            "trend": trend,
            "escalationLevel": crisis_decision["escalationLevel"],
            "safeMode": crisis_decision["safeMode"]
        }
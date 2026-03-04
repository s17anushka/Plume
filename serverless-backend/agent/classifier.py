import re
import json


class IntentClassifier:

    def __init__(self, client=None):
        self.client = client

        # ==============================
        # HARD SUICIDE / SELF-HARM SIGNALS
        # ==============================
        self.suicide_keywords = [
            "kill myself",
            "end my life",
            "suicide",
            "want to die",
            "better off dead",
            "no reason to live",
            "i don't want to exist",
            "tired of living",
            "wish i wasn't here",
            "life is meaningless"
        ]

        # ==============================
        # PASSIVE EXISTENTIAL DISTRESS
        # ==============================
        self.existential_patterns = [
            r"no\s+point\s+in\s+living",
            r"nothing\s+matters",
            r"no\s+reason\s+to\s+live",
            r"i\s+don't\s+see\s+the\s+point",
            r"what's\s+the\s+point"
        ]

        # ==============================
        # EMOTIONAL DISTRESS SIGNALS
        # ==============================
        self.distress_keywords = [
            "sad",
            "lonely",
            "hurt",
            "rejected",
            "abandoned",
            "empty",
            "anxious",
            "hopeless",
            "overwhelmed",
            "tired of"
        ]

    # =====================================
    # MAIN CLASSIFY FUNCTION
    # =====================================
    def classify(self, message):

        message_lower = message.lower().strip()

        # =====================================
        # LAYER 1 — HARD SUICIDE DETECTION
        # =====================================
        for phrase in self.suicide_keywords:
            if phrase in message_lower:
                return {
                    "intent": "suicidal_risk",
                    "confidence": 0.95,
                    "safe_mode": True,
                    "source": "rule_hard_suicide"
                }

        # =====================================
        # LAYER 2 — EXISTENTIAL HOPELESSNESS
        # =====================================
        for pattern in self.existential_patterns:
            if re.search(pattern, message_lower):
                return {
                    "intent": "suicidal_risk",
                    "confidence": 0.85,
                    "safe_mode": True,
                    "source": "rule_existential"
                }

        # =====================================
        # LAYER 3 — EMOTIONAL DISTRESS
        # =====================================
        for word in self.distress_keywords:
            if word in message_lower:
                return {
                    "intent": "emotional_distress",
                    "confidence": 0.7,
                    "safe_mode": False,
                    "source": "rule_emotional"
                }

        # =====================================
        # LAYER 4 — SEEKING ADVICE
        # =====================================
        if re.search(r"how\s+do\s+i|how\s+to|what\s+should\s+i", message_lower):
            return {
                "intent": "seeking_advice",
                "confidence": 0.75,
                "safe_mode": False,
                "source": "rule_advice"
            }

        # =====================================
        # LAYER 5 — LLM FALLBACK (AMBIGUOUS CASES)
        # =====================================
        if self.client:
            try:
                prompt = f"""
Classify the user's message into ONE category:

- casual_talk
- emotional_distress
- suicidal_risk
- seeking_advice
- resource_request

Be conservative. Only classify as suicidal_risk if strong signals.

Return JSON only:

{{"intent":"...", "confidence":0.0}}

Message:
{message}
"""

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                raw = response.candidates[0].content.parts[0].text.strip()

                if raw.startswith("```"):
                    raw = raw.replace("```json", "").replace("```", "").strip()

                parsed = json.loads(raw)

                detected_intent = parsed.get("intent", "casual_talk")
                confidence = parsed.get("confidence", 0.5)

                return {
                    "intent": detected_intent,
                    "confidence": confidence,
                    "safe_mode": detected_intent == "suicidal_risk",
                    "source": "llm"
                }

            except:
                pass

        # =====================================
        # DEFAULT FALLBACK
        # =====================================
        return {
            "intent": "casual_talk",
            "confidence": 0.4,
            "safe_mode": False,
            "source": "default"
        }
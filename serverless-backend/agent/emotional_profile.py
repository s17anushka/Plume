import json


class EmotionalProfileEngine:

    def __init__(self, client):
        self.client = client

    def update_profile(self, session_id, history, latest_message, previous_profile):

        if not self.client:
            return previous_profile

        context_text = ""
        for msg in history[-10:]:
            context_text += f"{msg['role'].upper()}: {msg['content']}\n"

        context_text += f"USER: {latest_message}"

        prompt = f"""
You are a psychological pattern extraction engine.

Analyze the user's emotional patterns.

Return ONLY valid JSON:

{{
  "abandonment_sensitivity": 0-10,
  "rejection_sensitivity": 0-10,
  "validation_dependence": 0-10,
  "self_worth_instability": 0-10,
  "hopelessness_index": 0-10,
  "social_isolation_index": 0-10,
  "cognitive_distortion_index": 0-10,
  "shadow_conflict_index": 0-10
}}

Conversation:
{context_text}
"""

        try:
            ai = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            raw = ai.candidates[0].content.parts[0].text.strip()

            if raw.startswith("```"):
                raw = raw.replace("```json", "").replace("```", "").strip()

            extracted = json.loads(raw)

            return self._stabilize_profile(previous_profile, extracted)

        except:
            return previous_profile

    def _stabilize_profile(self, old_profile, new_profile):

        if not old_profile:
            return new_profile

        stabilized = {}

        for key in new_profile:
            old_val = old_profile.get(key, 0)
            new_val = new_profile.get(key, 0)

            # 70% old + 30% new
            stabilized[key] = round((0.7 * old_val) + (0.3 * new_val), 2)

        return stabilized
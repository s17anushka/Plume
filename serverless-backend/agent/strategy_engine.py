class StrategyEngine:

    def decide(self, profile, crisis_level, mood_trend, intent):

        intervention = "general_support"
        tone = "balanced"
        intensity = "low"

        # ---------- CRISIS PRIORITY ----------
        if crisis_level >= 3:
            return {
                "intervention": "crisis_stabilization",
                "tone": "grounded",
                "intensity": "high"
            }

        # ---------- HIGH DISTRESS ----------
        if mood_trend in ["high_distress", "critical"]:
            return {
                "intervention": "emotional_stabilization",
                "tone": "grounded",
                "intensity": "moderate"
            }

        # ---------- PROFILE-DRIVEN ----------
        if profile:

            if profile.get("abandonment_sensitivity", 0) >= 7:
                intervention = "attachment_reassurance"

            elif profile.get("self_worth_instability", 0) >= 7:
                intervention = "self_compassion_framework"

            elif profile.get("cognitive_distortion_index", 0) >= 7:
                intervention = "cognitive_reframing"

            elif profile.get("social_isolation_index", 0) >= 7:
                intervention = "connection_activation"

        # ---------- INTENT ADJUSTMENT ----------
        if intent == "seeking_advice":
            intensity = "moderate"

        return {
            "intervention": intervention,
            "tone": tone,
            "intensity": intensity
        }
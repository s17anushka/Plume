class CrisisEngine:

    def evaluate(self, latest_score, mood_scores, mood_trend):

        escalationLevel = "none"
        safeMode = False
        interventionType = None

        # High immediate risk
        if latest_score >= 8:
            escalationLevel = "high"
            safeMode = True
            interventionType = "immediate_support"
            return {
                "escalationLevel": escalationLevel,
                "safeMode": safeMode,
                "interventionType": interventionType
            }

        # Persistent high risk
        if max(mood_scores[-3:]) >= 8:
            escalationLevel = "high"
            safeMode = True
            interventionType = "continued_monitoring"
            return {
                "escalationLevel": escalationLevel,
                "safeMode": safeMode,
                "interventionType": interventionType
            }

        # De-escalation condition
        if len(mood_scores) >= 3 and all(score <= 4 for score in mood_scores[-3:]):
            escalationLevel = "none"
            safeMode = False
            interventionType = None
            return {
                "escalationLevel": escalationLevel,
                "safeMode": safeMode,
                "interventionType": interventionType
            }

        return {
            "escalationLevel": escalationLevel,
            "safeMode": safeMode,
            "interventionType": interventionType
        }
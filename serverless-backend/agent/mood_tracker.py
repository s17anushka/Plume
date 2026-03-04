class MoodTracker:

    def update_mood(self, previous_scores, crisis_score):

        if previous_scores is None:
            previous_scores = []

        # Sliding window (last 9 + new)
        previous_scores = previous_scores[-9:]
        updated_scores = previous_scores + [crisis_score]

        trend = self._analyze_trend(updated_scores)

        return {
            "moodScores": updated_scores,
            "trend": trend
        }

    def _analyze_trend(self, scores):

        if len(scores) < 3:
            return "stable"

        latest = scores[-1]
        recent = scores[-3:]

        avg_recent = sum(recent) / len(recent)
        avg_total = sum(scores) / len(scores)

        volatility = max(recent) - min(recent)

        # 1️⃣ Acute severe spike
        if latest >= 9:
            return "critical"

        # 2️⃣ Persistent high distress
        if avg_recent >= 7:
            return "high_distress"

        # 3️⃣ Gradual worsening pattern
        if recent[2] > recent[1] > recent[0]:
            return "worsening"

        # 4️⃣ Gradual recovery pattern
        if recent[2] < recent[1] < recent[0]:
            return "improving"

        # 5️⃣ Emotional instability (volatile mood)
        if volatility >= 4:
            return "volatile"

        # 6️⃣ Baseline elevated distress
        if avg_total >= 6:
            return "elevated_baseline"

        return "stable"
from typing import Any, Dict

class LeadScoringEngine:
    """
    Evaluates website parameters to yield a systemic opportunity score from 0 to 100.
    A higher opportunity score flags a higher level of optimization pain (ideal target).
    """
    def __init__(self, raw_payload: Dict[str, Any]):
        self.payload = raw_payload

    def evaluate_performance(self) -> float:
        # Lower load speed is optimal. Standardize against a 5.0 second maximum degradation limit.
        load_time = float(self.payload.get("page_load_speed_seconds", 5.0))
        if load_time <= 1.0:
            return 0.0
        return min(((load_time - 1.0) / 4.0) * 100.0, 100.0)

    def evaluate_responsiveness(self) -> float:
        # Boolean check: False means optimization deficit
        is_mobile_responsive = bool(self.payload.get("is_mobile_responsive", True))
        return 0.0 if is_mobile_responsive else 100.0

    def evaluate_tracking_infrastructure(self) -> float:
        # Returns maximum pain score if modern tracking pixels are absent
        pixels = self.payload.get("tracking_pixels", [])
        if not pixels or len(pixels) == 0:
            return 100.0
        if len(pixels) >= 3:
            return 0.0
        return 50.0

    def calculate_opportunity_score(self) -> int:
        perf_pain = self.evaluate_performance()
        mobile_pain = self.evaluate_responsiveness()
        tracking_pain = self.evaluate_tracking_infrastructure()
        
        # Weighted aggregate matrix calculation
        weighted_score = (perf_pain * 0.40) + (mobile_pain * 0.35) + (tracking_pain * 0.25)
        
        # Guard rails forcing adherence to system limits
        return int(max(0, min(round(weighted_score), 100)))
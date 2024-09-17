from TradingMoneyManagementTool.Factors.FactorBase import FactorBase
from TradingMoneyManagementTool.Messages.Message import Message


class FundamentalFactors(FactorBase):
    def __init__(self):
        factors = {
            "Daily news result": "Is there any relevant news affecting the market today (positive/negative/neutral)?",
            "VIX": "Is the VIX indicating high volatility (positive/negative/neutral)?",
            "Geopolitical and sector situation":
                "Is there any relevant geopolitical or sector-specific news (positive/negative/neutral)?"
        }
        valid_responses = ["positive", "negative", "neutral"]
        score_map = {"positive": 1, "negative": -1, "neutral": 0}
        super().__init__(factors, valid_responses, score_map)

    def get_fundamental_values(self, direction):
        direction_multiplier = 1 if direction == "long" else -1
        return self.get_values(direction_multiplier)


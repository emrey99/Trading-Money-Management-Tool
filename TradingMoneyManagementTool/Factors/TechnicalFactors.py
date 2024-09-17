from TradingMoneyManagementTool.Factors.FactorBase import FactorBase
from TradingMoneyManagementTool.Messages.Message import Message


class TechnicalFactors(FactorBase):
    def __init__(self):
        factors = {
            "Volume": "Is there volume? (yes or no)",
            "Overall trend": "Is overall trend in your direction? (yes or no)",
            "Liquidity sweep": "Is there a liquidity sweep? (yes or no)",
            "Reaction from a good zone": "Is there a reaction from a good zone? (yes or no)",
            "Deep correction to OTE level": "Is there a deep correction to OTE level? (yes or no)",
            "Extra setup": "Is there an extra setup? (yes or no)",
            "Good attack point": "Is there a good attack point? (yes or no)"
        }
        valid_responses = ["yes", "no"]
        score_map = {"yes": 1, "no": 0}
        super().__init__(factors, valid_responses, score_map)

    def get_technical_values(self):
        return self.get_values()


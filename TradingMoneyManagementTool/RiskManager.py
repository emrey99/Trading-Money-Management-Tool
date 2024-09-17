from TradingMoneyManagementTool.Messages.Message import Message


class RiskManager:
    def __init__(self):
        self.__low_threshold = 0.25
        self.__medium_threshold = 0.50
        self.__high_threshold = 1.0

    def __categorize_risk(self, score):
        if self.__low_threshold <= score < self.__medium_threshold:
            return 1
        elif self.__low_threshold < score < self.__high_threshold:
            return 2
        elif score >= self.__high_threshold:
            return 3
        else:
            return 0

    @staticmethod
    def get_score(responses):
        score = sum(responses.values())
        return score / len(responses) if responses else 0

    @staticmethod
    def check_final_score(score):
        if score <= 0:
            print(Message.FINAL_SCORE_LOW)
            quit()

    def get_risk_category(self, score):
        return self.__categorize_risk(score)

    def get_overall_score(self, technical_score, fundamental_score):
        return min(technical_score + fundamental_score, self.__high_threshold)

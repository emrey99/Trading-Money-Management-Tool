from TradingMoneyManagementTool.Messages.Message import Message


class FactorBase:
    def __init__(self, factors, valid_responses, score_map=None):
        self.factors = factors
        self.valid_responses = valid_responses
        self.responses = {}
        self.score_map = score_map if score_map is not None else {}

    def get_values(self, direction_multiplier=1):
        self.responses = {
            factor: self.score_map[self.get_user_input(question)] * direction_multiplier
            for factor, question in self.factors.items()
        }
        return self.__transform_responses()

    def get_user_input(self, question):
        while True:
            response = input(f"{question}: ").strip().lower()
            if response in self.valid_responses:
                return response
            print(f"{Message.INVALID_INPUT}")

    def __transform_responses(self):
        return {
            self.__format_key(factor): value
            for factor, value in self.responses.items()
        }

    @staticmethod
    def __format_key(factor):
        return factor.lower().replace(" ", "_")


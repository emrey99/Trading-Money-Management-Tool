from TradingMoneyManagementTool.Combinations.CombinationDB import CombinationDB


class CombinationManager:

    def __init__(self):
        self.db = CombinationDB()

    def get_combination(self, technical_category, fundamental_category):
        return self.db.get_combination(technical_category, fundamental_category)

    def create_combination(self, technical_category, fundamental_category, initial_weight=0):
        self.db.create_combination(technical_category,
                                   fundamental_category,
                                   initial_weight)

    def get_combination_id(self, combination):
        return self.db.get_combination_id(combination)

    def get_combination_weight(self, combination):
        return self.db.get_combination_weight(combination)

    def update_weight(self, combination_id, trade_result):
        self.db.update_combination_weight(combination_id=combination_id,
                                          trade_result=trade_result)

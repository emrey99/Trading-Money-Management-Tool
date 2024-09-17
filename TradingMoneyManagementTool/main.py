from TradingMoneyManagementTool.Factors.FundamentalFactors import FundamentalFactors
from TradingMoneyManagementTool.RiskManager import RiskManager
from TradingMoneyManagementTool.Factors.TechnicalFactors import TechnicalFactors
from TradingMoneyManagementTool.Messages.Message import Message
from TradingMoneyManagementTool.Messages.MessageHandler import MessageHandler
from TradingMoneyManagementTool.Trades.TradeManager import TradeManager
from TradingMoneyManagementTool.Combinations.CombinationManager import CombinationManager


class Controller:
    def __init__(self):
        self.technical_analysis = TechnicalFactors()
        self.fundamental_analysis = FundamentalFactors()
        self.risk_manager = RiskManager()
        self.trade_manager = TradeManager()
        self.message_handler = MessageHandler()
        self.combination_manager = CombinationManager()

    def main(self):
        self.trade_manager.handle_open_trades()
        trade_direction = self.message_handler.get_trade_direction()
        technical_values = self.technical_analysis.get_technical_values()
        fundamental_values = self.fundamental_analysis.get_fundamental_values(trade_direction)
        technical_score = self.risk_manager.get_score(technical_values)
        fundamental_score = self.risk_manager.get_score(fundamental_values)
        technical_category = self.risk_manager.get_risk_category(technical_score)
        fundamental_category = self.risk_manager.get_risk_category(fundamental_score)
        overall_score = self.risk_manager.get_overall_score(technical_score, fundamental_score)
        overall_category = self.risk_manager.get_risk_category(overall_score)
        self.risk_manager.check_final_score(overall_score)
        combination = self.combination_manager.get_combination(technical_category=technical_category,
                                                               fundamental_category=fundamental_category)
        combination_id = self.combination_manager.get_combination_id(combination)
        combination_weight = self.combination_manager.get_combination_weight(combination)
        if not combination_id:
            self.combination_manager.create_combination(technical_category, fundamental_category)
        self.message_handler.display_risk_summary(technical_score=technical_score,
                                                  fundamental_score=fundamental_score,
                                                  technical_category=technical_category,
                                                  fundamental_category=fundamental_category,
                                                  weight=combination_weight,
                                                  overall_category=overall_category,
                                                  overall_score=overall_score)
        if self.message_handler.get_user_confirmation(f"{Message.TAKE_TRADE}"):
            self.trade_manager.execute_trade(
                combination_id=combination_id,
                fundamental_values=fundamental_values,
                technical_values=technical_values,
                trade_direction=trade_direction
            )


controller = Controller()
controller.main()

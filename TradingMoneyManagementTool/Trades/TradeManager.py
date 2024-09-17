from TradingMoneyManagementTool.Messages.MessageHandler import MessageHandler
from TradingMoneyManagementTool.Messages.Message import Message
from TradingMoneyManagementTool.Trades.TradesDB import TradesDB
from TradingMoneyManagementTool.Factors.FactorsDB import FactorsDB
from TradingMoneyManagementTool.Combinations.CombinationManager import CombinationManager


class TradeManager:

    def __init__(self):
        self.trades_db = TradesDB()
        self.factor_db = FactorsDB()
        self.combination_manager = CombinationManager()
        self.messages = MessageHandler()

    def handle_open_trades(self):
        open_trades = self.trades_db.get_open_trades()
        for trade in open_trades:
            print(f"Trade with ID {trade[0]} is still open.")  # TODO show the date here not the ID
            if self.messages.get_user_input(Message.IS_TRADE_IN_PROGRESS) == Message.NEGATIVE_ANSWER:
                trade_result = self.messages.get_user_input(Message.WIN_OR_LOSE)
                self.trades_db.update_trade_status(trade_id=trade[0], status="closed", result=trade_result)
                self.combination_manager.update_weight(combination_id=trade[1], trade_result=trade_result)

    def execute_trade(self, trade_direction, combination_id, technical_values, fundamental_values):
        self.trades_db.insert_trade(direction=trade_direction,
                                    combination_id=combination_id,
                                    result="")
        trade_id = self.trades_db.cursor.lastrowid
        self.factor_db.insert_technicals(trade_id,
                                         technical_values=technical_values)
        self.factor_db.insert_fundamentals(trade_id,
                                           fundamental_values=fundamental_values)

from TradingMoneyManagementTool.Messages.Message import Message


class MessageHandler:

    @staticmethod
    def get_trade_direction():
        return input(f"{Message.LONG_OR_SHORT}")

    @staticmethod
    def get_user_confirmation(message):
        return input(f"{message} (yes/no): ").lower() == 'yes'

    @staticmethod
    def get_user_input(message):
        return input(message).strip().lower()

    @staticmethod
    def display_risk_summary(technical_score,
                             fundamental_score,
                             technical_category,
                             fundamental_category,
                             overall_category,
                             overall_score,
                             weight):

        print(f"Technical score is {technical_score}")
        print(f"Fundamental score is {fundamental_score}")
        print(f"Technical category is {technical_category}")
        print(f"Fundamental category is {fundamental_category}")
        print(f"Overall category is {overall_category}")
        print(f"Overall score is {overall_score}")
        print(f"Weigh ot combination is {weight}")



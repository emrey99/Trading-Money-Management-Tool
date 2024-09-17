class Message:
    LONG_OR_SHORT = "Do you want to go Long or Short: "
    TECHNICAL_SCORE = "Your technical score is: "
    FUNDAMENTAL_SCORE = "Fundamental Score: "
    FINAL_SCORE_LOW = "Final score is less than or equal to 0, please consider not taking the trade."
    FINAL_SCORE_SUMMARY = (
        "Final Score: {final_score:.2f}, Technical category: {technical_category}, "
        "Fundamental category: {fundamental_category}, Category: {final_category}"
    )
    TAKE_TRADE = "Are you taking this trade? (yes/no): "
    COMBINATION_WEIGHT = "The weight of this combination is {weight}"
    COMBINATION_NOT_EXIST = "This combination does not exist, but will be added"
    POSITIVE_ANSWER = "yes"
    NEGATIVE_ANSWER = "no"
    INVALID_INPUT_TECHNICALS = "Invalid input. Please respond with 'YES' or 'NO'."
    INVALID_INPUT_FUNDAMENTALS = "Invalid input. Please respond with positive, negative or neutral."
    CONTINUING_WITH_TRADE = "Continuing with technical and fundamental analysis for the open trade."
    IS_TRADE_IN_PROGRESS = "Is the trade still in progress? (yes/no): "
    WIN_OR_LOSE = "Did the trade result in a win or loss?"
    INVALID_INPUT = "Invalid input."


import random

class RPSTrainer:
    def __init__(self):
        """
        Actions:
        Rock (R) = 0
        Paper (P) = 1
        Scissors (S) = 2
        """
        self.NUM_ACTIONS = 3

        self.regret_sum = [0, 0, 0]
        self.opp_regret_sum = [0, 0, 0]
        self.actions = [0, 1, 2]
        self.action_utility = [
            [0, -1, 1],
            [1, 0, -1],
            [-1, 1, 0]
        ]

        self.strategy_sum = [0, 0, 0]
        self.opp_strategy_sum = [0, 0, 0]

    def get_strategy(self, regret_sum):
        strategy = [0, 0, 0]

        regret_sum = [regret if regret >= 0 else 0 for regret in regret_sum]
        total_regret_sum = sum(regret_sum)

        for i in range(self.NUM_ACTIONS):
            if total_regret_sum > 0:
                strategy[i] = regret_sum[i] / total_regret_sum
            else:
                strategy[i] = 1.0 / self.NUM_ACTIONS
        
        return strategy
    
    def get_average_strategy(self, player):
        strategy_sum = self.strategy_sum if not player else self.opp_strategy_sum

        average_strategy = [0, 0, 0]
        total_strategy_sum = sum(strategy_sum)

        for i in range(self.NUM_ACTIONS):
            if total_strategy_sum > 0:
                average_strategy[i] = strategy_sum[i] / total_strategy_sum
            else:
                average_strategy[i] = 1.0 / self.NUM_ACTIONS

        return average_strategy
    
    def get_action(self, strategy):
        if sum(strategy) == 0:
            return random.choice(self.actions)
        else:
            return random.choices(self.actions, weights = strategy, k = 1)[0]
    
    def get_reward(self, action_1, action_2):
        return self.action_utility[action_1][action_2]
    
    def train(self, iterations):
        for _ in range(iterations):
            strategy = self.get_strategy(self.regret_sum)
            opp_strategy = self.get_strategy(self.opp_regret_sum)

            for i in range(self.NUM_ACTIONS):
                self.strategy_sum[i] += strategy[i]
                self.opp_strategy_sum[i] += opp_strategy[i]

            action = self.get_action(strategy)
            opp_action = self.get_action(opp_strategy)

            reward = self.get_reward(action, opp_action)
            opp_reward = self.get_reward(opp_action, action)

            for counterfactual_action in range(self.NUM_ACTIONS):
                # Regret = Counterfactual reward - Actual reward
                regret = self.get_reward(counterfactual_action, opp_action) - reward
                opp_regret = self.get_reward(counterfactual_action, action) - opp_reward
                
                self.regret_sum[counterfactual_action] += regret
                self.opp_regret_sum[counterfactual_action] += opp_regret

def format_strategy_decimal(strategy, decimal_point):
    return [f"%.{decimal_point}f" % frequency for frequency in strategy ]

def main():
    trainer = RPSTrainer()
    trainer.train(100000)

    strategy = format_strategy_decimal(trainer.get_average_strategy(0), 4)
    opp_strategy = format_strategy_decimal(trainer.get_average_strategy(1), 4)

    print("Average strategy:", strategy)
    print("Opponent's strategy:", opp_strategy)

if __name__ == "__main__":
    main()
import random

AI = 0
PLAYER = 1

ROLL = 1
PASS = 0


class QLearner:
    def __init__(self):
        self.Q_pass = {}
        self.Q_roll = {}
        self.gamma = 0.8    # discount factor
        self.alpha = 0.05   # learning rate
        self.last_move = None
        self.last_state = None

    def ql_ai(self, turn, rolled, my_points, opp_points):
        # compatibility parameters:
        #   turn - can be ignored
        # useful parameters:
        #   rolled, my_points, opp_points - the current state, to determine
        #                                  action: PASS or ROLL

        state_index = state_idx(my_points, opp_points, rolled)
        roll_value = self.Q_roll[state_index]
        pass_value = self.Q_pass[state_index]

        if pass_value == 0 and roll_value == 0 or random.random() < 0.05:
            return round(random.random())
        if roll_value > pass_value:
            return ROLL
        return PASS

    def update(self, s, action, reward, s_prim):
        # s - old state (my points, opp points, rolled)
        # action - action taken from state s
        # reward - 0 usually, 100 if I won, -100 if I lost
        # s_prim - new state. What happened after my action was taken
        max_Q = max(self.Q_pass[s_prim], self.Q_roll[s_prim])
        if action == PASS:
            self.Q_pass[s] += self.alpha * (reward + self.gamma * max_Q - self.Q_pass[s])
        if action == ROLL:
            self.Q_roll[s] += self.alpha * (reward + self.gamma * max_Q - self.Q_roll[s])

    def runner(self, turn, rolled, ai_points, opp_points):
        state_index = state_idx(ai_points, opp_points, rolled)
        if state_index not in self.Q_pass.keys():
            self.Q_pass[state_index] = 0
        if state_index not in self.Q_roll.keys():
            self.Q_roll[state_index] = 0

        if self.last_move is not None and self.last_state is not None:
            r = 0
            if ai_points >= 100:
                r = 100
            if opp_points >= 100:
                r = -100
            self.update(self.last_state, self.last_move, r, state_index)
        self.last_move = self.ql_ai(turn, rolled, ai_points, opp_points)
        self.last_state = state_index
        return self.last_move


def pig_game(ai_func, opponent_func):
    rolled = 0
    turn = PLAYER
    player_points = ai_points = 0
    if random.random() < 0.5:
        turn = AI

    while True:

        if turn == PLAYER:
            decision = opponent_func(turn, rolled, player_points, ai_points)
            if player_points >= 100:
                return PLAYER
            if decision == PASS:
                rolled = 0
                turn = AI
            else:
                dieroll = random.randint(1, 6)
                if dieroll == 1:
                    player_points -= rolled  # lose all points again
                    rolled = 0
                    turn = AI
                else:
                    rolled += dieroll
                    player_points += dieroll

        else:
            decision = ai_func(turn, rolled, ai_points, player_points)
            if ai_points >= 100:
                return AI
            if decision == PASS:
                rolled = 0
                turn = PLAYER
            else:
                dieroll = random.randint(1, 6)
                if dieroll == 1:
                    ai_points -= rolled  # lose all points again
                    rolled = 0
                    turn = PLAYER
                else:
                    rolled += dieroll
                    ai_points += dieroll


def dummy_ai(turn, rolled, my_points, opp_points):
    if rolled < 21:
        return ROLL
    else:
        return PASS


def state_idx(ai_points, opp_points, rolled):
    ap = min(ai_points//10, 10)    # ai points: 0-9, 10-19, ..., 90-99, 100
    op = min(opp_points//10, 10)
    r = min(rolled//5, 10)         # rolled: 0-4, 5-9, ..., 45-49, 50+
    return (ap, op, r)


def trainer(ai_strategy, opponent_strategy, training_games, dummy_games, cycles):

    for i in range(cycles):
        for j in range(training_games):
            pig_game(ai_strategy, opponent_strategy)
        ai_wins = 0
        opponent_wins = 0
        for j in range(dummy_games):
            if pig_game(ai_strategy, dummy_ai) == 1:
                opponent_wins += 1
            else:
                ai_wins += 1
        print("Win percentage for cycle " + str(i) + ": " + str(ai_wins / dummy_games))


ql1 = QLearner()
ql2 = QLearner()

trainer(ql1.runner, ql2.runner, 10000, 100, 100)
print(ql1.Q_pass)
print(ql1.Q_roll)

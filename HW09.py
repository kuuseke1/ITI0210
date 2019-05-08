import random


class QLearner:
    def __init__(self):
        self.Q_pass = {}
        self.Q_roll = {}
        self.gamma = 0.8    # discount factor
        self.alpha = 0.05   # learning rate

    def ql_ai(self, turn, rolled, my_points, opp_points):
        # compatibility parameters:
        #   turn - can be ignored
        # useful parameters:
        #   rolled, my_points, opp_points - the current state, to determine
        #                                  action: PASS or ROLL
        state_index = state_idx(my_points, opp_points, rolled)
        if state_index in self.Q_pass.keys():
            pass_chance = self.Q_pass[state_index]
        else:
            pass_chance = 0
            self.Q_pass[state_index] = 0
        if state_index in self.Q_roll.keys():
            roll_chance = self.Q_roll[state_index]
        else:
            roll_chance = 0
            self.Q_roll[state_index] = 0
        if pass_chance == 0 and roll_chance == 0:
            print("Both have 0 points, random move")
            return round(random.random())
        if random.random() < 0.05:
            print("Random move")
            return round(random.random())
        if roll_chance > pass_chance:
            print("Pass seems more beneficial")
            return 1
        print("Roll seems more beneficial")
        return 0

    def update(self, s, action, reward, s_prim):
        # s - old state (my points, opp points, rolled)
        # action - action taken from state s
        # reward - 0 usually, 100 if I won, -100 if I lost
        # s_prim - new state. What happened after my action was taken
        max_Q = max(self.Q_pass[s_prim], self.Q_roll[s_prim])
        if action == 0:
            self.Q_pass[s] += self.alpha * (reward + self.gamma * max_Q - self.Q_pass[s])
        if action == 1:
            self.Q_roll[s] += self.alpha * (reward + self.gamma * max_Q - self.Q_roll[s])

    def runner(self):
        return

AI = 0
PLAYER = 1

ROLL = 1
PASS = 0


def pig_game(ai_func):
    rolled = 0
    turn = PLAYER
    player_points = ai_points = 0
    if random.random() < 0.5:
        turn = AI

    while True:
        print("Your points", player_points,
            "AI points", ai_points,
            "holding", rolled)

        if turn == PLAYER:
            decision = ai_func(turn, rolled, player_points, ai_points)
            if player_points >= 100:
                return PLAYER
            if decision == PASS:
                print("-- PLAYER decides to pass.")
                rolled = 0
                turn = AI
            else:
                dieroll = random.randint(1, 6)
                print("-- PLAYER rolled...", dieroll)
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
                print("-- AI decides to pass.")
                rolled = 0
                turn = PLAYER
            else:
                dieroll = random.randint(1, 6)
                print("-- AI rolled...", dieroll)
                if dieroll == 1:
                    ai_points -= rolled # lose all points again
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


ql = QLearner()
print(ql.ql_ai('op', 24, 0, 1))

pig_game(dummy_ai)

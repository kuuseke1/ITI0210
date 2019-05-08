import random


class QLearner:
    def __init__(self):
        self.Q = {}
        self.gamma = 0.8    # discount factor
        self.alpha = 0.05   # learning rate

    def ql_ai(self, turn, rolled, my_points, opp_points):
        # compatibility parameters:
        #   turn - can be ignored
        # useful parameters:
        #   rolled, my_points, opp_points - the current state, to determine
        #                                  action: PASS or ROLL
        my_state_index = state_idx(my_points, opp_points, rolled)
        opp_state_index = state_idx(opp_points, my_points, rolled)
        if my_state_index in self.Q.keys():
            pass_chance = self.Q[my_state_index]['PASS']
            roll_chance = self.Q[my_state_index]['ROLL']
        if self.Q[my_state_index]['PASS'] == 0 and self.Q[opp_state_index]['ROLL'] == 0:
            print("Both have 0 points, random move")
            return round(random.random())
        if random.random() < 0.05:
            print("Random move")
            return round(random.random())
        if self.Q[my_state_index][0] > self.Q[opp_state_index][1]:
            print("Pass seems more beneficial")
            return 0
        print("Roll seems more beneficial")
        return 1

    def update(self, s, action, reward, s_prim):
        # s - old state (my points, opp points, rolled)
        # action - action taken from state s
        # reward - 0 usually, 100 if I won, -100 if I lost
        # s_prim - new state. What happened after my action was taken
        return

AI = 0
PLAYER = 1

ROLL = 0
PASS = 1


def pig_game(ai_func):
    rolled = 0
    turn = PLAYER
    player_points = ai_points = 0

    while player_points < 100 and ai_points < 100:
        print("Your points", player_points,
            "AI points", ai_points,
            "holding", rolled)

        if turn == PLAYER:
            decision = ROLL
            if rolled > 0:
                s = input("Do you want to keep rolling (Y/n)? ")
                if len(s) > 0 and s[0].lower() == "n":
                    decision = PASS

            if decision == PASS:
                rolled = 0
                turn = AI
            else:
                dieroll = random.randint(1, 6)
                print("You rolled...", dieroll)
                if dieroll == 1:
                    player_points -= rolled # lose all points again
                    rolled = 0
                    turn = AI
                else:
                    rolled += dieroll
                    player_points += dieroll

        else:
            decision = ai_func(turn, rolled, ai_points, player_points)
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

    if player_points >= 100:
        print("You won!")
    elif ai_points >= 100:
        print("AI won.")


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

# pig_game(dummy_ai)

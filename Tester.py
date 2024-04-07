from Random_Agent import Randon_Agent
# from Fix_Agent import Fix_Agent
from RushHour import RushHour

class Tester:
    def __init__(self, rushhour:RushHour, player) -> None:
        self.rushhour = rushhour
        self.player = player
        

    def test (self, games_num):
        env = self.rushhour
        player_steps = 0
        games = 0
        score = 0
        while games < games_num:
            action = self.player.get_Action(state=env.state, train = False)
            env.move2( env.state , action)
            player_steps = player_steps + 1
            if env.is_end_of_game(env.state):
                score = score + player_steps
                env.state = env.get_init_state()
                games += 1
        print("done")
        return score / games_num       

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = RushHour()
    player = Randon_Agent(env)
    test = Tester(env,player)
    print(test.test(100))

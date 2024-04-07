from RushHour import RushHour
from DQN_Agent import DQN_Agent
from Replay_Buffer import ReplayBuffer
from Random_Agent import Randon_Agent
from Constant import *
import torch
from Tester import Tester

epochs = 2000000
start_epoch = 0
C = 100
learning_rate = 0.0001 # למד עם 0.0001
batch_size = 64
env = RushHour()
MIN_Buffer = 4000

File_Num = 5
path_load= None
path_Save=f'Data/params_{File_Num}.pth'
path_best = f'Data/best_params_{File_Num}.pth'
buffer_path = f'Data/buffer_{File_Num}.pth'
results_path=f'Data/results_{File_Num}.pth'
random_results_path = f'Data/random_results_{File_Num}.pth'
path_best_random = f'Data/best_random_params_{File_Num}.pth'


def main ():
    
    player = DQN_Agent(rushhour=env , parametes_path=path_load)
    player_hat = DQN_Agent(rushhour=env, train=False)
    Q = player.DQN
    Q_hat = Q.copy()
    Q_hat.train = False
    player_hat.DQN = Q_hat
    
    # player2 = Random_Agent(player=-1, env=env)   
    buffer = ReplayBuffer(path=None) # None
    
    results_file = [] #torch.load(results_path)
    results = [] #results_file['results'] # []
    avgLosses = [] #results_file['avglosses']     #[]
    avgLoss = 0 #avgLosses[-1] #0
    loss = 0
    # res = 0
    best_step = 200
    loss_count = 0
    tester = Tester(rushhour=env , player=player)
    random_results = [] #torch.load(random_results_path)   # []
    best_random = 0 #max(random_results)
    
    
    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,1000 * 10, gamma=0.50)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        # print(f'epoch = {epoch}', end='\r')
        state_1 = env.get_init_state()
        while not env.is_end_of_game(state_1) :
            print (state_1.step, end='\r')
            
            # Sample Environement
            action_1 = player.get_Action(state_1, epoch=epoch)
            after_state_1 = env.get_next_State(state=state_1, action=action_1)
            reward_1 = env.reward(after_state_1 , action_1)
            if reward_1 == 10: 
                buffer.push(state_1, action_1, reward_1, after_state_1, True)
                break
            if after_state_1.step > 200:
                buffer.push(state_1, action_1, 0, after_state_1, False)
                break
     
            buffer.push(state_1, action_1, reward_1, after_state_1, False)
            state_1 = after_state_1
            
            if len(buffer) < MIN_BUFFER: # MIN_Buffer: , 100:
                continue
            
            # Train NN
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states, actions)
            next_actions = player.get_Actions(next_states, dones)  # DDQN
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions) 

            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            
            scheduler.step()
            if loss_count <= 1000:
                avgLoss = (avgLoss * loss_count + loss.item()) / (loss_count + 1)
                loss_count += 1
            else:
                avgLoss += (loss.item()-avgLoss)* 0.00001 
            
        if epoch % C == 0:
                Q_hat.load_state_dict(Q.state_dict())

        if (epoch+1) % 10 == 0:
            print(f'\nres= {state_1.step}')
            avgLosses.append(avgLoss)
            results.append(state_1.step)
            # results.append(res)
        if best_step > state_1.step:      
            best_step = state_1.step
            

        # if (epoch+1) % 1000 == 0:
        #     print(f'\nres= {res}')
        #     test = tester(100)
        #     # test_score = test[0]-test[1]
        #     test_score = test
        #     if best_random < test_score and tester(1) == 1:
        #         best_random = test_score
        #         player.save_param(path_best_random)
        #     print(test)
        #     random_results.append(test_score)

        if (epoch+1) % 500 == 0:
            torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
            torch.save(buffer, buffer_path)
            player.save_param(path_Save)
            torch.save(random_results, random_results_path)
        

        print (f'epoch={epoch} loss={loss:.5f} step={state_1.step} avgloss={avgLoss:.5f}', end=" ")
        print (f'learning rate={scheduler.get_last_lr()[0]} path={path_Save} step= {state_1.step} best_step = {best_step}')

    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(buffer, buffer_path)
    torch.save(random_results, random_results_path)

if __name__ == '__main__':
    main()
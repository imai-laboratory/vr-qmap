import diambra.arena
import time 
import socket
import numpy as np
import time
import torch
import math
import diambra.arena
from diambra.arena.ray_rllib.make_ray_env import DiambraArena, preprocess_ray_config
from ray.rllib.algorithms.ppo import PPO

ckpt_dir = "/home/rintaro/ray_results/PPO_DiambraArena_2023-02-12_01-55-45rey654r_/checkpoint_030001"

OP_SIZE = 8


class Qmapping:
    def __init__(self, agent):
        self.qmapping = {}
        self.PPO = agent
        self.actor = None
        
        # self.key_lists = ["a","s","d","f", "g","h","j","k","l",";"]
        self.key_lists = []
        for i in range(OP_SIZE):
            # ges_name = f"ges_{i}"
            self.key_lists.append(self.gesnum_to_key(i))
        l = len(self.key_lists)
        for key in self.key_lists:
            self.qmapping[key] = np.array([1.0 / l ] * l)
    
    def gesnum_to_key(self, ges_num):
        key = "ges_" + str(ges_num)
        return key

    def interpret(self, key, obs, frame):
        alpha = self.calc_beta(frame, 0.05, 100)

        advantage_value = self.calc_advantage(obs)

        for action_idx in range(len(self.key_lists)):
            Qm_value = self.qmapping[key][action_idx]
            new_Qm_value = (1-alpha) * Qm_value + alpha * advantage_value[action_idx]

            self.qmapping[key][action_idx] = new_Qm_value
    
        ret_action_idx = np.argmax(self.qmapping[key])
        print(self.qmapping)
        return ret_action_idx

    def calc_alpha(self, x, k = 30, x_0 = 0.08):
        return 1 - self.logistic(x,k,x_0)
    def calc_beta(self, x, k = 30, x_0 = 0.08):
        return (1 - 1 / (1 + math.exp(-k * (x - x_0))))

    def calc_advantage(self, obs):
            # advantage_value = self.actor(torch.tensor(obs, dtype=torch.float32))
        _, _, extra = agent.compute_single_action(observation, full_fetch=True)
        advantage_value = self.softmax(extra['action_dist_inputs'])
        return advantage_value

    def softmax(self,x):
        ret = []
        deno = 0
        for i in x:
            deno += math.exp(i)
        for i in x:
            ret.append(math.exp(i)/deno)

        return np.array(ret)


if __name__ == "__main__":

    settings = {}
    settings["frame_shape"] = (84, 84, 1)
    settings["characters"] = ("Kasumi")
    settings["action_space"] = "discrete"
    settings["attack_but_combination"] = False

    # Wrappers Settings
    wrappers_settings = {}
    wrappers_settings["reward_normalization"] = True
    wrappers_settings["actions_stack"] = 12
    wrappers_settings["frame_stack"] = 5
    wrappers_settings["scale"] = True
    wrappers_settings["process_discrete_binary"] = True

    config = {
        # Define and configure the environment
        "env": DiambraArena,
        "env_config": {
            "game_id": "doapp",
            "settings": settings,
            "wrappers_settings": wrappers_settings,
        },
        "num_workers": 0,
        "num_gpus": 1,
        # "train_batch_size": 200,
        "framework": "torch",
    }
    config = preprocess_ray_config(config)
    env = diambra.arena.make("doapp", settings, wrappers_settings)

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Create the RLlib Agent.
    agent = PPO(config=config)
    agent.restore(ckpt_dir)

    observation = env.reset()
    Qmap = Qmapping(agent)
    cnt = 0

    s.bind(('0.0.0.0', 50051))
    s.listen(50)
    print("listen")

    print("press enter")
    while True:
        key = input(' Enterキーを押したら終了します')
        if not key:
            break

    # for _ in range(2):
    #     observation = env.reset()
    #     conn, addr = s.accept()
    #     print("listening")
    #     while True:
    #         cnt += 1
    #         env.render()

    #         action = None
            
    #         data = conn.recv(1024)
    #         ges_num = int(data.decode())
    #         if ges_num == 9999:
    #             action = 11
    #         else:
    #             action = Qmap.interpret(ges_num, observation, cnt)



    #         observation, reward, done, info = env.step(action)
            
    #         if done:
    #             observation = env.reset()
    #             break



    for _ in range(2):
        observation = env.reset()
        conn, addr = s.accept()
        conn.setblocking(0)
        while True:
            cnt += 1
            time.sleep(0.05)
            env.render()

            action = 11
            
            try:
                data = conn.recv(1024)
                if data:
                    print(data)
                    ges_num = int(data.decode())
                    action = Qmap.interpret(ges_num, observation, cnt)

            except BlockingIOError:
                pass

            observation, reward, done, info = env.step(action)
            
            if done:
                observation = env.reset()
                break







import numpy as np
import time
import torch
import math
import diambra.arena
from diambra.arena.ray_rllib.make_ray_env import DiambraArena, preprocess_ray_config
from ray.rllib.algorithms.ppo import PPO

from pynput import keyboard
from pynput.keyboard import Key, Listener
ckpt_dir = "/home/rintaro/ray_results/PPO_DiambraArena_2023-02-12_01-55-45rey654r_/checkpoint_030001"


class MonKeyBoard:
    def __init__(self):
        self.action = -1
        self.char = None
    def on_press(self,key):
        # try:
        #     print('press: {}'.format(key.char))
        # except AttributeError:
        #     print('spkey press: {}'.format(key))
        try:
            c = key.char
            self.char = c
            # print(f"key.char:{key.char}")
            # print(f"key     :{key}")
            if c == "a":
                self.action = 0
            elif c == "s" or c == "'s'":
                # print("changed")
                self.action = 1
            elif c == "d":
                self.action = 2
            elif c == "f":
                self.action = 3
            elif c == "g":
                self.action = 4
            elif c == "h":
                self.action = 5
            elif c == "j":
                self.action = 6
            elif c == "k":
                self.action = 7
            elif c == "l":
                self.action = 8
            elif c == ";":
                self.action = 9
            elif c == ":":
                self.action = 10
        except AttributeError:
            print('spkey press: {}'.format(key))        
    
    def on_release(self,key):
        # print('release: {}'.format(key))
        if( key == keyboard.Key.esc):
            print("StopKey")
            self.listener.stop()
            self.listener = None
            
    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
    def getstatus(self):
        if(self.listener == None):
            return False       
        return True


class Qmapping:
    def __init__(self, agent):
        self.qmapping = {}
        self.PPO = agent
        self.actor = None
        
        self.key_lists = ["a","s","d","f", "g","h","j","k","l",";"]
        l = len(self.key_lists)
        for key in self.key_lists:
            self.qmapping[key] = np.array([1.0 / l ] * l)
        

    def interpret(self, key, obs, frame):
        alpha = self.calc_beta(frame, 0.05, 100)

        advantage_value = self.calc_advantage(obs)
        # advantage_value = advantage_value.detach().numpy()

        for action_idx in range(len(self.key_lists)):
            Qm_value = self.qmapping[key][action_idx]
            new_Qm_value = (1-alpha) * Qm_value + alpha * advantage_value[action_idx]

            # diff_qmapping = abs(new_Qm_value - Qm_value)
            # self.log.qmapping_diff_log[tmp_ch].append(diff_qmapping)

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
    # Create the RLlib Agent.
    agent = PPO(config=config)
    agent.restore(ckpt_dir)

    observation = env.reset()
    Qmap = Qmapping(agent)
    cnt = 0

    monitor = MonKeyBoard()
    monitor.start()
    for _ in range(2):
        while True:
            cnt += 1
            time.sleep(0.05)
            
            env.render()
            print(monitor.action)
            
            if monitor.action != -1:
                # observation, reward, done, info = env.step()
                action = Qmap.interpret(monitor.char, observation, cnt)
                print(action)
                monitor.action = -1
            else:
                action = 11
            observation, reward, done, info = env.step(action)
            if done:
                observation = env.reset()
                break

            print()
            # action, state, extra = agent.compute_actions(observation)
            
            # action, state, extra = agent.compute_action(observation)
            # action, state, extra = agent.compute_actions(observation, full_fetch=True)
            # action, state, extra = agent.compute_single_action(observation, full_fetch=True)
            # print(extra['action_dist_inputs'])
            # print(len(extra["action_dist_inputs"]))
            if done:
                observation = env.reset()
                break


import numpy as np
import time
import torch
import math
import diambra.arena
from diambra.arena.ray_rllib.make_ray_env import DiambraArena, preprocess_ray_config
from ray.rllib.algorithms.ppo import PPO

from pynput import keyboard
from pynput.keyboard import Key, Listener
ckpt_dir = "/home/rintaro/ray_results/PPO_DiambraArena_2023-02-12_01-55-45rey654r_/checkpoint_090001"


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
    # Qmap = Qmapping(agent)
    cnt = 0

    for _ in range(2):
        while True:
            cnt += 1
            time.sleep(0.05)
            
            env.render()
            action = agent.compute_action(observation)
            observation, reward, done, info = env.step(action)

            if done:
                print("============== info ==============")
                print(info)
                print("============== info ==============")
                observation = env.reset()
                break

            # action, state, extra = agent.compute_actions(observation)
            
            # action, state, extra = agent.compute_action(observation)
            # action, state, extra = agent.compute_actions(observation, full_fetch=True)
            # action, state, extra = agent.compute_single_action(observation, full_fetch=True)
            # print(extra['action_dist_inputs'])
            # print(len(extra["action_dist_inputs"]))
            if done:
                observation = env.reset()
                break


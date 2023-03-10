import diambra.arena
from diambra.arena.ray_rllib.make_ray_env import DiambraArena, preprocess_ray_config
from ray.rllib.algorithms.ppo import PPO
from ray.tune.logger import pretty_print

TRAINING_STEP = int(1e8)

if __name__ == "__main__":

    ckpt_freq = 10000

    # Settings
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
        "train_batch_size": 200,
        "framework": "torch",
    }

    # Update config file
    config = preprocess_ray_config(config)

    # Create the RLlib Agent.
    agent = PPO(config=config)
    print("Policy architecture =\n{}".format(agent.get_policy().model))

    # Run it for n training iterations
    print("\nStarting training ...\n")


    for idx in range(TRAINING_STEP):
        print("Training iteration:", idx + 1)
        results = agent.train()
        if idx % ckpt_freq == 0:
            checkpoint_dir = agent.save()
            print(f"checkpoing saved at {checkpoint_dir}")
    print("\n .. training completed.")
    print("Training results:\n{}".format(pretty_print(results)))

    # Evaluate the trained agent (and render each timestep to the shell's
    # output).
    print("\nStarting evaluation ...\n")
    results = agent.evaluate()
    print("\n... evaluation completed.\n")
    print("Evaluation results:\n{}".format(pretty_print(results)))

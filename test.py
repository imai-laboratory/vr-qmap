import diambra.arena

env_settings = {}
env_settings["action_space"] = "discrete"
env_settings["attack_but_combination"] = False
env = diambra.arena.make("doapp", env_settings)

observation = env.reset()

while True:
    env.render()

    actions = env.action_space.sample()

    observation, reward, done, info = env.step(actions)

    if done:
        observation = env.reset()
        break

env.close()

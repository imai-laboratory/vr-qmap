import diambra.arena
import time 
import socket

env_settings = {}
env_settings["action_space"] = "discrete"
env_settings["attack_but_combination"] = False
env_settings["difficulty"] = 1

env = diambra.arena.make("doapp", env_settings)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 50008))
s.bind(('0.0.0.0', 50051))
s.listen(1)
print("listen")
while True:
    conn, addr = s.accept()
    data = None
    data = conn.recv(1024)
    if data:
        print('data : {}'.format(data))
        break
    
print("game start")


observation = env.reset()
conn, addr = s.accept()
while True:

    time.sleep(0.05)
    env.render()

    
    action = 11
    data = conn.recv(1024)
    if data:
        print(data)
        action = int(data.decode())
    
    
    observation, reward, done, info = env.step(action)


    # if action != -1:
    #     observation, reward, done, info = env.step(action)
    # else:
    #     observation, reward, done, info = env.step(11)
    
    if done:
        observation = env.reset()
        break
conn.close()

env.close()

import diambra.arena
import time 
from pynput import keyboard
from pynput.keyboard import Key, Listener



class MonKeyBoard:
    def __init__(self):
        self.action = -1
    def on_press(self,key):
        # try:
        #     print('press: {}'.format(key.char))
        # except AttributeError:
        #     print('spkey press: {}'.format(key))
        try:
            c = key.char
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


monitor = MonKeyBoard()
monitor.start()

env_settings = {}
env_settings["action_space"] = "discrete"
env_settings["attack_but_combination"] = False
env_settings["difficulty"] = 1
env = diambra.arena.make("doapp", env_settings)

observation = env.reset()
# with Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()
while True:
    # status = monitor.getstatus()

    time.sleep(0.05)
    env.render()

    # action = env.action_space.sample()
    print(monitor.action)
    if monitor.action != -1:
        observation, reward, done, info = env.step(monitor.action)
        # print(monitor.action)
        # self.action = -1
    else:
        observation, reward, done, info = env.step(11)
    
    if done:
        observation = env.reset()
        break

env.close()

import hottub_gym
import gymnasium as gym
import matplotlib.pyplot as plt

env = gym.make("HotTub-v0")
state, info = env.reset()
action = 0
done = False

hottub_temps = []
step = 0
while not done:
    state, reward, done, terminated, info = env.step(action=action)
    print(info)

    # if step > 50:
    #     action = 0
    #
    # if step > 100:
    #     action = 1
    #
    # if step > 105:
    #     action = 0

    hottub_temps.append(info['tub_temp'])
    step += 1

plt.ylim([25, 35])
plt.plot(hottub_temps)
plt.show()
import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces


class HotTubEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, interval_len=5, heat_deg_hour=2):

        # start algorithm at 6h, end at 19h => run for 13h
        self.n_intervals = (13*60)/interval_len
        self.interval_len = interval_len
        self.heat_deg_hour = 2
        self.energy_usage_hour = 0.680  # kwh
        self.cooling_k = 0.001

        self.observation_space = spaces.Box(0, 1, shape=(3,), dtype=float)

        self.ambient_temp = 20
        self.tub_temp = 32
        self.max_tub_temp = 40
        self.current_interval = 0
        self.energy_usage = 0

        # We have 2 actions, corresponding to "turn on heater for interval min", "do not heat for interval min"
        self.action_space = spaces.Discrete(4)

    def _get_obs(self):
        return np.array([self.tub_temp/40, self.ambient_temp/40, self.current_interval/self.n_intervals])

    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.current_interval = 0
        self.tub_temp = 32
        self.ambient_temp = 20
        self.energy_usage = 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def _heat_interval(self):
        heat_deg = self.heat_deg_hour*(self.interval/60)

        self.tub_temp += heat_deg
        self.energy_usage += self.energy_usage_hour*(self.interval/60)

        if self.tub_temp > self.max_tub_temp:
            self.tub_temp = self.max_tub_temp

    def _idle_interval(self):
        new_temp = self.ambient_temp+(self.tub_temp-self.ambient_temp)*np.exp(self.cooling_k)

    def step(self, action):

        if action == 0:
            # do nothing cool the tub for 5min
            self._idle_interval()
        elif action == 1:
            # heat the tub for 5min, use enery
            self._heat_interval()

        terminated = self.current_interval = self.n_intervals
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
from gymnasium.envs.registration import register

register(
     id="HotTub-v0",
     entry_point="hottub_gym.hottub_env:HotTubEnv",
     max_episode_steps=300,
)
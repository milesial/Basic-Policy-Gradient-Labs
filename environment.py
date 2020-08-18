import gym
import my_gym  # Necessary to see CartPoleContinuous, though PyCharm does not understand this
import numpy as np
from wrappers import FeatureInverter, BinaryShifter, BinaryShifterDiscrete, ActionVectorAdapter, PerfWriter
from gym.wrappers import TimeLimit

# to see the list of available gym environments, type:
# from gym import envs
# print(envs.registry.all())


def make_env(env_name, policy_type, max_episode_steps, env_obs_space_name=None):
    """
    Wrap the environment into a set of wrappers depending on some hyper-parameters
    Used so that most environments can be used with the same policies and algorithms
    :param env_name: the name of the environment, as a string. For instance, "MountainCarContinuous-v0"
    :param policy_type: a string specifying the type of policy. So far, "bernoulli" or "normal"
    :param max_episode_steps: the max duration of an episode. If None, uses the default gym max duration
    :param env_obs_space_name: a vector of names of the environment features. E.g. ["position","velocity"] for MountainCar
    :return: the wrapped environment
    """
    env = gym.make(env_name)
    if max_episode_steps is not None:
        env = TimeLimit(env, max_episode_steps)
    if env_name == "CartPole-v0" or env_name == "CartPoleContinuous-v0":
        env = FeatureInverter(env, 1, 2)
        env = ActionVectorAdapter(env)

    env.observation_space.names = env_obs_space_name

    if policy_type == "bernoulli":
        if env.action_space.contains(np.array([0.5])):
            env = BinaryShifter(env)
        # else:
        #    env = BinaryShifterDiscrete(env)

    env = PerfWriter(env)
    return env

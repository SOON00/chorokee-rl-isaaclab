# height_actions.py
import torch
from isaaclab.envs.mdp.actions.joint_actions import JointPositionAction
from isaaclab.envs.mdp.actions.actions_cfg import JointPositionActionCfg


# height_actions.py
class HeightAwareJointPositionAction(JointPositionAction):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)

        self.kp_height = getattr(cfg, "kp_height", 1.0)
        self.hip_joint_names = getattr(cfg, "hip_joint_names", [])
        self.knee_joint_names = getattr(cfg, "knee_joint_names", [])

        joint_names_list = getattr(self, "_joint_names", None)
        if joint_names_list is None:
            raise AttributeError("Parent class JointPositionAction has no attribute '_joint_names'")

        self.joint_name_to_index = {j: i for i, j in enumerate(joint_names_list)}
        self.hip_indices = [self.joint_name_to_index[n] for n in self.hip_joint_names]
        self.knee_indices = [self.joint_name_to_index[n] for n in self.knee_joint_names]

    def compute(self, actions, env_ids):

        base_actions = actions.clone()

        # --- height command ---
        desired_height = self._env.command_manager.get_command("base_height")[env_ids]

        # base height from root state
        current_height = self._env.scene.robot.data.root_state_w[env_ids, 2]

        height_error = desired_height - current_height
        correction = height_error * self.kp_height

        # hip correction
        for idx in self.hip_indices:
            base_actions[env_ids, idx] += correction

        # knee correction
        for idx in self.knee_indices:
            base_actions[env_ids, idx] -= 0.5 * correction

        return super().compute(base_actions, env_ids)

from isaaclab.utils.configclass import configclass
from isaaclab.envs.mdp.actions.actions_cfg import JointPositionActionCfg
from .height_actions import HeightAwareJointPositionAction

@configclass
class HeightAwareJointPositionActionCfg(JointPositionActionCfg):
    class_type = HeightAwareJointPositionAction
    hip_joint_names: list[str] = []
    knee_joint_names: list[str] = []
    kp_height: float = 1.0


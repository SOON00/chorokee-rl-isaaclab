import torch
from isaaclab.managers import CommandTerm

class UniformHeightCommand(CommandTerm):
    """
    Uniformly sampled base height command.
    """

    def __init__(self, cfg, env):
        super().__init__(cfg, env)

        self.range = torch.tensor(cfg.ranges["height"], device=env.device)
        self.resample_time_min = cfg.resampling_time_range[0]
        self.resample_time_max = cfg.resampling_time_range[1]

        self._time_left = torch.zeros(env.num_envs, device=env.device)
        self._command = torch.zeros(env.num_envs, 1, device=env.device)

    @property
    def command(self) -> torch.Tensor:
        return self._command

    def _resample_command(self, env_ids):
        """Resample the height for the specified envs."""
        r = torch.rand(len(env_ids), device=self._command.device)
        self._command[env_ids, 0] = self.range[0] + (self.range[1] - self.range[0]) * r

    # def _resample_command(self, env_ids):
    #     """Resample the height for the specified envs."""
    #     r = torch.rand(len(env_ids), device=self._command.device)
    #     self._command[env_ids, 0] = self.range[0] + (self.range[1] - self.range[0]) * r
    #     # 디버깅용 출력
    #     print("[DEBUG] Resampled base_height:", self._command[:min(5, len(self._command))])

    def _update_command(self):
        """Update command based on timer."""
        self._time_left -= self._env.step_dt
        resample_mask = self._time_left <= 0
        if torch.any(resample_mask):
            self._resample_command(resample_mask.nonzero(as_tuple=True)[0])
            self._time_left[resample_mask] = torch.rand(torch.sum(resample_mask), device=self._env.device) * (
                self.resample_time_max - self.resample_time_min
            ) + self.resample_time_min

    def _update_metrics(self):
        """Optionally update metrics (can be empty)."""
        pass


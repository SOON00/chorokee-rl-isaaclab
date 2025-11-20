import math
from dataclasses import MISSING

from isaaclab.managers import CommandTermCfg
from isaaclab.utils import configclass

from .gait_command import GaitCommand  # Import the GaitCommand class


@configclass
class UniformGaitCommandCfg(CommandTermCfg):
    """Configuration for the gait command generator."""

    class_type: type = GaitCommand  # Specify the class type for dynamic instantiation

    @configclass
    class Ranges:
        """Uniform distribution ranges for the gait parameters."""

        frequencies: tuple[float, float] = MISSING
        """Range for gait frequencies [Hz]."""
        offsets: tuple[float, float] = MISSING
        """Range for phase offsets [0-1]."""
        durations: tuple[float, float] = MISSING
        """Range for contact durations [0-1]."""

    ranges: Ranges = MISSING
    """Distribution ranges for the gait parameters."""

    resampling_time_range: tuple[float, float] = MISSING
    """Time interval for resampling the gait (in seconds)."""
    
 

from .uniform_height_command import UniformHeightCommand
from dataclasses import field

@configclass
class UniformHeightCommandCfg(CommandTermCfg):
    asset_name: str = MISSING
    resampling_time_range: tuple[float, float] = (0.5, 2.0)
    ranges: dict = field(default_factory=lambda: {"height": (0.6, 1.0)})
    class_type: type = UniformHeightCommand
    command_dim: int = 1

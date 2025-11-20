import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

current_dir = os.path.dirname(__file__)
usd_path = os.path.join(current_dir, "../usd/WF_TRON1A/WF_TRON1A.usd")

WHEELFOOT_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=usd_path,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            rigid_body_enabled=True,
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=0,
        ),
        activate_contact_sensors=True,
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.6),
        # pos=(0.0, 0.0, 0.8+0.166),
        joint_pos={
            ".*_Joint": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[
                # "abad_L_Joint",
                # "abad_R_Joint",
                "hip_L_Joint",
                "hip_R_Joint",
                "knee_L_Joint",
                "knee_R_Joint",
            ],
            effort_limit=80.0,
            velocity_limit=15.0,
            stiffness=42.0,
            damping=2.5,
            friction=0.0,
        ),
        # Abad만 별도 설정
        "abad": ImplicitActuatorCfg(
            joint_names_expr=[
                "abad_L_Joint",
                "abad_R_Joint",
            ],
            effort_limit=200.0,     # 강한 복원력에 대응할 수 있도록 토크 여유 확보
            velocity_limit=1.0,     # 사실상 움직임 제한
            stiffness=5000.0,       # 거의 rigid 수준의 강성 (움직임 억제)
            damping=100.0,          # 진동 억제
            friction=0.0,
        ),
        "wheels": ImplicitActuatorCfg(
            joint_names_expr=[
                "wheel_L_Joint",
                "wheel_R_Joint",
            ],
            effort_limit=80.0,
            velocity_limit=15.0,
            stiffness=0.0,
            damping=0.8,
            friction=0.0,
        ), # TODO: change to delayed implicit actuator
    },
)

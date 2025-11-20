import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

# 현재 파일 기준 USD 경로
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

    # 초기 상태
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.8 + 0.166),
        joint_pos={
            ".*_joint": 0.0,  # 모든 조인트 초기 각도
        },
        joint_vel={".*": 0.0},  # 모든 조인트 초기 속도
    ),

    soft_joint_pos_limit_factor=0.9,

    actuators={
        # 다리 관절
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[
                "Left_hip_yaw_joint",    # abad_L_Joint
                "Right_hip_yaw_joint",   # abad_R_Joint
                "Left_hip_pitch_joint",  # hip_L_Joint
                "Right_hip_pitch_joint", # hip_R_Joint
                "Left_knee_pitch_joint", # knee_L_Joint
                "Right_knee_pitch_joint" # knee_R_Joint
            ],
            effort_limit=80.0,
            velocity_limit=15.0,
            stiffness=42.0,
            damping=2.5,
            friction=0.0,
        ),

        # 바퀴 관절
        "wheels": ImplicitActuatorCfg(
            joint_names_expr=[
                "Left_wheel_pitch_joint",  # wheel_L_Joint
                "Right_wheel_pitch_joint", # wheel_R_Joint
            ],
            effort_limit=80.0,
            velocity_limit=15.0,
            stiffness=0.0,
            damping=0.8,
            friction=0.0,
        ),
    },
)

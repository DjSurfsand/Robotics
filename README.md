# Robotics - Cloud-Connected AI Agent Wrestling Robots

## Project Vision

Build autonomous wrestling robots (inspired by Japanese Robot Sumo) with cloud-based AI agent capabilities, similar to TARS AI robot.

## Architecture

**Edge-Cloud Hybrid Model:**
- **Cloud Brain (LLM)**: High-level planning, strategy generation, learning from all robots, natural language interface
- **Edge Computing (ESP32/RPi)**: Real-time sensor fusion, motor control loops, local RL policies, fast reflexes (<10ms)
- **Physical Robot**: Motors, sensors, actuators, encoders, IMU, IR sensors

## Project Structure

```
Robotics/
├── docs/                    # Documentation
│   ├── research-summary.md
│   ├── hardware-specs.md
│   └── architecture.md
├── simulation/              # Simulation environments
│   ├── gazebo/             # Gazebo + ROS 2 setups
│   └── isaac-sim/          # NVIDIA Isaac Sim configs
├── firmware/                # Robot firmware
│   ├── esp32/              # ESP32 embedded code
│   └── ros2/               # ROS 2 nodes
├── cloud/                   # Cloud infrastructure
│   ├── api/                # REST/WebSocket APIs
│   └── llm-agent/          # LLM-based agent logic
├── rl-training/             # Reinforcement learning
│   ├── environments/       # Gymnasium environments
│   └── policies/           # Trained policies
└── hardware/                # Hardware designs
    ├── chassis-designs/    # 3D models
    └── schematics/         # Circuit diagrams
```

## Hardware Stack

**Microcontrollers:** ESP32-S3 (WiFi + Bluetooth, dual-core, $5-10)

**Motors:** Brushed DC motors with encoders (N20 for budget, Maxon/Faulhaber for premium)

**Sensors:**
- IR Sensors (TCRT5000, QTR-8RC) - Opponent detection
- Ultrasonic (HC-SR04) - Distance measurement
- IMU (MPU6050) - Orientation/balance
- Current Sensors (ACS712) - Motor load detection

**Motor Drivers:** TB6612FNG (efficient) or BTS7960 (high current 43A)

**Power:** LiPo Battery 3S 2200mAh

## Software Stack

- **ROS 2** - Robot Operating System (industry standard)
- **Gazebo / NVIDIA Isaac Sim** - Simulation
- **Gymnasium + Stable Baselines3** - Reinforcement Learning
- **FastAPI + MQTT** - Cloud communication

## Project Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Build basic Mini Sumo robot (500g class)
- ESP32 + motor drivers + IR sensors
- Basic autonomous sumo behavior (search + attack)
- Test in physical arena

### Phase 2: Simulation (Weeks 5-8)
- Set up ROS 2 + Gazebo environment
- Create virtual sumo arena
- Train RL policies in simulation
- Sim-to-real transfer

### Phase 3: Cloud Brain (Weeks 9-12)
- Set up cloud server (Python + FastAPI)
- Integrate LLM for strategy
- MQTT/WebSocket communication
- Robot learns from cloud experiences

### Phase 4: Multi-Robot (Weeks 13+)
- Multiple robots sharing cloud brain
- Collaborative learning
- Tournament mode

## Budget Estimate (Per Robot)

| Component | Cost (USD) |
|-----------|------------|
| ESP32-S3 Development Board | $8-15 |
| 4x N20 DC Motors with Encoders | $20-40 |
| Motor Driver (TB6612FNG x2) | $8-12 |
| IR Sensors (TCRT5000 x8) | $5-10 |
| Ultrasonic Sensor (HC-SR04) | $2-5 |
| IMU (MPU6050) | $5-8 |
| LiPo Battery 3S 2200mAh | $15-25 |
| 3D Printed Chassis | $5-15 |
| Misc (wires, screws, PCB) | $15-25 |
| **TOTAL** | **$83-159** |

## Key References

- [TARS-AI Robot](https://github.com/TARS-AI-Community/TARS-AI) - Open-source LLM-powered robot
- [Awesome-LLM-Robotics](https://github.com/GT-RIPL/Awesome-LLM-Robotics) - Curated papers
- [ROS 2 Documentation](https://docs.ros.org/)
- [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac/sim)
- [Robot Sumo Wikipedia](https://en.wikipedia.org/wiki/Robot-sumo)

## Getting Started

```bash
# Clone the repository
git clone https://github.com/DjSurfsand/Robotics.git
cd Robotics

# Review the research summary
cat docs/research-summary.md

# Start with Phase 1: Basic Sumo Robot
cd firmware/esp32
```

## License

MIT License - Feel free to use for personal and commercial projects.

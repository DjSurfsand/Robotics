# Research Summary: Cloud-Connected AI Agent Wrestling Robots

## Project Vision

Build autonomous wrestling robots (inspired by Japanese Robot Sumo) with cloud-based AI agent capabilities, similar to TARS AI robot.

---

## 1. Inspiration: Japanese Robot Sumo

### Overview
- Competition where robots push each other out of a circular arena (dohyo)
- Created by FUJISOFT in 1989 to promote "Monozukuri" (art of making things)
- Global tournaments: All Japan Robot-Sumo Tournament, RoboCore (Brazil), RoboGames (USA)

### Robot Classes & Specifications

| Class | Weight | Dimensions | Key Features |
|-------|--------|------------|--------------|
| Mega Sumo | 3 kg | 20x20 cm | Magnets for >100kgf downforce |
| **Mini Sumo** | **500 g** | **10x10 cm** | **Most popular entry-level** |
| Micro Sumo | 100 g | 5x5x5 cm | High precision |
| Nano Sumo | 50 g | 2.5 cm cube | Extremely miniature |

**Recommendation: Start with Mini Sumo (500g class)** - Best balance of complexity, cost, and community support.

### Core Engineering Challenges

1. **Opponent Detection** - Infrared/ultrasonic sensors to find opponent
2. **Edge Detection** - Reflectance sensors (QTR-style) to avoid leaving ring
3. **Mechanical Advantage** - Wedge/blade design to lift opponent
4. **Tactics** - Search patterns (random/circular) + Attack routines

---

## 2. Inspiration: TARS AI Robot

### Project Overview
- **GitHub:** https://github.com/TARS-AI-Community/TARS-AI
- **Inspired by:** TARS from Interstellar movie
- **Cost:** $500-$1,000
- **License:** CC-BY-NC 4.0 (non-commercial)

### Key Features to Copy
- ✅ Modular design
- ✅ LLM-powered personality/interaction
- ✅ Reinforcement Learning for movement
- ✅ Community-driven development

---

## 3. Hardware Stack

### Microcontrollers

| Option | Description | Cost |
|--------|-------------|------|
| **ESP32-S3** | WiFi + Bluetooth, dual-core, low power | $5-10 |
| Arduino Nano | Classic, simple, good for beginners | $4-8 |
| Raspberry Pi 4 | Full Linux, cloud connectivity | $35-75 |
| Jetson Nano | AI inference at edge | $100 |

**Recommendation:** ESP32-S3 for core control + Raspberry Pi 4 for cloud edge computing.

### Motors
- **Brushed DC motors with encoders** - For speed control (N20 for budget)
- **Brushless motors** - Higher performance, need ESC
- **Continuous rotation servos** - 360° servos for simpler control
- **Premium brands:** Maxon, Faulhaber

### Sensors

| Sensor | Purpose | Example |
|--------|---------|---------|
| IR Sensors | Opponent detection | TCRT5000, QTR-8RC |
| Ultrasonic | Distance measurement | HC-SR04 |
| IMU | Orientation/balance | MPU6050 |
| Current Sensors | Motor load detection | ACS712 |
| LiPo Battery | High-discharge power | 2000-5000mAh |

### Motor Drivers
- **L298N** - Cheap, basic
- **TB6612FNG** - Better efficiency (recommended)
- **BTS7960** - High current (43A)

---

## 4. Software Stack

### Robot Operating System

**ROS 2 (Robot Operating System 2)**
- Industry standard middleware for robotics
- Topics, services, actions for robot communication
- Navigation2 (Nav2) - most deployed AMR navigation solution
- Works with Python & C++
- Official: https://docs.ros.org/

### Simulation Frameworks

| Framework | Description |
|-----------|-------------|
| **NVIDIA Isaac Sim** | Physically-based, GPU-accelerated, ROS 2 integration |
| **Gazebo + ROS 2** | Open-source, widely used, ros_gazebo_gym for RL |
| **Webots** | Commercial with free version, good ROS 2 integration |
| **ManiSkill3** | GPU-parallelized, optimized for manipulation |

### Reinforcement Learning

| Framework | Description |
|-----------|-------------|
| **Gymnasium** | OpenAI Gym successor, standard RL interface |
| **Stable Baselines3** | PPO, A2C, DQN implementations |
| **Ray RLlib** | Scalable, distributed training |

**Key Integration:** ros_gazebo_gym - ROS + Gazebo + Gymnasium integration

---

## 5. LLM-Powered Robotics (AI Agent Brains)

### Key Research Areas (from Awesome-LLM-Robotics)

#### A) Reasoning & Spatial Understanding
- **RoboTracer (Dec 2025):** Mastering spatial traces with reasoning in VLMs
- **RoboSpatial (June 2025):** Teaching 2D/3D spatial understanding
- **RT-2 (July 2023):** Vision-Language-Action models

#### B) Planning & Task Orchestration
- **SayCan (2021):** Grounding language in robotic affordances
- **Code as Policies (2022):** LLMs generate Python code for robot control
- **FLARE (Mar 2025):** Multi-modal grounded planning

#### C) Manipulation & Skills
- **VIMA (2022):** General robot manipulation with multimodal prompts
- **VoxPoser (2023):** Composable 3D value maps for manipulation

### Recommended Approach
1. Use LLM for high-level decision making (cloud-based)
2. Use RL for low-level motor control (edge-based)
3. Hybrid architecture: Cloud brain + Edge reflexes

---

## 6. Cloud-Robotics Architecture

### Edge-Cloud Hybrid Model

```
                    ┌──────────────────────────────────────┐
                    │         CLOUD BRAIN (LLM)            │
                    │  - High-level planning               │
                    │  - Strategy generation               │
                    │  - Learning from all robots          │
                    │  - Natural language interface        │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────┐
                    │      EDGE COMPUTING (ESP32/RPi)      │
                    │  - Real-time sensor fusion           │
                    │  - Motor control loops               │
                    │  - Local RL policies                 │
                    │  - Fast reflexes (<10ms)             │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────┐
                    │       PHYSICAL ROBOT                 │
                    │  - Motors, sensors, actuators        │
                    │  - Encoders, IMU, IR sensors         │
                    └──────────────────────────────────────┘
```

### Communication Protocols
- **MQTT:** Lightweight pub/sub for cloud-edge comms
- **WebSockets:** Real-time bidirectional communication
- **gRPC:** Efficient RPC for structured data
- **HTTP REST:** Simple API calls for configuration

---

## 7. Project Roadmap

### Phase 1: Foundation (Weeks 1-4)
- ✅ Build basic Mini Sumo robot (500g class)
- ✅ ESP32 + motor drivers + IR sensors
- ✅ Basic autonomous sumo behavior (search + attack)
- ✅ Test in physical arena

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

---

## 8. Key GitHub Repositories

### Core Frameworks
- https://github.com/ros2/navigation (Nav2)
- https://github.com/osrf/gazebo (Simulation)
- https://github.com/gymnasium/gymnasium (RL environments)

### LLM + Robotics
- https://github.com/GT-RIPL/Awesome-LLM-Robotics (Curated papers)
- https://github.com/TARS-AI-Community/TARS-AI (TARS robot)
- https://github.com/mjyc/awesome-robotics-projects (General robotics)

### Simulation + RL
- https://github.com/jackvice/RoboTerrain (Off-road RL)
- https://github.com/DLR-RM/stable-baselines3 (RL algorithms)

---

## 9. Budget Estimate (Per Robot)

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

### Optional Upgrades
- Raspberry Pi 4 (cloud edge): +$35-75
- Jetson Nano (AI at edge): +$100
- Brushless motors + ESC: +$50-100
- Custom PCB design: +$20-50

---

## 10. Next Steps

1. ✅ Research complete
2. ✅ Repo created: DjSurfsand/Robotics
3. ✅ Repo cloned locally
4. ✅ Initial file structure created
5. → **Next: Start Phase 1 - Design basic sumo robot hardware**

---

*Generated: March 29, 2026*
*Research sources: TARS-AI, Robot Sumo Wikipedia, Awesome-LLM-Robotics, ROS 2 docs, NVIDIA Isaac Sim*

# Robot Arm Simulator

**Personal project demonstrating inverse kinematics and basic robotics principles.**

This application simulates a 2-joint planar robotic arm that reaches a target point selected by the user. The system computes joint angles using inverse kinematics and smoothly interpolates the movement toward the desired position.

## Mathematical Model

The solution is derived using the **law of cosines** for a 2-segment arm:
- Upper arm length L₁ = 8 cm  
- Forearm length L₂ = 10 cm  

The distance to the target point (x, y) is:
r = √(x² + y²)

Joint angles are calculated as:
- θ₂ = arccos((r² - L₁² - L₂²) / (2L₁L₂))
- θ₁ = atan2(y, x) - atan2(L₂ sin θ₂, L₁ + L₂ cos θ₂)

A target is considered unreachable when:
r > L₁ + L₂ or r < |L₁ - L₂|

![Derivation](math_notes.pdf)

## Controls
- **Mouse click**: Select a target point  
- **Red flash**: Target outside reachable zone  

## Features
- Real-time inverse kinematics computation
- Smooth adaptive interpolation for natural motion
- Visual feedback for unreachable positions
- Simple 3D-style rendering for depth perception

## Purpose
This project was created to demonstrate my understanding of:
- Trigonometry and geometric modeling  
- Inverse kinematics principles  
- Real-time graphical simulation using Python and Pygame

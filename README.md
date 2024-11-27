# IoT Pong Game

This project brings the classic Pong game to life by using a gyro sensor (MPU6050) to control the paddles instead of a keyboard or controller. The game features cooperative multiplayer, and a buzzer sound effect is triggered when the ball hits the paddle.

## Features
- **Gyro Sensor Control:** Use the MPU6050 gyro sensor to control the paddles in the Pong game.
- **Co-op Multiplayer:** Play with a partner in a cooperative mode.
- **Buzzer Sound Effect:** Hear a beep sound from the buzzer when the ball hits the paddle.

## Technologies Used
- **Python:** Programming language used for game logic and sensor integration.
- **MPU6050:** Gyroscope sensor for controlling paddle movements.
- **Raspberry Pi 400:** Hardware platform for running the game and connecting the components.
- **Buzzer:** Provides sound feedback when the ball hits the paddle.

## Getting Started
1. Set up your Raspberry Pi 400 and connect the MPU6050 sensor and buzzer.
2. Clone the repository.
3. Install necessary Python libraries:
   ```bash
   pip install mpu6050-python
   ```
4. Run the game:
   ```bash
   python pong_game.py
   ```

## Contributing
Feel free to fork the repository, raise issues, or submit pull requests to improve the game!

# Pong Game

A classic Pong game implementation using Python and Pygame.

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Configuration](#configuration)
-   [Development](#development)
    -   [File Structure](#file-structure)
    -   [Dependencies](#dependencies)
    -   [Testing](#testing)
-   [Contributing](#contributing)

## Overview

Pong is a classic arcade game where two players control paddles and try to hit a ball back and forth. This implementation of the Pong game uses Python and the Pygame library to create a responsive and engaging game experience.

The game features two players, each controlling a vertical paddle using a motion sensor (MPU6050). The objective is to keep the ball in play by hitting it back to the opposing player's side. The game keeps track of the scores, and the first player to reach 3 points wins.

## Features

-   **Two-Player Gameplay**: Two players can compete against each other, using motion sensors to control their paddles.
-   **Responsive Controls**: The paddles move vertically based on the players' motion sensor input, providing a natural and intuitive control scheme.
-   **Dynamic Ball Behavior**: The ball's speed and trajectory are affected by where it hits the paddle, adding an element of strategy to the game.
-   **Visual Feedback**: The game provides clear visual cues, including a countdown timer, score displays, and a victory message when a player wins.
-   **Audio Feedback**: The game plays a buzzer sound when the ball hits a paddle, enhancing the overall game experience.

## Installation

To run the Pong game, you'll need to have the following dependencies installed:

-   Python 3.x
-   Pygame
-   RPi.GPIO (for Raspberry Pi users)
-   mpu6050-raspberrypi (for Raspberry Pi users)

You can install the Python dependencies using pip:

pip install pygame RPi.GPIO mpu6050-raspberrypi

## Usage

1. Clone the repository:
   git clone https://github.com/your-username/pong.git

2. Run the game:
   cd pong
   python main.py

This will start the Pong game. The two players can control their paddles using their motion sensors (MPU6050 sensors).

## Configuration

The game's configuration settings are located in the game_manager.py file. You can adjust the following parameters:

-   WIDTH and HEIGHT: The dimensions of the game window.
-   BUZZER_PIN: The GPIO pin number connected to the buzzer.
-   mpu6050_1_address and mpu6050_2_address: The I2C addresses of the MPU6050 sensors.
-   Font sizes and colors.

## Development

### File Structure

The Pong game application is structured as follows:

pong/
├── [main.py](http://_vscodecontentref_/0)
├── src/
│ ├── [game_manager.py](http://_vscodecontentref_/1)
│ ├── [game_state.py](http://_vscodecontentref_/2)
│ ├── [renderer.py](http://_vscodecontentref_/3)
│ ├── [striker.py](http://_vscodecontentref_/4)
│ └── [ball.py](http://_vscodecontentref_/5)
└── test*hardware/
├── test_1_mpu.py
├── [test_both_mpu.py](http://\_vscodecontentref*/6)
└── [test_buzzer.py](http://_vscodecontentref*/7)

-   main.py: The entry point of the application, which creates and runs the GameManager.
-   src/game_manager.py: Contains the GameManager class, which handles the main game loop, event handling, and game state updates.
-   src/game_state.py: Contains the GameState class, which manages the game state, including scores, timers, and game over conditions.
-   src/renderer.py: Contains the Renderer class, which is responsible for rendering the game objects and displaying the game state.
-   src/striker.py: Contains the Striker class, which represents a player's paddle.
-   src/ball.py: Contains the Ball class, which represents the game ball.

### Dependencies

The Pong game application uses the following dependencies:

-   Pygame: A set of Python modules designed for writing video games.
-   RPi.GPIO: A Python module to control the GPIO (General-Purpose Input/Output) pins on a Raspberry Pi.
-   mpu6050-raspberrypi: A Python library for interacting with the MPU6050 motion sensor on a Raspberry Pi.

### Testing

The current implementation does not include any unit tests or integration tests. Adding a testing framework and writing tests for the game logic and game objects would be an important next step in the development process.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure the code passes any existing tests.
4. Add new tests if necessary.
5. Submit a pull request with a detailed description of your changes.

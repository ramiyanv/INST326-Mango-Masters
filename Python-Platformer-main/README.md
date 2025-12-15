# Mango Masters

A simple 2D platformer game built with Python and Pygame where players navigate through the course to collect mangoes while avoiding fire traps. 

## Description

Mango Masters is a classic platformer with collectible items, animated traps, and physics-based movement.The player navigates platforms, collects mangoes for points, and avoids fire traps.

## Features

- Character movement with running and jumping animations
- Double jump mechanic
- Side-scrolling camera system
- Collectible mangoes that increase score
- Animated fire hazards
- Collision detection

## Requirements

- Python 3.13+
- Pygame 

## Project Structure

```
mango-masters/
├── main.py                 # Main game file
└── assets/                 # Game assets directory
    ├── Background/
    │   └── Blue.png       # Background image
    ├── MainCharacters/
    │   └── MaskDude/      # Player sprite sheets
    │       ├── idle.png
    │       ├── run.png
    │       ├── jump.png
    │       ├── double_jump.png
    │       ├── fall.png
    │       └── hit.png
    ├── Terrain/
    │   └── Terrain.png    # Platform tiles
    ├── Traps/
    │   └── Fire/          # Fire trap animations
    │       ├── on.png
    │       └── off.png
    └── Items/
        └── Fruits/
            └── mango.png  # Collectible sprite
```

## File Descriptions

**main.py** - Contains all game logic and classes:
- `Player` class: Handles player movement, animations, physics, and score tracking
- `Block` class: Creates platform terrain
- `Fire` class: Animated trap that kills the player on contact
- `Mango` class: Collectible items that increases score
- `start_screen()`: Displays welcome screen
- `main()`: Initializes game objects and runs game loop
- 

**assets/** - Contains all game sprites and images organized by type

## Installation

1. Install Pygame:
```bash
pip install pygame
```

2. Verify the assets folder structure matches the structure above

## Running the Program

Navigate to project directory and run:
```bash
python main.py
```


Expected behavior:
1. Game window opens 
2. Start screen displays "Welcome to Mango Masters!"
3. Press SPACE to begin

## Controls

- `LEFT ARROW` - Move left
- `RIGHT ARROW` - Move right
- `SPACE` - Jump (press twice for double jump)
- Close window to quit

https://youtu.be/GJxPGzO37-A

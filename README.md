# Labyrinth of Wunn

## Setup
1. Install requirements: ```pip install -r requirements.txt```
2. Create an account and setup API key here: https://console.groq.com/keys
3. Create a file named `secrets.yaml`
4. In `secrets.yaml`, write:
   ```
   groq:
     api_key: {YOUR_API_KEY}
   ```

## Run
1. Change to root directory (labyrinth-of-wunn)
2. Run `main.py`

## Controls
- WASD or arrow keys: Movement
- Space: Interact
- Enter: Enter response
- X: Attack
- Mouse wheel: Zoom
### Admin mode
- G: Toggle admin mode
- T: Teleport to NPC (cycles through each one)
- F: Spawn NPC
- K: Remove all NPCs
- H: Toggle hitboxes
- R: Toggle cross-NPC interaction (useful for testing without sending API requests)

## Demos
![Player dialogue](https://github.com/Magikarp4000/labyrinth-of-wunn/blob/main/demos/player_dialogue.png)
![NPC dialogue](https://github.com/Magikarp4000/labyrinth-of-wunn/blob/main/demos/npc_dialogue.png)

### Video Demos
- https://github.com/user-attachments/assets/1f97cf41-dc68-4c16-8379-771d1151a824
- https://github.com/user-attachments/assets/e1b6bc58-edfe-43b0-8486-521355933122

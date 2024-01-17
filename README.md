# Hand Gesture virtual mouse and  Painter

This is a simple hand gesture detector made with mediapipe. There are 2 applications. First is a hand detecting app that allows you to draw on the screen using your hand gestures. The project uses the OpenCV library for computer vision and the Mediapipe library for hand tracking. Second app is made similar, just tracking your finger, makes the mouse move as your finger.


- `mouse.py`: Allows controlling the mouse using hand gestures.
- `painter.p`: Implements a simple painting application using hand movements.
- 
## Features for mouse
Moving the coursor: Use your index finger to move them curose around.
Click Mode: Use the 2 finger (peace sign) gesture to select click (putting the other finger up makes it click) 
 
## Features for painter
Drawing Mode: Use your index finger to draw on the screen.
Selection Mode: Use the 2 finger (peace sign) gesture to select different colors and tools.

Create V env 

```
python -m venv myenv
source myenv/bin/activate
# On Windows, use `myenv\Scripts\activate
```

Install libs
```
pip install opencv-python
pip install mediapipe
pip install pyautogui
```

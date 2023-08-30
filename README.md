# a-star-visualiser
[https://www.youtube.com/watch?v=JtiK0DOeI4A](https://www.youtube.com/watch?v=JtiK0DOeI4A) <br>

### how to use
- space to start
- right click to draw
- left click to remove
- backspace to clear
- enter to load image

<br><hr>

### notes on drawing mazes
the program can only detect black pixels, and may be innacurate if the black lines are too thin <br>
if you would like to use your own maze:
- draw with thick black lines (like in the image provided) on an 800px square canvas
- place image in the 'Image' folder

The program will select the first image in the folder, make sure the one you want is the only one in there
<br><br>
To improve accuracy, increase 'rows' value (a_star.py, inside main function, ~ line 240)


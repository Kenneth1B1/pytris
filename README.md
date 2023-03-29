# pytris
Tetris Clone Built in Python

Currently, this is functioning at a playable level, however there are still several bugs that need to be fixed.

1. Shapes falling from the sky can move sideways into already placed pieces, as there is no check for that.
2. Certain shapes, due to the nature of the matrix that holds them, can be unable to go against the wall.

Otherwise, the game is 'playable'.

Future Updates:

1. Fixing the above bugs.
2. Implementing a ML model that will learn to play.
   Currently I am looking at Q-Learning techniques as a potential way to train a model.

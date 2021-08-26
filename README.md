# Tetris_AI
A simple tetris AI written in Python. More specific info is available on the [wiki](https://github.com/pebblS/Tetris_AI/wiki).

## Installation
Follow the [guide](https://github.com/pebblS/Tetris_AI/wiki/Installation).

## Dependencies
`Pygame v2.0.0`

`Python 3.7`



## Usage
### `python3 evolution.py` - run the genetic algorithm. Saves output of each generation in a file.

`-b` add a custom brain that's used as the starting point for the algorithm. Write the 9 weights of the network like this: `x,x,x,x,x,x,x,x,x`.
  
`-s` change the number of agents per generation. Default value is 10.
  
`-c` change the number of generations the program will simulate. Default is 4.

Example: `python3 evolution.py -b 1,1,-1.4,1,12,1,0.7,1,1 -s 20 -c 15`

### `python3 main.py` - run the game in manual mode.



## Manual controls
`Esc` - quit game. Works in AI mode as well

`Left arrow` - move falling piece left

`Right arrow` - move falling piece right

`Up arrow` - rotate falling piece

`Down arrow` - make the falling piece drop faster

`Space` - drop the falling piece all the way down


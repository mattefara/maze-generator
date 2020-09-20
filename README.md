# maze-generator
A simple maze generator CLI in python 3.8.5.

# Usage
All the following commands are on test.py

## Generate and save a 10 x 10 random maze 
```bash
python cli.py images/random_maze_0.png
```
![random_maze](/images/random_maze_0.png)
```bash
python cli.py images/random_maze_2.png -g
```
![random_maze](/images/random_maze_2.png)

## Generate and save a 15 x 15 or 200 x 200 random maze
```bash
python cli.py images/random_maze_1.png -g 15 15
```
![random_maze](/images/random_maze_1.png)
```bash
python cli.py images/random_maze_3.png -g 200 200
```
![random_maze](/images/random_maze_3.png)

## Generate, solve and save a 10 x 10 random maze 
```bash
python cli.py images/random_maze_4.png -g 10 10 -s images/solved_random_maze_4.png
```
![random_maze](/images/random_maze_4.png)
![random_maze](/images/solved_random_maze_4.png)

## Generate, solve and save (with a generated name) a 10 x 10 random maze 
```bash
python cli.py images/random_maze_5.png -g 10 10 -s
```
![random_maze](/images/random_maze_5.png)
![random_maze](/images/solved_random_maze_5.png)

## Load a maze from an image
Basically it does nothing special.
```bash
python cli.py images/random_maze_0.png -l
```

## Load a maze from an image, solve it and save it
```bash
python cli.py images/random_maze_1.png -l -s images/result_random_maze_1.png
```

![random_maze](/images/random_maze_1.png)
![random_maze](/images/result_random_maze_1.png)
## Load a maze from an image, solve it and save it with a generated name
```bash
python cli.py images/random_maze_2.png -l -s 
```

![random_maze](/images/random_maze_2.png)
![random_maze](/images/solved_random_maze_2.png)
# The Abstraction and Reasoning Corpus (ARC)

This repository contains the ARC task data, as well as a browser-based interface for humans to try their hand at solving the tasks manually.

*"ARC can be seen as a general artificial intelligence benchmark, as a program synthesis benchmark, or as a psychometric intelligence test. It is targeted at both humans and artificially intelligent systems that aim at emulating a human-like form of general fluid intelligence."*

A complete description of the dataset, its goals, and its underlying logic, can be found in: [The Measure of Intelligence](https://arxiv.org/abs/1911.01547).

As a reminder, a test-taker is said to solve a task when, upon seeing the task for the first time, they are able to produce the correct output grid for *all* test inputs in the task (this includes picking the dimensions of the output grid). For each test input, the test-taker is allowed 3 trials (this holds for all test-takers, either humans or AI).


## Task file format

The `data` directory contains two subdirectories:

- `data/training`: contains the task files for training (400 tasks). Use these to prototype your algorithm or to train your algorithm to acquire ARC-relevant cognitive priors.
- `data/evaluation`: contains the task files for evaluation (400 tasks). Use these to evaluate your final algorithm. To ensure fair evaluation results, do not leak information from the evaluation set into your algorithm (e.g. by looking at the evaluation tasks yourself during development, or by repeatedly modifying an algorithm while using its evaluation score as feedback).

The tasks are stored in JSON format. Each task JSON file contains a dictionary with two fields:

- `"train"`: demonstration input/output pairs. It is a list of "pairs" (typically 3 pairs).
- `"test"`: test input/output pairs. It is a list of "pairs" (typically 1 pair).

A "pair" is a dictionary with two fields:

- `"input"`: the input "grid" for the pair.
- `"output"`: the output "grid" for the pair.

A "grid" is a rectangular matrix (list of lists) of integers between 0 and 9 (inclusive). The smallest possible grid size is 1x1 and the largest is 30x30.

When looking at a task, a test-taker has access to inputs & outputs of the demonstration pairs, plus the input(s) of the test pair(s). The goal is to construct the output grid(s) corresponding to the test input grid(s), using 3 trials for each test input. "Constructing the output grid" involves picking the height and width of the output grid, then filling each cell in the grid with a symbol (integer between 0 and 9, which are visualized as colors). Only *exact* solutions (all cells match the expected answer) can be said to be correct.


## Usage of the testing interface

The testing interface is located at `apps/testing_interface.html`. Open it in a web browser (Chrome recommended). It will prompt you to select a task JSON file.

After loading a task, you will enter the test space, which looks like this:

![test space](https://arc-benchmark.s3.amazonaws.com/figs/arc_test_space.png)

On the left, you will see the input/output pairs demonstrating the nature of the task. In the middle, you will see the current test input grid. On the right, you will see the controls you can use to construct the corresponding output grid.

You have access to the following tools:

### Grid controls

- Resize: input a grid size (e.g. "10x20" or "4x4") and click "Resize". This preserves existing grid content (in the top left corner).
- Copy from input: copy the input grid to the output grid. This is useful for tasks where the output consists of some modification of the input.
- Reset grid: fill the grid with 0s.

### Symbol controls

- Edit: select a color (symbol) from the color picking bar, then click on a cell to set its color.
- Select: click and drag on either the output grid or the input grid to select cells.
    - After selecting cells on the output grid, you can select a color from the color picking to set the color of the selected cells. This is useful to draw solid rectangles or lines.
    - After selecting cells on either the input grid or the output grid, you can press C to copy their content. After copying, you can select a cell on the output grid and press "V" to paste the copied content. You should select the cell in the top left corner of the zone you want to paste into.
- Floodfill: click on a cell from the output grid to color all connected cells to the selected color. "Connected cells" are contiguous cells with the same color.

### Answer validation

When your output grid is ready, click the green "Submit!" button to check your answer. We do not enforce the 3-trials rule.

After you've obtained the correct answer for the current test input grid, you can switch to the next test input grid for the task using the "Next test input" button (if there is any available; most tasks only have one test input).

When you're done with a task, use the "load task" button to open a new task.

## Manually Solved Problems

Humans, given time and patience, can solve any of these 400 tasks without difficulty even if no instructions are given to them. This shows their intelligence and if we were to measure the same for machines, where would they stand? Right now, little too far behind. Here, we attempt to solve some of the challenges manually and also attempt to solve the ARC using machine learning. Since most of the current known solutions are data-hungry, the results are not all positive.

Some of the 400 available problems picked randomly and solved manually based on the patterns noticed and is available `src/manual_solve.py` file in this repo. The details of the tasks are as follows.

- 83302e8f
- c8cbb738
- 2dd70a9a
- ded97339
- ae3edfdc
- 
### The Problem Description:
This tries to explain the pattern as interpreted by the programmer and further showcase how humans are able to identify patterns and connect problems to previously known information.
#### 83302e8f

##### Difficulty: high

There is a square grid, lets call it Grid A, (can be of any size) partitioned into smaller equally sized square grids, let that be Grid B (equally spaced in one task but not constant across each task). These squares are surrounded by a single square boundaries of a constant colour on all sides excepts the edges of the Grid A. These boundaries are broken at several points in such a way that some of the Grid Bs are completely surrounded by the boundaries and some have broken edges. The task is to colour the Grids Bs which are completely surrounded by boundaries in green and the others in yellow. The broken boundaries are also filled with yellow.

![image](https://user-images.githubusercontent.com/74540513/143771351-3d6a3cdc-bfb9-48d8-b55f-5d2564912c16.png)

Correctness of the solution: All test cases are passed

#### c8cbb738

##### Difficulty: high

We have a space with a background colour and several squares of different colours arranged in various patterns. The patterns can either be a square, cross or rectangle. All of them will have to be arranged into a square in such a way that all their centers are alligned. The rectangles can be of different alignment; length greater than breadth or breadth greater than length. The task on further observation can be thought of as a centre allignment problem
    

![image](https://user-images.githubusercontent.com/74540513/143841385-ee34c01a-e222-4576-8f4c-56ea9a65c84b.png)

Correctness of the solution: All test cases are passed


#### f35d900a
##### Difficulty: High

Expand and connect. The input grid is a rectangular (list of lists) matrix with variable shape, with numbers ranging from 0 to 9. (inclusive). Different colors of the color spectrum are represented by the integers. The task is to identify the different colours and their respective positions in the input grid, create a sqaure matrix around each coloured element such that the colour of the sqaure matrix should be of the colour of the element present in its sequential position. Then create a horizontal and
vertical connection amongst all the square matrices, the connection is a step by step increment from middle element of each square matrix towards each other at the same time.

![image](https://user-images.githubusercontent.com/74540513/143908496-61d70002-1070-468e-9f2f-7bd39f5d4d3d.png)


Correctness of the solution: All test cases are passed


### ded97339

##### Difficulty: medium-high


Stars in the night sky! A grid of black squares represents the sky and the tiny blue squares, the stars. The task is to find the constellations hidden in the sky and connect them. How do we do this? We need to identify the ones that belong and a constellation and ones that do not. On observation, we can see that there is a simple common rule. All stars belonging to a constellation are on the same row or column.
All the other stars are loners. 

![image](https://user-images.githubusercontent.com/74540513/143848307-14741ef1-5745-458e-bc5d-82ccc3947b71.png)


Correctness of the solution: All constellations are identified and marked


#### ae3edfdc

##### Difficulty: medium

 Gravity- well, not the regular kind. There are two centres of gravity, blue and red - which has the ability to bring orange and green squares in it's path towards itself, so that it occupies the closest postition wrt to it. The one condition; the attracted squares must be perpendicular to the centre of gravity to get attracted to it.
 
 ![image](https://user-images.githubusercontent.com/74540513/143843654-6230a8ec-908f-4330-b0be-13c1331d9765.png)

Correctness of the solution: All test cases are passed

#### feca6190

##### Difficulty: medium

The input grid is a rectangular (list of lists) matrix with variable shape, with numbers rangingfrom 0 to 9. (inclusive). Different colors of the color spectrum are represented by the integers. The task is to determine the color schemes in the input grid, generate a matrix whose shape is given bymultiplication of size of input matrix and the number of colors present inside the grid.Next step is to fill the formed matrix diagonally with color from the input grid, starting with the index value of the
color in the input grid.

![image](https://user-images.githubusercontent.com/74540513/143889936-4816338f-7f25-4fdd-a5ca-44935e469b1c.png)

Correctness of the solution: All test cases are passed

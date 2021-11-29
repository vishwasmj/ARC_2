#!/usr/bin/python

import os, sys
import json
import numpy as np
import re
from collections import Counter
import itertools
import collections
### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

#---------------------------------------------------solve_83302e8f start-----------------------------------------

def solve_83302e8f(x):
    """
    Difficulty: High
    
    The Problem: There is a square grid containing squares. With in these squares there are smaller 
    equally sized squares. These squares are surrounded by a single square boundaries of various colours
    The task is to colour the squares which are completely surrounded by boundaries in green and the 
    others in yellow.
    
    Assumptions: The Grid is always square. The smaller ones are also squares.
    
    The Approach: Identify the size of the grid
                  Identify the size of the inner square
                  Identify the boundary colour
                  Then for each inner square along with boundary, check if the number of black coloured or
                  non-yellow coloured squares are equal to (size of the inner square)^2.
                  If so, we colour it green, else yellow.
    Note: All test cases passed
    
    Arguments: x, the nd array representing the square grid
    return: x, the resultant array with the transformations applied.
    
    """
    X_1 = x.copy()  # just duplicating x
    grid_len, grid_width = X_1.shape  # Getting the grid size
    #make sure its a square
    assert grid_len == grid_width, "Grid not square, can't proceed any further"
    #look for the size of the square inside
    inner_sq_found = -1
    #length of the square is found by traversing diagonally until a non-black square is encountered
    #Here, it is observed that the pattern never has a missing corner. This logic will fail in case, this is not true
    i=j=0
    while (inner_sq_found == -1 and i < grid_len):
        if X_1[i][j]==0:
            i=j=i+1
        else:
            size_square=i
            bound_colour=X_1[i][j]
            inner_sq_found=0
    assert inner_sq_found != -1, "Pattern not square, can't proceed any further"
    # checking each sub grid square to see if there is more than size_square*2 black squares in the grid
    #+1 is added to include the boundaries as well when you consider square size.
    for i in range(0,grid_len,size_square+1):
        for j in range(0,grid_len,size_square+1):
            X_1=colour_row(X_1,i,j,size_square,grid_len,bound_colour)
    x=X_1
    return x


def colour_row(x,r_i,r_j,size_square,grid_len,bound_colour):
    """
    This function takes in the below arguments and takes each subset of the grid at a time including the
    boundaries in all directions. It then evaluates how many black squares are present and if there are any
    yellow filled squares in the boundary indicating a break in the square. If the number of squares are
    as expected, then colours it green else yellow
    
    Arguments:
        x : The grid modified so far
        r_i : starting point of the row
        r_j : starting point of the column
        size_square : The size of the smaller square to be coloured
        grid_len : total Grid length
        bound_colour : Boundary colour
    Return: x, the modified array
    """
    #counting black squares in a subset. initialize to 0
    count_black=0
    #expected square count for a fully filled case.
    count_square=size_square*size_square
    #to hold all the black within the range
    dict_black={}
    #
    yellow_filled=0
    #variables set to control the range
    #the last column and row  will have no boundary on the right or botton respectively
    #so handling the boundary conditions
    if r_i+size_square+1<grid_len:
        r_i_x=r_i+size_square+1
        #to include the already considered boundary for the next square
        if r_i !=0:
            r_i =r_i-1
    #if last row, then change it to length of the grid
    else:
        r_i_x=grid_len
        #to include the already considered boundary for the next square
        r_i=r_i-1
    if r_j+size_square<grid_len:
        r_j_x=r_j+size_square+1
        if r_j !=0:
            r_j =r_j-1
    else:
        r_j_x=grid_len
        r_j=r_j-1
    #consider each subgrid of rows and columns, including all the boundaries
    for i in range(r_i,r_i_x):
        for j in range(r_j,r_j_x):
            #if black, count it
            if x[i][j]==0:
                count_black=count_black+1
                #so that we can change the colour of it later
                if x[i][j] in dict_black:
                    dict_black[x[i][j]].append((i,j))
                else:
                    dict_black[x[i][j]] = [(i,j)]
            # if there is any non black non-background(boundary) colour, then it's part of the broken square
            #hence, filled yellow
            elif x[i][j]!=bound_colour:
                yellow_filled=1
    #if there are exactly length of square*2 squares and no boundary is filled already, then
    #it's a perfect square and is hence coloured green
    if count_black==count_square and yellow_filled==0:
        for i,j in dict_black[0]:
            x[i][j]=3
    #else it is coloured yellow
    else:
        for i,j in dict_black[0]:
            x[i][j]=4 
    return x

#---------------------------------------------------solve_83302e8f end-----------------------------------------
#---------------------------------------------------solve_c8cbb738 start---------------------------------------
def solve_c8cbb738(x):
    """
    Difficulty: High
    The problem: We have a space with a background colour and several squares of different colours arranged in 
    various patterns. The patterns can either be a square, cross or rectangle. All of them will have to be arranged 
    into a square in such a way that all their centers are alligned.
    Note:Rectangle 2 is longer in the vertical direction and rectangle 1 is longer in the horizontal direction
    
    Assumptions: Only the three shapes and the rectangle shape in two different forms will be present in the 
    input pattern.
    
    Testing:All test cases passed
    
    Approach:Step 1: Identify the background colour.
             Step 2: Create a dictionary with non background colours and their positions
             Step 3:Using this Dictionary, identify the shapes and their size
             Step 4:Create a new Matrix based on the shape, and position the various shapes in it.
    
    Argument: x, the n-d array representing the space
    return: x, after the above transformation is done.
    
    """
    #Step 1: Find the background colour or the most common colour
    list=x.tolist()
    #looks for a row that contains only one value and assigns that as the background value.
    #This is used to avaoid ambiguity in case too many shapes are present and we can't tell the backgroung colour 
    #by any one row.
    for i in range(len(list)):
        #checks if the row has only one colour present
        if(len(Counter(list[i]).most_common())==1):
            #if only one colour, that is assumed to be the background colour and
            c=Counter(list[i]).most_common()
            #assigned values
            background_colour=c[0][0]
            #once background values is found, no further iteration required.
            break
    #Step 2: find other colours and their shapes
    
    a_dict={}
    # find the location of all the non-background colour values and add them to a dictionary
    #with it's position and colour
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] !=background_colour:
                if list[i][j] in a_dict:
                  a_dict[list[i][j]].append((i,j))
                else:
                  a_dict[list[i][j]] = [(i,j)]
    # Step3: create new square using this dictionary value.
    square= get_outputMatrix(a_dict,background_colour)
    #changing the float values to int
    x=square.astype(int)

    return x
def get_outputMatrix(a_dict,background_colour):
    """
    The major task here is to find the shapes of each of the items with different colours.
    We assume that it can be any one of the three shapes:- square,cross and rectangle(two variations)
    First differenciate the squares and rectangles from the cross by checking for 2 values present on the
    same row and same column. Then we check the length and breadth to tell apart the sqaure and rectangles.
    Once we seperate everything, we plot it.
    
    Arguments: a_dict-The dictionary with all the positions different shapes by their colour as key
                background_colour- background colour of the initial matrix
    Return:The new matrix with the centres alligned
    """
    # initially we take that none of the shapes are present.
    square_colour=0
    rect_1_col=0
    rect_2_col=0
    cross_col=0
    #num of shapes present in the fig
    size_dict=len(a_dict.keys())
    
    for key in a_dict:
        # all the points for a particular shape
        list1=a_dict[key]
        row1=0
        col1=0
        #-1 as we're accessing elements using i+1
        for i in range(len(list1)-1):
            #checking for squares on the same row
            if (list1[i][0]==list1[i+1][0]):
                row1=row1+1
            #checking for squares on the same column
            #comparing 1st and 3rd and 2nd and 4th elements
            if(i==0 or i==1):
                if (list1[i][1]==list1[i+2][1]):
                    col1=col1+1
        #two pair of items on the same row and along the same column
        if (row1==col1) and (col1==2):
        #finding length and breadth
            length=list1[1][1]-list1[0][1]
            breadth=list1[2][0]-list1[0][0]
            #condition for square
            if length==breadth:
                print("Shape: square Colour ",key)
                square_colour=key
                size_sq=abs(length)
            #rectangle that's longer than broader
            elif length>breadth:
                print(" Shape: rectangle 1 Colour ",key)
                rect_1_col=key
            #rectangle that's broader than longer
            else:
                print("Shape: rectangle 2 Colour ",key)
                rect_2_col=key
        #if it doesnt have 2 pairs in the same row and column, it's a cross
        else:
            print("Shape: cross Colour ",key)
            cross_col=key
    #create a new matrix that can hold the aligned centers
    square=np.zeros((size_sq+1,size_sq+1))
    #change the background colour
    square=np.where(square==0,background_colour, square) 
    i=0
    j=0
    #if square present, plot the square positions
    if square_colour>0:
        square[i][j]=square_colour
        square[i+size_sq][j]=square_colour
        square[i][j+size_sq]=square_colour
        square[i+size_sq][j+size_sq]=square_colour
    #if cross present, plot the cross positions
    if cross_col>0:
        square[int(size_sq/2)][0]=cross_col
        square[0][int(size_sq/2)]=cross_col
        square[size_sq][int(size_sq/2)]=cross_col
        square[int(size_sq/2)][size_sq]=cross_col
    #if rectangle 2 present, plot it's  positions
    if rect_2_col>0:
        square[size_sq][int(size_sq/2)+1]=rect_2_col
        square[size_sq][int(size_sq/2)-1]=rect_2_col
        square[0][int(size_sq/2)+1]=rect_2_col
        square[0][int(size_sq/2)-1]=rect_2_col
    #if rectangle 1 present, plot it's  positions
    if rect_1_col>0:
        square[int(size_sq/2)-1][0]=rect_1_col
        square[int(size_sq/2)+1][0]=rect_1_col
        square[int(size_sq/2)-1][size_sq]=rect_1_col
        square[int(size_sq/2)+1][size_sq]=rect_1_col
    #return the transformed square
    return square
#---------------------------------------------------solve_c8cbb738 end---------------------------------------
def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()


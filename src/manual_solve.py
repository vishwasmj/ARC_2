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
    square_colour=rect_1_col=rect_2_col=cross_col=0
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

# ---------------------------------------------------solve_f35d900a start-------------------------------------


def solve_f35d900a(x):
    """
    Difficulty: High

    The Problem: The input grid is a rectangular (list of lists) matrix with variable shape, with numbers ranging
                 from 0 to 9. (inclusive). Different colors of the color spectrum are represented by the integers.
                 The task is to identify the different colours and their respective positions in the input grid,
                 create a sqaure matrix around each coloured element such that the colour of the sqaure matrix should
                 be of the colour of the element present in its sequential position. Then create a horizontal and
                 vertical connection amongst all the square matrices, the connection is a step by step increment
                 from middle element of each square matrix towards each other at the same time.


    Assumptions: The colour for connecting two sqaure matrix is always 5 (Silver).




    The Approach: Identify the lists where there is a coloured element.
                  Idenitfy the coloured elemets index, row and column values.
                  Create square matrix around each coloured element.
                  Identify the index of zero elements between two non zero elements.
                  Create hoorizontal connection, Colour code the zero elements connecting the two coloured matrix on the row.
                  Create Vertical connection, Colour code the zero elements connecting the two coloured matrix on the columns.
                  Fill the created grid with diagonal elements.

    Note: All test cases passed

    Arguments: x, the nd array representing the input grid
    return: x, the resultant array with the transformations applied.

    """

    # Create a copy of input array
    ip_1 = x.copy()

    # COnvert array to a rectangular grid
    ip_1 = ip_1.tolist()

    # Find the position of coloured elements in the inpput grid
    pos_input = list(position_of_ele_in_ip(sublist) for sublist in ip_1)

    # Identifying the elements position ,column value holding the element and sublists where the elements are present
    pos_index, ele_present_index, ele_present_col_num = identifying_col_pos_ele(ip_1)

    # Colours of the elements
    colour_codes = get_colour_codes(ip_1)

    # New grid having square matrix around the coloured elements
    ip_1 = create_shape_for_ip_ele(pos_index, colour_codes, ip_1)

    # Remove duplicate rows where element is present in the grid
    ele_present_index = list(dict.fromkeys(ele_present_index))
    
    # Creating horizontal connections
    ip_1 = create_horizontal_connections(ip_1, ele_present_index)

    # Remove duplicate columns where element is present in the grid
    ele_present_col_num = list(dict.fromkeys(ele_present_col_num))

    # Create horizontal connections
    x = create_vertical_connections(ele_present_col_num, ip_1)

    return np.array(x)



# Identify the positions of the different colours present in the input grid
def position_of_ele_in_ip(sublist_seq):

    """
    The major task here is to iterate through each input list and store the position index of different colours.
    
    Arguments: sublist_seq- A sublist of input grid.
    
    Return:Position of coloured elements present in each sublist
    """


    # list to store the index of the element
    pos_of_ele = []

    # Iterate through sublists of the input
    for index, val in enumerate(sublist_seq):
        # If the value present in the index is greater than 0
        if val > 0:
            # Store the index
            pos_of_ele.append(index)

    return pos_of_ele



def identifying_col_pos_ele(ip_1):

    """
    The task of this function is to identify the coloured elements position ,column value holding the element and sublists where the elements are present
    
    Arguments: sublist_seq- A sublist of input grid.
    
    Return:Position of coloured elements present in each sublist, Value of the element  and column number of the element present
    """


    # Row and column in which the colours are present
    pos_index = []

    # Rows where the colours are present
    ele_present_index = []

    # Column index where the colours are present
    ele_present_columns = []

    # Iterate over each sublist to find the elements
    for index, sublist in enumerate(ip_1):
        for n, k in enumerate(sublist):
            if k > 0:
                a = [index, n]
                pos_index.append(a)
                ele_present_index.append(index)
                ele_present_columns.append(n)

    return pos_index, ele_present_index, ele_present_columns


# Idenitfy different colours present in the input grip
def get_colour_codes(ip_1):

    
    """
    The task of this function is to identify different type of colours of the elements present in the input grid
    
    Arguments: sublist_seq- A sublist of input grid.
    
    Return:Colour code value of each coloured element
    """

    
    # Store colour codes
    colour_codes = []

    for i in range(len(ip_1)):
        # check for any value in the row that has value other than 0
        if any(list(ip_1[i])) != 0:
            # index of the first colour present in the sublist
            first_colour_indx = np.min(np.nonzero(ip_1[i]))
            # get the colour code of first colour based on its index
            first_colour = ip_1[i][first_colour_indx]
            # index of the first colour present in the sublist
            second_colour_indx = np.max(np.nonzero(ip_1[i]))
            # get the colour code of second colour based on its index
            second_colour = ip_1[i][second_colour_indx]
            colour_codes.append(second_colour)
            colour_codes.append(first_colour)

    return colour_codes


def create_shape_for_ip_ele(pos_index, colour_codes, ip_1):
    
    """
    The task of this function is to identify the boundaries of a sqaure matrix around the given position of the coloured element
    and find the position values of boundaries and fill them with a colour code of the next sequential coloured element of the list.
    Fill the square matrix position for all the coloured elements.
    
    Arguments: ip_1- Entire manipulated input grid.
               pos_index -  Which gives us the row and position where the coloured element is present
               colour_codes - Colour code of the next coloured element
    
    Return: Manipulated input grid containing coloured square matrix with current coloured element in its centre position
    """



    # Iterate over element present index and colour codes
    for i, j in zip(pos_index, colour_codes):
        # Row of the coloured element
        a = i[0]
        # Column of the coloured element
        b = i[1]

        # Previous row of the coloured element
        a1 = a - 1

        # succeeding row of the coloured element
        a2 = a + 1

        # previous column position index
        b1 = b - 1

        # succeeding column position index
        b2 = b + 1

        # Manipulating positions
        # Filling the identified positions of the sqaure matrix values with colour codes
        # Fill horizontal position
        ip_1[a][b1] = j
        ip_1[a][b2] = j

        # Fill the previous row positions
        ip_1[a1][b] = j
        ip_1[a1][b1] = j
        ip_1[a1][b2] = j

        # Fill next row positions
        ip_1[a2][b] = j
        ip_1[a2][b1] = j
        ip_1[a2][b2] = j

    return ip_1


# 
def find_enclosed_zeroes(lst):
    
    """
    The task of this function is to find the number of enclosed zeros between two non-zero elements of a list.
    We first identify the first non-zero element of the list and then find the last position value of the non-zero value.
    Once we get a list with zero value present between two non zero values, we idenitfy the index value of the elements which will
    help us determine the link between two lists in the grid.
    
    Arguments: lst- sublist of the input grid.
    
    Return: Index of the zero elements presents between two non zero values and the position of the first non-zero value.
    """
    
    
    # Identify First non zero and last non zero element in the list
    try:
        first_nonzero = next(
            i
            for (i, e) in enumerate(lst)
            if e != 0
        )
        last_nonzero = next(
            len(lst) - i - 1
            for (i, e) in enumerate(reversed(lst))
            if e != 0
        )
    except StopIteration:
        return lst[:]

    # Include the element present in the last non-zero position
    last_nonzero_pos = last_nonzero + 1
    first_nonzero_pos = first_nonzero

    # Find the index of the elements holding 0 values between two non-zero elements
    idx_list = [idx for idx, val in enumerate(lst[:first_nonzero_pos] + lst[first_nonzero_pos:last_nonzero_pos]) if
                val == 0]

    return idx_list, first_nonzero_pos


# Create a horizontal connection between the created square matrices
def create_horizontal_connections(ip_1, ele_present_index):

    """
    The task of this function is to create horizontal connections between two square matrices present in the same row.
    We first identify the position of the zero values between two non zero values, then divide the list containiing the position 
    of non zero elements into two parts. We then reverse the second list and find the alternate position index of zeros which needs 
    to be filled in order to make connections. We then take the positions which needs to colour coded and then fill the index values 
    of the grid with silver colour code(5) to make connections.
    
    Arguments: ip_1- Manipulated input grid.
               ele_present_index - Rows and column value where coloured elements are present
    
    Return: manipulated input grid containing horizontal connection between the sequential sqaure matrices
    """

    for i in ele_present_index:

        # Get the index values of the zeros present between two non zero elements
        lst_containing_zero_ele_index, first_non_zero_pos = find_enclosed_zeroes(ip_1[i])

        # remove/ keep only zeros present after the first non zero element
        pos_list_clean = []

        for k in lst_containing_zero_ele_index:
            if k > first_non_zero_pos:
                pos_list_clean.append(k)

        # Breaking the zero element positions into two seperate lists
        first_half_lst = pos_list_clean[:len(pos_list_clean) // 2]
        second_half_lst = pos_list_clean[len(pos_list_clean) // 2:]

        ## Identifying the alternate positions of zero element that has to be coloured from first list
        ele_to_colour_from_first_lst = first_half_lst[::2]

        # Reversing the second half of the list
        # As we need to increment from two ends of the matrix
        new_second_half_lst = second_half_lst[::-1]

        # Identifying the alternate positions of zero element that has to be coloured from second list
        ele_to_colour_from_second_list = new_second_half_lst[::2]

        # Colour code the connecting elements
        for j in ele_to_colour_from_first_lst:
            ip_1[i][j] = 5

        for k in ele_to_colour_from_second_list:
            ip_1[i][k] = 5

    return ip_1


# Create a vertical connection between the created square matrices
def create_vertical_connections(ele_present_columns, ip_1):
    
    """
    The task of this function is to create verticalconnections between two square matrices present in the same column.
    We first identify the position of the zero values between two non zero values, then divide the list containiing the position 
    of non zero elements into two parts. We then reverse the second list and find the alternate position index of zeros which needs 
    to be filled in order to make connections. We then take the positions which needs to colour coded and then fill the index values 
    of the grid with silver colour code(5) to make connections.
    
    Arguments: ip_1- Manipulated input grid.
               ele_present_index - Rows and column value where coloured elements are present
    
    Return: manipulated input grid containing vertical connection between the sqaure matrices.
    """


    # iterate over columns of the coloured elements
    for j in ele_present_columns:

        # Get column values of coloured element
        col_list = []

        for i in range(len(ip_1)):
            col_list.append(ip_1[i][j])

        # Get the index values of the zeros present between two non zero elements
        lst_containing_zero_ele_index, first_non_zero_pos = find_enclosed_zeroes(col_list)

        # remove/ keep only zeros present after the first non zero element
        pos_list_clean = []

        for k in lst_containing_zero_ele_index:
            if k > first_non_zero_pos:
                pos_list_clean.append(k)

        first_half_lst = pos_list_clean[:len(pos_list_clean) // 2]

        second_half_lst = pos_list_clean[len(pos_list_clean) // 2:]

        # Identifying the alternate positions of zero element that has to be coloured from first list
        ele_to_colour_from_first_lst = first_half_lst[::2]

        # Reversing the second half of the list
        # As we need to increment from two ends of the matrix
        new_second_half_lst = second_half_lst[::-1]

        # Identifying the alternate positions of zero element that has to be coloured from second list
        ele_to_colour_from_second_list = new_second_half_lst[::2]

        # Colour code the connecting elements from first element
        for n in ele_to_colour_from_first_lst:
            ip_1[n][j] = 5

        # Colour code the connecting elements from the second element
        for m in ele_to_colour_from_second_list:
            ip_1[m][j] = 5

    return ip_1



# ---------------------------------------------------solve_f35d900a end------------------------------------------------


#---------------------------------------------------solve_ae3edfdc start-------------------------------------
def solve_ae3edfdc(x):
    """
    Difficulty: Medium
    
    The problem description: Gravity- well, not the regular kind. There are two centres of gravity, blue and
    red - which has the ability to bring orange and green squares in it's path towards itself, so that it 
    occupies the closest postition wrt to it. The one condition, the attracted squares must be 
    perpendicular to the centre of gravity to get attracted to it.
    
    Assumptions: There are no other colours in the space. The non-centres are always perpendicular to the centres.
    
    The approach: Locate all the colourfull squares in the 'space'. Then locate the centres of gravity.
    Pair them up together as blue to orange and red to green. Check along the perpendicular path.
    If there are any squares in it's path, move it to the closest position in the same line.
    
    Testing:All test cases passed
    
    Argument: x, the n-d array representing the space
    return: x, after the above transformation is done.
    
    """
    
    # find all the squares where colour not equal to black
    row,column = np.where(x > 0)
    colour_dict={}
    #put them all into one dictionary
    for r,c in zip(row,column):
        if x[r][c] in colour_dict:
            colour_dict[x[r][c]].append((r,c))
        else:
            colour_dict[x[r][c]] = [(r,c)]
    
    #-------------------Hardcoding the colours for the centres and it's pairs
    center1=2
    center2=1
    pair1=3
    pair2=7
    #-----------------
    #Creating two dictionaries based on the centre-pair value
    keyPair1 = [center1, pair1]
    keyPair2 = [center2, pair2]
    d1 = {x: colour_dict[x] for x in colour_dict if x in keyPair1}
    d2 = {x: colour_dict[x] for x in colour_dict if x in keyPair2}
    #moving the position of the first centre-pair pair
    half_done=match_pattern(d1,x,keyPair1)
    #sending the half transformed to transform the rest
    final=match_pattern(d2,half_done,keyPair2)
    x=final
    return x

def match_pattern(dict_fig,x,keyPair):
   #get the row and column of the centre
    r=dict_fig[keyPair[0]][0][0]
    c=dict_fig[keyPair[0]][0][1]
    #for every square belonging to this key-pair
    for v in dict_fig[keyPair[1]]:
        #if in the same row as the centre of gravity but before it
        if v[0]==r and v[1]<c:
            #closest point to centre on the same side
            x[r][c-1]=keyPair[1]
            #set the old position to 0
            x[v[0]][v[1]]=0
      #if in the same row as the centre of gravity but after it
        elif v[0]==r and v[1]>c:
            #closest point to centre on the same side
            x[r][c+1]=keyPair[1]
            x[v[0]][v[1]]=0
        #if in the same column as the centre of gravity but above it
        elif v[1]==c and v[0]<c:
            x[r-1][c]=keyPair[1] 
            x[v[0]][v[1]]=0
        #if in the same column as the centre of gravity but below it
        elif v[1]==c and v[0]>c:
            x[r+1][c]=keyPair[1]
            x[v[0]][v[1]]=0
        else:
            #not per assumption
            raise Exception("Pattern not handled")

    return x
#---------------------------------------------------solve_ae3edfdc start-------------------------------------



#---------------------------------------------------solve_ded97339 start-------------------------------------
def solve_ded97339(x):
    """
    Difficulty- medium to high
    Problem description: Stars in the night sky! A grid of black squares represents the sky and the tiny blue 
    squares, the stars. The task is to find the constellations hidden in the sky and connect them. 
    How do we do this? We need to identify the ones that belong and a constellation and ones that do not. 
    On observation, we can see that there is a simple common rule. All stars belonging to a constellation are
    on the same row or column.
    All the other starts are loners. 
    
    Assumptions: There are no other colours on the grid besides black and blue.
    
    Solution: First find the non-black squres. Then find the ones that are on the same row or column. Connect the ones in 
    the same row, then connect the ones in the same column.
    
    Arguments: x the nd array 
    return: x the transformed array

    """
    start_pos=[]
    #find all the non-black squares
    row,column = np.where(x >0)
    #get a list of their co-ordinates
    for r,c in zip(row,column):
        start_pos.append((r,c))
        
    if len(row) != len(set(row)) and len(column) != len(set(column)) :
        #checking for perpendicular elements by checking for items on the same row
        b=[item for item, count in collections.Counter(row).items() if count > 1]
        #checking for points on the same column and creating a list
        c=[item for item, count in collections.Counter(column).items() if count > 1]
    row_list=[]
    col_list=[]
    #finding all the items perpendicular along the row and columns seperately
    for (k,h) in start_pos:
        if k in b:
            row_list.append((k,h))
        if h in c:
            col_list.append((k,h))
    #find start and end of all the elements in the same row and fill up 
    for i in range(len(row_list)-1):
        if row_list[i][0]==row_list[i+1][0]:
            a=row_list[i]
            b=row_list[i+1]
            for i in range(a[1],b[1]):
                x[a[0],i]=8
    #find start and end of all the elements in the same column and fill up
    for a,b in itertools.product(col_list,col_list):
        if a!=b and a[0]<b[0] and a[1]==b[1]:
            for i in range(a[0],b[0]):
                x[i,a[1]]=8           
    return x
#------------------------------------------------------solve_ded97339- end------------------------------------------


# ---------------------------------------------------solve_d0f5fe59 start-----------------------------------------------


def solve_d0f5fe59(x):
    """
    Difficulty: Medium-to-difficult

    The Problem: The input grid is a rectangular (list of lists) matrix of variable shape, with a single integer number.
                 Blue colour of the color spectrum are represented by the integer 8.
                 The task is to identify the boundaries between different shapes, identify and differentiate different shapes,
                 and create a matrix whose diagnol elements reprents one shape.The created matrix should have a size of
                 (identified shape * identified shape).

    Assumptions: The colour inside the input grid is always 8.
                 The number of different shapes in each given input list is not more than 2.



    The Approach: Identify the lists where there is a coloured element.
                  Idenitfy the different boundaries of the all the shapes.
                  Order the elements by checking their boundaries according to its connection with respect to the next elements.
                  Check for link between the elements of each list.
                  Identify number of shapes from the link between elements of the grid.
                  Create a grid having number of shapes present inside the input grid as the shape.
                  Fill the created grid with diagonal elements.

    Note: All test cases passed

    Arguments: x, the nd array representing the input grid
    return: x, the resultant array with the transformations applied.

    """
    # Identify the lists where there is a coloured element
    pos_of_ele = list(position_of_elements(sublist) for sublist in x)
    # Remove the null lists from the returned list of list position of elements
    clean_pos_of_ele = list(filter(lambda x: x, pos_of_ele))
    # Identify the different boundaries of the all the shapes
    identified_boundaries_lst = identify_boundaries_of_the_shape(clean_pos_of_ele)
    # Order the returned list according to its connection with respect to the elements
    ordered_boundaries_lst = ordered_lst_ele(identified_boundaries_lst)
    # Check for link between the elements of each list
    ele_link = link_between_the_elements(ordered_boundaries_lst)
    # Identify number of shapes from the link between elements of the list of list
    identified_shapes = identify_diff_shapes(ele_link)
    # Create an empty grid having number of shapes present inside the input grid as the shape
    empty_op_grid = np.zeros(shape=(len(identified_shapes), len(identified_shapes)))
    # Fill the created grid with diagonal elements
    x = creating_diagnol_matrix(empty_op_grid)

    return np.array(x)
    

# Check which list of list has elements present inside them
def position_of_elements(sublist_seq):
    # list to store the index of the element
    pos_of_ele = []

    # Iterate through sublists of the input
    for index, val in enumerate(sublist_seq):
        # If the value present in the index is greater than 0
        if val > 0:
            # Store the index
            pos_of_ele.append(index)

    return pos_of_ele


# Identify the different boundaries of the shape
def identify_boundaries_of_the_shape(pos_clean_ip):

 
    """
    The task of this function is to identify the boundaries of different shapes present in the input grid. Identify the list of elements 
    having no null lists amongst them, if the values in sublist are having a difference of more than 1 then it means that the elements present
    in the list may belong to a different shape or belongs to same shape with any other element connected to it.We further investigate these type 
    of sublists. We check these sublists with their previous sublist value to check if any element is having a connection with the disconnected 
    element, if not then we seperate the elements from the list else we keep them in the same list.
    
    Arguments: pos_clean_ip- List of elements without containing null list amongst them.
    
    Return: boundary splits - list of list , Where each sublist doesnt belong to more than one different shape. 
    """
    
    boundary_splits = []

    for index, sublist in enumerate(pos_clean_ip):

        # Check for difference between the elements of the sublist
        chck_or_diff_bw_ele = np.diff(sublist)

        # Store it as a list
        ele_diff = list(chck_or_diff_bw_ele)

        # Store the elements after classifying that they belong to different shapes
        split_ele_lst = []

        # Check if the difference between the elements of the sublist is greater than 1
        if (all(ele == 1 for ele in ele_diff)) == False:

            # Check if the previous index is not 0
            if index != 0:
                # get the previous sublist
                before_sublist = pos_clean_ip[index - 1]

            # Find if all the elements present in the current sublist are also present in the previous sublist
            result = all(elem in before_sublist for elem in sublist)

            # Split the elements in the same row belonging to different shape
            if result == False:

                num_of_splits = 0

                # Number of splits that should take place in the sublist
                for j in range(len(sublist) - 1):
                    difference_of_ele = abs(sublist[j] - sublist[j + 1])
                    if difference_of_ele > 1:
                        num_of_splits = num_of_splits + 1

                pos_to_split = []
                # Find the position where the split should take place
                for k, n in enumerate(ele_diff):
                    if n > 1:
                        pos_to_split.append(k)

                # Split the sublist into further subist based on different identified position boundaries
                for pos_split in pos_to_split:
                    size = len(sublist)

                    # Find the idex which is matching the position to split
                    idx_list = [idx + 1 for idx, val in enumerate(sublist) if idx == pos_split]
                    # Split and merge the values present in the position split
                    split_based_on_pos = [sublist[i: j] for i, j in zip([0] + idx_list, idx_list
                                                                        + ([size] if idx_list[-1] != size else []))]

                    split_ele_lst.append(split_based_on_pos)

        # If there is no elements in sublist to split, then append the sublist
        if not split_ele_lst:
            boundary_splits.append(sublist)

        else:
            # Append the "split and merged list" to the sublist
            for i in range(len(split_ele_lst)):
                for j in range(len(split_ele_lst) + 1):
                    sub_split_lst = split_ele_lst[i][j]
                    boundary_splits.append(sub_split_lst)

    return boundary_splits


# Identify the link between the elements of the list
def link_between_the_elements(final_list):
    
    """
    The task of this function is to identify the relationship between a current sublist and its succeeding sublist. 
    Then we store how many elements are matching between the lists.
    
    Arguments: final_list- manipulated input grid
    
    Return: ele_link - list of list holding elements that are having connections with the elementsts in the successive list.
    """


    ele_link = []

    # Iterate over each row of the boundary list
    for index in range(len(final_list) - 1):
        # Elements matching in the current list and next sublistr
        elements_matching = len([x for x in final_list[index] if x in final_list[index + 1]])

        ele_link.append(elements_matching)

    return ele_link


# Check if the list created after spliting is in the correct order
def ordered_lst_ele(ident_boud_lst):

    """
    The task of this function is to identify if the elements boundaries list created are in a proper order i.e., to check if the connected elements
    are present next to each other in the list. If the current element is having connections with the element in successive second index position, 
    then we change the position of the lists.
    
    Arguments: ident_boud_lst- Identified boundary list
    
    Return: ident_boud_lst - correctly ordered boundary list.
    """

    
    # Iterate over the created list
    for index, val in enumerate(ident_boud_lst):

        current_sublist = ident_boud_lst[index]

        index_1 = index + 1

        if index_1 < (len(ident_boud_lst) - 1):

            next_sublist = ident_boud_lst[index + 1]

            # check if there is any elements matching between current list and next sublist

            if len(set(current_sublist) & set(next_sublist)) == 0:

                index_2 = index + 2

                if index_2 < (len(ident_boud_lst) - 1):
                    # check if there is any match of elements on the next to next sublist
                    nxt_to_nxt_sublist = ident_boud_lst[index_2]

                    if len(set(current_sublist) & set(nxt_to_nxt_sublist)) != 0:
                        # If there is an element matching the element in our current list then change the
                        # position of the sublists
                        ident_boud_lst[index_2], ident_boud_lst[index_1] = ident_boud_lst[index_1], ident_boud_lst[
                            index_2]

    return ident_boud_lst


# Idenitfy different shapes based on the link between the elements
def identify_diff_shapes(store_link):
    size = len(store_link)

    # If there is no connection between the shapes then the difference between the list is represented by 0
    # Find the occourance of the value 0 in the list having the list of elements mapping the of boundaries
    boundary_idx_list = [idx + 1 for idx, val in enumerate(store_link) if val == 0]

    # Create sublists representing different shapes present in boundary list
    shapes_present_in_grid = [store_link[i: j] for i, j in
                              zip([0] + boundary_idx_list, boundary_idx_list +
                                  ([size] if boundary_idx_list[-1] != size else []))]

    return shapes_present_in_grid


# Creating a diagnal matrix whose diagnol elements represents different shapes present in the input grid
def creating_diagnol_matrix(empty_op_grid):
    len_of_seq = len(empty_op_grid)

    # assigning iter the value of length of the matrix
    i = len_of_seq

    pos_counter = [0]

    pos_counter_len = len(pos_counter)

    puzzle_ele = []

    # Colour code the diagnol elements into blue clour
    target = [8]

    # Iterating till the index is 1
    while (i >= 1):

        i = i - 1
        # Elements in the row
        curr_lst_ele = empty_op_grid[i]

        # Assigning colour value to the diagnol index of the elements
        for x, y in zip(pos_counter, target):
            if x < len_of_seq:
                curr_lst_ele[x] = y

        # Storing the assigned values to the list
        puzzle_ele.append(curr_lst_ele)

        # Increasing the counter to get the dignol positions for that colour in each row
        pos_counter = [x + 1 for x in pos_counter]

    manipulated_puzzle_op = [arr.tolist() for arr in puzzle_ele]

    return manipulated_puzzle_op



# ---------------------------------------------------solve_d0f5fe59 end------------------------------------------------




# ---------------------------------------------------solve_feca6190 start----------------------------------------------



def solve_feca6190(x):
    """
    Difficulty: Medium

    The Problem: The input grid is a rectangular (list of lists) matrix with variable shape, with numbers ranging
                 from 0 to 9. (inclusive). Different colors of the color spectrum are represented by the integers.
                 The task is to determine the color schemes in the input grid, generate a matrix whose shape is given by
                 multiplication of size of input matrix and the number of colors present inside the grid.Next step is to
                 fill the formed matrix diagonally with color from the input grid, starting with the index value of the
                 color in the input grid.

    Assumptions: The Input Grid is always of shape 1 * 5.
                 There cannot be more than five colours present in the grid.
                 No Colour is repeated.


    The Approach: Identify the size of the grid.
                  Identify the colours present in the grid.
                  Identify the position of the colour in the grid.
                  Create an empty array whose shape would be of the size (number of colours * grid size,number of
                  colours * grid size).
                  Fill the first array with colours as per their index position of the input grid.
                  Identify the dignol positions for the elements in the first array and fill them with integers
                  present in the starting array.
                  Inverse the matrix to get the matching output.

    Note: All test cases passed

    Arguments: x, the nd array representing the input grid
    return: x, the resultant array with the transformations applied.

    """
    # Finding the number of colours and length of the input grid
    # Returns list of tuple
    colour_count_and_len_of_ip = list(number_of_colours(sublist) for sublist in x)

    # Finding the index of the colours and return the positions as a list
    colour_pos_in_input = list(position_of_colours(sublist) for sublist in x)

    # Colour code present in the input grid and return the list of colours
    col_codes = list(colour_code_count(sublist) for sublist in x)

    # Create an empty matrix based on the number of colours and length of the input array
    manipulation_grid = create_the_empty_grid(colour_count_and_len_of_ip)

    # Manipulate the empty array
    # Identify the diagonal positions in the grid
    # Fill the diagonal positions with its respective colour codes
    x = create_output_grid(manipulation_grid, colour_pos_in_input, col_codes)

    return np.array(x)


# Find the different number of colours in each sublist
def number_of_colours(sublist_seq):
    colour_count = 0

    # Iterate over each value of the sublist
    for index, val in enumerate(sublist_seq):
        # if their value is greater than zero
        if val > 0:
            # increase the count
            colour_count = colour_count + 1

    # Length of the sublist
    len_of_sublist_seq = len(sublist_seq)

    return colour_count, len_of_sublist_seq


# Find the index where the colours are present in the sublist
def position_of_colours(sublist_seq):
    pos_count = []

    for index, val in enumerate(sublist_seq):
        if val > 0:
            pos_count.append(index)

    return pos_count


# Identify different colours present in the input grid
def colour_code_count(sublist_seq):
    colour_codes = []

    for index, val in enumerate(sublist_seq):

        if val > 0:
            colour_codes.append(val)

    return colour_codes


# Create an empty grid based on the length of the sublist and colour count
def create_the_empty_grid(colour_input):
    input_seq = np.zeros(shape=(colour_input[0][0] * colour_input[0][1], colour_input[0][0] * colour_input[0][1]))

    return input_seq


# Manipulating the created grid to solve the puzzle
def create_output_grid(ip_seq, colour_pos_in_input, col_codes):
    len_of_seq = len(ip_seq)

    # assigning iter the value of length of the matrix
    i = len_of_seq

    # Initiating a counter at the index of the first colour
    pos_counter = colour_pos_in_input[0]

    pos_counter_len = len(pos_counter)

    # Storing the created dignol rows
    puzzle_ele = []

    # getting the colour value
    target = col_codes[0]

    # Iterating till the index is 1
    while (i >= 1):

        i = i - 1

        # Elements in the row
        curr_lst_ele = ip_seq[i]

        # Assigning colour value to the diagnol index of the elements
        for x, y in zip(pos_counter, target):
            if x < len_of_seq:
                curr_lst_ele[x] = y

        # Storing the assigned values to the list
        puzzle_ele.append(curr_lst_ele)

        # Increasing the counter to get the dignol positions for that colour in each row
        pos_counter = [x + 1 for x in pos_counter]

    # Reversing the list of list
    final_output = puzzle_ele[::-1]

    # Converting array to list
    final_output_lst = [arr.tolist() for arr in final_output]

    return final_output_lst

# ---------------------------------------------------solve_feca6190 end-------------------------------------------------




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


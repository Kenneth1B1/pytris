import tetromino as tm
import pygame
import numpy as np
import os
import socket


def runGame():
    def checkWall(curArea, board_width_px):
        return True

    def checkFloor(curY, board_height):
        if(curY >= 19):
            return False
        else:
            return True



    pygame.init()
    #screen size
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    #board size
    board_width = 10
    board_height = 20




    #create background grid with one extra column on both sides for shape manipulation
    #also adds a bottom row of 3, which prevents shapes from falling further
    grid = np.zeros((board_height + 2,board_width + 2))
    grid[20,:] = 3
    grid[:,0] = 4 # Set all values in the first column to 3
    grid[:,-1] = 4 # Set all values in the last column to 3



    #grid = grid.astype(int)

    #display grid- takes previous grid and turns into proper dimensions
    display_grid = np.zeros((board_height, board_width))

    #for grid:
    #0 -> empty
    #1 -> moving shape
    #2 -> filled spaces (previously laid shapes)


    #calculate size of each cell on the board
    cell_size = min(screen_width //board_width, screen_height // board_height) * .8


    #calculate total size of the board
    board_width_px = cell_size * board_width
    board_height_px = cell_size * board_height

    #calc position of board on screen
    board_x = (screen_width - board_width_px) // 2
    board_y = (screen_height - board_height_px)  // 2

    #create a rectangle object for the board:
    board_rect = pygame.Rect(board_x, board_y, board_width_px, board_height_px)

    startArea = (301,1)


    #testing importing shapes
    curShape = tm.Tetromino(tm.t_shape,0)
    curArea = startArea
    curRow = 0
    curCol = 4
    # Create a timer to update the rectangle position every second
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)


    #scoreboard------------------------------------------------------------

    #scoreboard var
    linesCleared = 0

    # create a font object
    font = pygame.font.Font(None, 36)

    # define function to render the score
    def render_score():
        score_text = font.render("Score: {}".format(linesCleared), True, (255, 255, 255))
        screen.blit(score_text, (board_x + board_width_px + 20, board_y))

        
    #---------------------------------------------------------------------
    def moveLeft():
        return
    def moveRight():
        return
    def clearOldSpaces():
        grid = np.where(grid == 1, 0, grid)
        grid = np.where(grid == 2, 0, grid)
        grid[10,:] = 3

    def resetWalls(grid):
        grid[:,0] = 4 # Set all values in the first column to 3
        grid[:,-1] = 4 # Set all values in the last column to 3
        return grid

    def clearBoard():
        grid = np.zeros((board_height,board_width))

    def drawDisplay():
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the board outline
        pygame.draw.rect(screen, (255, 255, 255), board_rect, 1)

        # Draw the horizontal lines
        for i in range(1, board_height):
            y = board_y + i * cell_size
            pygame.draw.line(screen, (255, 255, 255), (board_x, y), (board_x + board_width_px, y))

        # Draw the vertical lines
        for i in range(1, board_width):
            x = board_x + i * cell_size
            pygame.draw.line(screen, (255, 255, 255), (x, board_y), (x, board_y + board_height_px))


    def drawDisplayGrid(curRow, curCol, grid, curShape):
        
        #console grid (not being rendered)
        grid = np.where(grid == 1, 0, grid) #clear old grid spaces
        
        # convert shape matrix into small matrix var
        small_matrix = curShape.shape
        print(small_matrix)
        
        # Define the location to place the small matrix
        row_start = curRow
        col_start = curCol

        # Place the small matrix in the large matrix
        rows, cols = np.nonzero(small_matrix)
        mask = small_matrix != 0
        grid[row_start:row_start+small_matrix.shape[0], col_start:col_start+small_matrix.shape[1]][mask] = 1


        # Print the result with propper grid
        display_grid = grid[0:-1, 1:-1]

        return grid, display_grid

    def drawFilling(board_height, board_width,cell_size, board_x, board_y):
        for i in range(board_height):
            for j in range(board_width):
                if grid[i][j+1] == 1:
                    pygame.draw.rect(screen, (100, 255, 200), pygame.Rect(board_x+j*cell_size, board_y+i*cell_size, cell_size - 1, cell_size - 1))
                if grid[i][j+1] == 2:
                    pygame.draw.rect(screen, (100, 12, 255), pygame.Rect(board_x+j*cell_size, board_y+i*cell_size, cell_size - 1, cell_size - 1))

        
    def checkShapeAtBottom(curRow, curCol, curShape, grid, display_grid, small_matrix):
        # get the height of the curShape
        shape_height = curShape.shape.shape[0]
        if(curRow + small_matrix.shape[0] > len(grid)-2):
            # The shape has reached the bottom of the grid
            return True

        # Check for collisions with the bottom of the grid
        for i in range(grid.shape[0]-1):
            for j in range(grid.shape[1]):
                if grid[i,j] == 2 and grid[i+1,j] == 1:
                    return True
        
        # Check for collisions with the already placed shapes
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i,j] == 1:
                    if i == grid.shape[0]-1 or grid[i+1,j] == 2 or grid[i+1,j] == 3:
                        # The shape has collided with the already placed shapes
                        return True
        
        # curShape has not reached the bottom or collided with already placed shapes
        return False

    def checkRowComplete(display_grid, grid, linesCleared):
        full_rows = [i for i, row in enumerate(display_grid) if np.all(row == 1)]

        # Remove the full rows and insert empty rows at the top

        for i in range(display_grid.shape[0]):
            if np.all(display_grid[i] == 2):
                print("full")
                linesCleared = linesCleared + 1
                grid[i,:] = 0
                # Get all rows and columns above the specified row
                above_rows = display_grid[:i, :]
                # Update the corresponding part of the grid
                grid[1:i+1, 1:-1] = above_rows
                
        return grid, linesCleared


    #grid[:,0] = 4 # Set all values in the first column to 3
    #grid[:,-1] = 4 # Set all values in the last column to 3
    def checkWalls(grid, curShape, curCol):
        if not np.all(grid[:, 0] == 4):
            curCol = 1
            grid = resetWalls(grid)
        if not np.all(grid[:, -1] == 4):
            curCol = curCol - 1
            grid = resetWalls(grid) 
        return grid, curCol


    def checkLoss(display_grid):
        print("loss?", np.any(display_grid[2,:] == 2))
        if (np.any(display_grid[2,:] == 2 )):
            print("loss")
            return -1
        
    #show score 
    score_text = font.render("Score: {}".format(linesCleared), True, (255, 255, 255))
    screen.blit(score_text, (board_x + board_width_px + 20, board_y))


    #draw board on screen
    while True:
        for event in pygame.event.get():
            print(grid)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == timer_event:
                # Update the rectangle position
                if(checkFloor(curRow, board_height)):
                    curArea = (curArea[0],curArea[1] + cell_size)
                    curRow += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    curShape.rotateCCW()
                if event.key == pygame.K_DOWN:
                    curShape.rotateCW()
                if event.key == pygame.K_a:
                    if(curCol > 0):        
                        curCol = curCol - 1
                if event.key == pygame.K_d:
                    width = curShape.shape[1]
                    print(width)
                    if(curCol + width.size < grid[1].size):
                        curCol = curCol + 1
                if(event.key == pygame.K_s):
                    if(checkFloor(curRow, board_height)):
                        curArea = (curArea[0],curArea[1] + cell_size)
                        curRow += 1

        #draw display_grid
        drawDisplay()
        
        grid, display_grid = drawDisplayGrid(curRow, curCol, grid, curShape)
        #print(display_grid.shape)
        drawFilling(board_height, board_width,cell_size, board_x, board_y)
        
        if(checkShapeAtBottom(curRow, curCol, curShape, grid, display_grid, curShape.shape)):
            #turn all 1s into 2s on main grid
            grid[grid == 1] = 2
            curShape = tm.Tetromino(tm.returnRandomShape(),0)
            curRow = 1
            curCol = 4
             

        #-------------------------------------------------------------

        #check rows complete
        grid, linesCleared = checkRowComplete(display_grid, grid, linesCleared)
        score_text = font.render("Score: {}".format(linesCleared), True, (255, 255, 255))

        
        #-------------------------------------------------------------        
        #check walls outside of function
        grid, curCol = checkWalls(grid, curShape, curCol)
        


        #checkLoss ---------------------------------------------------
        checkLoss(display_grid)

        #update Score   
        screen.blit(score_text, (board_x + board_width_px + 20, board_y))
        
        
        pygame.display.update()





runGame() 


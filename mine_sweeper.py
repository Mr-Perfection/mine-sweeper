'''
mine_sweeper
  board: 2D array
    cell
      state: mine or not
      revealed: revealed or not
      value: number of mines in surrounding zone
      
  reveal(x,y): reveal the cell
  game_over(): exit the game
  
'''
import random
import sys

def print_board(board):
  n, m = len(board), len(board[0])
  for i in range(n):
    s = ''
    for j in range(m):
      s += board[i][j].render_cell()
    print(s)
class Cell():
  def __init__(self, state, revealed, value, x, y):
    self.state = state
    self.revealed = revealed
    self.value = value
    self.x, self.y = x, y
  def render_cell(self):
    if self.revealed: return str(self.value)
    else: return '-'
  
class mine_sweeper():
  board = []
  mines = []
  total_cells = 0
  total_mines = 0
  is_game_over = False
  def __init__(self, width, height):
      width, height = int(width), int(height)
      self.board = [[Cell(False, False, 0, x, y) for x in range(width)] for y in range(height)]
      self.total_cells = width * height
      # set random mines into board
      self.__randomize_mines(width, height, self.board)
      
      # calculate value of each cell
      self.__calculate_values(width, height, self.board)
  
  def print_mine_locations(self):
    n, m = len(self.board), len(self.board[0])
  
    for i in range(n):
      s = ''
      for j in range(m):
        s += 'M' if self.board[i][j].state else '-'
      print(s)
      
  def print_values(self):
    n, m = len(self.board), len(self.board[0])
  
    for i in range(n):
      s = ''
      for j in range(m):
        s += str(self.board[i][j].value)
      print(s)
  
  def reveal(self, x, y):
    board = self.board
    x, y = int(x), int(y)
    # check row
    if y >= len(board) or y < 0:
      print('Please enter a value between ',0,' and ',len(board)-1)
      return
    # check col
    if x >= len(board[0]) or x < 0:
      print('Please enter a value between ',0,' and ',len(board[0])-1)
      return
    if self.board[y][x].state: self.game_over()
    else: 
      self.board[y][x].revealed = True
      if self.board[y][x].value == 0:
        self.__expand_blank(x, y, self.board)
  
  def game_over(self):
    print('Opps... Game over!')
    self.is_game_over = True
    
  def __expand_blank(self, x, y, board):
    deltas = [
      (-1,  -1), (0,   1), (1,   1),
      (-1,   0),           (1,   0),
      (-1,   1), (0,  -1), (1,  -1),
    ]
    queue = [board[y][x]]
    # is this cell blank? (meaning value is 0?)
    if board[y][x].value == 0:
      while queue:
        cell = queue.pop(0)
        x,y = cell.x, cell.y
        # are cell's neighboring cells blank?
        for delta in deltas:
          dx, dy = x+delta[0], y+delta[1]
          if self.__is_within_range(dx, dy) and\
             not board[dy][dx].revealed:
            
            # not a bomb?
            if not board[dy][dx].state:
              board[dy][dx].revealed = True
              #  is value zero?
              if board[dy][dx].value == 0:
                queue.append(board[dy][dx])
    
            
  def __randomize_mines(self, width, height, board):
    # adjust how many mines are in the board.
    # I set it to 1/3
    # 1/3 is too hard. Let's do 1/4
    self.total_mines = int(self.total_cells/4)
    # self.total_mines = 4
    remaining_mines = self.total_mines
    xrange, yrange = range(width),range(height)
    
    # print('total mines are', self.total_mines)
    # are mines all planted?
    while remaining_mines > 0:
      xpos,ypos = random.choice(xrange),random.choice(yrange)
      
      # is mine not planted yet?
      if not board[xpos][ypos].state:
        self.mines.append(board[xpos][ypos])
        board[xpos][ypos].state = True; remaining_mines -= 1
  
  def __calculate_values(self, width, height, board):
    
    deltas = [
      (-1,  -1), (0,   1), (1,   1),
      (-1,   0),           (1,   0),
      (-1,   1), (0,  -1), (1,  -1),
    ]
    # intead of checking all the corners, loop through mines and deltas
    # and increment the values surrounding mine
    for mine in self.mines:
      for delta in deltas:
        y, x = mine.y+delta[1], mine.x+delta[0]
        if self.__is_within_range(x, y):
          board[y][x].value += 1
    
  def __is_within_range(self, x, y):
    board = self.board
    width, length = len(board[0]), len(board)
    return x >= 0 and x < width and y >= 0 and y < length
    
print('input the size of the minesweeper board')
W = input('width:')
H = input('height:')
game = mine_sweeper(int(W), int(H))
# game.print_mine_locations()
# game.print_values()
print_board(game.board)
print('welcome to the mine sweeper.\nPlease, enter a x and y coordinates to reveal!')
while True:
  print('Input x and y position of your next sweep! x and y are zero based.')
  print('zero based means instead of starting 1, it will start with 0')
  x = input('x:')
  y = input('y:')
  game.reveal(x,y)
  # game.print_mine_locations()
  print_board(game.board)
  # game.print_values()
  
  if game.is_game_over: break
from Tkinter import *

# Global Variables

# 1. Basic Config
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE / 3
GRID_LINE_WIDTH = 20
SYMBOL_SIZE = 0.5
SYMBOL_WIDTH = WINDOW_SIZE / 12

# 2. Colors
BG_COLOR = "white"
GRID_COLOR = "light grey"
X_COLOR = "dodger blue"
O_COLOR = "tomato"
DRAW_COLOR = "light sea green"

# 3. Game Screens
STATE_TITLE_SCREEN = 0
STATE_X_TURN = 1
STATE_O_TURN = 2
STATE_GAME_OVER = 3
FIRST_PLAYER = STATE_O_TURN

# 4. Board States
EMPTY = 0
X = 1
O = 2

class Game(Tk):
	def __init__(self):
		Tk.__init__(self)

		# Creating the canvas
		self.canvas = Canvas(height = WINDOW_SIZE, width = WINDOW_SIZE, bg = BG_COLOR)
		self.canvas.pack()

		# Bind the keys / mouse events to the canvas
		self.bind("<x>", self.exit) # X - key to exit
		self.canvas.bind("<Button-1>", self.click) # Mouse's left click

		# Starting off the game at title screen
		self.gamestate = STATE_TITLE_SCREEN
		self.title_screen()

		# Tic Tac Toe Gameboard
		self.board = [
		[EMPTY, EMPTY, EMPTY],
		[EMPTY, EMPTY, EMPTY],
		[EMPTY, EMPTY, EMPTY]
		]

	def title_screen(self):
		# Remove everything just in case
		self.canvas.delete("all")

		# Background colors
		self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill="tomato", outline="")
		self.canvas.create_rectangle(int(WINDOW_SIZE/15), int(WINDOW_SIZE/15), int(WINDOW_SIZE*14/15), int(WINDOW_SIZE*14/15), width=(WINDOW_SIZE/20), outline="dodger blue")
		self.canvas.create_rectangle(int(WINDOW_SIZE/10), int(WINDOW_SIZE/10), int(WINDOW_SIZE*9/10), int(WINDOW_SIZE*9/10), fill="dodger blue", outline="")

		# Display Titles
		self.canvas.create_text(WINDOW_SIZE/2, WINDOW_SIZE/3, text="TIC TAC TOE", fill="white", font=("Franklin Gothic", int(-WINDOW_SIZE/12), "bold"))

		self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/1.5), text="[PLAY]", fill="white", font=("Franklin Gothic", int(-WINDOW_SIZE/25)))

	def new_board(self):
		# Remove everything
		self.canvas.delete("all")

		# Create a new board
		self.board = [
		[EMPTY, EMPTY, EMPTY],
		[EMPTY, EMPTY, EMPTY],
		[EMPTY, EMPTY, EMPTY]
		]

		# Draw the grid lines for Tic Tac Toe
		for n in range(1, 3):
			# Draw Vertical Line
			self.canvas.create_line(CELL_SIZE * n, 0, CELL_SIZE * n, WINDOW_SIZE, width=GRID_LINE_WIDTH, fill=GRID_COLOR)
			# Draw Horizontal Line
			self.canvas.create_line(0, CELL_SIZE * n, WINDOW_SIZE, CELL_SIZE * n, width=GRID_LINE_WIDTH, fill=GRID_COLOR)

	def gameover_screen(self, result):
		# Clear everything
		self.canvas.delete("all")

		# Base on result, change the text & color for display
		if result == "X WINS":
			winText = "X wins!"
			winColor = X_COLOR

		elif result == "O WINS":
			winText = "O wins!"
			winColor = O_COLOR

		elif result == "DRAW":
			winText = "Draw"
			winColor = DRAW_COLOR

		self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill=winColor, outline="") 
		self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/2), text=winText, fill="white", font=("Franklin Gothic", int(-WINDOW_SIZE/6), "bold"))
		self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/1.65), text="[CLICK TO PLAY AGAIN]", fill="white", font=("Franklin Gothic", int(-WINDOW_SIZE/25), "bold"))

	# Handling the click event
	def click(self, event):
		# check which position did the player click
		x = self.ptgrid(event.x)
		y = self.ptgrid(event.y)

		# If the player is in title screen, go to a new game screen
		if self.gamestate == STATE_TITLE_SCREEN:
			self.new_board()
			self.gamestate = FIRST_PLAYER

		# If it is X's turn and the grid it clicked is empty, we put X there
		elif (self.gamestate == STATE_X_TURN and self.board[y][x] == EMPTY):
			self.new_move(X, x, y)

			if self.has_won(X):
				self.gamestate = STATE_GAME_OVER
				self.gameover_screen("X WINS")

			elif self.is_a_draw():
				self.gamestate = STATE_GAME_OVER
				self.gameover_screen("DRAW")

			else:
				self.gamestate = STATE_O_TURN

		# If it is O's turn and the grid it clicked is empty, we put O there
		elif (self.gamestate == STATE_O_TURN and self.board[y][x] == EMPTY):
			self.new_move(O, x, y)

			if self.has_won(O):
				self.gamestate = STATE_GAME_OVER
				self.gameover_screen("O WINS")

			elif self.is_a_draw():
				self.gamestate = STATE_GAME_OVER
				self.gameover_screen("DRAW")

			else:
				self.gamestate = STATE_X_TURN

		# If we are in game over screen and restart the game
		elif self.gamestate == STATE_GAME_OVER:
			self.new_board()
			self.gamestate = FIRST_PLAYER

	# Make a move and draw the result on the board
	def new_move(self, player, grid_x, grid_y):
		if player == X:
			self.draw_X(grid_x, grid_y) # draw the result to display
			self.board[grid_y][grid_x] = X # add the symbol to the array for checking later

		elif player == O:
			self.draw_O(grid_x, grid_y) # draw the result to display
			self.board[grid_y][grid_x] = O # add the symbol to the array for checking later

	# To draw and display the symbol "X"
	def draw_X(self, grid_x, grid_y):
		# Getting coordinates for the center point of the grid
		x = self.gtpix(grid_x)
		y = self.gtpix(grid_y)
		# Variable "delta" for adjusting position of the symbol
		delta = CELL_SIZE / 2 * SYMBOL_SIZE

		# Drawing the 2 strokes for the symbol "X"
		self.canvas.create_line(x-delta, y-delta, x+delta, y+delta, width=SYMBOL_WIDTH, fill=X_COLOR)
		self.canvas.create_line(x-delta, y+delta, x+delta, y-delta, width=SYMBOL_WIDTH, fill=X_COLOR)


	# To draw and display the symbol "O"
	def draw_O(self, grid_x, grid_y):
		# Getting coordinates for the center point of the grid
		x = self.gtpix(grid_x)
		y = self.gtpix(grid_y)
		# Variable "delta" for adjusting position of the symbol
		delta = CELL_SIZE / 2 * SYMBOL_SIZE

		# Drawing the symbol "O"
		self.canvas.create_oval(x-delta, y-delta, x+delta, y+delta, width=SYMBOL_WIDTH, outline=O_COLOR)

	# Check if either player wins
	def has_won(self, symbol):
		# Check Horizontally
		for i in range(3):
			if self.board[i] == [symbol, symbol, symbol]:
				return True

		# Check Vertically
		for i in range(3):
			if self.board[0][i] == self.board[1][i] == self.board[2][i] == symbol:
				return True

		# Check Diagonally
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
			return True

		elif self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
			return True

		# If nothing matched above conditions
		return False

	# Cbeck if all the slots are filled
	def is_a_draw(self):
		# Loop through each row in the board array
		for row in self.board:
			# Check if "EMPTY" is inside the row
			if EMPTY in row:
				return False

		# If no EMPTY is found - all slots are filled
		return True

	# Get the center x, y coordinates of a grid
	def gtpix(self, grid_coor):
		pixel_coor = grid_coor * CELL_SIZE + CELL_SIZE / 2
		return pixel_coor

	# Get the grid index from the click's coordinates
	def ptgrid(self, pixel_coor):
		# To be safe - if the user clicked on somewhere beyond the screen
		if pixel_coor >= WINDOW_SIZE:
			pixel_coor = WINDOW_SIZE - 1

		# Converting the pixel's coordinate into grid's index
		grid_coor = int(pixel_coor / CELL_SIZE)
		return grid_coor

	# Exit Function
	def exit(self, event):
		self.destroy()

def main():
	root = Game()
	root.mainloop()

main()









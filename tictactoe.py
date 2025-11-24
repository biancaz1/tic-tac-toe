import tkinter


def set_tile(row: int, col: int) -> None:
    """Set the desired board tile to the correct player
    """
    global current_player

    if game_over:
        return

    if board[row][col]["text"] != "":  # spot already taken
        return

    board[row][col]["text"] = current_player

    # switch current player
    if current_player == playerX:
        current_player = playerO
    else:
        current_player = playerX
    label["text"] = current_player + "'s turn"

    check_winner()


def check_winner() -> None:
    """Check for a winner
    """
    global turns, game_over
    turns += 1

    # check vertical
    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] and board[0][col]["text"] != "":
            label.config(text=board[0][col]["text"] + " wins!", foreground=colour_green)
            for row in range(3):
                board[row][col].config(foreground=colour_green, background=colour_light_grey)
            game_over = True
            return

    # check horizontal
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            label.config(text=board[row][0]["text"] + " wins!", foreground=colour_green)
            for col in range(3):
                board[row][col].config(foreground=colour_green, background=colour_light_grey)
            game_over = True
            return

    # check diagonal
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        label.config(text=board[0][0]["text"] + " wins!", foreground=colour_green)
        for i in range(3):
            board[i][i].config(foreground=colour_green, background=colour_light_grey)
        game_over = True
        return

    # check second diagonal
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        label.config(text=board[0][2]["text"] + " wins!", foreground=colour_green)
        board[0][2].config(foreground=colour_green, background=colour_light_grey)
        board[1][1].config(foreground=colour_green, background=colour_light_grey)
        board[2][0].config(foreground=colour_green, background=colour_light_grey)
        game_over = True
        return

    # check tie
    if turns == 9:
        game_over = True
        label.config(text="Tie Game", foreground=colour_green)


def new_game() -> None:
    """Reset game board
    """
    global turns, game_over, current_player

    current_player = playerX
    turns = 0
    game_over = False

    label.config(text=current_player + "'s turn", foreground="white")
    for row in range(3):
        for col in range(3):
            board[row][col].config(text="", foreground=colour_blue, background=colour_grey)


def click_effect(widget) -> None:
    """Create clicking effect
    """
    widget.config(relief="sunken")
    widget.after(200, lambda:widget.config(relief="solid"))


def resize_fonts():
    """Updates font size accordingly
    """
    tile_width = board[0][0].winfo_width()
    tile_height = board[0][0].winfo_height()
    tile_size = min(tile_width, tile_height)

    font_size = max(10, int(tile_size * 0.45))

    for row in range(3):
        for col in range(3):
            board[row][col].config(font=("Consolas", font_size, "bold"))


# game setup
playerX = "X"
playerO = "O"
current_player = playerX
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
colour_blue = "#4584B6"
colour_green = "#028A0F"
colour_grey = "#343434"
colour_light_grey = "#646464"

turns = 0
game_over = False

# window setup
window = tkinter.Tk()
window.title("Tic Tac Toe")
window.geometry("450x500")

frame = tkinter.Frame(window)
for i in range(3):
    frame.grid_rowconfigure(i + 1, weight=1)
    frame.grid_columnconfigure(i, weight=1)
label = tkinter.Label(
    frame,
    text=current_player + "'s turn",
    font=("Consolas", 20, "bold"),
    background=colour_grey,
    foreground="white"
)
label.grid(row=0, column=0, columnspan=3, sticky="we")
for r in range(3):
    for c in range(3):
        tile = tkinter.Label(
            frame,
            text="",
            font=("Consolas", 50, "bold"),
            background=colour_grey,
            foreground=colour_blue,
            borderwidth=2,
            relief="solid",
            anchor="center"
        )
        tile.bind("<Button-1>", lambda event, r=r, c=c: (click_effect(event.widget), set_tile(r, c)))
        board[r][c] = tile
        tile.grid(row=r+1, column=c, sticky="nsew")
        tile.grid_propagate(False)
        tile.config(width=1, height=1)
restart_button = tkinter.Label(
    frame,
    text="restart",
    font=("Consolas", 20),
    background=colour_grey,
    foreground="white",
    command=new_game()
)
restart_button.bind("<Button-1>", lambda event: (click_effect(event.widget), new_game()))
restart_button.grid(row=4, column=0, columnspan=3, sticky="we")
frame.pack(expand=True, fill="both")

# center the window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int(screen_width/2 - window_width/2)
window_y = int(screen_height/2 - window_height/2)
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.bind("<Configure>", lambda event: resize_fonts())
window.mainloop()

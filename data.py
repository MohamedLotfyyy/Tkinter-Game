from tkinter import Tk, Canvas, PhotoImage, Label, Pack, Place, Button, Entry, END, Toplevel, Listbox
from PIL import ImageTk, Image
import random
import json
import time
window = Tk()
width = 1440
height = 900
canvas = Canvas(window, width = width, height = height, bg = "red", bd=0, highlightthickness=0)
canvas.pack()

"""0) configuring the window"""
def configureWindow():
    window.geometry("1440x900")
    window.title("Bounce Game")

background_image = Image.open("space.jpg")
background_image = background_image.resize((1450, 900))
background_img = ImageTk.PhotoImage(background_image)
canvas.create_image(0,0, image = background_img, anchor = "nw")

menu_img = Image.open("menu.png")
menu_img = menu_img.resize((50,50))
menu_icon = ImageTk.PhotoImage(menu_img)

'''1) get the username input'''
def username_input():
    global username_box, username_label, input_btn1, username_label, welcome_label, game_end_label
    '''menu_btn = Button(canvas, image = menu_icon, borderwidth = 0, command = game_menu)
    menu_btn_wind = canvas.create_window(80, 60, window = menu_btn, height = 65, width = 75)'''
    canvas.bind("<Return>", boss_key)
    if game_ended:
        game_end_label = canvas.create_text(505, 300, anchor = "nw", text = "Game has ended. You lost.", font = "Times 40 bold", fill = "#fff")
        menu_btn = Button(canvas, image = menu_icon, borderwidth = 0, command = game_menu)
        menu_btn_wind = canvas.create_window(80, 60, window = menu_btn, height = 65, width = 75)
    elif game_ended ==False:
        welcome_label = canvas.create_text(460, 300, anchor = "nw", text = "Welcome to the Bounce Game.", font = "Times 40 bold", fill = "#fff")
    username_label = canvas.create_text(500, 350, anchor = "nw", text = "Please enter your first and last name in the box below.", font = "Times 20 bold", fill = "#fff")
    username_box = Entry(window)
    username_box.place(relx = 0.5, rely = 0.5, anchor = "center")
    input_btn1 = Button(window, text = "Register", command = save_username, font = 'calibri 20 bold', foreground = 'blue')
    input_btn1.place(relx = 0.5, rely = 0.55, anchor = "center")
    

username_list = []
def save_username():
    global username
    username = username_box.get()
    username_list.append(username)
    print(username_list)
    username_box.delete(0, END)
    input_btn1.destroy()
    username_box.destroy()
    canvas.delete("all")
    title_screen()

'''2) creating the canvas_elements'''
def canvas_elements():
    global ball, paddle, paddle2, paddle3, last_rectangle, score, start, data, ball_coords, paddle_coords, ball
    ball = canvas.create_oval(670, 675, 695, 700, fill = "yellow") 
    ball_coords = canvas.coords(ball)
    paddle = canvas.create_rectangle(600, 775, 800, 775, fill = "white", width = 10, outline = "white")
    paddle_coords = canvas.coords(paddle)
    paddle2 = canvas.create_rectangle(120, 250, 370, 250, fill = "white", width = 10, outline = "white")
    paddle3 = canvas.create_rectangle(1070, 250, 1330, 250, fill = "white", width = 10, outline = "white")
    last_rectangle = canvas.create_rectangle(575, 150, 825, 150, fill = "white", width = 10, outline = "white")

'''3) the title screen that specifies if we wand to start or go to menu'''
def title_screen():
    global start, open_menu, press_start
    menu_btn = Button(canvas, image = menu_icon, borderwidth = 0, command = game_menu)
    menu_btn_wind = canvas.create_window(80, 60, window = menu_btn, height = 65, width = 75)
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    press_start = canvas.create_text(725, 385, text = "Press the Space bar to start!!", font="Times 30 bold", fill = "white")
    canvas.bind('<space>', onSpace)
    canvas.bind("<Return>", boss_key)
    canvas.bind("<Escape>", pauseGame)
    canvas.focus_set()
    start = False
    open_menu = False

def clearTitle():
    for widgets in window.winfo_children():
        widgets.destroy()

'''4) these are the functions that moves the ball, bounces the ball'''
ball = ""
x = 5
y = 5
level_up = False
def move_ball():
    global x, y, ball_move_var, score, level_up
    canvas.move(ball, x, y)
    ball_move_var = canvas.after(10, move_ball)

direction = None
empty_list = []
with open("coords_file", "w") as coordsFile:
        json.dump(empty_list, coordsFile)

def bounce_ball():
    global x, y, width, collision, score, paddle, canvas, paddle_coords, ball_bounce_var
    ball_coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle)
    collision = canvas.find_overlapping(paddle_coords[0], paddle_coords[1], paddle_coords[2], paddle_coords[3])
    collision = list(collision)
    canvas.bind("1", score_increment)
    canvas.bind("2", score_1000)
    canvas.bind("3", x_y_speed)
    canvas.bind("4", x_y_decrease1)
    canvas.bind("5", paddle_fill)
    canvas.bind("6", ball_bigger)
    if ball_coords[0] <= 0:
        x = -x
    elif ball_coords[2] >= width:
        x = -x
    elif ball_coords[1] <= 0:
        y = -y
    elif ball in collision:
        y = -y
        score_update()
    elif ball_coords[3] >800:
        game_end()
    elif score == 6:
        x = y = 7
    elif score == 12:
        x = 8
        y = 8
    elif score == 18:
        x = 9
        y = 9
    elif score == 24:
        x = 10
        y = 10
    ball_bounce_var = canvas.after(10, bounce_ball)
    #ball_bounce_var = canvas.after(10, bounce_ball)

def bounce_other_paddles():
    global paddle2, paddle3, last_rectangle, ball, y, canvas, bounce_paddle_variable
    paddle2_coords = canvas.coords(paddle2)
    paddle3_coords = canvas.coords(paddle3)
    last_rectangle_coords = canvas.coords(last_rectangle)
    paddle2_collision = canvas.find_overlapping(paddle2_coords[0], paddle2_coords[1], paddle2_coords[2], paddle2_coords[3])
    paddle2_collision = list(paddle2_collision)
    paddle3_collision = canvas.find_overlapping(paddle3_coords[0], paddle3_coords[1], paddle3_coords[2], paddle3_coords[3])
    paddle3_collision = list(paddle3_collision)
    last_rec_collision = canvas.find_overlapping(last_rectangle_coords[0], last_rectangle_coords[1], last_rectangle_coords[2], last_rectangle_coords[3])
    last_rec_collision = list(last_rec_collision)
    if (ball in paddle2_collision):
        y = -y
    elif ball in paddle3_collision:
        y = -y
    elif ball in last_rec_collision:
        y = -y
    bounce_paddle_variable = canvas.after(10, bounce_other_paddles)
"""5) these 2 functions which starts the game when button is clicked"""
def start_game():
    global start, canvas, ball, paddle, ball_move_var, ball_bounce_var, ball_coords, paddle2, paddle3, last_rectangle, data, x, y
    score = 0
    Label.configure(score_label, text = "score" + str(score))
    canvas.delete("all")
    canvas.bind("<Return>", boss_key)
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    canvas_elements()
    canvas.bind('<Left>', leftKey)
    canvas.bind('<Right>', rightKey)
    start = True
    if  start == True:
        ball_move_var = canvas.after(10, move_ball)
        ball_bounce_var = canvas.after(10,bounce_ball)
        canvas.after(1, bounce_other_paddles)

def onSpace(event):
    global game_started
    game_started = True
    if game_started:
        start_game()

'''6) moving the paddle left and right'''
def leftKey(event):
    global paddle
    left = -50
    canvas.move(paddle, left, 0)
    
def rightKey(event):
    global paddle
    right = 50
    canvas.move(paddle, right, 0)

'''7) the score functions'''
score = 0
score_label = Label( text = "Score: " + str(score), font = "Times 25 bold")
def score_update():
    global score, collision, score_label
    score_label = Label( text = "Score: " + str(score), font = "Times 25 bold")
    score_label.place(relx = 0.9, rely = 0.05)
    if ball in collision:
        score = score + 1
        return True
    game_end()

'''8) function that pauses and unpauses the game'''
game_paused = False
def pauseGame(event):
    global start, game_started, game_paused, score, continue_button, data, ball_coords, paddle_coords, direction, save_game_button
    game_started = True
    game_paused = True 
    canvas.bind("<Return>", boss_key)
    if game_started == True:
        canvas.after_cancel(ball_bounce_var)
        canvas.after_cancel(ball_move_var)
        ball_coords = canvas.coords(ball)
        paddle_coords = canvas.coords(paddle)
        continue_button = Button(canvas, text = "Resume", font = "Helvetica 20", bg="cyan", command = continue_game)
        continue_button.place(relx = 0.5, rely = 0.45, anchor = "center")
        save_game_button = Button(window, text = "Save game", font = "Helvetica 20", bg="cyan", command = save_game)
        save_game_button.place(relx = 0.5, rely = 0.5, anchor = "center")
        data = {
        "ball_coordinates": ball_coords,
        "paddle_coordinates": paddle_coords,
        "score_count": score,
        "ball_direction": direction
        }

def continue_game():
    global game_paused, ball_bounce_var, ball_move_var, continue_button
    game_paused = False
    canvas.bind("<Return>", boss_key)
    continue_button.destroy()
    save_game_button.destroy()
    if game_paused == False:
        ball_move_var = canvas.after(10, move_ball)    
        canvas.after(10, bounce_ball)  

'''9) functions that end and restart the game'''
score_list = []
game_ended = False
def game_end():
    global game_ended, score, end_label, welcome_label, end_game_label, score_list, leaderboard_dict, username_list, number_games, new_dict, x, y
    score_list.append(score)
    print(score_list)
    game_ended = True
    game_ended = True
    canvas.delete("all")
    if game_ended == True:
        score = 0
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    username_input()
    canvas.after_cancel(ball_move_var)
    canvas.bind("<Return>", boss_key)
    canvas.bind("<space>", restart_game)
    
def restart_game(event):
    global score
    score = 0
    Label.configure(score_label, text = "score" + str(score))
    start_game()


def game_menu():
    global welcome_label, press_start, start_btn, load_game_button, leaderboard_btn, customize_binds, cheat_codes_button
    canvas.delete("all")
    canvas.bind("<Return>", boss_key)
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    start_btn = Button(text = "Start Game", font = "Helvetica 20 bold", command = start_game_menu)
    start_btn.place(relx = 0.5, rely = 0.40, anchor = "center")
    leaderboard_btn = Button(text = "Leaderboard", font = "Helvetica 20 bold", command = create_leaderboard)
    leaderboard_btn.place(relx = 0.5, rely = 0.45, anchor = "center")
    load_game_button = Button(text = "Load game", font = "Helvetica 20 bold", command = load_game)
    load_game_button.place(relx = 0.5, rely = 0.5, anchor = "center")
    cheat_codes_button = Button(text = "Cheat codes", font = "Helvetica 20 bold", command = cheat_code_display)
    cheat_codes_button.place(relx = 0.5, rely = 0.55, anchor = "center")
    customize_binds = Button(text = "Customize Contronls", font = "Helvetica 20 bold", command = choose_binds)
    customize_binds.place(relx = 0.5, rely = 0.60, anchor = "center")

    username_box.destroy()
    input_btn1.destroy()
    score_label.destroy()
    

def start_game_menu():
    global x, y
    x = 5
    y = 5
    start_btn.destroy()
    leaderboard_btn.destroy()
    load_game_button.destroy()
    customize_binds.destroy()
    cheat_codes_button.destroy()
    start_game()

'''10) the functions that create the leaderboard and everything inside of it'''
def create_leaderboard():
    global username, username_list, score_list
    leaderboard_dict = {}
    for key in username_list:
        for value in score_list:
                if value == 0:
                    leaderboard_dict[key] = value
                elif value > 0:
                    leaderboard_dict[key] = value - 1
                score_list.remove(value)
                with open("save_name", "r") as new_file:
                    data2 = json.load(new_file)
                data2.update(leaderboard_dict)
                with open("save_name", "w") as new_file:
                    json.dump(data2, new_file)
    with open("save_name", "r") as new_file:
         data3 = json.load(new_file)
         data3 = dict(sorted(data3.items(), key=lambda kv: kv[1], reverse=True))
         print(data3)
    new_window = Toplevel(window)
    new_window.title("Leaderboard")
    display_listbox = Listbox(new_window)
    display_listbox.pack()
    display_listbox.insert(END, "Username: Score")
    for key in data3:
        display_listbox.insert(END, '{}: {}'.format(key, data3[key]))

'''11) BOSS KEY'''
boss_img = Image.open("mymanchester.jpg")
boss_img = boss_img.resize((1450, 900))
boss_image = ImageTk.PhotoImage(boss_img)
def boss_key(event):
    boss_window = Toplevel(window)
    boss_window.geometry("1920x1080")
    boss_window.title("University of Manchester")
    boss_canvas = Canvas(boss_window, width= 1920, height =1080)
    boss_canvas.create_image(0,0, image = boss_image, anchor = "nw")
    boss_canvas.pack()

level = 0
    
'''12) this is the code that saves the game'''
def save_game():
    global data, file_saved, ball_coords
    with open("game_saved", "w") as file_saved:
        json.dump(data, file_saved)
def move_ball2():
    global x, y, ball_move_var, direction
    canvas.move(ball, x, y)
    canvas.after(10, move_ball2)

def load_game():
    global game_started
    game_started = True
    load_text = canvas.create_text(530, 380, anchor = "nw", text = "Press Space to load the game.", font = "Times 30 bold", fill = "white")
    canvas.bind("<space>", load_positions)
    start_btn.destroy()
    leaderboard_btn.destroy()
    load_game_button.destroy()
    customize_binds.destroy()
    cheat_codes_button.destroy()

def load_positions(event):
    start_game2()
def start_game2():
    global file_saved, score, paddle, start, canvas, ball, paddle2, paddle3, last_rectangle, x, y
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    with open("game_saved", "r") as file_saved:
        file_1 = json.load(file_saved)
        my_list = list(file_1.values())
        print(my_list)
        score = file_1['score_count']
        paddle2 = canvas.create_rectangle(120, 250, 370, 250, fill = "white", width = 10, outline = "white")
        paddle3 = canvas.create_rectangle(1070, 250, 1330, 250, fill = "white", width = 10, outline = "white")
        last_rectangle = canvas.create_rectangle(575, 150, 825, 150, fill = "white", width = 10, outline = "white")
        ball = canvas.create_oval(int(my_list[0][0]), int(my_list[0][1]), int(my_list[0][2]), int(my_list[0][3]), fill = "yellow") 
        paddle = canvas.create_rectangle(int(my_list[1][0]), int(my_list[1][1]), int(my_list[1][2]), int(my_list[1][3]), fill = "white", width = 10, outline = "white")
        start = True
        x = 5
        y = 5
        if  start == True:
            canvas.after(10, move_ball2)
            canvas.after(10, bounce_ball)
            bounce_paddle_variable = canvas.after(1, bounce_other_paddles)

'''13) cheat codes'''
def score_increment(event):
    global score
    score = score + 1
def score_1000(event):
    global score
    if score < 1000:
        score = 1000
    if score > 1000:
        score = score + 1000
def x_y_speed(event):
    global x, y
    x = -3
    y = -3
def  x_y_decrease1(even):
    global x, y
    if x > 1 and y > 1:
        x = x - 1
        y = y - 1

def paddle_fill(event):
    global paddle, width
    canvas.delete("paddle")
    paddle = canvas.create_rectangle(0, 775, width, 775, width = 10, fill = "white", outline = "white")

def ball_bigger(event):
    global ball, ball_coords, paddle
    canvas.delete("all")
    canvas.create_image(0,0, image = background_img, anchor = "nw")
    ball = canvas.create_oval(640, 645, 725, 730, fill = "yellow")
    paddle = canvas.create_rectangle(620, 775, 820, 775, fill = "white", width = 10, outline = "white")
cheat_codes = {
    "Cheat Key": "Cheat effect",
    "press 1": "score + 1",
    "press 2": "score + 1000",
    "press 3": "speed slower",
    "press 4": "speed - 1",
    "press 5": "bigger paddle",
    "press 6": "Bigger ball and remove obstacles"
}

def cheat_code_display():
    global cheat_codes
    cheat_window = Toplevel(window)
    cheat_window.title("Cheat Codes")
    cheat_window.geometry("300x300")
    display_cheat = Listbox(cheat_window)
    display_cheat.pack(padx=10,pady=10,fill="both", expand=True)
    for key in cheat_codes:
        display_cheat.insert(END, '{}: {}'.format(key, cheat_codes[key]))

'''14) user chooses his binds'''
def choose_binds():
    global right_entry, left_entry
    binds_window = Toplevel(window)
    binds_window.title("Cheat Codes")
    binds_window.geometry("1440x900")
    binds_canvas = Canvas(binds_window, width= 1440, height =900)
    binds_canvas.create_image(0,0, image = background_img, anchor = "nw")
    binds_canvas.pack()
    binds_text = binds_canvas.create_text(420, 250, anchor = "nw", text = "Enter the bind to move the paddle to the left from the options below", font = "calibri 20 bold", fill = "white")
    left_entry = Entry(binds_window)
    left_entry.place(relx = 0.5, rely = 0.38, anchor = "center")
    binds_text2 = binds_canvas.create_text(420, 370, anchor = "nw", text = "Enter the bind to move the paddle to the right from the options below", font = "calibri 20 bold", fill = "white")
    right_entry = Entry(binds_window)
    right_entry.place(relx = 0.5, rely = 0.53, anchor = "center")
    options = binds_canvas.create_text(360, 490, anchor = "nw",  text = "a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, 7, 8, 9, <Up>, <Down>", font = "calibri 20 bold", fill = "white")
    get_btn1 = Button(binds_window, text = "submit left mouvement", font = "calibri 20 bold", foreground = "blue", command = leftBind)
    get_btn1.place(relx = 0.5, rely = 0.43, anchor = "center")
    get_btn2 = Button(binds_window, text = "submit right mouvement", font = "calibri 20 bold", foreground = "blue",  command = rightBind)
    get_btn2.place(relx = 0.5, rely = 0.58, anchor = "center")

def leftBind():
    global left_bind
    left_bind = left_entry.get()
    canvas.bind(left_bind, leftKey)
    print(left_bind)

def rightBind():
    global right_bind
    right_bind = right_entry.get()
    canvas.bind(right_bind, rightKey)
    print(right_bind)
username_input()
configureWindow()
window.mainloop()
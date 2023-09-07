# import utilities
from graphics import Canvas
import time
import random

# Constant Variables    
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
SIZE = 20
DELAY = 0.05

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    game_cover(canvas)
    welcome_screen(canvas)
    action_button_click(canvas)
    n_of_meals = set_number_of_meals(canvas)
    cooked_number = cook_digits(canvas, n_of_meals)
    is_meal_cooked(cooked_number, canvas, n_of_meals)
    
    
def set_number_of_meals(canvas):
    instruction1 = "Use Left and Right Key to adjust the number of meals at a time"
    n = 1
    
    canvas.create_text(50, 200, font="Poppins", font_size=20, text=instruction1, color='blue')
    number_of_meals = canvas.create_text(190, 300, font="Poppins", font_size=54, text=f"<<   {n}   >>", color='black')
    
    # Button Design
    canvas.create_rectangle(250, 450, 350, 510, '#0B0775')
    canvas.create_text(260, 465, font="Poppins", font_size=30, text="PLAY", color='white')
    
    # Clicking the button will clear the previous canvas
    click = canvas.get_last_click()
    if click!=None:
        x, y = click
    else:
        x = 0
        y = 0
    
    # key setup
    key = canvas.get_last_key_press()
        
    while True:
        print(x, y)
        if (x >= 250 and x <= 350) and (y >= 450 and y <= 510):
            break;
        click = canvas.get_last_click()
        if click!=None:
            x, y = click
        if key == 'ArrowLeft':
            if n > 1:
                n -= 1
                canvas.delete(number_of_meals)
                number_of_meals = canvas.create_text(190, 300, font="Poppins", font_size=54, text=f"<<   {n}   >>", color='black')
        if key == 'ArrowRight':
            if n < 50:
                n += 1
                canvas.delete(number_of_meals)
                number_of_meals = canvas.create_text(190, 300, font="Poppins", font_size=54, text=f"<<   {n}   >>", color='black')
        key = canvas.get_last_key_press()
    canvas.clear()
    return n
 
def is_meal_cooked(cooked_number, canvas, n_of_meals):
    if len(cooked_number) != n_of_meals:
        canvas.create_text(150, 100, font="Poppins", font_size=50, text="GAME OVER", color='red')
    else:
        canvas.create_text(150, 100, font="Poppins", font_size=50, text="DECLICIOUS", color='#0B0775')
        
        take_out_msg1 = "Stage 1 Cleared. Now the meals are served to the destinated place."
        take_out_msg2 = "Guide the YETI in Stage 2 for take out"
        canvas.create_rectangle(90, 350, 510, 420, '#6fbbc9')
        canvas.create_text(95, 380, font="Poppins", font_size=15, text=take_out_msg1, color='black')
        canvas.create_text(200, 400, font="Poppins", font_size=15, text=take_out_msg2, color='black')
        # Button Design
        canvas.create_rectangle(250, 450, 350, 510, '#0B0775')
        canvas.create_text(255, 465, font="Poppins", font_size=30, text="SERVE", color='white')
        
        action_button_click(canvas)
        take_out_map = serve_meal(canvas, cooked_number)
        take_out(canvas, take_out_map, n_of_meals)
    
def serve_meal(canvas, cooked_number):
    meal_locations = []
    for i in range(len(cooked_number)):
        meal_locations.append(set_meal(canvas, cooked_number[i]))
    return meal_locations
    
def set_meal(canvas, meal):
    meal_x = generate_random_coordinate()
    meal_y = generate_random_coordinate()
    meal_plate = canvas.create_oval(meal_x, meal_y, meal_x+20, meal_y+20, '#6fbbc9')
    put_meal = canvas.create_text(meal_x+5, meal_y+2, font="Poppins", font_size=20, text=meal, color='black')
    meal_points = [meal_x, meal_y, meal_plate, put_meal]
    return meal_points

def take_out(canvas, take_out_map, n_of_meals):
    player_start_x = 0
    player_start_y = 0
    player_size = 20
    player = canvas.create_image_with_size(player_start_x, player_start_y, player_size, player_size, "yeti.jpg")
    
    points = 0
    ok = True
    key = 'ArrowRight'
    while ok:
        if points == n_of_meals:
            break
        if key == 'ArrowRight':
            key = canvas.get_last_key_press()
            if isGoal(canvas, player_start_x, player_start_y, take_out_map):
                points += 1
            while key != 'ArrowRight' and key != 'ArrowLeft' and key != 'ArrowUp' and key != 'ArrowDown':
                if player_start_x + 20 <= CANVAS_WIDTH-20:
                    if isGoal(canvas, player_start_x+20, player_start_y, take_out_map):
                        points += 1
                    player_start_x += 20
                    canvas.moveto(player, player_start_x, player_start_y)
                    time.sleep(DELAY)
                else:
                    ok = False
                    break
                key = canvas.get_last_key_press()
        elif key == 'ArrowLeft':
            key = canvas.get_last_key_press()
            if isGoal(canvas, player_start_x, player_start_y, take_out_map):
                points += 1
            while key != 'ArrowRight' and key != 'ArrowLeft' and key != 'ArrowUp' and key != 'ArrowDown':
                if player_start_x - 20 >= 0:
                    if isGoal(canvas, player_start_x-20, player_start_y, take_out_map):
                        points += 1
                    player_start_x -= 20
                    canvas.moveto(player, player_start_x, player_start_y)
                    time.sleep(DELAY)
                else:
                    ok = False
                    break
                key = canvas.get_last_key_press()
        elif key == 'ArrowUp':
            key = canvas.get_last_key_press()
            if isGoal(canvas, player_start_x, player_start_y, take_out_map):
                points += 1
            while key != 'ArrowRight' and key != 'ArrowLeft' and key != 'ArrowUp' and key != 'ArrowDown':
                if player_start_y - 20 >= 0:
                    if isGoal(canvas, player_start_x, player_start_y-20, take_out_map):
                        points += 1
                    player_start_y -= 20
                    canvas.moveto(player, player_start_x, player_start_y)
                    time.sleep(DELAY)
                else:
                    ok = False
                    break
                key = canvas.get_last_key_press()
        else:
            key = canvas.get_last_key_press()
            if isGoal(canvas, player_start_x, player_start_y, take_out_map):
                points += 1
            while key != 'ArrowRight' and key != 'ArrowLeft' and key != 'ArrowUp' and key != 'ArrowDown':
                if player_start_y + 20 <= CANVAS_HEIGHT-20:
                    if isGoal(canvas, player_start_x, player_start_y+20, take_out_map):
                        points += 1
                    player_start_y += 20
                    canvas.moveto(player, player_start_x, player_start_y)
                    time.sleep(DELAY)
                else:
                    ok = False
                    break
                key = canvas.get_last_key_press()
    if points>=n_of_meals:
        canvas.create_text(150, 100, font="Poppins", font_size=50, text="TASTY MEAL!", color='#0B0775')
        canvas.create_text(140, 250, font='Arial', font_size = 20, text=f"Your Score is {points} The King is Happy!", color='black')
    else:
        canvas.create_text(150, 100, font="Poppins", font_size=50, text="GAME OVER", color='red')

def isGoal(canvas, player_start_x, player_start_y, take_out_map):
    # Checks if the current state is goal state
    ok = False
    for i in range(len(take_out_map)):
        if i < len(take_out_map):
            meal_points = take_out_map[i]
            if meal_points[0] == player_start_x and player_start_y == meal_points[1]:
                ok = True
                canvas.delete(meal_points[2])
                canvas.delete(meal_points[3])
                take_out_map.remove(meal_points)
        else:
            break
    return ok
    
def cook_digits(canvas, n_of_meals):
    # Returns a number of random digits, the number is the dish for the snake king
    
    number_of_digits = n_of_meals
    cooked_number = ""
    
    plate_x = 0
    plate_y = 540
    plate_width = 60
    plate_height = 560
    plate = canvas.create_rectangle(plate_x, plate_y, plate_width, plate_height, "#0B0775")
    for i in range(number_of_digits):
        random_digit = random.randint(0, 9)
        digit_x = generate_random_coordinate()
        digit_y = 20
        digit = canvas.create_text(digit_x, digit_y, font="Poppins", font_size=SIZE, text=str(random_digit), color='#0B0775')
        digit_y += 20
        digit_plate = canvas.create_oval(digit_x, digit_y, digit_x+20, digit_y+20, 'white')
        canvas.set_outline_color(digit_plate, '#0B0775')
        
        while True:
            x = canvas.get_mouse_x()-0.5*plate_width
            y = plate_y
            
            if is_in_plate(x, y, x+plate_width, y+plate_height, digit_x, digit_y):
                cooked_number += str(random_digit)
                canvas.delete(digit_plate)
                canvas.delete(digit)
                break
            
            if x<0:
                x=0
            if x+plate_width>CANVAS_WIDTH:
                x=CANVAS_WIDTH-plate_width
                
            canvas.moveto(plate, x, y)
            if digit_y < 580:
                digit_y += 20
                canvas.moveto(digit_plate, digit_x, digit_y)
                time.sleep(DELAY)
            else:
                canvas.delete(digit)
                break
    
    return cooked_number    
    
def is_in_plate(plate_x, plate_y, plate_width, plate_height, digit_x, digit_y):
    # Checks if the food lands on the plate
    return (digit_x >= plate_x and digit_x <= plate_width) and (digit_y >= plate_y and digit_y <= plate_height)
        
def generate_random_coordinate():
    # Generate new coordinate that is a multiple of 20
    x = random.randint(20, CANVAS_WIDTH-20)
    while x%20 != 0:
        x = random.randint(20, CANVAS_WIDTH-20)
    return x 
    
def welcome_screen(canvas):
    # Present welcome screen with messages and start
    
    # All messages are stored in variables
    welcome_headline = "Welcome to 'Digits Take Out' Mini Game!"
    welcome_description1 = "Cook a Delicious Meal of Digits and Feed the YETI King!"
    welcome_description2 = "If you clear the 2 stages, you won't be killed by the YETI King!"
    stage1_description1 = "Stage 1: You just have to use left and right arrow on"
    stage1_description2 = "keyboard to move the plate. If the plate receives all the numbers,"
    stage1_description3 = "you can move on to the next stage. Remember the digits and"
    stage1_description4 = "order of the digits that you received. It will help you on next stage."
    stage2_description1 = "Stage 2: Guide your YETI to eat all the numbers in "
    stage2_description2 = "the order you received back in stage 1. Be careful with speed and"
    stage2_description3 = "the walls of course."
    
    # Design of the canvas
    canvas.create_text(60, 100, font="Poppins", font_size=30, text=welcome_headline, color='#6fbbc9')
    canvas.create_text(60, 140, font="Poppins", font_size=20, text=welcome_description1, color='black')
    canvas.create_text(50, 170, font="Poppins", font_size=20, text=welcome_description2, color='black')
    canvas.create_rectangle(90, 210, 510, 305, '#6fbbc9')
    canvas.create_text(140, 220, font="Poppins", font_size=15, text=stage1_description1, color='#0B0775')
    canvas.create_text(110, 240, font="Poppins", font_size=15, text=stage1_description2, color='#0B0775')
    canvas.create_text(120, 260, font="Poppins", font_size=15, text=stage1_description3, color='#0B0775')
    canvas.create_text(100, 280, font="Poppins", font_size=15, text=stage1_description4, color='#0B0775')
    canvas.create_rectangle(90, 350, 510, 420, '#6fbbc9')
    canvas.create_text(140, 360, font="Poppins", font_size=15, text=stage2_description1, color='#0B0775')
    canvas.create_text(95, 380, font="Poppins", font_size=15, text=stage2_description2, color='#0B0775')
    canvas.create_text(240, 400, font="Poppins", font_size=15, text=stage2_description3, color='#0B0775')
    
    # Button Design
    canvas.create_rectangle(250, 450, 350, 510, '#0B0775')
    canvas.create_text(255, 465, font="Poppins", font_size=35, text="PLAY", color='white')
    
def game_cover(canvas):
    image = canvas.create_image_with_size(130, 150, 330, 350, "blue_yeti.jpg")
    canvas.create_text(193, 30, font="Poppins", font_size=50, text="D I G I T S", color='#6fbbc9')
    canvas.create_text(145, 80, font="Poppins", font_size=50, text="T A K E  O U T", color='#0B0775')
    
    # Button Design
    canvas.create_rectangle(250, 520, 350, 580, '#0B0775')
    canvas.create_text(255, 535, font="Poppins", font_size=35, text="PLAY", color='white')
    
    click = canvas.get_last_click()
    if click != None:
        x, y = click
    else:
        x = 0
        y = 0
    while True:
        if (x >= 250 and x <= 350) and (y >= 520 and y <= 580):
            break;
        click = canvas.get_last_click()
        if click != None:
            x, y = click
    canvas.clear()
    # start_game(canvas)
    
def action_button_click(canvas):
    # Clicking the button will clear the previous canvas
    click = canvas.get_last_click()
    if click != None:
        x, y = click
    else:
        x = 0
        y = 0
    while True:
        if (x >= 250 and x <= 350) and (y >= 450 and y <= 510):
            break;
        click = canvas.get_last_click()
        if click != None:
            x, y = click
    canvas.clear()
    
    
if __name__ == '__main__':
    main()

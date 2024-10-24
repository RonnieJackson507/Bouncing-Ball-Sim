import os, threading
from os import environ
# Hide the pygame support prompt
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import Ball, Border
import pygame
import tkinter as tk
from tkinter import filedialog as fd
import cv2, pyautogui
import pygetwindow as gw
import numpy as np
import threading
import sounddevice, wave

WIDTH = 400
HEIGHT = int(WIDTH * 1.778)
window_title = "Bouncing Ball Simulator"
FPS = 60

output_video_file = "simulation.mp4"

# Flags to control the recording process
record_flag = False

def record_video():
    # Get the first window that matches the title (if any)
    window = gw.getWindowsWithTitle(window_title)[0] if gw.getWindowsWithTitle(window_title) else None
    recording_window = [WIDTH, HEIGHT] # The window for recording

    # Define codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_file, fourcc, FPS, (recording_window[0], recording_window[1]))    
    
    while record_flag:
        # Add screenshots to the frames array
        img = pyautogui.screenshot(region=(window.left + 8 , window.top + 32 , recording_window[0], recording_window[1]))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

        # Write the frame to the video file
        out.write(frame)

    out.release()

# TODO Add screen recording functionality with audio

# Global file path variables
sound_path = None
img_path = None

# Open a file dialog and get the selected file path
def open_sound():
    global sound_path
    sound_path = fd.askopenfilename(
        title="Select a file",
        filetypes=(("All files", "*.*"),)  # Allow all file types
    )
    if sound_path == "":
        sound_path = None

# Open a file dialog and get the selected file path
def open_image():
    global img_path
    img_path = fd.askopenfilename(
        title="Select a file",
        filetypes=(("All files", "*.*"),)  # Allow all file types
    )
    if img_path == "":
        img_path = None

# Initializes the simulator
def init_sim():
    global record_flag

    # Get the number of balls
    balls_num = int(entry_balls.get())

    # Get the flag for recording the simulator
    record_flag = True if record.get() == 1 else False

    # Destroy the Menu's window
    root.destroy()

    # Start the simulation
    start_sim(balls_num)

# Starts the simulation
def start_sim(balls_num):
    global record_flag

    # Initialize Pygame and the mixer
    pygame.init()
    pygame.mixer.init()

    # Create a screen (window) with aspect ration of 9:16
    CENTER = [WIDTH / 2, HEIGHT / 2]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set title of the window
    pygame.display.set_caption(window_title)

    

    # Increase the number of sound channels
    CHANNELS_NUM = 32
    pygame.mixer.set_num_channels(CHANNELS_NUM)

    # Load sound effects
    try:
        sound_effect = pygame.mixer.Sound(sound_path)
        sound_effect.set_volume(0.05)  # 5% volume
    except pygame.error and TypeError:
        sound_effect = None

    # Load images
    try:
        ball_img = pygame.image.load(img_path).convert_alpha() # Load once
    except pygame.error and TypeError:
        ball_img = None

    # Create a font object
    font = pygame.font.Font(None, 50)

    # Border object
    border = Border.Border(CENTER[0], CENTER[1] - 50, 200, 2)

    # Ball object(s)
    balls = []
    for i in range(0,balls_num):
        balls.append(Ball.Ball(border, sound_effect, i % CHANNELS_NUM, ball_img))

    # Draws the text onto the screen
    def draw_text (text, font, color, surface, x, y):
        # Render the updated collision count
        text_surface = font.render(text, True, color)

        # Get the position of the text
        text_rect = text_surface.get_rect(center = (x, y))

        # Display the text onto the bottom of the screen
        surface.blit(text_surface, text_rect)

    # Main game loop flag
    running = True

    # Recording
    if record_flag:
        # Start the video recording in a separate thread
        video_thread = threading.Thread(target=record_video)
        video_thread.start()

    # Main game loop
    while running:
        # Check for events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color (RGB)
        screen.fill((0, 0, 0))  # Fill with black

        # Draw the border in the center of the screen
        border.draw(screen)

        collision = 0 # Collisions from the ball

        # Traverse through the Balls array
        for ball in balls:
            # Update the ball
            ball.update()

            collision += ball.collision

            # Draw the ball
            ball.draw(screen)

        # Draw the text for the number of balls
        draw_text(f"Balls = {balls_num}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] - 300)

        # Draw the text for the collision
        draw_text(f"Collisions = {collision}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] + 300)

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        pygame.time.Clock().tick(FPS)

    # Release the VideoWriter
    if record_flag:
        record_flag = False
    
        video_thread.join()

    # Quit Pygame
    pygame.quit()

# MENU
# Create the menu window
root = tk.Tk()
root.title("Bouncing Ball Simulator")

# Center and Size the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 275 # Width of the screen
height = 225 # Height of the screen
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(width=False, height=False)

# Colors - Dark Theme
bg_color = "grey20"
text_color = "white"
divider_color = "grey20"
entry_bg_color = "gray30"

# Set background color on the window
root.configure(bg=bg_color)

# Add Weights to the widgets
root.grid_rowconfigure(6, weight=1) # Make the last row expandable

# Input Fields
# Field for number of balls
tk.Label(root, text="Number of Balls:", bg=bg_color, fg=text_color).grid(row=0, column=0, padx=10, pady=5)
entry_balls = tk.Entry(root, bg=entry_bg_color, fg=text_color, insertbackground=text_color, justify="right")
entry_balls.insert(0, "1")
entry_balls.grid(row=0, column=1, padx=10, pady=5, sticky="e")

# Button for grabbing the sound file of the ball
tk.Label(root, text="Ball's Sound:", bg=bg_color, fg=text_color).grid(row=1, column=0, padx=10, pady=5)
tk.Button(root, text="Press to give Sound File", bg=bg_color, fg=text_color, highlightbackground=divider_color, command= open_sound).grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

# Button for grabbing the image file of the ball
tk.Label(root, text="Ball's Image:", bg=bg_color, fg=text_color).grid(row=2, column=0, padx=10, pady=5)
tk.Button(root, text="Press to give Image File", bg=bg_color, fg=text_color, highlightbackground=divider_color, command= open_image).grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

# Checkbox for recording the simulation or not
record = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Record", variable=record,
                              bg=bg_color,
                              fg=text_color,
                              selectcolor=divider_color,
                              activebackground=bg_color,
                              activeforeground=text_color,
                              highlightbackground=text_color).grid(row=3,column=1, columnspan=3, padx=10, pady=10, sticky="ew")

# Button to perform the simulation by quitting the menu
tk.Button(root, text="Simulate Bouncing Balls", bg=bg_color, fg=text_color, highlightbackground=divider_color, command= init_sim).grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Run the Tkinter event loop
root.mainloop()
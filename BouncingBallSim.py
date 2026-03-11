import os, threading, queue
from os import environ
# Hide the pygame support prompt
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import Ball, Border
import pygame
import tkinter as tk
from tkinter import filedialog as fd
import cv2
import numpy as np
import wave, subprocess
import imageio_ffmpeg

# Simulation window parameters
WIDTH = 400
HEIGHT = int(WIDTH * 1.778)
window_title = "Bouncing Ball Simulator"
FPS = 60

output_video_file = "simulation.mp4" # Video of the simulation

# Flags to control the recording process
record_flag = False

# Queue for passing frames from the main loop to the recording thread
frame_queue = queue.Queue(maxsize=120)  # buffer up to 2 seconds of frames at 60 FPS

# Record the frames of the simulation
def record_video():
    # Define codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_file, fourcc, FPS, (WIDTH, HEIGHT))

    while record_flag or not frame_queue.empty():
        try:
            frame = frame_queue.get(timeout=0.1)
            out.write(frame)
        except queue.Empty:
            continue

    out.release()

# Mix bounce sounds at their exact frame timestamps and mux into the video
def mix_and_mux(sound_effect, bounce_events, total_frames):
    freq, _, channels = pygame.mixer.get_init()
    sound_array = pygame.sndarray.array(sound_effect)  # raw audio data from pygame
    volume = 0.05  # match the in-sim volume

    samples_per_frame = freq / FPS
    total_samples = int(total_frames * samples_per_frame)

    # Build silent buffer then mix in each bounce
    if channels == 2:
        audio_buffer = np.zeros((total_samples, 2), dtype=np.float32)
    else:
        audio_buffer = np.zeros(total_samples, dtype=np.float32)

    for frame in bounce_events:
        start = int(frame * samples_per_frame)
        end = start + len(sound_array)
        end_clipped = min(end, total_samples)
        length = end_clipped - start
        audio_buffer[start:end_clipped] += sound_array[:length] * volume

    # Clip to int16 range and convert
    audio_int16 = np.clip(audio_buffer, -32768, 32767).astype(np.int16)

    # Write temp WAV file
    temp_audio = output_video_file + ".tmp_audio.wav"
    temp_video = output_video_file + ".tmp_video.mp4"
    os.rename(output_video_file, temp_video)

    with wave.open(temp_audio, 'w') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit = 2 bytes
        wf.setframerate(freq)
        wf.writeframes(audio_int16.tobytes())

    # Mux video + audio with ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ffmpeg, '-y',
        '-i', temp_video,
        '-i', temp_audio,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_video_file
    ], check=True)

    os.remove(temp_video)
    os.remove(temp_audio)

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

    # Prompt for output file path if recording
    if record_flag:
        global output_video_file
        path = fd.asksaveasfilename(
            title="Save recording as",
            defaultextension=".mp4",
            filetypes=(("MP4 files", "*.mp4"),)
        )
        if path:
            output_video_file = path
        else:
            record_flag = False  # User cancelled, don't record

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

    # Audio tracking for recording
    bounce_events = []
    prev_collisions = [0] * balls_num
    frame_num = 0

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
        for i, ball in enumerate(balls):
            # Update the ball
            ball.update()

            # Track bounce events for audio mixing
            if ball.collision > prev_collisions[i]:
                bounce_events.append(frame_num)
                prev_collisions[i] = ball.collision

            collision += ball.collision

            # Draw the ball
            ball.draw(screen)

        # Draw the text for the number of balls
        draw_text(f"Balls = {balls_num}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] - 300)

        # Draw the text for the collision
        draw_text(f"Collisions = {collision}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] + 300)

        # Update the display
        pygame.display.update()

        # Capture the frame directly from the pygame surface
        if record_flag and not frame_queue.full():
            raw = pygame.surfarray.array3d(screen)
            frame = cv2.cvtColor(raw.transpose(1, 0, 2), cv2.COLOR_RGB2BGR)
            frame_queue.put(frame)

        # Limit the frame rate
        pygame.time.Clock().tick(FPS)

        frame_num += 1

    # Release the VideoWriter
    if record_flag:
        record_flag = False

        video_thread.join()

        # Mix audio into the video if a sound was provided and bounces occurred
        if sound_effect is not None and bounce_events:
            mix_and_mux(sound_effect, bounce_events, frame_num)

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
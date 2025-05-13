from gpiozero import Button
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw
from time import sleep
from RPi import GPIO

from api_manager import send_message

"""
GPIO layout
VCC                     - 1 - 3.3V
SDA                     - GPIO2 
SCL                     - GPIO3
GND                     - 9
BTN-Signal              - GPIO22
Si es un touch-sensor va al reves, el 1 significa que no ha sido tocado

CLK_PIN_ROTARY_ENCODER  - GPIO23
DT_PIN_ROTARY_ENCODER   - GPIO24

LED                     - GPIO5


LESS_VOLUME             - GPIO6
MORE_VOLUME             - GPIO13

"""

BTN_PIN = 22
SCREEN_ADDRESS = 0x3C

CLK_PIN_ROTARY_ENCODER = 23
DT_PIN_ROTARY_ENCODER = 24

LED_PIN = 5

PREV_SONG_PIN = 13
NEXT_SONG_PIN = 6

# Configura el modo de numeración de pines
GPIO.setmode(GPIO.BCM) # The numbers that come after GPIO

# Set the GPIO pins for the rotary encoder
GPIO.setup(CLK_PIN_ROTARY_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT_PIN_ROTARY_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 100)  
pwm.start(0)  # Start with 0% duty cycle
pwm_state = 0


# Inicializa el botón conectado al pin GPIO 22
mute_btn = Button(BTN_PIN)

prev_song_btn = Button(PREV_SONG_PIN)
next_song_btn = Button(NEXT_SONG_PIN)

# Initialize the I2C interface for the Oled display
serial = i2c(port=1, address=SCREEN_ADDRESS)  # Adjust address if needed
device = sh1106(serial)

# Create a blank image
width = device.width
height = device.height

image = Image.new("1", (width, height))
# Create a drawing object
draw = ImageDraw.Draw(image)

def draw_text(acc: bool):
    # Draw something (e.g., a rectangle and text)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((10, 10), f"You have pressed\n the button {acc} times", fill=255)
    device.display(image)


def show_volume(volume: int, mute: bool):
    if not mute:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((10, 10), f"Volume: {volume}%", fill=255)
        device.display(image)
    else:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((10, 10), "Muted", fill=255)
        device.display(image)

def draw_image():
    image_path = "pano.jpg"  # Replace with your image file path
    image = Image.open(image_path)

    # Resize and convert the image to 1-bit monochrome
    image = image.resize((device.width, device.height)).convert("1")

    # Display the image
    device.display(image)

mute = False
volume = 30
clkLastState = GPIO.input(CLK_PIN_ROTARY_ENCODER)
prev_vol = volume
show_volume(volume, mute)


try:
    while True:
        # Calculate PWM duty cycle (0-100%)
        if volume > 0 and not mute:
            pwm_state = volume
        else:
            pwm_state = 0
        try:
            pwm.ChangeDutyCycle(pwm_state / 5)
        except RuntimeError:
            pass

        # Touch volume buttons
        if prev_song_btn.value == 0:
            mute = False
            send_message("previous")
            sleep(0.2)

        if next_song_btn.value == 0:
            mute = False
            send_message("next")
            sleep(0.2)

        # Rotary encoder logic
        clkState = GPIO.input(CLK_PIN_ROTARY_ENCODER)
        dtState = GPIO.input(DT_PIN_ROTARY_ENCODER)
        if clkState != clkLastState:
            mute = False
            if dtState == clkState: # Changing this to != makes it go the other way
                volume = min(100, volume + 1)
            else:
                volume = max(0, volume - 1)
            if volume != prev_vol:
                prev_vol = volume
                show_volume(volume, mute)
            clkLastState = clkState

        # Mute button logic
        if mute_btn.value == 1: # If it is a touch sensor 0, it traditional button 1
            mute = not mute
            pwm.ChangeDutyCycle(0)
            if mute:
                send_message("pause")
            else:
                send_message("play")
            show_volume(volume, mute)
            sleep(0.2)  # Debounce delay
            

        sleep(0.001)
finally:
    pwm.stop()
    GPIO.cleanup()


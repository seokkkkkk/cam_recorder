# Cam Recorder

A simple camera recording application developed using Python and OpenCV, designed to capture video from your laptop's camera with basic functionalities.

## Development Environment
- **Python Version:** 3.9.6
- **OpenCV Version:** 4.9.0

## Features

### Display Laptop Cam Video on Screen
Allows you to view the video captured by your laptop's camera directly on your screen.

### End Program (Esc)
- You can exit the application by pressing the `Esc` key.

### Left and Right Inversion Function (F)
- Toggle the left and right sides of the video feed by pressing the `F` key.

### Recording Mode (Space)
- Initiate recording of the video feed by pressing the `Space` key.
- A recording indicator will be displayed when in recording mode.

### Black Box Mode (B)
- Activate black box mode by pressing the `B` key, which automatically starts recording upon detecting movement in the video.
- A black box indicator will be displayed when this mode is active.
    - The application will switch to recording mode upon motion detection and revert to black box mode if no movement is detected for a specified period.

## Installation

To run this application, ensure you have Python 3.9.6 and OpenCV 4.9.0 installed. Clone this repository, navigate to the project directory, and execute the main script. Please note that operation on versions other than Python 3.9.6 and OpenCV 4.9.0 is not guaranteed.

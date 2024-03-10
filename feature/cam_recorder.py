import cv2 as cv

video = cv.VideoCapture(0)

if video.isOpened():
    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1/fps * 1000)

    while True:
        isTrue, frame = video.read()
        cv.imshow('Video', frame)
        if cv.waitKey(wait_msec) & 0xFF == ord('q'):
            break
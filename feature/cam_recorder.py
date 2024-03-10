from datetime import datetime

import cv2 as cv

video = cv.VideoCapture(0)

if video.isOpened():
    fixed_fps = 30
    wait_msec = int(1/fixed_fps * 1000)

    while True:
        isTrue, frame = video.read()
        cv.imshow('Video', frame)
        key = cv.waitKey(wait_msec) & 0xFF
        # ESC 눌러서 종료
        if key == 27:
            break
        # SPACE 눌러서 녹화
        if key == 32:
            now = datetime.now()
            filename = now.strftime('%Y-%m-%d_%H-%M-%S.avi')
            h, w, *_ = frame.shape
            is_color = (frame.ndim > 2) and (frame.shape[2] > 1)
            out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'XVID'), fixed_fps, (w, h), is_color)
            start = datetime.now()
            while True:
                isTrue, frame = video.read()
                time = datetime.now() - start
                elapsed_seconds = int(time.total_seconds())
                time_str = f"{elapsed_seconds // 3600:02}:{(elapsed_seconds % 3600) // 60:02}:{elapsed_seconds % 60:02}"  # HH:MM:SS 형태로 변환
                cv.circle(frame, (33, 30), 15, (0, 0, 255), -1)
                cv.putText(frame, time_str, (57, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                if not isTrue:  # 비디오 캡처 실패시 루프 종료
                    break
                out.write(frame)
                cv.imshow('Video', frame)
                key = cv.waitKey(wait_msec) & 0xFF
                if key == 32:
                    break
            out.release()
    cv.destroyAllWindows()
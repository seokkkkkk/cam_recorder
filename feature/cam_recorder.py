from datetime import datetime

import cv2 as cv

video = cv.VideoCapture(0)

if video.isOpened():
    # fps 30으로 고정
    fixed_fps = 60
    wait_msec = int(1 / fixed_fps * 1000)
    recording = False
    isFlip = False

    while True:
        isTrue, frame = video.read()
        if not isTrue:
            break
        key = cv.waitKey(wait_msec) & 0xFF
        # ESC 눌러서 종료
        if key == 27:
            break
        # SPACE 눌러서 녹화
        if key == 32:
            if not recording:
                recording = True
                # 녹화 시작 시간
                now = datetime.now()
                filename = now.strftime('%Y-%m-%d_%H-%M-%S.avi')

                h, w, *_ = frame.shape
                is_color = (frame.ndim > 2) and (frame.shape[2] > 1)
                out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'XVID'), fixed_fps, (w, h), is_color)
            else:
                recording = False
                out.release()
        # 좌우 반전
        if key == ord('f'):
            isFlip = not isFlip

        if isFlip:
            frame = cv.flip(frame, 1)

        if recording:
            record_video = frame.copy()
            # 녹화 진행 시간
            time = datetime.now() - now
            elapsed_seconds = int(time.total_seconds())
            time_str = f"{elapsed_seconds // 3600:02}:{(elapsed_seconds % 3600) // 60:02}:{elapsed_seconds % 60:02}"  # HH:MM:SS 형태로 변환

            # 녹화 중 표시
            cv.circle(frame, (33, 30), 15, (0, 0, 255), -1)
            cv.putText(frame, time_str, (57, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            if not isTrue:
                break

            out.write(record_video)
        else:
            # 도움말 표시
            cv.putText(frame, "Exit: ESC", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Record: Space", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Left/Right Inversion: F", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow('Video', frame)

    cv.destroyAllWindows()

from datetime import datetime

import cv2 as cv


def format_elapsed_time(seconds):
    # 초 단위의 시간을 HH:MM:SS 형식의 문자열로 변환
    return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"


def main():
    video = cv.VideoCapture(0)

    if not video.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    fixed_fps = 60
    wait_msec = int(1 / fixed_fps * 1000)
    recording = False
    is_flip = False

    while True:
        valid, frame = video.read()

        if not valid:
            break

        key = cv.waitKey(wait_msec) & 0xFF

        if key == 27:  # ESC로 종료
            break
        elif key == 32:  # SPACE로 녹화 시작
            if recording:
                recording = False
                out.release()
            else:
                recording = True
                now = datetime.now()
                filename = now.strftime('%Y-%m-%d_%H-%M-%S.avi')
                h, w = frame.shape[:2]
                out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'XVID'), fixed_fps, (w, h), frame.ndim > 2)
        elif key == ord('f') or key == ord('F'): # F로 좌우 반전
            is_flip = not is_flip

        if is_flip:
            frame = cv.flip(frame, 1)

        if recording:
            record_video = frame.copy()
            elapsed_time = datetime.now() - now
            elapsed_seconds = int(elapsed_time.total_seconds())
            time_str = format_elapsed_time(elapsed_seconds)
            cv.circle(frame, (33, 30), 15, (0, 0, 255), -1)
            cv.putText(frame, time_str, (57, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            out.write(record_video)

        if not recording:
            cv.putText(frame, "Exit: ESC", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Record: Space", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Left/Right Inversion: F", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow('Video', frame)

    cv.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    main()

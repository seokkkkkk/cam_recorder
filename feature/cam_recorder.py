from datetime import datetime

import cv2 as cv


def format_elapsed_time(seconds):
    # 초 단위의 시간을 HH:MM:SS 형식의 문자열로 변환
    return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"


def detect_motion(cur_frame, prev_frame, threshold=10000):
    # 현재 프레임과 이전 프레임의 차이를 계산하여 움직임을 감지
    # 차이가 크면 True, 작으면 False 반환
    diff = cv.absdiff(cur_frame, prev_frame)
    diff = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    _, diff = cv.threshold(diff, 30, 255, cv.THRESH_BINARY)
    diff_count = cv.countNonZero(diff)
    return diff_count > threshold


def main():
    video = cv.VideoCapture(0)

    if not video.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    not_detected = 0
    prev_frame = None
    fixed_fps = 60
    wait_msec = int(1 / fixed_fps * 1000)
    recording = False
    is_flip = False
    blackbox_mode = False

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
        elif key == ord('f') or key == ord('F'):  # F로 좌우 반전
            is_flip = not is_flip
        elif key == ord('b') or key == ord('B'):  # B로 블랙 박스 모드 변경
            blackbox_mode = not blackbox_mode

        if blackbox_mode and not recording:
            if detect_motion(frame, prev_frame):
                recording = True
                now = datetime.now()
                filename = now.strftime('%Y-%m-%d_%H-%M-%S.avi')
                h, w = frame.shape[:2]
                out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'XVID'), fixed_fps, (w, h), frame.ndim > 2)

        if is_flip:
            frame = cv.flip(frame, 1)

        if recording:
            record_video = frame.copy()

            if blackbox_mode:
                if not detect_motion(frame, prev_frame):
                    not_detected += 1
                else:
                    not_detected = 0
                if not_detected > 100:
                    recording = False
                    not_detected = 0
                cv.putText(frame, f"Motion Not Detected: {not_detected}/300", (1420, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            elapsed_time = datetime.now() - now
            elapsed_seconds = int(elapsed_time.total_seconds())
            time_str = format_elapsed_time(elapsed_seconds)
            cv.circle(frame, (33, 30), 15, (0, 0, 255), -1)
            cv.putText(frame, time_str, (57, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            out.write(record_video)

        elif blackbox_mode:
            cv.circle(frame, (33, 30), 15, (0, 0, 0), -1)
            cv.putText(frame, 'BlackBox Mode', (57, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        elif not recording:
            cv.putText(frame, "Exit: ESC", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Record: Space", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "Left/Right Inversion: F", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv.putText(frame, "BlackBox Mode: B", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv.imshow('Video', frame)
        prev_frame = frame.copy()
    cv.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    main()

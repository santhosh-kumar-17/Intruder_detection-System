"""
Intruder Detection System
--------------------------
Detects human presence in a video using Haarcascade classifier and triggers an alarm.
Developed using Python, OpenCV, and Pygame.

Author: (Santhosh kumar A)
Date: (27/04/25)
"""

import cv2
import pygame
import os
import time

class IntruderDetector:
    def __init__(self, video_path, alarm_path):
        self.video_path = video_path
        self.alarm_path = alarm_path
        self.human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
        self.alarm_playing = False
        self.cap = None

        pygame.mixer.init()

        if not os.path.exists(self.alarm_path):
            raise FileNotFoundError(f"Alarm file not found at {self.alarm_path}")

        try:
            self.alarm_sound = pygame.mixer.Sound(self.alarm_path)
            print(f"[INFO] Alarm sound loaded successfully from {self.alarm_path}")
        except pygame.error as e:
            print(f"[ERROR] Could not load alarm sound. Error: {e}")
            raise

    def load_video(self):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found at {self.video_path}")
        self.cap = cv2.VideoCapture(self.video_path)

    def detect_humans(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = self.human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        return humans

    def start_alarm(self):
        if not self.alarm_playing:
            print("[ALERT] Human detected! Starting alarm...")
            self.alarm_sound.play(-1)
            self.alarm_playing = True

    def stop_alarm(self):
        if self.alarm_playing:
            print("[INFO] No human detected. Stopping alarm.")
            self.alarm_sound.stop()
            self.alarm_playing = False

    def run(self):
        self.load_video()
        print("[INFO] Intruder detection started...")

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("[INFO] Video ended or frame not read properly.")
                break

            frame = cv2.resize(frame, (640, 480))
            humans = self.detect_humans(frame)

            if len(humans) > 0:
                self.start_alarm()
            else:
                self.stop_alarm()

            for (x, y, w, h) in humans:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, f"Human Detected - {timestamp}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.imshow('Human Intruder Detection', frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                print("[INFO] Exiting on user request (Q pressed).")
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        print("[INFO] Resources released and application closed.")
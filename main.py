"""
Intruder Detection Application
-------------------------------
Main file to execute the intruder detection system.
"""

from intruder_detector import IntruderDetector

if __name__ == "__main__":
    video_file = 'IMG_2693.MP4'  
    alarm_file = 'house-fire-or-burglar-alarm-with-ending-36587.mp3'  

    try:
        detector = IntruderDetector(video_file, alarm_file)
        detector.run()
    except Exception as e:
        print(f"[ERROR] {str(e)}")

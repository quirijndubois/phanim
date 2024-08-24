import cv2
import pygame


class ScreenRecorder:
    def __init__(self, width, height, fps, out_file='output.avi'):
        from os import environ
        environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        four_cc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(
            out_file, four_cc, float(fps), (width, height))
        self.surface_to_frame = pygame.surfarray.pixels3d
        self.rotate_frame = cv2.rotate
        self.flip_frame = cv2.flip
        self.convert_frame = cv2.cvtColor

    def capture_frame(self, surf):
        pixels = self.convert_frame(self.flip_frame(
            self.rotate_frame(
                self.surface_to_frame(surf),
                cv2.ROTATE_90_CLOCKWISE
            ),
            1
        ), cv2.COLOR_RGB2BGR)
        self.video.write(pixels)

    def start_recording(self):
        pass

    def end_recording(self):
        self.video.release()

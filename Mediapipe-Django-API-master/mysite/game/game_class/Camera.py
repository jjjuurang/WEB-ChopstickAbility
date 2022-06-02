import cv2



class Camera(object):
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.video.set(cv2.CAP_PROP_FPS,20)

    def __del__(self):
        self.video.release()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_frame(self):
        success, image = self.video.read()
        if success:
            # call the detection here
            image = self.hand_video(success, image)

        return image


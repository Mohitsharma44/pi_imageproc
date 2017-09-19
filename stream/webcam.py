import cv2
from threading import Thread


class WebcamVideoStream():
    """
    class containing methods for
    grabbing video stream in a multi-threaded
    configuration
    """
    def __init__(self, cam_id):
        """
        Initialize the video camera
        for streaming.
        Parameters
        ----------
        cam_id: int
            id of the camera to stream from
        """
        self.stream = self._acquire_camera(cam_id)
        (self.grabbed, self.frame) = self.stream.read()
        self.stop = False

    def _acquire_camera(self, cam_id):
        """
        Acquire lock on the camera specified by `cam_id`
        Parameters
        ----------
        cam_id: int
            id of the camera to acquire lock on
        Returns
        -------
        `cv2.VideoCapture` stream object for the
        camera specified by `cam_id`
        """
        try:
            return cv2.VideoCapture(cam_id)
        except Exception as ex:
            print("Error obtaining lock on the camera with cam_id {}: {}".
                  format(cam_id, ex))

    def start(self):
        """
        Start thread to read the frames from the stream
        """
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """
        Keep looping until `self.stop = False`
        """
        while True:
            if self.stop:
                return
        (self.grabbed, self.frame) = self.stream.read()

    def read(self, scale=1):
        """
        Return the fram read from the camera
        scale: float
           resize the image by scaling factor.
           default: 1 (original size)
        """
        return cv2.resize(self.frame, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_AREA)

    def stop_stream(self):
        """
        stop the camera from streaming
        """
        self.stop = True

    def release_camera(self):
        """
        Release the lock from the camera
        """
        self.stream.release()
        cv2.destroyAllWindows()

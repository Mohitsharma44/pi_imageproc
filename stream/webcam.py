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
        self.ctr = 0
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

    def start(self, scale=1):
        """
        Start thread to read the frames from the stream
        """
        cam_thread = Thread(target=self.update, args=())
        cam_thread.daemon = True
        cam_thread.start()
        return self

    def update(self):
        """
        Keep looping until `self.stop = False`
        """
        while True:
            if self.stop:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """
        Return the fram read from the camera
        """
        return self.frame

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

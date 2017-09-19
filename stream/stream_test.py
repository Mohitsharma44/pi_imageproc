import webcam
import cv2

try:
    wvs = webcam.WebcamVideoStream(0)
    print(" ... Displaying images till Ctrl C is pressed")
    wvs.start()
    while True:
        frame = wvs.read()
        res_frame = cv2.resize(frame, None, fx=0.3, fy=0.3,
                               interpolation=cv2.INTER_AREA)
        cv2.imshow("Frame", res_frame)
        key = cv2.waitKey(1) & 0xFF
except KeyboardInterrupt as ki:
    print()
    print(" ... Cleaning up")
    wvs.stop_stream()
    wvs.release_camera()
    #cv2.destroyAllWindows()
    print(" ... Done")
except Exception as ex:
    print("Exception streaming: {}".format(ex))

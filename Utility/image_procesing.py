import cv2


def resize_image_to_frame(image_size: tuple, frame_size: tuple) -> tuple:
    
    # inputs
    # frame inputs
    w_frame, h_frame = frame_size
    frame_ratio = h_frame/w_frame

    # image_inputs
    w_image, h_image = image_size
    image_ratio = h_image/w_image

    if frame_ratio < image_ratio:

        h_ratio = h_frame/h_image
        h = h_image*h_ratio
        w = w_image*h_ratio

    elif frame_ratio > image_ratio:

        w_ratio = w_frame / w_image
        h = h_image * w_ratio
        w = w_image * w_ratio

    else:

        p = w_frame / w_image
        h = p*h_image
        w = p*w_image

    new_image_size = (int(w), int(h))

    return new_image_size


def test_camera_device(source)->bool:

    cap = cv2.VideoCapture(source)

    if cap is None or not cap.isOpened():
        camera_device_exist = False
        print('Warning: unable to open video source: ', source)
    else:
        camera_device_exist = True

    return camera_device_exist







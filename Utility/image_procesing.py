
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

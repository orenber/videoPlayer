import numpy as np        


def resize_image_to_frame(image: np.array, frame: np.array)->tuple:
    
    # inputs

    # frame inputs
    width_frame, height_frame = frame.shape
    frame_ratio = height_frame/width_frame

    # image_inputs
    width_image, height_image = image.shape
    image_ratio = height_image/width_image

    if frame_ratio < image_ratio:

        height_ratio = height_frame / height_image
        height = height_image * height_ratio
        width = width_image * height_ratio

    elif frame_ratio > image_ratio:

        width_ratio = width_frame / width_image
        height = height_image * width_ratio
        width = width_image * width_ratio

    else:

        p = width_frame / width_image
        height = p*height_image
        width = p*width_image

    new_image_size = (int(width), int(height))

    return new_image_size


def main():

    image = np.zeros((700, 480), float)
    frame = np.zeros((800, 1480), float)
    size = resize_image_to_frame(image, frame)
    print(size)
    print(size)


if __name__ == "__main__":
    main()

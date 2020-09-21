import numpy as np
# from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt

from utils import helpers

FOLDER = '/home/filipkr/Documents/xjob/videos/test1/'
CSV_FILE = FOLDER + 'knee-silent_coordinates-IV.csv'
VIDEO = FOLDER + 'knee-silent.mp4'
plot = True
resolution = 600


def annotate(coords, vid):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))  # or .get(3)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # or .get(4)
    fps = int(np.round(vid.get(cv2.CAP_PROP_FPS)))
    vid_new = cv2.VideoWriter(FOLDER + 'annotated-adj.avi', fourcc, fps,
                              (width, height))

    success, im = vid.read()
    count = 1

    while success:
        if count % 10 == 0:
            print('frame:', count)
            print('expected:', coords[-1, 0])

        im = cv2.flip(im, 0)

        for i in range(1, len(coords[1, :]), 2):  # len -1?
            # print('x', coords[count, :])
            # print('x', coords[count + 1, :])
            # print('y', coords[count, i + 1] * height)
            y = int(np.round((coords[count, i]) * height))
            x = int(np.round((coords[count, i + 1] + 0.025) * width))

            im = cv2.drawMarker(im, (x, y), (255, 0, 0),
                                markerType=cv2.MARKER_CROSS,
                                markerSize=10, thickness=5)

        vid_new.write(im)
        if plot and count < 3:
            plt.imshow(im)
            plt.show()
        success, im = vid.read()
        count += 1

    vid_new.release()

    # print(vid_new)


def main():
    coords = np.genfromtxt(CSV_FILE, delimiter=',')
    vid = cv2.VideoCapture(VIDEO)

    annotate(coords, vid)

    print(coords.shape)
    print(coords[1, :])


if __name__ == '__main__':
    main()

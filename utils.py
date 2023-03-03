import re
import os

def natural_sort(given_list):
    """ Sort the given list in the way that humans expect."""
    given_list.sort(key=alphanum_key)

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"] """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def tryint(s):
    try:
        return int(s)
    except:
        return s


def make_video_from_images(img_paths, outvid_path, fps=25, size=None,
               is_color=True, format="XVID"):
    """
    Create a video from a list of images.
    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for ct, img_path in enumerate(img_paths):
        if not os.path.exists(img_path):
            raise FileNotFoundError(img_path)
        img = imread(img_path)
        if img is None:
            print(img_path)
            continue
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid_path, fourcc, float(fps), size, is_color)

        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    if vid is not None:
        vid.release()
    return vid

def get_video_frames(video_path, output_path):
  vid = cv2.VideoCapture(video_path) # detect on video    
  count = 0 
  while(True):
      ret,frame = vid.read()
      if frame is None:
          break

      frame_name = 'frame' + '{:05d}'.format(count) + '.jpg'
      count+= 1
      filename = os.path.join(output_path,frame_name)
      cv2.imwrite(filename, frame)


def pad_img(image):
  h, w = image.shape[:2]
  # Padding on the small side to get a square shape
  frame_size = max(h, w)
  pad_h = int((frame_size - h)/2)
  pad_w = int((frame_size - w)/2)
  frame = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT)
  return frame



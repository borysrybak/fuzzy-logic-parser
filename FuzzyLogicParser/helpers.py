import cv2
import PIL
import ntpath
from PIL import Image

def image_resize(img_file_path):
    img_file_name = path_leaf(img_file_path)
    basewidth = 1500
    img = Image.open(img_file_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    resized_img_path = 'img/resizedimg/resized_' + img_file_name
    img.save(resized_img_path)

    return resized_img_path

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

#def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
#    # initialize the dimensions of the image to be resized and
#    # grab the image size
#    dim = None
#    (h, w) = image.shape[:2]

#    # if both the width and height are None, then return the
#    # original image
#    if width is None and height is None:
#        return image

#    # check to see if the width is None
#    if width is None:
#        # calculate the ratio of the height and construct the
#        # dimensions
#        r = height / float(h)
#        dim = (int(w * r), height)

#    # otherwise, the height is None
#    else:
#        # calculate the ratio of the width and construct the
#        # dimensions
#        r = width / float(w)
#        dim = (width, int(h * r))

#    # resize the image
#    resized = cv2.resize(image, dim, interpolation = inter)

#    # return the resized image
#    return resized

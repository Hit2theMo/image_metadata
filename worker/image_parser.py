from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
import regex as re
from pathlib import Path
import logging
import logging.config

import exiftool
# files = ["a.jpg", "b.png", "c.tif"]
def exiftoolfun(path):
    # exiftool.executable = r'/mnt/c/Program Files/exiftool-12.40/exiftool'
    with exiftool.ExifTool('exiftool') as et:
        metadata = et.get_metadata(path)
    return metadata

logger = logging.getLogger(__name__)

def extractMetadata(path):
    metadata_dict = {}
    path = str(path)
    image = Image.open(path)
    image.verify()
    # extracting the exif metadata
    exifdata = image._getexif()
    # looping through all the tags present in exifdata
    for tagid, value in exifdata.items():
        # getting the tag name instead of tag id
        tagname = TAGS.get(tagid, tagid)
        # decode bytes
        if isinstance(value, bytes):
            value = value.decode(errors='replace')
            # value = ''.join(str(ord(c)) for c in value)
        if isinstance(value, str):
            value = value.strip()
        if tagname not in ("PrintImageMatching", "MakerNote"):
            metadata_dict[tagname] = value
        # print(f"{tagname:25}: {value}")
    return metadata_dict


# --------------------------------------------------------------------------------------
if __name__ == '__main__':
    path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch-image-parser/worker/images/P1013747.JPG"
    path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch_image_parser/worker/images/P1013746.JPG"
    # path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch_image_parser/worker/images/P1013748.JPG"
    # path = r"/mnt/c/Users/Mohit Khanwale/Desktop/Maldives/ADEM1771.JPG"
    # path = r"worker/images/P1013747.JPG"

    # data = extractMetadata(path)
    # pprint(data)
    data = exiftoolfun(path)
    pprint(data)
    # exif = get_exif(path)
    # labeled = get_labeled_exif(exif)
    # pprint(labeled)

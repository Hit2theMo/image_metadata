
from pprint import pprint
import logging
import logging.config
import exiftool


def extractMetadata(path):
    # exiftool.executable = r'/mnt/c/Program Files/exiftool-12.40/exiftool'
    with exiftool.ExifTool('exiftool') as et:
        metadata = et.get_metadata(path)
    return metadata

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------
if __name__ == '__main__':
    path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch-image-parser/worker/images/P1013747.JPG"
    path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch_image_parser/worker/images/P1013746.JPG"
    # path = r"/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch_image_parser/worker/images/P1013748.JPG"
    # path = r"/mnt/c/Users/Mohit Khanwale/Desktop/Maldives/ADEM1771.JPG"
    data = extractMetadata(path)
    pprint(data)

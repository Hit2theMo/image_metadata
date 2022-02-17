import base64
# from pprint import pprint
import json
import logging
import os
import pathlib
import time
from zipfile import ZipFile

import sentry_sdk
import shortuuid
from celery import Celery
from sentry_sdk import capture_message

from image_parser import extractMetadata

SENTRY_DSN = os.environ.get('SENTRY_DSN')
sentry_sdk.init(SENTRY_DSN,traces_sample_rate=1.0)

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
CELERY_TASK_TIMEOUT = int(os.environ.get('CELERY_TASK_TIMEOUT',18000))

# logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
celery_app = Celery('batch_parsing', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# logger = logging.getLogger('batch_parsing')


def generate_filename(org_name):
    uuid = shortuuid.ShortUUID()
    file_name = org_name.strip() + "_" + uuid.uuid()
    return file_name


@celery_app.task(soft_time_limit=CELERY_TASK_TIMEOUT)
def parseUnzippedFiles(path):
    path = os.path.join('/','flask-app', path)
    logger.info('Got Request - Starting work ')
    #raise ValueError('test')
    capture_message("Starting the Batch Parsing of {0}".format(path))
    file_names = os.listdir(path)
    # file_rename_dict = {}
    unparsed_files = []
    batch_output = {}
    final_batch_output = {}
    for fn in file_names:
        try:
            org_file_name, file_extn = os.path.splitext(fn)
            file_extn = file_extn.replace('.', '')
            #org_file_name, file_extn = fn.split(".")
            org_file_name = org_file_name.strip()
            org_file_path = pathlib.PurePath(path, fn)
            new_file_name = generate_filename(org_file_name).strip() + "." + file_extn
            new_file_path = pathlib.PurePath(path, new_file_name)
            # file_rename_dict[fn] = new_file_name
            # Rename file to the new name
            os.rename(org_file_path, new_file_path)
            output_dict = extractMetadata(str(new_file_path))
            if not output_dict:
                raise Exception
            temp_dict = {}
            temp_dict["original_filename"] = fn
            temp_dict["extracted_data"] = output_dict
            batch_output[new_file_name] = temp_dict

        except Exception as e:
            logger.exception(
                f"Error in batch parser while parsing file- {fn}- {e}"
            )
            if new_file_path:
                unparsed_files.append(str(fn))
                # unparsed_files.append(str(new_file_path))
            continue

    final_batch_output["output"] = batch_output
    final_batch_output["unparsed_files"] = unparsed_files
    # final_batch_output["unparsed_file_zip_as_base64"] = base64str
    json_object = json.dumps(final_batch_output, indent=4)
    capture_message(
        "Finished processing batch file- {0}, JSON Result-{1}".format(path, json_object)
    )
    logger.info('Work Finished ')
    return json_object


if __name__ == "__main__":
    # path = r"batch_parsing\ipNLfea4wEqA34W8YnFzoe"
    path = r'/mnt/c/Users/Mohit Khanwale/Desktop/SplitReq/batch_image_parser/worker/images'
    print(json.loads(parseUnzippedFiles(path)))
    print(time.perf_counter())

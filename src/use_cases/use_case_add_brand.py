import os
import logging

import conf

logger = logging.getLogger(conf.LOGGER_NAME)

class UseCaseAddBrand(object):

    @staticmethod
    def get_path_to_keep(brand_name):
        """
        Get the path to keep the brand image
        """
        if brand_name not in os.listdir(conf.BRAND_FOLDER):
            os.mkdir(os.path.join(conf.BRAND_FOLDER, brand_name))
            return os.path.join(conf.BRAND_FOLDER, brand_name, '1.png')
        else:
            brand_files = os.listdir(os.path.join(conf.BRAND_FOLDER, brand_name))
            jpg_files = [file for file in brand_files if file.endswith('.jpg')]
            jpg_files.sort()
            if len(jpg_files) == 0:
                return os.path.join(conf.BRAND_FOLDER, brand_name, '1.png')
            else:
                path_to_save = os.path.join(conf.BRAND_FOLDER, brand_name,
                                            str(int(jpg_files[-1].replace('.jpg', '')) + 1) + ".jpg")
                return path_to_save

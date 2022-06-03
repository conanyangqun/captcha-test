#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
func: 用于测试不同的验证码识别模型
usage: python captcha_test.py
"""

import argparse
import logging
import os
import re
import sys

import numpy as np
from PIL import Image
import tesserocr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def preprocess(image, threshold=50):
    # 预处理图片，转换为灰度图
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > threshold, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image

def tesserocr_recog(image):
    text = tesserocr.image_to_text(image)
    text = re.sub('[^A-Za-z0-9]', '', text).upper()
    logging.debug("识别为: {}".format(text))
    return text

def get_captcha_images(image_dir):
    # 获取目录下的验证码图片
    images = {} # key: text, value: Image
    for f in os.listdir(image_dir):
        if not f.endswith('.jpeg'):
            logging.warning("{} not a jpeg img.".format(f))
            continue

        text = f.replace('.jpeg', '')
        image = Image.open(os.path.join(image_dir, f))
        images[text] = image
    
    return images



def main(args):
    captcha_images = get_captcha_images(args.i)
    results_right = [] # 识别正确的验证码
    results_wrong = []
    logging.info("获得{}张验证码图片".format(len(captcha_images)))

    if not captcha_images:
        sys.exit(0)

    for text in captcha_images:
        # 判断每一张验证码
        logging.debug("获取到验证码: {}".format(text))

        image = captcha_images[text]
        # image = preprocess(captcha_images[text], threshold=200)

        result = tesserocr_recog(image)
        if result == text:
            logging.debug("识别正确")
            results_right.append(text)
        else:
            logging.debug("识别错误")
            results_wrong.append((text, result))
    
    logging.info("{}张验证码识别正确，{}张验证码识别错误，正确率：{:.2f}%（总{}张）".format(
        len(results_right), 
        len(results_wrong),
        len(results_right) / len(captcha_images) * 100,
        len(captcha_images)
    ))

    # 输出错误识别的验证码
    logging.info("错误识别的验证码为:")
    for result in results_wrong:
        x, y = result
        logging.info("{} -> {}".format(x, y))


if __name__ == '__main__':
    argparse_parser = argparse.ArgumentParser()
    argparse_parser.add_argument('-i', help="captcha dir", required=True)

    myargs = argparse_parser.parse_args(sys.argv[1:])
    main(myargs)

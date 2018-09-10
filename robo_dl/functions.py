# _*_ coding:utf-8 _*_
__author__ = 'jiangchao'
__date__ = '2018/8/13 0013 下午 2:31'
import requests
import time
import os
import os.path as ops
import imghdr

from . import turi
from robo_dl_api.settings import BASE_DIR
from utils.http import APIResponse
from .models import WeldingImage
from robo_dl_api.settings import CDN_HOST
from utils.log import logger


def predict_image(request):
    url = request.data.get('url', '')
    if not url:
        response = APIResponse(success=False, data={}, msg='url为必填字段')
        return response
    if 'http' not in url:
        url = CDN_HOST + url
    file_path = download(url)
    if not file_path:
        response = APIResponse(success=False, data={}, msg='图片地址(%s)不存在' % CDN_HOST + url)
        return response
    try:
        predictions = turi.predict(file_path)
    except Exception as e:
        print(e)
        logger.info(e)
        clear_file(file_path)
        response = APIResponse(success=False, msg='该文件格式无法进行解码(原因:非标准编码的图片格式/或图片格式有损)')
        return response
    if not WeldingImage.objects.filter(url=url):
        welding = WeldingImage.objects.create(url=url, predict_label=predictions)
    else:
        welding = WeldingImage.objects.filter(url=url).first()
    clear_file(file_path)
    data = {
        'predict': predictions,
        'id': welding.id
    }
    response = APIResponse(success=True, data=data)
    return response


def download(url):
    response = requests.get(url=url, verify=False)
    timestamp = time.time()
    file_path = BASE_DIR + '/images/%s/' % timestamp
    try:
        if not ops.exists(file_path):
            os.mkdir(file_path)
        if response.status_code == 200:
            open(file_path + '%s.jpg' % int(timestamp), 'wb').write(response.content)
            image_format = get_image_format(file_path + '%s.jpg' % int(timestamp))
            os.rename(file_path + '%s.jpg' % int(timestamp), file_path + '%s.%s' % (int(timestamp), image_format))
    except Exception as e:
        print('exception: %s', e)
        clear_file(file_path)
        return None
    return file_path


def clear_file(file_path):
    for image in os.listdir(file_path):
        os.remove(ops.join(file_path, image))
    os.rmdir(file_path)


def get_image_format(file_path):
    return imghdr.what(file_path)


def update_real_label(self, request):
    pk = self.kwargs.get('pk')
    real_label = request.data.get('label', '')
    welding = WeldingImage.objects.get(pk=pk)
    welding.real_label = real_label
    welding.save()
    response = APIResponse(success=True, msg='标记成功', data={})
    return response

import os
import hashlib


def getMD5(name):
    if isinstance(name, str):
        name = name.encode('utf-8')
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()


def changeName(instance, filename):
    """
    :param instance: 函数类的一个实例
    :param filename: 上传文件的文件名
    :return: 对文件名重新编码，规定文件的读写路径
    """

    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        split = filename.split('.')

        file_rename = getMD5(instance.name + split[0]) + '.' + split[-1]  # 对文件名进行重编码，并规定文件读写路径
        itemID = str(instance.itemID.pk)
        pic_write_path = os.path.join('itemPics', itemID, file_rename)

        return pic_write_path


def changeTempName(instance, filename):
    """
    :param instance: 函数类的一个实例
    :param filename: 上传文件的文件名
    :return: 对文件名重新编码，规定文件的读写路径
    """
    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        split = filename.split('.')

        file_rename = getMD5(instance.name + split[0]) + '.' + split[-1]  # 对文件名进行重编码，并规定文件读写路径

        pic_write_path = os.path.join('itemPics', 'temp', file_rename)

        return pic_write_path


def changeUserName(instance, filename):
    """
        :param instance: 函数类的一个实例
        :param filename: 上传文件的文件名
        :return: 对文件名重新编码，规定文件的读写路径
        """
    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        split = filename.split('.')
        file_rename = getMD5(instance.pk + split[0]) + '.' + split[-1]  # 对文件名进行重编码，并规定文件读写路径
        ID = str(instance.pk)
        pic_write_path = os.path.join('UserAvatar', ID, file_rename)

        return pic_write_path


def item_directory_path(instance, filename):
    # print(dir(instance), dir(filename))
    # ext = filename.split('.').pop()
    # filename = '{0}.{1}'.format(instance.name, ext)
    return instance.name  # 系统路径分隔符差异，增强代码重用性

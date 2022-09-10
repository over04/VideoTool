import os
import shutil
from util import message, other
from typing import Tuple, Set, List


class Action:

    @classmethod
    def remove(cls, path) -> 'message.Log':
        """
        删除文件夹或文件夹目录
        :param path: 文件/文件夹目录
        :return:
        """
        message_type = 'file.Action.remove'
        if not Path.exists(path):
            return message.Log(f'不存在文件/文件夹[{path}]', message_type, False)
        if Path.isfile(path):
            os.remove(path)
            return message.Log(f'成功删除文件[{path}]', message_type, True)
        elif Path.isdir(path):
            shutil.rmtree(path)
            return message.Log(f'成功删除文件夹[{path}]', message_type, True)
        else:
            return message.Log(f'未知状态[{path}]', message_type, False)

    @classmethod
    def link(cls, source_path, target_path, mode=0):
        source_path, target_path = Path.abspath(source_path), Path.abspath(target_path)
        if Path.exists(source_path) is False:  # 不存在源文件
            return

        if Path.exists(target_path):
            if mode == 0:  # 非强制模式
                return

            elif mode == 1:  # 强制模式,强制删除
                Action.remove(target_path)
            elif mode == 2:  # 存在文件的话pass,否则链接,这里仅留空
                pass

        if Path.isfile(source_path):
            os.link(source_path, target_path)

        elif Path.isdir(source_path):
            if mode == 2:
                pass
            else:
                Action.mkdir(target_path)
            Action.__link_dir(source_path, target_path, mode=mode)

    @classmethod
    def __link_dir(cls, source_path, target_path, mode: int):
        for source_work_path, dirs, files in os.walk(source_path):
            target_work_path = f'{target_path}{source_work_path[len(source_path):]}'
            for each_dir in dirs:
                if mode == 2 and Path.exists(f'{target_work_path}/{each_dir}'):
                    continue
                Action.mkdir(f'{target_work_path}/{each_dir}')
            for each_file in files:
                if mode == 2 and Path.exists(f'{target_work_path}/{each_file}'):
                    continue
                os.link(f'{source_work_path}/{each_file}', f'{target_work_path}/{each_file}')

    @classmethod
    def mkdir(cls, path):
        os.mkdir(path)

    @classmethod
    def mkdir_father(cls, path):
        sp = os.path.split
        first, tail = sp(path)
        if tail == '' or first == '':
            return
        Action.mkdir_father(first)
        if not Path.exists(first):
            Action.mkdir(first)


class Path:
    @classmethod
    def is_video(cls, path):
        return Path.file_type(path).lower() in [
            'mkv',
            'mp4',
            'mov',
            'flv',
            'avi',
            'ts'
        ]

    @classmethod
    def file_type(cls, path):
        return os.path.splitext(path)[1].strip('.')

    @classmethod
    def file_name(cls, path):
        return os.path.splitext(os.path.split(path)[-1])[0]

    @classmethod
    def isfile(cls, path):
        return os.path.isfile(path)

    @classmethod
    def isdir(cls, path):
        return not cls.isfile(path)

    @classmethod
    def exists(cls, path):
        return os.path.exists(path)

    @classmethod
    def isabs(cls, path):
        return os.path.isabs(path)

    @classmethod
    def abspath(cls, path):
        return os.path.abspath(path)

    @classmethod
    def listdir(cls, path, full_path=False) -> List[str]:
        """
        获取目录结构
        :param path: 路径
        :param full_path: True为获取完整路径(拼接原地址)
        :return:
        """
        path.rstrip('/').rstrip('\\')
        if full_path:
            return list(map(lambda x: f'{path}/{x}', os.listdir(path)))
        return os.listdir(path)

    @classmethod
    def listall(cls, path: str) -> Tuple[List, List]:
        _files = []
        _dirs = []
        for root, dirs, files in os.walk(path):
            for each_file in files:
                _files.append(os.path.join(root, each_file))
            for each_dir in dirs:
                _dirs.append(os.path.join(root, each_dir))
        return _files, _dirs


def parse(path) -> 'File' or 'Dir' or 'message.Log':
    if not Path.exists(path):
        return message.Log(f'解析失败,不存在文件/文件夹[{path}]', 'file.Parse', False)
    if Path.isfile(path):
        return File(path)
    else:
        return Dir(path)


class BaseFile:
    def __init__(self, path):
        self.__path = Path.abspath(path)

    def remove(self) -> message.Log:
        return Action.remove(self.__path)

    @property
    def path(self) -> str:
        return self.__path

    @property
    def hash_name(self) -> str:
        return 'test'

    @property
    def hash_path(self) -> str:
        return other.md5(self.path)

    @property
    def isfile(self) -> bool:
        return Path.isfile(self.path)

    @property
    def isdir(self) -> bool:
        return not self.isfile

    @property
    def isabs(self):
        return Path.isabs(self.path)

    @property
    def file_name(self):
        return Path.file_name(self.path)

    def link(self, target_path):
        Action.link(self.path, target_path)


class File(BaseFile):
    def __init__(self, path):
        """
        文件对象
        :param path: 文件地址
        """
        super().__init__(path)

    def __repr__(self):
        return f'文件类 at {self.path}'

    @property
    def is_video(self):
        return Path.is_video(self.path)

    @property
    def file_type(self):
        return Path.file_type(self.path)


class Dir(BaseFile):
    def __init__(self, path):
        """
        文件夹对象
        :param path: 文件地址
        """
        super().__init__(path)

    @property
    def child(self) -> 'FileSet':
        """
        获取子文件/文件夹
        :return: FileSet类
        """
        file_set = FileSet()
        for i in Path.listdir(self.path, full_path=True):
            _ = parse(i)
            if not isinstance(_, message.Log):
                file_set.add(_)
        return file_set

    def __repr__(self):
        return f'文件夹类 at {self.path}'

    def listall(self) -> 'FileSet':
        files, dirs = Path.listall(self.path)
        temp = FileSet()
        for i in files:
            temp.add(File(i))
        for i in dirs:
            temp.add(Dir(i))

        return temp


class FileSet:
    def __init__(self):
        self.__files: 'Set[File]' = set()
        self.__dirs: 'Set[Dir]' = set()

    def add(self, value: 'File' or 'Dir' or 'FileSet'):
        if isinstance(value, File):
            self.__files.add(value)
            return message.Log('成功添加File对象', 'file.FileSet.add', True)

        elif isinstance(value, Dir):
            self.__dirs.add(value)
            return message.Log('成功添加Dir对象', 'file.FileSet.add', True)

        elif isinstance(value, FileSet):
            self.__files = self.__files.union(value.value[0])
            self.__dirs = self.__dirs.union(value.value[1])
            return message.Log('成功添加FileSet对象', 'file.FileSet.add', True)
        return message.Log(f'不能添加{type(value)}对象', 'file.FileSet.add', File)

    @property
    def value(self) -> 'Tuple[Set[File],Set[Dir]]':
        return self.__files, self.__dirs

    @property
    def child(self) -> 'FileSet':
        file_set = FileSet()
        for i in self.__dirs:
            file_set.add(i.child)
        return file_set

    @property
    def file(self) -> Set[File]:
        return self.__files

    @property
    def dir(self) -> Set[Dir]:
        return self.__dirs

    def __repr__(self):
        return '文件:{}\n' \
               '文件夹:{}'.format("\n".join(map(str, self.__files)), "\n".join(map(str, self.__dirs)))


if __name__ == '__main__':
    pass

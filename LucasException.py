class PathNotExists(Exception):
    def __init__(self, message = '传入了不存在的文件路径.'):
        self.message = message
        super().__init__(self.message)

class ArgsMissing(Exception):
    def __init__(self, message = '缺少关键参数.'):
        self.message = message
        super().__init__(self.message)

class KeyNotExists(Exception):
    def __init__(self, message = '无法读取不存在的键值对.'):
        self.message = message
        super().__init__(self.message)

class KeyAlreadyExists(Exception):
    def __init__(self, message = '无法添加已存在的键.'):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    ClassTest = PathNotExists()
    ClassTest = ArgsMissing()
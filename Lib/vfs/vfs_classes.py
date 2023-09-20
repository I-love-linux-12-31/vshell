import datetime


class VFSObject:
    name = ""
    access = "----------"
    #         d123456789
    # d - is a directory
    file_size = 0
    items = None
    date = (1980, 1, 1, 0, 0, 0)
    user = "root"
    group = "root"
    path = "/"
    path_in_archive = ""

    def __str__(self) -> str:
        return self.name

    def _get_date_string(self) -> str:
        if isinstance(self.date, tuple):
            return f"{self.date[1]}{self.date[2]} {self.date[0]}"
        return str(datetime.datetime.fromtimestamp(self.date))

    def get_ls_string(self) -> str:
        return f"{self.access} root\troot\t{self.file_size:10} {self._get_date_string()}\t {self.name}"

    def find_item_by_name(self, name: str):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def print_recursion(self, t=0):
        print("\t" * t + '|-', self.name)
        for item in self.items:
            item.print_recursion(t=t + 1)


class VFSRoot(VFSObject):
    def __init__(self):
        self.name = "/"
        self.access = "drwxrwxr-x"
        self.items = []
        self.path = "/"


class VFSDirectory(VFSObject):
    def __init__(self, name, date, path, arh_path, access=None, items=None):
        if access is None:
            access = "d---------"
        self.path_in_archive = arh_path
        self.name = name.strip("/")
        self.path = path.strip("./")
        if not self.path.startswith('/'):
            self.path = '/' + self.path
        self.access = access
        if items is None:
            self.items = []
        else:
            self.items = items
        self.date = date


class VFSFile(VFSObject):
    def __init__(self, name, size, date, path, arh_path, access=None):
        if access is None:
            access = "----------"
        self.name = name.strip("/")
        self.path = path.strip("./")
        self.path_in_archive = arh_path
        if not self.path.startswith('/'):
            self.path = '/' + self.path
        self.file_size = size
        self.access = access
        self.date = date
        self.items = tuple()

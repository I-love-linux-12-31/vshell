class Command:
    cmd: str = ""
    args_raw: list = None
    kwargs: dict = None
    args: list = None

    def __init__(self, line_in: str):
        self.args_raw = line_in.split()
        self.cmd = self.args_raw[0]
        self.kwargs = dict()
        self.args = []

        stack = self.args_raw[1:]
        while stack:
            item = stack.pop(0)
            item: str
            if item.startswith("--"):
                if len(stack) > 0 and not stack[0].startswith("-"):
                    item = item.lstrip("--")
                    self.kwargs[item] = stack.pop(0)
                else:
                    self.args.append(item)
            else:
                self.args.append(item)

        # for i in self.args:
        #     print(f"arg: {i}")
        #
        # for i in self.kwargs:
        #     print(f"kwarg: {i} : {self.kwargs[i]}")

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.args[item]
        return self.kwargs[item]

    def __call__(self, function):
        function(*self.args, **self.kwargs)

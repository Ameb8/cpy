class Cmd:
    def __init__(self, cmd: str, args: list[str], flags: dict[str, list[str]]) -> None:
        self.cmd = cmd
        self.args = args
        self.flags = flags

    @classmethod
    def get_cmd(cls, content: str) -> 'Cmd':
        parts = content.strip().split()
        cmd = parts[0]
        args: list[str] = []
        flags: dict[str, list[str]] = {}
        last_flag: str = ""

        for part in parts:
            part = part.strip()

            if part.startswith("--"):
                flags[part] = []
                last_flag = part
            else:
                if last_flag:
                    flags[last_flag].append(part)
                else:
                    args.append(part)

        return cls(cmd, args, flags)


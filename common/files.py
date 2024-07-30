class Files:

    @staticmethod
    def prompt_selection() -> str:
        ...

    @staticmethod
    def get_content(file: str) -> str:
        with open(file, "r") as f:
            return f.read()

    @staticmethod
    def parse_content(file_content: str) -> list[list[str]]:
        lines = file_content.splitlines()
        result = [list(line) for line in lines]
        result[0].insert(0, 1)

        return result

    @staticmethod
    def rebuild_content(split_code):
        code_lines = [''.join([char for char in line if char != 1]) for line in split_code]
        return "\n".join(code_lines)


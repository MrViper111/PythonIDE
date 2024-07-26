class TextPointer:

    @staticmethod
    def insert_char(content: list[list], char: str):
        for row in content:
            if 1 in row:
                idx = row.index(1)
                row.insert(idx, char)
                break
        return content

    @staticmethod
    def move_cursor(content: list[list], from_i: int, from_j: int, to_i: int, to_j: int):
        content[from_i].pop(from_j)
        if to_j >= len(content[to_i]):
            content[to_i].append(1)
        else:
            content[to_i].insert(to_j, 1)

    @staticmethod
    def shift_pointer(content: list[list], direction: tuple[int, int]):
        rows = len(content)
        for i in range(rows):
            for j in range(len(content[i])):
                if content[i][j] == 1:
                    new_i, new_j = i + direction[0], j + direction[1]
                    if direction == (-1, 0) and new_i >= 0:
                        TextPointer.move_cursor(content, i, j, new_i, min(new_j, len(content[new_i])))
                    elif direction == (1, 0) and new_i < rows:
                        TextPointer.move_cursor(content, i, j, new_i, min(new_j, len(content[new_i])))
                    elif direction == (0, -1):
                        if new_j >= 0:
                            content[i][j], content[i][new_j] = content[i][new_j], content[i][j]
                        elif new_j == -1 and new_i > 0:
                            TextPointer.move_cursor(content, i, j, new_i - 1, len(content[new_i - 1]))
                    elif direction == (0, 1):
                        if new_j < len(content[i]):
                            content[i][j], content[i][new_j] = content[i][new_j], content[i][j]
                        elif new_j == len(content[i]) and new_i < rows - 1:
                            TextPointer.move_cursor(content, i, j, new_i + 1, 0)
                    return content
        return content

    @staticmethod
    def handle_backspace(content: list[list]):
        for i, row in enumerate(content):
            if 1 in row:
                idx = row.index(1)
                consecutive_spaces = 0
                for k in range(idx - 1, -1, -1):
                    if row[k] == ' ':
                        consecutive_spaces += 1
                    else:
                        break
                if consecutive_spaces >= 4:
                    del row[idx - 4:idx]
                elif consecutive_spaces > 0:
                    del row[idx - 1]
                elif idx > 0:
                    del row[idx - 1]
                else:
                    if i > 0:
                        prev_row = content[i - 1]
                        row.pop(idx)
                        prev_row.extend(row)
                        prev_row.append(1)
                        content.pop(i)
                    elif len(content) > 1:
                        row.pop(idx)
                        content[0].insert(0, 1)
                        if not row:
                            content.pop(i)
                if not row and i < len(content):
                    content[i] = [1]
                break
        return content

    @staticmethod
    def handle_enter(content: list[list]):
        for i, row in enumerate(content):
            if 1 in row:
                idx = row.index(1)
                new_row = row[idx:]
                row[idx:] = []
                content.insert(i + 1, new_row)
                break
        return content

    @staticmethod
    def handle_ctrl_backspace(content: list[list]):
        for i, row in enumerate(content):
            if 1 in row:
                idx = row.index(1)
                if idx > 0:
                    consecutive_spaces = 0
                    for k in range(idx - 1, -1, -1):
                        if row[k] == ' ':
                            consecutive_spaces += 1
                        else:
                            break
                    if consecutive_spaces >= 4:
                        del row[idx - 4:idx]
                    elif consecutive_spaces > 0:
                        del row[idx - 1]
                    elif idx > 0:
                        del row[idx - 1]
                break
        return content

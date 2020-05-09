console_colors = {
    "Black": "\u001b[30m",
    "Red": "\u001b[31m",
    "Green": "\u001b[32m",
    "Yellow": "\u001b[33m",
    "Blue": "\u001b[34m",
    "Magenta": "\u001b[35m",
    "Cyan": "\u001b[36m",
    "White": "\u001b[37m",
    "Reset": "\u001b[0m"
}

cols = (0, 11, 23, 16, 25, 22, 5)

def set_color(color):
    print(f"{console_colors[color]}", end="")

def reset_color():
    print(f"{console_colors['Reset']}", end="")

def set_position(row, column):
    print(f"\u001b[{row};{column}H", end="")

def clear_screen():
    print("\u001b[2J")

def print_result(result):
    to_print = result[["year_film", "film", "name", "category", "Genres", "Rate"]]
    temp = [to_print.iloc[i].values for i in range(len(to_print))]
    row = 2
    current_column = 1
    clear_screen()
    for column,e in enumerate(to_print.columns):
        current_column += cols[column]
        set_position(1, current_column)
        print(e, end="")
    for i, e in enumerate(temp):
        if result.iloc[i]["win"] == True:
            set_color("Yellow")
        else:
            set_color("Cyan")
        current_column = 1
        for column, text in enumerate(e):
            current_column += cols[column]
            set_position(row, current_column)
            text = redim_text(str(text), cols[column+1])
            print(text)
        row += 1


def redim_text(text, num_characters):
    if len(text) > num_characters-1:
        return text[:num_characters-4] + "..."
    return text
    
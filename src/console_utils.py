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

cols = (1, 12, 34, 51, 76, 98)

def set_color(color):
    print(f"{console_colors[color]}", end="")

def reset_color(text):
    print(f"{console_colors['Reset']}", end="")

def set_position(row, column):
    print(f"\u001b[{row};{column}H", end="")

def clear_screen():
    print("\u001b[2J")

def print_result(result):
    to_print = result[["year_film", "film", "name", "category", "Genres", "Rate"]]
    temp = [to_print.iloc[i].values for i in range(len(to_print))]
    row = 2
    clear_screen()
    for column,e in enumerate(to_print.columns):
        set_position(1, cols[column])
        print(e, end="")
    for i, e in enumerate(temp):
        if result.iloc[i]["win"] == True:
            set_color("Yellow")
        else:
            set_color("Cyan")
        for column, text in enumerate(e):
            set_position(row, cols[column])
            print(text, end = "")
        row += 1
import re

DIRTY_FILE = "bt_xi_3_1.csv"
CLEAN_FILE = "clean_" + DIRTY_FILE


def main():
    lines = []
    with open(DIRTY_FILE) as f:
        for line in f.readlines():
            line = line.strip()
            clean_line = re.sub(r'\{.*\}', 'lol', line)
            if line != clean_line:
                print(line)
                print(clean_line)
            lines.append(clean_line)
    with open(CLEAN_FILE, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == '__main__':
    main()

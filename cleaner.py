import os


def clean():
    directory = os.listdir(".")
    print("Removing temporary files...")
    for item in directory:
        if item.endswith((".txt", ".csv", ".jpg", ".png", ".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".synctex.gz", ".tex")) and item != "logo 512.png" and item != "latex.tex":
            os.remove(item)


if __name__ == '__main__':
    clean()

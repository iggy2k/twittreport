import os


def clean():
    directory = os.listdir(".")
    print("Removing temporary files...")
    for item in directory:
        if item.endswith((".txt", ".csv", ".jpg", ".html", ".png")) and item != "logo 512.png":
            os.remove(item)


if __name__ == '__main__':
    clean()
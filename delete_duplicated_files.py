import hashlib
import pathlib

def file_checksum(filename, printing=False):
    hasher = hashlib.sha256()
    try:
        try:
            with open(filename, 'rb') as afile:
                buf = afile.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(65536)
            checksum = hasher.hexdigest()
            if printing:
                print(filename + " - " + checksum)
            return checksum
        except PermissionError:
            return "ERROR"
    except Exception as e:
        return "ERROR"

def delete(file):
    print("Removing file:", str(file))
    file.unlink()


if __name__ == "__main__":
    path = pathlib.Path('./data')
    tested_imgs = []
    deleted = 0
    checked = 0
    for i in path.iterdir():
        if '.' not in str(i):
            for img in i.iterdir():
                if img.is_dir():
                    continue
                checked += 1
                checksum = file_checksum(img)
                print("File:", str(img), checksum)
                print("number:", checked)
                if checksum in tested_imgs:
                    delete(img)
                    deleted += 1
                    print("Files deleted:", deleted)
                else:
                    tested_imgs.append(checksum)
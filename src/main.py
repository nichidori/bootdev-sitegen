import os
import shutil


def main():
    copy_content(os.getcwd(), "static", "public")


def copy_content(directory, src, dst):
    src_path = os.path.join(directory, src)
    dst_path = os.path.join(directory, dst)

    if not os.path.exists(src_path):
        return

    if os.path.exists(dst_path):
        print(f"Removing existing directory {dst_path}")
        shutil.rmtree(dst_path)

    print(f"Creating directory {dst_path}")
    os.mkdir(dst_path)

    entries = os.listdir(src_path)
    for entry in entries:
        full_src = os.path.join(src_path, entry)
        full_dst = os.path.join(dst_path, entry)
        if os.path.isdir(full_src):
            entry_src = os.path.join(src, entry)
            entry_dst = os.path.join(dst, entry)
            copy_content(directory, entry_src, entry_dst)
        else:
            print(f"Copying file from {full_src} to {full_dst}")
            shutil.copy(full_src, full_dst)

    print(f"Finished copying {src} to {dst}")


if __name__ == "__main__":
    main()

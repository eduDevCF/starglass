import os
import shutil
from textnode import TextType, TextNode

def main():
    # new_node = TextNode("My boot.dev project", TextType.LINK, "https://github.com/eduDevCF/starglass")
    # print(new_node)

    # Capture abspaths for the static and public directories
    if not is_run_from_root():
        raise Exception("Error: main.py must be run from the project's root directory")
    static_path = os.path.abspath("./static")
    public_path = os.path.abspath("./public")

    # Empty the public folder and copy contents from static
    print("STARTING to empty public dir: ", public_path)
    public_contents = empty_public_dir(public_path)
    if len(public_contents) == 0:
        print("Public dir is empty. Ready to start copying!")
        print(f"STARTING TO COPY {static_path} to {public_path}")
        copy_folders(static_path, public_path)
    else:
        print("ERROR: Public dir failed to empty")


def is_run_from_root():
    cwd = os.getcwd()
    src_path = os.path.join(cwd, "src")
    if os.path.exists(src_path):
        return True
    return False


def empty_public_dir(public_path: str) -> list[str]:
    if not os.path.exists(public_path):
        raise Exception("public directory does not exist")
    
    contents = os.listdir(public_path)

    if len(contents) != 0:
        # delete the public directory tree
        print("DELETING ", public_path)
        shutil.rmtree(public_path)
        if os.path.exists(public_path):
            raise Exception("ERROR: Public directory did not get deleted")
        else:
            print("MAKING a new PUBLIC DIRECTORY at ", public_path)
            os.mkdir(public_path)
            contents = os.listdir(public_path)
    else:
        print("ALERT: Public dir is already empty")
    
    return contents



def copy_folders(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        raise Exception(f"SRC_DIR does not exist: {src_dir}")
    if not os.path.exists(dst_dir):
        raise Exception(f"DST_DIR does not exist: {dst_dir}")

    contents = os.listdir(src_dir)
    print(f"CONTENTS of {src_dir}: {contents}")
    for item in contents:
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst_dir)
            print(f"COPIED {item_path} to {dst_dir} directory")
        elif os.path.isdir(item_path):
            new_dst_path = os.path.join(dst_dir, item)
            print("MAKING DIR:", new_dst_path)
            os.mkdir(new_dst_path)
            new_src_path = os.path.join(src_dir, item)
            print(f"CALLING copy_folder on {new_src_path} and {new_dst_path}")
            copy_folders(new_src_path, new_dst_path)
        else:
            print(f"ATTN: {item_path} is not a file nor a directory")
    print("DONE with", src_dir)




if __name__ == '__main__':
    main()

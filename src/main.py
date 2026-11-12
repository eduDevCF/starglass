import os
import shutil
import sys
from textnode import TextType, TextNode
from parse_markdown import markdown_to_html_node, extract_title

def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]

    # Capture abspaths for the static and public directories
    if not is_run_from_root():
        raise Exception("Error: main.py must be run from the project's root directory")
    static_path = os.path.abspath("./static")
    public_path = os.path.abspath("./docs")
    template_path = os.path.abspath("template.html")
    content_path = os.path.abspath("./content")
    print(f"PATHS:\n static - {static_path}\n public - {public_path}\n template - {template_path}\n content - {content_path}\n")

    # Empty the public folder (now called "/docs") and copy contents from static
    print("STARTING to empty public dir: ", public_path)
    public_contents = empty_public_dir(public_path)
    if len(public_contents) == 0:
        print("Public dir is empty. Ready to start copying!")
        print(f"STARTING TO COPY {static_path} to {public_path}")
        copy_folders(static_path, public_path)
    else:
        print("ERROR: Public dir failed to empty")

    print("GENERATING pages from /content to /docs")
    generate_pages_recursive(content_path, template_path, public_path, basepath)


def generate_pages_recursive(src_dir: str, template_path: str, dst_dir: str, basepath: str) -> None:
    check_paths_exist([src_dir, template_path])
    contents = os.listdir(src_dir)
    print(f"CONTENTS of {src_dir}: {contents}")
    for content in contents:
        content_path = os.path.join(src_dir, content)
        if os.path.isfile(content_path):
            if content[-3:] == ".md":
                public_name = content[:-3] + ".html"
                public_path = os.path.join(dst_dir, public_name)
                generate_page(content_path, template_path, public_path, basepath)
                print(f"GENERATED PAGE: {content_path} to {public_path}")
        elif os.path.isdir(content_path):
            new_dst_path = os.path.join(dst_dir, content)
            new_src_path = os.path.join(src_dir, content)
            print(f"CALLING generate_pages_recursive on {new_src_path} and {new_dst_path}")
            generate_pages_recursive(new_src_path, template_path, new_dst_path, basepath)
        else:
            print(f"ATTN: {content_path} is not a file nor a directory")
    print("DONE with", src_dir)


def is_run_from_root():
    cwd = os.getcwd()
    src_path = os.path.join(cwd, "src")
    if os.path.exists(src_path):
        return True
    return False


def empty_public_dir(public_path: str) -> list[str]:
    check_paths_exist([public_path])

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


def check_paths_exist(paths: list[str]) -> None:
    for i in range(len(paths)):
        if not os.path.exists(paths[i]):
            raise Exception(f"PATH {i+1} does not exist: {paths[i]}")


def copy_folders(src_dir: str, dst_dir: str) -> None:
    check_paths_exist([src_dir, dst_dir])

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


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    check_paths_exist([from_path, template_path])
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template_html = f.read()
    
    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_html = template_html.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page_html = page_html.replace('href="/', 'href="' + basepath)
    page_html = page_html.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        num_chars = f.write(page_html)
    
    if num_chars == len(page_html):
        print(f"Successfully generated page at {dest_path}!")
    else:
        raise Exception(f"ALERT: file write oddity - {num_chars} out of {len(page_html)} chars written")


if __name__ == '__main__':
    main()

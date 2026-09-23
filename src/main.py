from textnode import TextType, TextNode

def main():
    new_node = TextNode("My boot.dev project", TextType.LINK, "https://github.com/eduDevCF/starglass")
    print(new_node)


if __name__ == '__main__':
    main()

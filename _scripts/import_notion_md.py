import zipfile
import shutil
import argparse
import os
import re
import urllib.parse
import glob


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--notion-md-zip', type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    post_dir = os.path.join(base_dir, "_posts")
    shutil.rmtree(post_dir, ignore_errors=True)
    os.mkdir(post_dir)

    notion_md_zip = args.notion_md_zip
    notion_md_zip_file = os.path.basename(notion_md_zip)

    notion_dir = os.path.join(base_dir, '_notion')
    shutil.rmtree(notion_dir, ignore_errors=True)
    os.mkdir(notion_dir)
    notion_md_copied = os.path.join(notion_dir, notion_md_zip_file)

    # copy notion md zip file
    shutil.copy(notion_md_zip, notion_md_copied)
    
    # unzip notion md zip file
    notion_md_unzipped = os.path.splitext(notion_md_copied)[0]
    with zipfile.ZipFile(notion_md_copied, "r") as zip_file:
        zip_file.extractall(notion_md_unzipped)

    # read main md
    main_md = [ f for f in os.listdir(notion_md_unzipped) if os.path.isfile(os.path.join(notion_md_unzipped, f))][0]
    main_md_quoted = urllib.parse.quote(main_md)
    main_md_quoted_name = os.path.splitext(main_md_quoted)[0]
    
    # make README.md
    with open(os.path.join(base_dir, "README.md"), "w+") as readme:
        readme.writelines([
            "---\n"
            "layout: home\n",
            "title: Home\n",
            "permalink: /\n",
            "---\n"
        ])

        with open(os.path.join(notion_md_unzipped, main_md), "r") as main_md_file:
            link_regex = r"^\[.*\]\(.*\)"
            category_regex = r"^## .*"
            category = None
            for line in main_md_file.readlines():
                category_matched = re.search(category_regex, line[:-1])
                if category_matched:
                    category = category_matched.group()
                    category = category.replace("## ", "")

                link_matched = re.search(link_regex, line[:-1])
                if link_matched:
                    link_str = link_matched.group()
                    link_title = re.search(r"^\[.*\]", link_str).group()[1:-1]

                    link_title_encoded = link_title.strip()
                    link_title_encoded = re.sub(r"[^a-zA-Z0-9 ]", "", link_title).strip()
                    link_title_encoded = re.sub(r"\s+", "-", link_title_encoded) # space

                    link_hash = re.split(r"^\[.*\]", link_str)[1][-32-4:-4]
                    link_url = f"{link_title_encoded}-{link_hash}"
                    link_url = re.sub(r"--", "-", link_url)
                    link_url = re.sub(r"^-", "", link_url)

                    readme.write(f"[{link_title}](https://boundless-whitefish-53e.notion.site/{link_url})\n")

                    with open(os.path.join(post_dir, f"2019-04-28-{link_hash}.md"), "w+") as post_md_file:
                        post_md_file.writelines([
                            "---\n",
                            f"title: {link_title}\n",
                            f"slug: {link_hash}\n",
                            "author: Dong-Yong Lee\n",
                            f"category: {category}\n",
                            "date: 2019-04-28\n",
                            f"external: {link_url}\n",
                            "layout: post\n",
                            "---\n",
                        ])
                        post_md_file.write(f"\n[https://boundless-whitefish-53e.notion.site/{link_url}](https://boundless-whitefish-53e.notion.site/{link_url})")
                else:
                    readme.write(line)
                # readme.write(line.replace(main_md_quoted_name, f"https://boundless-whitefish-53e.notion.site").replace(".md", ""))
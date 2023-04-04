import os
import numpy as np
import argparse

config = argparse.ArgumentParser()
config.add_argument("--dir", "-d", help="Top direction path to create readme_map.", default="./")  # 默认处理路径
config.add_argument("--level", help="Max number of level.", type=int, default=3)  # 最大标题层级
config.add_argument('-l','--skip_list', nargs='*', help='<Required> Set flag', required=False, default=[])  # 跳过的的文件夹(包含即跳过)
config.add_argument("--output", "-o", help="Output file path.", default="./readme_map.md")  # 默认处理路径

config = config.parse_args()
config.skip_list.extend([".obsidian", ".Assets", ".assets", ".git", "__pycache__", ".idea", ".vs"])
print(config)


def create_link(fp, full_path, level, pre_fix):
    """ 递归访问每个文件夹 -> 构建出文件链接
    fp: 输出文件句柄
    full_path: 当前处理的文件夹全路径
    pre_fix: int 当前文件夹对应的level (一级标题 #, 二级标题 ##)
    """
    files = os.listdir(full_path)

    # list of md file and usefull dir name
    name_md = []
    name_dir = []
    for file in files:
        if file.endswith(".md"):
            name_md.append(file)
        elif os.path.isdir(os.path.join(full_path, file)):
            is_special = [ file.find(s) >= 0 for s in config.skip_list ]  # wiout post fix
            if np.any(is_special):
                continue
            name_dir.append(file)

    # write md link
    for item in name_md:
        s = "- [{}]({})\n".format(item[:item.rfind(".md")], os.path.join(full_path, item))
        fp.write(s)
    fp.write("\n")
        
    # write dir
    for item in name_dir:
        dir_path = os.path.join(full_path, item)
        if level <= config.level:
            s = pre_fix + "# {}\n".format(item)
            fp.write(s)
            s = "> [dir:{}]({})\n\n".format(item, dir_path)
            fp.write(s)
            create_link(fp, dir_path, level + 1, pre_fix+"#")
        else:
            if pre_fix.find("#") >= 0:
                pre_fix = "-"
            s = "**[{}]({})**\n".format(item, dir_path)
            fp.write(s)
            create_link(fp, dir_path, level + 1, pre_fix)
            return

"""
以 path 为数据库来创建readme
"""
with open(config.output, mode='w', encoding="utf-8") as fp:
    create_link(fp, config.dir, 1, "")
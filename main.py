#!/usr/bin/env python3
"""
分离PNG图像的RGB和Alpha通道
参数：文件夹路径
处理文件夹中的所有PNG文件，生成：
1. RGB图像（无Alpha通道），保持原文件名
2. Alpha图像（灰度），文件名为原文件名加下划线前缀（例如 a.png -> a_.png）
注意：Alpha图像中，不透明区域为黑色，透明区域为白色（使用反转Alpha值：255 - 原始Alpha）
"""

import os
import sys
from pathlib import Path
from PIL import Image
import argparse


def split_png_rgb_alpha(image_path: Path, output_dir: Path = None):
    """
    分离单个PNG图像的RGB和Alpha通道
    
    Args:
        image_path: 输入PNG文件路径
        output_dir: 输出目录（如果为None，则覆盖原文件？）
    """
    try:
        with Image.open(image_path) as img:
            print(f"处理: {image_path.name}")
            print(f"  原始模式: {img.mode}, 尺寸: {img.size}")
            
            # 检查是否有alpha通道
            has_alpha = img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info)
            print(f"  是否有Alpha通道: {has_alpha}")
            
            # 转换为RGBA（确保有alpha通道）
            rgba = img.convert("RGBA")
            # 分离通道
            r, g, b, a = rgba.split()
            
            # 分析alpha通道（使用get_flattened_data避免弃用警告）
            try:
                a_data = list(a.get_flattened_data())
            except AttributeError:
                # 回退到getdata（旧版本Pillow）
                a_data = list(a.getdata())
            a_min = min(a_data)
            a_max = max(a_data)
            a_avg = sum(a_data) / len(a_data) if a_data else 0
            print(f"  Alpha范围: {a_min} - {a_max}, 平均值: {a_avg:.2f}")
            
            if a_min == a_max:
                print(f"  警告: Alpha通道是恒定的 ({a_min})，生成的Alpha图像将是纯色")
            else:
                # 计算不同值的数量
                unique_values = len(set(a_data))
                print(f"  Alpha不同值数量: {unique_values}")
            
            # 创建RGB图像（合并RGB通道，无Alpha）
            rgb_img = Image.merge("RGB", (r, g, b))
            
            # 反转Alpha通道：255 - a（不透明区域变为黑色，透明区域变为白色）
            a_inv = a.point(lambda x: 255 - x)
            # 创建Alpha灰度图像（RGB模式，三个通道相同，兼容性更好）
            alpha_img = Image.merge("RGB", (a_inv, a_inv, a_inv))
            
            # 确定输出路径
            if output_dir is None:
                output_dir = image_path.parent
            
            # RGB输出文件名（与原文件相同）
            rgb_output_path = output_dir / image_path.name
            # Alpha输出文件名：原文件名加下划线前缀
            stem = image_path.stem
            suffix = image_path.suffix
            alpha_output_path = output_dir / f"{stem}_{suffix}"
            
            # 保存图像
            rgb_img.save(rgb_output_path, "PNG")
            alpha_img.save(alpha_output_path, "PNG")
            
            print(f"处理完成: {image_path.name}")
            print(f"  RGB保存至: {rgb_output_path}")
            print(f"  Alpha保存至: {alpha_output_path}")
            
    except Exception as e:
        print(f"处理失败 {image_path.name}: {e}")


def process_directory(directory_path: Path):
    """
    处理目录中的所有PNG文件
    """
    if not directory_path.exists():
        print(f"错误: 目录不存在 {directory_path}")
        return False
    
    if not directory_path.is_dir():
        print(f"错误: 不是目录 {directory_path}")
        return False
    
    # 查找所有PNG文件（使用集合去重，避免大小写重复）
    png_files_set = set()
    for pattern in ("*.png", "*.PNG"):
        for file in directory_path.glob(pattern):
            png_files_set.add(file.resolve())  # 使用绝对路径避免重复
    
    png_files = sorted(png_files_set)
    
    if not png_files:
        print(f"警告: 目录中没有PNG文件 {directory_path}")
        return True
    
    print(f"找到 {len(png_files)} 个PNG文件")
    
    for png_file in png_files:
        split_png_rgb_alpha(png_file, directory_path)
    
    return True


def main():
    parser = argparse.ArgumentParser(description="分离PNG图像的RGB和Alpha通道")
    parser.add_argument("directory", help="包含PNG文件的文件夹路径")
    args = parser.parse_args()
    
    directory_path = Path(args.directory).resolve()
    
    if not directory_path.exists():
        print(f"错误: 路径不存在 {directory_path}")
        sys.exit(1)
    
    success = process_directory(directory_path)
    if not success:
        sys.exit(1)
    
    print("所有文件处理完成")


if __name__ == "__main__":
    main()

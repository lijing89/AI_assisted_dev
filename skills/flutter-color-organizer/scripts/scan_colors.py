#!/usr/bin/env python3
"""扫描 Flutter 项目中的颜色使用并生成报告"""
import re
import os
import json
from pathlib import Path
from collections import defaultdict

# 颜色模式匹配
PATTERNS = {
    'Colors.': r'Colors\.\w+',
    'Color.fromARGB': r'Color\.fromARGB\([^)]+\)',
    'Color.fromRGBO': r'Color\.fromRGBO\([^)]+\)',
    'Color(0x': r'Color\(0x[0-9A-Fa-f]+\)',
}

def scan_file(file_path):
    """扫描单个文件中的颜色使用"""
    colors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern_name, pattern in PATTERNS.items():
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        colors.append({
                            'file': str(file_path),
                            'line': line_num,
                            'type': pattern_name,
                            'original': match.group(),
                            'context': line.strip()
                        })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return colors

def scan_project(project_root, exclude_dirs=None):
    """扫描整个项目"""
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'build', '.dart_tool', 'ios', 'android', '.cursor'}
    
    all_colors = []
    dart_files = []
    
    # 查找所有 .dart 文件
    for root, dirs, files in os.walk(project_root):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.dart'):
                file_path = os.path.join(root, file)
                dart_files.append(file_path)
                colors = scan_file(file_path)
                all_colors.extend(colors)
    
    return all_colors, dart_files

def scan_target(target_path, exclude_dirs=None):
    """扫描指定的文件或文件夹"""
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'build', '.dart_tool', 'ios', 'android', '.cursor'}
    
    target = Path(target_path)
    
    # 如果是单个文件
    if target.is_file():
        if target.suffix == '.dart':
            colors = scan_file(target)
            return colors, [str(target)]
        else:
            print(f"⚠️  {target_path} is not a .dart file")
            return [], []
    
    # 如果是文件夹
    elif target.is_dir():
        return scan_project(target_path, exclude_dirs)
    
    # 路径不存在
    else:
        print(f"❌ Path not found: {target_path}")
        return [], []

def convert_to_hex(color_str):
    """将颜色转换为 16 进制格式"""
    # Colors.red -> 0xFFFF0000
    color_map = {
        'Colors.red': '0xFFF44336',
        'Colors.blue': '0xFF2196F3',
        'Colors.green': '0xFF4CAF50',
        'Colors.yellow': '0xFFFFEB3B',
        'Colors.orange': '0xFFFF9800',
        'Colors.purple': '0xFF9C27B0',
        'Colors.pink': '0xFFE91E63',
        'Colors.white': '0xFFFFFFFF',
        'Colors.black': '0xFF000000',
        'Colors.grey': '0xFF9E9E9E',
        'Colors.transparent': '0x00000000',
    }
    
    if color_str.startswith('Colors.'):
        return color_map.get(color_str, None)
    
    # Color.fromARGB(255, 244, 67, 54) -> 0xFFF44336
    if 'fromARGB' in color_str:
        match = re.search(r'\(([^)]+)\)', color_str)
        if match:
            parts = [p.strip() for p in match.group(1).split(',')]
            if len(parts) == 4:
                try:
                    a, r, g, b = [int(float(p)) for p in parts]
                    return f"0x{a:02X}{r:02X}{g:02X}{b:02X}"
                except:
                    return None
    
    # Color.fromRGBO(244, 67, 54, 1) -> 0xFFF44336
    if 'fromRGBO' in color_str:
        match = re.search(r'\(([^)]+)\)', color_str)
        if match:
            parts = [p.strip() for p in match.group(1).split(',')]
            if len(parts) == 4:
                try:
                    r, g, b, a = [float(p) for p in parts]
                    # Handle both 0-255 and 0-1 ranges
                    if r <= 1 and g <= 1 and b <= 1:
                        r, g, b = int(r * 255), int(g * 255), int(b * 255)
                    else:
                        r, g, b = int(r), int(g), int(b)
                    a_val = int(a * 255) if a <= 1 else int(a)
                    return f"0x{a_val:02X}{r:02X}{g:02X}{b:02X}"
                except:
                    return None
    
    # Color(0xFFFF0000) -> 已经是 16 进制格式
    if color_str.startswith('Color(0x'):
        match = re.search(r'0x[0-9A-Fa-f]+', color_str)
        if match:
            return match.group()
    
    return None

def categorize_by_module(colors):
    """根据文件路径分类颜色"""
    modules = defaultdict(list)
    
    for color in colors:
        file_path = color['file']
        
        # 提取模块名（从 lib/ 后的第一个目录）
        if '/lib/' in file_path:
            parts = file_path.split('/lib/')[-1].split('/')
            if len(parts) > 1:
                module = parts[0]
            else:
                module = 'root'
        else:
            module = 'unknown'
        
        modules[module].append(color)
    
    return dict(modules)

def generate_report(colors, output_file='color_report.json'):
    """生成颜色使用报告"""
    # 按模块分类
    modules = categorize_by_module(colors)
    
    # 统计信息
    stats = {
        'total_colors': len(colors),
        'by_type': defaultdict(int),
        'by_module': {module: len(items) for module, items in modules.items()},
        'unique_colors': set()
    }
    
    for color in colors:
        stats['by_type'][color['type']] += 1
        hex_color = convert_to_hex(color['original'])
        if hex_color:
            stats['unique_colors'].add(hex_color)
    
    stats['unique_colors'] = list(stats['unique_colors'])
    stats['by_type'] = dict(stats['by_type'])
    
    report = {
        'stats': stats,
        'modules': modules,
        'colors': colors
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Report saved to {output_file}")
    print(f"\n📊 Statistics:")
    print(f"  Total colors found: {stats['total_colors']}")
    print(f"  Unique colors: {len(stats['unique_colors'])}")
    print(f"  By type:")
    for type_name, count in stats['by_type'].items():
        print(f"    {type_name}: {count}")
    print(f"  By module:")
    for module, count in stats['by_module'].items():
        print(f"    {module}: {count}")
    
    return report

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scan_colors.py <file_or_folder_path> [output_file]")
        print("\nExamples:")
        print("  python scan_colors.py lib/page/live/")
        print("  python scan_colors.py lib/page/home/home_page.dart")
        print("  python scan_colors.py . colors.json")
        sys.exit(1)
    
    target_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'color_report.json'
    
    print(f"🔍 Scanning: {target_path}")
    colors, dart_files = scan_target(target_path)
    print(f"📄 Found {len(dart_files)} Dart files")
    
    if colors:
        report = generate_report(colors, output_file)
    else:
        print("⚠️  No colors found")

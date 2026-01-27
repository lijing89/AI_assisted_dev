#!/usr/bin/env python3
"""规范化颜色定义并更新 lib/util/ui.dart"""
import re
import json
from pathlib import Path
from collections import defaultdict

def convert_to_hex(color_str):
    """将颜色转换为 Color(0xFFFFFFFF) 格式"""
    # Colors.red -> Color(0xFFFF0000)
    color_map = {
        'Colors.red': 'Color(0xFFF44336)',
        'Colors.blue': 'Color(0xFF2196F3)',
        'Colors.green': 'Color(0xFF4CAF50)',
        'Colors.yellow': 'Color(0xFFFFEB3B)',
        'Colors.orange': 'Color(0xFFFF9800)',
        'Colors.purple': 'Color(0xFF9C27B0)',
        'Colors.pink': 'Color(0xFFE91E63)',
        'Colors.white': 'Color(0xFFFFFFFF)',
        'Colors.black': 'Color(0xFF000000)',
        'Colors.grey': 'Color(0xFF9E9E9E)',
        'Colors.transparent': 'Color(0x00000000)',
    }
    
    if color_str.startswith('Colors.'):
        return color_map.get(color_str, None)
    
    # Color.fromARGB(255, 244, 67, 54) -> Color(0xFFF44336)
    if 'fromARGB' in color_str:
        match = re.search(r'fromARGB\(([^)]+)\)', color_str)
        if match:
            parts = [p.strip() for p in match.group(1).split(',')]
            if len(parts) == 4:
                a, r, g, b = [int(p) for p in parts]
                return f"Color(0x{a:02X}{r:02X}{g:02X}{b:02X})"
    
    # Color.fromRGBO(244, 67, 54, 1) -> Color(0xFFF44336)
    if 'fromRGBO' in color_str:
        match = re.search(r'fromRGBO\(([^)]+)\)', color_str)
        if match:
            parts = [p.strip() for p in match.group(1).split(',')]
            if len(parts) == 4:
                r, g, b = [int(p) for p in parts[:3]]
                a = int(float(parts[3]) * 255)
                return f"Color(0x{a:02X}{r:02X}{g:02X}{b:02X})"
    
    # Color(0xFFFF0000) -> 已经是规范格式
    if color_str.startswith('Color(0x'):
        match = re.search(r'Color\((0x[0-9A-Fa-f]{8})\)', color_str)
        if match:
            return f"Color({match.group(1)})"
    
    return None

def generate_color_name(hex_value, module, index):
    """生成颜色变量名"""
    # 从模块名生成前缀
    module_prefix = ''.join([word.capitalize() for word in module.split('_')])
    return f"color{module_prefix}{index + 1}"

def update_ui_file(report, ui_file_path):
    """更新 lib/util/ui.dart 文件"""
    with open(ui_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 ColorUi 类的结束位置
    class_match = re.search(r'class ColorUi \{(.*?)\n\}', content, re.DOTALL)
    if not class_match:
        print("❌ Cannot find ColorUi class in ui.dart")
        return False
    
    # 按模块组织颜色
    modules = report['modules']
    new_colors = []
    
    for module, colors in sorted(modules.items()):
        if not colors:
            continue
        
        new_colors.append(f"\n  /// {module.upper()} 模块颜色")
        
        # 去重
        unique_colors = {}
        for color in colors:
            hex_color = convert_to_hex(color['original'])
            if hex_color and hex_color not in unique_colors.values():
                color_name = generate_color_name(hex_color, module, len(unique_colors))
                unique_colors[color_name] = hex_color
        
        # 添加颜色定义
        for color_name, hex_value in unique_colors.items():
            new_colors.append(f"  static const Color {color_name} = {hex_value};")
    
    # 插入新颜色定义到 ColorUi 类末尾
    insert_pos = class_match.end(1)
    new_content = content[:insert_pos] + '\n' + '\n'.join(new_colors) + content[insert_pos:]
    
    # 保存文件
    backup_path = ui_file_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup saved to {backup_path}")
    
    with open(ui_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Updated {ui_file_path}")
    
    return True

def replace_in_files(report):
    """替换项目文件中的颜色定义为 ColorUi 引用"""
    # 这个功能需要更复杂的实现，暂时留空
    pass

if __name__ == '__main__':
    import sys
    
    report_file = sys.argv[1] if len(sys.argv) > 1 else 'color_report.json'
    ui_file = sys.argv[2] if len(sys.argv) > 2 else 'lib/util/ui.dart'
    
    print(f"📖 Reading report: {report_file}")
    with open(report_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"📝 Updating {ui_file}")
    update_ui_file(report, ui_file)

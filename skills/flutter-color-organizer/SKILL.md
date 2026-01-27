---
name: flutter-color-organizer
description: "Organize and normalize Flutter color definitions in specific files or folders. Use when working with Flutter projects to: (1) Scan specified files/folders for color usages (Colors.red, Color.fromARGB, Color.fromRGBO, etc.), (2) Consolidate colors into lib/util/ui.dart ColorUi class, (3) Normalize colors to hexadecimal format Color(0xFFFFFFFF), (4) Organize colors by functional modules, or (5) Replace scattered color definitions with centralized references. Supports scanning entire projects, specific folders, or individual files."
---

# Flutter Color Organizer

扫描、整理和规范化 Flutter 项目中的颜色定义。支持扫描整个项目、指定文件夹或单个文件，帮助维护一致的颜色使用规范，并将所有颜色整合到 `lib/util/ui.dart` 中。

## Workflow

### Step 1: Scan Colors

扫描指定的文件、文件夹或整个项目以识别颜色使用：

```bash
python scripts/scan_colors.py <file_or_folder_path> [output_file]
```

**参数：**
- `file_or_folder_path`: 要扫描的目标（必需）
  - 单个文件：`lib/page/home/home_page.dart`
  - 指定文件夹：`lib/page/live/`
  - 整个项目：`.` 或项目根目录路径
- `output_file`: JSON 报告输出路径（默认：`color_report.json`）

**使用示例：**
```bash
# 扫描单个文件
python scripts/scan_colors.py lib/page/home/home_page.dart

# 扫描指定文件夹
python scripts/scan_colors.py lib/page/live/

# 扫描整个项目
python scripts/scan_colors.py /path/to/flutter/project

# 指定输出文件
python scripts/scan_colors.py lib/page/live/ live_colors.json
```

**输出：**
- JSON 报告包含统计信息、模块分类和所有颜色出现位置
- 检测类型：`Colors.*`、`Color.fromARGB()`、`Color.fromRGBO()`、`Color(0x...)`

### Step 2: Review Report

Examine `color_report.json` to understand:
- Total colors found and unique colors
- Distribution by type (Colors.*, fromARGB, fromRGBO, hex)
- Organization by functional modules (extracted from file paths)

**Example report structure:**
```json
{
  "stats": {
    "total_colors": 150,
    "unique_colors": 45,
    "by_type": {"Colors.": 30, "Color.fromRGBO": 80, ...},
    "by_module": {"live": 50, "chat": 40, "home": 30, ...}
  },
  "modules": {
    "live": [...],
    "chat": [...]
  }
}
```

### Step 3: Update lib/util/ui.dart

Add new colors to `ColorUi` class organized by module:

```bash
python scripts/normalize_colors.py [color_report.json] [lib/util/ui.dart]
```

**What it does:**
- Reads color report
- Converts all colors to `Color(0xFFFFFFFF)` format
- Generates color constants organized by module
- Appends to `ColorUi` class
- Creates backup at `lib/util/ui.dart.backup`

**Example output in ui.dart:**
```dart
class ColorUi {
  // ... existing colors ...

  /// LIVE 模块颜色
  static const Color colorLive1 = Color(0xFFF44336);
  static const Color colorLive2 = Color(0xFF2196F3);

  /// CHAT 模块颜色
  static const Color colorChat1 = Color(0xFF4CAF50);
  static const Color colorChat2 = Color(0xFFFFEB3B);
}
```

### Step 4: Replace Original Color References

Manually replace color references in source files:

**Before:**
```dart
Container(
  color: Colors.red,
  child: Text('Hello', style: TextStyle(color: Color.fromRGBO(244, 67, 54, 1))),
)
```

**After:**
```dart
Container(
  color: ColorUi.colorLive1,
  child: Text('Hello', style: TextStyle(color: ColorUi.colorLive2)),
)
```

Use search and replace based on the report to update references systematically.

## Color Format Normalization

All colors are normalized to `Color(0xFFRRGGBB)` format:

| Original | Normalized |
|----------|------------|
| `Colors.red` | `Color(0xFFF44336)` |
| `Color.fromARGB(255, 244, 67, 54)` | `Color(0xFFF44336)` |
| `Color.fromRGBO(244, 67, 54, 1)` | `Color(0xFFF44336)` |
| `Color(0xFFF44336)` | `Color(0xFFF44336)` (no change) |

## Best Practices

1. **按需扫描** - 可以只扫描特定模块或文件，无需每次扫描整个项目
2. **逐步整理** - 先整理单个文件夹，确认无误后再扩大范围
3. **更新前审查** - 检查颜色是否应与现有颜色合并
4. **使用语义化命名** - 重命名自动生成的名称（如 `colorLive1` → `colorLivePrimary`）
5. **按用途分组** - 按语义含义而非仅按模块组织颜色
6. **添加注释** - 为颜色添加说明其用途的注释

## Module Organization

颜色根据文件路径自动组织：
- `lib/page/live/` → `LIVE` 模块
- `lib/page/chat/` → `CHAT` 模块
- `lib/page/home/` → `HOME` 模块
- 等

在运行规范化脚本之前，可根据需要调整报告中的模块名称。

## 使用场景

**场景 1：整理单个功能模块**
```bash
# 只扫描直播模块
python scripts/scan_colors.py lib/page/live/ live_colors.json
python scripts/normalize_colors.py live_colors.json lib/util/ui.dart
```

**场景 2：快速检查单个文件**
```bash
# 检查某个页面的颜色使用
python scripts/scan_colors.py lib/page/home/home_page.dart
```

**场景 3：整个项目颜色审查**
```bash
# 扫描整个项目
python scripts/scan_colors.py . all_colors.json
python scripts/normalize_colors.py all_colors.json lib/util/ui.dart
```

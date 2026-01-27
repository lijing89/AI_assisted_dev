# AI 辅助开发资源库

收集和整理 AI 辅助软件开发过程中的实用工具、技能脚本和最佳实践。

## 📁 项目结构

```
AI_assisted_dev/
├── skills/                          # AI 辅助开发技能集合
│   └── flutter-color-organizer/    # Flutter 颜色管理工具
│       ├── scripts/                # Python 脚本
│       │   ├── scan_colors.py     # 扫描项目中的颜色使用
│       │   └── normalize_colors.py # 规范化颜色定义
│       └── SKILL.md               # 技能说明文档
└── README.md
```

## 🛠️ 已包含的技能

### Flutter Color Organizer

扫描、整理和规范化 Flutter 项目中的颜色定义，支持指定文件、文件夹或整个项目。

**功能：**
- 🔍 扫描指定文件/文件夹/整个项目中的颜色使用（`Colors.*`、`Color.fromARGB`、`Color.fromRGBO`等）
- 📊 生成颜色使用报告（统计、分布、模块化分组）
- 🎨 将颜色统一规范化为十六进制格式 `Color(0xFFFFFFFF)`
- 📦 按功能模块组织颜色到 `lib/util/ui.dart`
- 🎯 支持渐进式整理，无需一次性扫描整个项目

**查看详情：** [skills/flutter-color-organizer/SKILL.md](skills/flutter-color-organizer/SKILL.md)

## 🚀 快速开始

每个技能目录包含独立的使用说明，请查看对应的 `SKILL.md` 文件。

### Flutter Color Organizer 使用示例

```bash
# 扫描单个文件
python skills/flutter-color-organizer/scripts/scan_colors.py lib/page/home/home_page.dart

# 扫描指定文件夹
python skills/flutter-color-organizer/scripts/scan_colors.py lib/page/live/

# 扫描整个项目
python skills/flutter-color-organizer/scripts/scan_colors.py /path/to/flutter/project

# 规范化颜色定义
python skills/flutter-color-organizer/scripts/normalize_colors.py
```

## 📝 技能列表

| 技能名称 | 说明 | 适用场景 |
|---------|------|---------|
| flutter-color-organizer | Flutter 颜色管理工具 | Flutter 项目颜色整理和规范化 |

## 🤝 贡献

欢迎贡献新的 AI 辅助开发技能和工具！

### 添加新技能

1. 在 `skills/` 目录下创建新文件夹
2. 添加 `SKILL.md` 说明文档
3. 包含必要的脚本或工具文件
4. 更新本 README 文件

## 📄 License

MIT License

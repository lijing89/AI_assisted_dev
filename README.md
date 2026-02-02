# AI 辅助开发资源库

收集和整理 AI 辅助软件开发过程中的实用工具、技能脚本和最佳实践。

## 📁 项目结构

```
AI_assisted_dev/
├── skills/                          # AI 辅助开发技能集合
│   ├── flutter-color-organizer/    # Flutter 颜色管理工具
│   │   ├── scripts/                # Python 脚本
│   │   │   ├── scan_colors.py     # 扫描项目中的颜色使用
│   │   │   └── normalize_colors.py # 规范化颜色定义
│   │   └── SKILL.md               # 技能说明文档
│   ├── git-commit-cream/           # Git 提交信息生成助手
│   │   └── SKILL.md               # 技能说明文档
│   ├── 多彩输出/                   # 多彩输出技能
│   │   └── SKILL.md               # 技能说明文档
│   └── requirement2code/           # 全流程开发专家
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

### Git Commit Cream

生成高质量、简洁的中文 Git 提交信息，并根据特定规则过滤变动（自动忽略 ios/android 目录）。

**功能：**
- 🧹 智能过滤：自动忽略 `ios/` 和 `android/` 目录下的所有文件变动
- 📝 中文生成：生成符合规范的中文提交信息
- 🎯 格式规范：遵循 `<type>: <subject>` 格式
- ⚡️ 专注核心：专注于实际代码逻辑变更，排除原生构建配置干扰

**查看详情：** [skills/git-commit-cream/SKILL.md](skills/git-commit-cream/SKILL.md)

### 多彩输出

用多种颜色来包装 AI 回复的内容，通过颜色来区分内容的重要度，一眼就知道回复的关键点在哪里。

**功能：**
- 🎨 视觉增强：使用不同颜色区分信息类型（红、绿、蓝、粉、黄）
- 🎯 重点突出：自动高亮关键信息、警告、成功提示等
- 💬 自然触发：支持 "请用多彩颜色回复"、"多彩输出" 等自然语言触发
- 🚀 无需脚本：基于 Prompt 模板直接生效

**查看详情：** [skills/多彩输出/SKILL.md](skills/多彩输出/SKILL.md)

### Requirement2Code (全流程开发专家)

整合需求分析、架构设计、任务规划和代码实现四个阶段，从模糊需求直接交付高质量代码。

**功能：**
- 🔄 全流程覆盖：需求 -> 架构 -> 任务 -> 代码，端到端交付
- 📑 标准化文档：自动生成 `REQUIREMENT.md`、`DESIGN.md` 和 `TODO.md`
- 🤖 角色扮演：自动切换分析师、架构师、规划师和执行者角色
- ⚙️ 灵活模式：支持“分步确认模式”（复杂项目）和“自动流模式”（快速原型）

**查看详情：** [skills/requirement2code/SKILL.md](skills/requirement2code/SKILL.md)

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
| git-commit-cream | Git 提交信息生成助手 | 自动生成中文 Commit Message，智能忽略移动端构建文件 |
| 多彩输出 | 智能颜色排版 | 提升 AI 回复的可读性和重点识别效率 |
| requirement2code | 全流程开发专家 | 从模糊需求到代码实现的端到端标准化开发流程 |

## 🤝 贡献

欢迎贡献新的 AI 辅助开发技能和工具！

### 添加新技能

1. 在 `skills/` 目录下创建新文件夹
2. 添加 `SKILL.md` 说明文档
3. 包含必要的脚本或工具文件
4. 更新本 README 文件

## 📄 License

MIT License

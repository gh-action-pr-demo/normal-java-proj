#!/usr/bin/env python3
"""
解析 Maven dependency updates 输出并生成格式化的 Markdown 报告
"""
import re
import sys
import os


def parse_version(version_str):
    """解析版本号，返回 (major, minor, patch)"""
    if not version_str:
        return (0, 0, 0)
    # 移除非数字字符，只保留版本号部分
    version_str = re.sub(r'[^0-9.]', '', version_str.split()[0] if ' ' in version_str else version_str)
    parts = version_str.split('.')
    major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
    minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
    return (major, minor, patch)


def classify_update(current, latest):
    """分类更新类型"""
    cv = parse_version(current)
    lv = parse_version(latest)
    
    if lv[0] > cv[0]:
        return 'Major'
    elif lv[1] > cv[1]:
        return 'Minor'
    elif lv[2] > cv[2]:
        return 'Patch'
    return 'Unknown'


def main():
    input_file = 'target/dependency-updates.txt'
    output_file = 'target/dependency-updates.md'
    
    if not os.path.exists(input_file):
        print(f"# 依赖更新检查结果\n")
        print("## ⚠️ 未找到依赖更新文件")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print("# 依赖更新检查结果\n")
            print("## ✅ 所有依赖都是最新版本\n")
            print("没有发现需要更新的依赖。")
            return
        
        # 提取更新信息：格式通常是 groupId:artifactId:type:currentVersion -> latestVersion
        pattern = r'\[INFO\]\s+([^:]+:[^:]+:[^:]+):([^\s->]+)\s+->\s+([^\s]+)'
        matches = re.findall(pattern, content)
        
        if not matches:
            print("# 依赖更新检查结果\n")
            print("## ✅ 所有依赖都是最新版本\n")
            print("没有发现需要更新的依赖。")
            return
        
        updates = []
        for match in matches:
            dep_coord = match[0]  # groupId:artifactId:type
            current = match[1]
            latest = match[2]
            update_type = classify_update(current, latest)
            
            # 提取 groupId:artifactId
            dep_parts = dep_coord.split(':')
            dep_name = f"{dep_parts[0]}:{dep_parts[1]}" if len(dep_parts) >= 2 else dep_coord
            
            updates.append({
                'name': dep_name,
                'current': current,
                'latest': latest,
                'type': update_type
            })
        
        # 按类型分类
        major_updates = [u for u in updates if u['type'] == 'Major']
        minor_updates = [u for u in updates if u['type'] == 'Minor']
        patch_updates = [u for u in updates if u['type'] == 'Patch']
        
        # 生成 Markdown 报告
        output_lines = []
        output_lines.append("# 依赖更新检查结果\n")
        output_lines.append(f"> 💡 提示：发现 **{len(updates)}** 个依赖有可用更新，建议优先更新有安全修复的版本\n")
        output_lines.append(f"## 📦 更新摘要\n")
        output_lines.append(f"- 🔴 **主要版本更新（Major）**: {len(major_updates)} 个")
        output_lines.append(f"- 🟡 **次要版本更新（Minor）**: {len(minor_updates)} 个")
        output_lines.append(f"- 🟢 **补丁版本更新（Patch）**: {len(patch_updates)} 个\n")
        
        # 主要版本更新（最多显示前 30 个）
        if major_updates:
            output_lines.append("### 🔴 主要版本更新（Major）- 优先处理\n")
            output_lines.append("| 依赖 | 当前版本 | 最新版本 |\n")
            output_lines.append("|------|----------|----------|\n")
            for update in major_updates[:30]:
                output_lines.append(f"| `{update['name']}` | `{update['current']}` | `{update['latest']}` |\n")
            if len(major_updates) > 30:
                output_lines.append(f"| ... 还有 {len(major_updates) - 30} 个主要版本更新 | | |\n")
            output_lines.append("\n")
        
        # 次要版本更新（最多显示前 20 个）
        if minor_updates:
            output_lines.append("### 🟡 次要版本更新（Minor）\n")
            output_lines.append("| 依赖 | 当前版本 | 最新版本 |\n")
            output_lines.append("|------|----------|----------|\n")
            for update in minor_updates[:20]:
                output_lines.append(f"| `{update['name']}` | `{update['current']}` | `{update['latest']}` |\n")
            if len(minor_updates) > 20:
                output_lines.append(f"| ... 还有 {len(minor_updates) - 20} 个次要版本更新 | | |\n")
            output_lines.append("\n")
        
        # 补丁版本更新（最多显示前 10 个）
        if patch_updates:
            output_lines.append("### 🟢 补丁版本更新（Patch）- 建议及时更新\n")
            output_lines.append("| 依赖 | 当前版本 | 最新版本 |\n")
            output_lines.append("|------|----------|----------|\n")
            for update in patch_updates[:10]:
                output_lines.append(f"| `{update['name']}` | `{update['current']}` | `{update['latest']}` |\n")
            if len(patch_updates) > 10:
                output_lines.append(f"| ... 还有 {len(patch_updates) - 10} 个补丁版本更新 | | |\n")
            output_lines.append("\n")
        
        # 完整列表（可折叠）
        output_lines.append("---\n")
        output_lines.append("\n### 📋 完整更新列表\n\n")
        output_lines.append("<details>\n")
        output_lines.append(f"<summary>点击展开查看所有 {len(updates)} 个依赖更新详情</summary>\n\n")
        output_lines.append("```\n")
        with open(input_file, 'r', encoding='utf-8') as f:
            output_lines.append(f.read())
        output_lines.append("\n```\n\n")
        output_lines.append("</details>\n\n")
        output_lines.append("### 💡 更新建议\n\n")
        output_lines.append("1. **优先更新 Major 版本**：可能包含重大功能改进和安全修复\n")
        output_lines.append("2. **定期更新 Minor 版本**：通常包含新功能和向后兼容的改进\n")
        output_lines.append("3. **及时更新 Patch 版本**：通常包含重要的 bug 修复和安全补丁\n")
        output_lines.append("4. **使用 Maven 命令更新**：\n")
        output_lines.append("   ```bash\n")
        output_lines.append("   # 更新所有依赖到最新版本（谨慎使用，建议先测试）\n")
        output_lines.append("   mvn versions:use-latest-versions\n")
        output_lines.append("   \n")
        output_lines.append("   # 更新特定依赖\n")
        output_lines.append("   mvn versions:set -DnewVersion=新版本号 -DgroupId=组ID -DartifactId=构件ID\n")
        output_lines.append("   ```\n")
        
        # 写入输出文件
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        
        # 同时输出到 stdout（用于调试）
        print(''.join(output_lines))
        
    except Exception as e:
        error_msg = f"# 依赖更新检查结果\n\n⚠️ 解析依赖更新信息时出错: {e}\n\n### 原始输出\n\n```\n"
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                error_msg += f.read()
        except:
            error_msg += "无法读取文件"
        error_msg += "\n```\n"
        print(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()


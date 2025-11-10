#!/bin/bash

# 依赖安全检查脚本
# 在 GitHub Actions 不可用时，可以在本地运行此脚本进行检查

set -e

echo "🔍 开始依赖安全检查..."
echo ""

# 检查 Maven 是否安装
if ! command -v mvn &> /dev/null; then
    echo "❌ 错误: 未找到 Maven，请先安装 Maven"
    exit 1
fi

# 检查 Java 是否安装
if ! command -v java &> /dev/null; then
    echo "❌ 错误: 未找到 Java，请先安装 Java"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 运行依赖更新检查
echo "📦 检查依赖更新..."
mvn versions:display-dependency-updates -DoutputFile=target/dependency-updates.txt || true

if [ -f target/dependency-updates.txt ]; then
    echo "✅ 依赖更新信息已保存到 target/dependency-updates.txt"
fi

echo ""

# 运行 OWASP Dependency-Check
echo "🔒 运行 OWASP Dependency-Check 安全扫描..."
if mvn verify -DskipTests; then
    echo ""
    echo "✅ 依赖安全检查通过！"
    echo ""
    echo "📊 报告位置:"
    echo "   - HTML: target/dependency-check-reports/dependency-check-report.html"
    echo "   - JSON: target/dependency-check-reports/dependency-check-report.json"
    echo ""
    exit 0
else
    echo ""
    echo "❌ 依赖安全检查失败！"
    echo ""
    echo "📊 请查看详细报告:"
    echo "   - HTML: target/dependency-check-reports/dependency-check-report.html"
    echo "   - JSON: target/dependency-check-reports/dependency-check-report.json"
    echo ""
    echo "💡 提示:"
    echo "   - 如果某些漏洞可以接受，可以在 dependency-check-suppression.xml 中添加抑制规则"
    echo "   - 修复漏洞后重新运行此脚本"
    echo ""
    exit 1
fi



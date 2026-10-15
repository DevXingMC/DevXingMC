# 组件与真实主页参考

所有主页图片使用现成开源组件，没有 AI 绘图或自行绘制的封面。以下案例均检查过个人主页仓库的 README 源码（2026-10-15），不是仅从模板推荐清单推断。

| 本主页内容 | 开源组件 | 实际使用案例 |
| --- | --- | --- |
| 顶部横幅、底部波浪、静态文字 | [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) | [kyechan99 的 README](https://github.com/kyechan99/kyechan99/blob/master/README.md) 使用该组件的页眉和页脚；[SHANK885](https://github.com/SHANK885/SHANK885/blob/master/README.md) 使用 waving 页脚 |
| 打字动画 | [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | [DenverCoder1 的 README](https://github.com/DenverCoder1/DenverCoder1/blob/main/README.md) |
| 技术图标 | [tandpfun/skill-icons](https://github.com/tandpfun/skill-icons) | [tandpfun 的 README](https://github.com/tandpfun/tandpfun/blob/main/README.md) |
| 公开开发统计 | [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | [anuraghazra 的 README](https://github.com/anuraghazra/anuraghazra/blob/master/README.md)、[tandpfun](https://github.com/tandpfun/tandpfun/blob/main/README.md) |
| 连续贡献卡 | [DenverCoder1/github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) | [SHANK885 的 README](https://github.com/SHANK885/SHANK885/blob/master/README.md) |
| 贡献贪吃蛇 | [Platane/snk](https://github.com/Platane/snk) | [Platane 的 README](https://github.com/Platane/Platane/blob/master/README.md) |

## 保存方式

- Capsule Render 和 Typing SVG：官方组件服务输出的 SVG，下载到 `assets/`，只配置用户名、文案、尺寸和色系。
- Streak Stats：使用上游官方 GitHub Action 生成 SVG，避免公共服务缓存造成私有贡献数量延迟；使用 GitHub 对外提供的匿名贡献日历，不读取私有仓库内容。
- Skill Icons：官方服务在制作环境无法连接，因此从原仓库下载 Java、C++、Python、TypeScript、JavaScript、HTML、Git、GitHub 图标，按组件常见方式横向排列；图标路径未重画。
- GitHub Readme Stats：使用原仓库的卡片渲染器；数据查询改用公开汇总字段，以支持默认 Actions 令牌。没有重画统计卡。
- snk：使用上游 GitHub Action；只调整主题参数，并添加“减少动态效果”时暂停 CSS 动画的规则，保留原始图案。

横幅等服务地址与参数记录在 [`component-sources.json`](./component-sources.json)。这些地址仅包含公开用户名和展示配置。

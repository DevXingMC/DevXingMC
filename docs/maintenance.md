# 主页维护

这是 `DevXingMC/DevXingMC` 个人主页仓库，根目录的 `README.md` 会显示在 GitHub 个人主页。

## 修改内容

- 自我介绍、技术方向和项目链接：编辑 `README.md`。
- 横幅和页脚：使用 [Capsule Render](https://github.com/kyechan99/capsule-render) 的 `waving` 组件，保存为 `assets/header.svg` 和 `assets/footer.svg`。
- 打字动画：通过 [Typing SVG](https://readme-typing-svg.demolab.com/demo/) 配置后保存为 `assets/typing.svg`；减少动态效果时使用 Capsule Render 的透明文字组件 `assets/tagline.svg`。
- 技术图标：来自 [Skill Icons](https://github.com/tandpfun/skill-icons)，本地保存于 `assets/stack.svg`。

GitHub 会过滤 README 中的自定义 CSS 与脚本，因此深色视觉由 SVG 提供；README 周围的背景仍由访客的 GitHub 主题决定。

## 自动更新

工作流 `.github/workflows/profile.yml` 每天北京时间 06:23 更新公开统计、连续贡献卡和贡献动画，GitHub 的定时任务可能有延迟。也可以在 **Actions → Refresh profile visuals → Run workflow** 手动刷新。

工作流使用仓库自带的 `GITHUB_TOKEN`，不需要个人访问令牌。生成结果校验成功后才提交图片；任务失败时，上一次成功生成的图片仍然保留。

GitHub Readme Stats 的提交数为近一年，Stars、PR 和 Issues 按组件自身口径统计。没有展示语言占比，以免只有 Fork 或没有可识别源码的仓库产生空图或误导性的比例。Fork 身份在项目介绍中明确标注。

贪吃蛇动画提供深色和浅色版本；访客启用“减少动态效果”时，停留在原组件的初始画面。打字动画也有 Capsule Render 静态文字组件作为替代。

连续贡献卡来自 Streak Stats 的官方公共服务。本仓库每天下载并验证，服务暂时不可用时保留上一次的卡片，其余统计仍可正常更新。

第三方 Actions 固定到提交 SHA。升级前应检查上游变更，并在 Actions 中验证生成结果。GitHub 可能暂停长期没有仓库活动的公共仓库定时任务，届时在 Actions 中重新启用即可。

## 开源参考

2026-10-15 查询的仓库星数，后续会变化：

| 项目 | Stars | 用途 |
| --- | ---: | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | 181,189 | frontend-design 设计方法；星数属于整个 skills 仓库 |
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 135,888 | 配色与可读性参考 |
| [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | 79,841 | GitHub 统计图 |
| [skill-icons](https://github.com/tandpfun/skill-icons) | 13,266 | 技术栈图标 |
| [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | 9,422 | 打字动画 |
| [snk](https://github.com/Platane/snk) | 6,125 | 贡献日历贪吃蛇 |
| [capsule-render](https://github.com/kyechan99/capsule-render) | 1,841 | 波浪横幅、页脚及静态文字 |
| [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) | 7,164 | 连续贡献统计 |

统计图直接使用 `anuraghazra/github-readme-stats` 的原始渲染器，相关源文件保存在 `vendor/github-readme-stats`，来源提交和许可随文件保留。两个 npm 依赖通过 `package-lock.json` 锁定版本与完整性。`scripts/render_stats.mjs` 仅查询公开仓库的 `stargazerCount` 汇总和公开活动数据，不查询受限的 Stargazers 用户列表，因此兼容仓库自带的 `GITHUB_TOKEN`。

两个设计 skill 已存在于制作环境中，本次没有重复安装。所有图片均来自现成开源组件，仅调整用户名、文案和颜色参数。第三方许可保存在 `licenses/`，实际开发者主页案例和组件映射见 [组件来源](./components.md)。

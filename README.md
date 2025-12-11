# 关于项目
本项目会**每日抓取 arXiv**（默认 cs.CV、cs.GR、cs.CL 三个分类）最新论文列表，通过 LLM 自动生成中文摘要，并将结果以 Markdown 形式发布到 GitHub Pages。项目基于 Scrapy 爬虫、arxiv Python 库、LangChain 以及 GitHub Actions 的定时工作流构建，支持自定义模型、语言、抓取分类及单次抓取数量上限（`MAX_PAPER`，默认 10）。

## 整体流程
1. **爬取论文列表**：`daily_arxiv` 模块中的 Scrapy 爬虫按分类抓取最新论文，`MAX_PAPER` 用于限制单次抓取数量（0 或未设置表示不限制）。
2. **补充元数据**：`DailyArxivPipeline` 使用 arxiv 官方库补充作者、标题、分类、摘要、PDF/ABS 链接等信息，输出为 `.jsonl`。
3. **LLM 摘要增强**：`ai/enhance.py` 读取 `.jsonl`，调用指定模型（默认为 `deepseek-chat`，或通过 `MODEL_NAME` 覆盖），按 `LANGUAGE` 生成结构化摘要并写回 `_AI_enhanced_<LANGUAGE>.jsonl`。
4. **转为 Markdown**：`to_md/convert.py` 将增强后的 JSONL 转为 Markdown，方便发布展示。
5. **自动发布**：`update_readme.py` 更新 README 中的内容索引；`.github/workflows/run.yml` 每天定时运行 `run.sh` 完成上述流程并推送到 GitHub。

## 环境变量与配置
- `CATEGORIES`：爬取的 arXiv 分类，逗号分隔，例 `"cs.CL, cs.CV"`。
- `LANGUAGE`：输出摘要语言，例 `"Chinese"` / `"English"`。
- `MODEL_NAME`：LLM 模型名称，例 `"deepseek-chat"`。
- `OPENAI_API_KEY`：模型 API Key。
- `OPENAI_BASE_URL`：可选，自定义 API 入口，需包含协议。
- `MAX_PAPER`：单次抓取的最大论文数，默认 `10`，设为 `0` 或不设表示不限制。
- `EMAIL` / `NAME`：Git 提交身份信息（供工作流使用）。

## Instructions / 操作步骤（保留英文原文并附中文说明）
1. Fork this repo to your own account  
   将此仓库 Fork 到你自己的账户。
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions  
   进入你自己的仓库：Settings -> Secrets and variables -> Actions。
3. Go to Secrets. Secrets are encrypted and are used for sensitive data  
   打开 Secrets，Secrets 会加密存储敏感数据。
4. Create two repository secrets named `OPENAI_API_KEY` and `OPENAI_BASE_URL`, and input corresponding values.  
   创建名为 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 的两个仓库 Secrets，并填入对应的值。
5. Go to Variables. Variables are shown as plain text and are used for non-sensitive data  
   打开 Variables，Variables 以明文保存非敏感数据。
6. Create the following repository variables:  
   创建以下仓库 Variables：  
   1. `CATEGORIES`: separate the categories with ",", such as "cs.CL, cs.CV"  
      `CATEGORIES`：分类用逗号分隔，例如 "cs.CL, cs.CV"。  
   2. `LANGUAGE`: such as "Chinese" or "English"  
      `LANGUAGE`：例如 "Chinese" 或 "English"。  
   3. `MODEL_NAME`: such as "deepseek-chat"  
      `MODEL_NAME`：例如 "deepseek-chat"。  
   4. `MAX_PAPER`: limit papers fetched per run, e.g. "50" (optional)  
      `MAX_PAPER`：限制单次抓取的论文数量，例如 "50"（可选）。  
   5. `EMAIL`: your email for push to github  
      `EMAIL`：用于推送到 GitHub 的邮箱。  
   6. `NAME`: your name for push to github  
      `NAME`：用于推送到 GitHub 的用户名。
   7. `MAX_PAPER`: 最大论文数 
      `MAX_PAPER`：最大论文数
7. Go to your-own-repo -> Actions -> arXiv-daily-ai-enhanced  
   进入你的仓库 Actions，选择 arXiv-daily-ai-enhanced 工作流。
8. You can manually click **Run workflow** to test if it works well (it may takes about one hour).  
   你可以手动点击 **Run workflow** 进行测试（可能耗时约一小时）。  
   By default, this action will automatically run every day  
   默认情况下，该工作流会每天自动运行。  
   You can modify it in `.github/workflows/run.yml`  
   如需修改定时，可编辑 `.github/workflows/run.yml`。
9. If you wish to modify the content in `README.md`, do not directly edit README.md. You should edit `template.md`.  
   若需修改 `README.md` 内容，请编辑 `template.md`，不要直接改 README.md。

## 本地快速体验
1. 安装依赖：`uv sync`（或使用已有的 `.venv` 激活）。
2. 准备环境变量：可在 shell 中 export，或写入 `.env`。
3. 运行一键脚本：`bash run.sh`（将按当天日期生成 `data/<date>.jsonl`、增强文件与 Markdown）。
4. 结果查看：生成的 Markdown 位于 `data/` 目录，同时 README 会更新内容索引。

## GitHub Actions 定时任务
- 工作流位于 `.github/workflows/run.yml`，默认每天 UTC 16:30 触发，可在 `cron` 中调整。
- 运行步骤：拉取代码 → 安装依赖 → 导出环境变量 → 执行 `bash run.sh` → 提交并推送。
- 如需关闭自动运行，可在仓库 Actions 设置中暂停该工作流。

## 自定义与扩展
- 修改抓取分类：设置 `CATEGORIES`。
- 更换模型或私有部署：设置 `MODEL_NAME` 与 `OPENAI_BASE_URL`。
- 控制抓取规模：调整 `MAX_PAPER`。
- 切换摘要语言：设置 `LANGUAGE`。
- 想编辑 README 模板，可同步修改 `template.md`，以便与自动生成保持一致。
 

## 相关工具
- ICML、ICLR、NeurIPS 论文列表: https://dw-dengwei.github.io/OpenReview-paper-list/index.html

 
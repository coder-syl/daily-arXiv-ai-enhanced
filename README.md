# About
This tool will daily crawl https://arxiv.org and use LLMs to summarize them.

See in: https://dw-dengwei.github.io/daily-arXiv-ai-enhanced/

# How to use
This repo will daily crawl arXiv papers about **cs.CV, cs.GR and cs.CL**, and use **DeepSeek** to summarize the papers in **Chinese**.
If you wish to crawl other arXiv categories, use other LLMs or other languages, please follow the bellow instructions.
Otherwise, you can directly use this repo in https://dw-dengwei.github.io/daily-arXiv-ai-enhanced/ . Please star it if you like :)

**Instructions:**
1. Fork this repo to your own account
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions
3. Go to Secrets. Secrets are encrypted and are used for sensitive data
4. Create two repository secrets named `OPENAI_API_KEY` and `OPENAI_BASE_URL`, and input corresponding values.
5. Go to Variables. Variables are shown as plain text and are used for non-sensitive data
6. Create the following repository variables:
   1. `CATEGORIES`: separate the categories with ",", such as "cs.CL, cs.CV"
   2. `LANGUAGE`: such as "Chinese" or "English"
   3. `MODEL_NAME`: such as "deepseek-chat"
   4. `MAX_PAPER`: limit papers fetched per run, e.g. "50" (optional)
   5. `EMAIL`: your email for push to github
   6. `NAME`: your name for push to github
7. Go to your-own-repo -> Actions -> arXiv-daily-ai-enhanced
8. You can manually click **Run workflow** to test if it works well (it may takes about one hour). 
By default, this action will automatically run every day
You can modify it in `.github/workflows/run.yml`
9. If you wish to modify the content in `README.md`, do not directly edit README.md. You should edit `template.md`.

# To-do list
- [x] Replace markdown with GitHub pages front-end.
- [ ] Update instructions for fork users about how to use github pages.

# Content
[2025-12-28](data/2025-12-28.md)

[2025-12-27](data/2025-12-27.md)

[2025-12-26](data/2025-12-26.md)

[2025-12-25](data/2025-12-25.md)

[2025-12-24](data/2025-12-24.md)

[2025-12-23](data/2025-12-23.md)

[2025-12-22](data/2025-12-22.md)

[2025-12-21](data/2025-12-21.md)

[2025-12-20](data/2025-12-20.md)

[2025-12-19](data/2025-12-19.md)

[2025-12-18](data/2025-12-18.md)

[2025-12-17](data/2025-12-17.md)

[2025-12-16](data/2025-12-16.md)

[2025-12-15](data/2025-12-15.md)

[2025-12-14](data/2025-12-14.md)

[2025-12-13](data/2025-12-13.md)

[2025-12-12](data/2025-12-12.md)

[2025-12-11](data/2025-12-11.md)

# Related tools
- ICML, ICLR, NeurIPS list: https://dw-dengwei.github.io/OpenReview-paper-list/index.html

# Star history

[![Star History Chart](https://api.star-history.com/svg?repos=dw-dengwei/daily-arXiv-ai-enhanced&type=Date)](https://www.star-history.com/#dw-dengwei/daily-arXiv-ai-enhanced&Date)

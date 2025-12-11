import os
import json
import sys

import dotenv
import argparse

import langchain_core.exceptions
from langchain_openai import ChatOpenAI
from langchain.prompts import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate,
)
from structure import Structure
if os.path.exists('.env'):
    dotenv.load_dotenv()
template = open("template.txt", "r").read()
system = open("system.txt", "r").read()

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="jsonline data file")
    return parser.parse_args()

def main():
    args = parse_args()
    model_name = os.environ.get("MODEL_NAME", 'deepseek-chat')
    language = os.environ.get("LANGUAGE", 'Chinese')
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")

    data = []
    with open(args.data, "r") as f:
        for line in f:
            data.append(json.loads(line))

    seen_ids = set()
    unique_data = []
    for item in data:
        if item['id'] not in seen_ids:
            seen_ids.add(item['id'])
            unique_data.append(item)

    data = unique_data

    print('Open:', args.data, file=sys.stderr)

    # 构建 ChatOpenAI 参数
    llm_kwargs = {
        "model": model_name,
    }
    
    if api_key:
        llm_kwargs["api_key"] = api_key
    
    if base_url:
        # 确保 base_url 包含协议前缀
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
        llm_kwargs["base_url"] = base_url
        print('Using base_url:', base_url, file=sys.stderr)
    
    llm = ChatOpenAI(**llm_kwargs).with_structured_output(Structure, method="function_calling")
    print('Connect to:', model_name, file=sys.stderr)
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system),
        HumanMessagePromptTemplate.from_template(template=template)
    ])

    chain = prompt_template | llm

    for idx, d in enumerate(data):
        try:
            response: Structure = chain.invoke({
                "language": language,
                "content": d['summary']
            })
            d['AI'] = response.model_dump()
        except langchain_core.exceptions.OutputParserException as e:
            print(f"{d['id']} has an error: {e}", file=sys.stderr)
            d['AI'] = {
                 "tldr": "Error",
                 "motivation": "Error",
                 "method": "Error",
                 "result": "Error",
                 "conclusion": "Error"
            }
        except Exception as e:
            print(f"{d['id']} has a connection/API error: {e}", file=sys.stderr)
            # 如果是连接错误，检查配置
            if "UnsupportedProtocol" in str(e) or "Connection error" in str(e):
                print("ERROR: Check your OPENAI_BASE_URL configuration. It should start with http:// or https://", file=sys.stderr)
                if not base_url:
                    print("ERROR: OPENAI_BASE_URL environment variable is not set!", file=sys.stderr)
            d['AI'] = {
                 "tldr": "Error",
                 "motivation": "Error",
                 "method": "Error",
                 "result": "Error",
                 "conclusion": "Error"
            }
        with open(args.data.replace('.jsonl', f'_AI_enhanced_{language}.jsonl'), "a") as f:
            f.write(json.dumps(d) + "\n")

        print(f"Finished {idx+1}/{len(data)}", file=sys.stderr)

if __name__ == "__main__":
    main()

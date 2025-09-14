import re
import arxiv
import os
import sys
from datetime import datetime,timezone



# 根据论文title获取arxiv论文信息
def get_arxiv_paper_info(paper_title):
    client = arxiv.Client()
    search = arxiv.Search(
        query=f"ti:{paper_title}",
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    try:
        result = next(client.results(search))
        return {
            "arxiv_link": result.entry_id,
            "published_date": result.published.isoformat()
        }
    except StopIteration:
        return "未找到匹配的论文"
    except Exception as e:
        return f"请求出错: {str(e)}"
    



# 计算当前Python文件所在文件夹内的子文件夹数量，返回生成文件的ID
def count_subdirectories():
    """
    计算当前Python文件所在文件夹内的子文件夹数量
    (不包括文件、当前目录(.)和上级目录(..))
    
    返回:
        int: 子文件夹数量+1
    """
    try:
        # 获取当前.py文件所在的目录路径
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        # 列出目录中的所有条目
        all_entries = os.listdir(current_dir)
        
        # 筛选出子文件夹（排除文件和特殊目录）
        subdirectories = [
            entry for entry in all_entries
            if os.path.isdir(os.path.join(current_dir, entry))
            and entry not in ('.', '..')  # 排除当前目录和上级目录
        ]
        
        return len(subdirectories)+1
    
    except Exception as e:
        print(f"计算子文件夹数量时出错: {e}")
        return 0   



# 解析引文字符串，形成字典
def parse_citation(citation_str):
    
    # 分割四个主要部分
    parts = citation_str.split('. ', 3)
    if len(parts) != 4:
        raise ValueError("输入的引文字符串格式不正确")
    
    authors_str, year, title, venue_part = parts
    year = year.strip()
    title = title.strip()
    
    # 处理研究方向（//标记）
    if '//' in venue_part:
        venue, direction = venue_part.split('//', 1)
        venue = venue.strip()
        direction = direction.strip()
    else:
        venue = venue_part.strip()
        direction = ''
    
    # 处理作者列表
    authors_str = authors_str.replace(' and ', ', ')
    raw_authors = re.split(r',\s*(?![^()]*\))', authors_str)
    cleaned_authors = []
    author_notes = []
    
    for author in raw_authors:
        author = author.strip()
        if not author:
            continue
        # 处理特殊符号
        symbol_match = re.search(r'([+*])$', author)
        if symbol_match:
            symbol = symbol_match.group(1)
            cleaned_author = re.sub(r'[+*]$', '', author).strip()
            note = '共同一作' if symbol == '+' else '通讯作者' if symbol == '*' else ''
        else:
            cleaned_author = author
            note = ''
        cleaned_authors.append(cleaned_author)
        author_notes.append(note)
    # arxiv_info = get_arxiv_paper_info(title)
    # year = arxiv_info['published_date'] if 'published_date' in arxiv_info else year
    # arxiv_link = arxiv_info['arxiv_link'] if 'arxiv_link' in arxiv_info else ''
    return {
        'authors': cleaned_authors,
        'author_notes': author_notes,
        'year': year,
        'title': title,
        'venue': venue,
        'direction': direction
    }



# 根据生成的字典和输入的ID（当前论文数）生成Markdown文件
def generate_md_file(data_dict, output_id):
    # 输出data和id
    # 换行输出字典
    for key, value in data_dict.items():
        print(f"{key}: {value}")
    # 创建目标文件夹
    os.makedirs(output_id, exist_ok=True)
    # 构建YAML内容
    yaml_content = []
    yaml_content.append("---")

    # 1. 处理标题
    yaml_content.append(f'title: "{data_dict["title"]}"')
    
    # 2. 处理作者列表
    yaml_content.append("authors:")
    for author in data_dict["authors"]:
        yaml_content.append(f"- {author}")
    
    # 3. 处理作者注释
    yaml_content.append("author_notes:")
    for note in data_dict["author_notes"]:
        if note:
            yaml_content.append(f'- "{note}"')
        else:
            yaml_content.append("- ")
    
    # 4. 处理日期（使用当前月日 + 给定年份）
    now = datetime.now(timezone.utc)
    date_str = f"{data_dict['year']}-{now:%m-%dT%H:%M:%SZ}"
    yaml_content.append(f'date: "{date_str}"')
    
    # 5. 处理发布日期（当前真实时间）
    publish_date = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    yaml_content.append(f'publishDate: "{publish_date}"')
    
    # 6. 处理发表类型
    yaml_content.append(f'publication_types: [{data_dict["direction"]}]')
    
    # 7. 处理发表会议（加粗处理）
    venue = data_dict["venue"]
    # 分离会议主体和括号内容
    if '(' in venue:
        main_part, bracket_part = re.split(r'[\(（]', venue, 1)
        formatted_venue = f"**{main_part.strip()}** ({bracket_part}"
    else:
        formatted_venue = f"**{venue}**"
    yaml_content.append(f'publication: "{formatted_venue}"')
    
    yaml_content.append("---")
    
    # 写入文件
    with open(os.path.join(output_id, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_content))
        print(f"Markdown file created at: {os.path.join(output_id, 'index.md')}")




if __name__ == "__main__":

    """
    持续从命令行读取字符串输入，对每个输入的字符串处理
    输入'exit'或'quit'可退出循环
    """
    print("开始论文相应文件生成（输入 'exit' 或 'quit' 退出）")
    while True:
        try:
            # 获取用户输入
            user_input = input("请输入论文字符串: ")
            
            # 检查退出条件
            if user_input.lower() in ['exit', 'quit']:
                print("退出输入循环")
                break
                
            # 将输入传递给test函数处理
            data_dict = parse_citation(user_input)
            folder_count = count_subdirectories()
            generate_md_file(data_dict, str(folder_count))
            
        except KeyboardInterrupt:
            print("\n检测到Ctrl+C，退出程序")
            break
        except Exception as e:
            print(f"处理输入时出错: {e}")
    
    # text_dict=parse_citation('Yaoxiang Wang, Zhiyong Wu*, Junfeng Yao, and Jinsong Su*. 2025. TDAG: A Multi-Agent Framework based on Dynamic Task Decomposition and Agent Generation. Neural Networks. (CCF-B类) // directiona')
    # folder_count = count_subdirectories()
    # generate_md_file(text_dict, str(folder_count))
    # # 测试用例
    # test_cases = [
    #     "Xiaoyue Wang+, Linfeng Song+, Xin Liu, Chulun Zhou, Hualin Zeng and Jinsong Su*. 2022. Getting the Most out of Simile Recognition. In Proc. of EMNLP 2022 Findings. // 信息抽取",
    #     "Hui Jiang, Ziyao Lu, Fandong Meng, Chulun Zhou, Jie Zhou, Degen Huang and Jinsong Su*. 2022. Towards Robust k-Nearest-Neighbor Machine Translation. In Proc. of EMNLP 2022. (CCF-B类)// direction1",
        
    # ]   

    # for citation in test_cases:
    #     print(parse_citation(citation))
    #     print("-" * 50)
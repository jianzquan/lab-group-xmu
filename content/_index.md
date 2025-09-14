---
# Leave the homepage title empty to use the site title
title:
date: 2022-10-24
type: landing

sections:
  - block: lab-profile
    id: about
    content:
        title: Biography
        # Choose a user profile to display (a folder name within `content/authors/`)
        username: lab


  - block: markdown
    content:
      title: 研究方向
      subtitle:
      text: |
       
        课题组的研究主要聚焦于大模型和自然语言处理领域，目前的研究方向包括：</br>
        * **基于大模型的自然语言处理研究**：
          - 多模态机器翻译研究，包括图到文机器翻译，图到图机器翻译和文本到图像生成
          - 语音分析和处理研究，包括语音识别、翻译和合成
          - 信息抽取研究，主要聚焦实体识别，关系抽取和情感分析
        </br> </br>
        * **大模型基础技术研究**：
          - 数据体系建设，负责训练数据的采集以及评测基准的构建工作
          - 模型架构创新​​，致力于探索更为高效且扩展性强的模型结构
          - 训练算法优化，专注于预训练与微调阶段的训练算法设计工作
          - 推理加速方案，通过运用解码策略实现高效推理
        </br> </br>
        * **基于大模型的应用技术研究**：
          - 智能体研究，包括工具调用机制、任务规划方法及多智能体协作框架
          - 代码生成研究，包括代码补全与代码修复，提升大模型在软件开发中的实用能力。
        </br> </br>
        * **AI for Science**：
          - 文本分子跨模态检索
          - 分子类药性预测
    design:
      columns: '1'

  - block: collection
    content:
      archive:
        enable: true
        text: 查看所有资讯
        link: post/
      title: 最新资讯
      subtitle: 
      text:
      count: 5
      filters:
        author: ''
        category: ''
        exclude_featured: false
        publication_type: ''
        tag: ''
      offset: 0
      order: desc
      page_type: post
      sort_by: 'date'
    design:
      view: compact
      columns: '1'



  # - block: tag_cloud
  #   content:
  #     title: My title
  #     subtitle: My subtitle
  #     text: Add any **markdown** formatted content here - text, images, videos, galleries - and even HTML code!
  #     # Choose a taxonomy from the `taxonomies` list in `config.yaml` to display (e.g. tags, categories, authors)
  #     taxonomy: tags
  #     # Choose how many tags you would like to display (0 = all tags)
  #     count: 20
  #   design:
  #     # Minimum and maximum font sizes (1.0 = 100%).
  #     font_size_min: 0.7
  #     font_size_max: 2.0





---

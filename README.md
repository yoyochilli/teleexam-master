# 星辰期末高效通｜TeleAgent 期末备考 Skill

## 下载并导入 Skill

**[下载 teleexam-master-skill.zip](./teleexam-master-skill.zip)**

在中国电信星辰超级智能体（TeleAgent）中导入该 ZIP 后，上传脱敏的课程 PDF、PPTX、笔记、题目或考纲即可使用。

## 10 秒极速体验

完成 Skill 导入后：

1. 上传 [`examples/`](./examples/) 中的 3 个 `.txt` 样例：`sample_lecture_slides.txt`、`sample_exam_questions.txt`、`sample_syllabus.txt`。
2. 复制 [`quick_test_prompt.txt`](./examples/quick_test_prompt.txt) 的全部内容并发送。
3. 核验结果是否包含：按页码排列的复习笔记、逐条证据标签、3 题微型测验、`资料缺失` 提示和下一步复习行动。

可用 [`expected_output_excerpt.md`](./examples/expected_output_excerpt.md) 快速比对关键字段。

## 它解决什么问题

学生的课件、笔记和真题往往彼此割裂，复习时既难按老师讲课逻辑串联，也很难判断重点是否真的来自课程材料。

“星辰期末高效通”以用户上传资料为唯一事实边界，建立：

```text
课程资料 → 可定位证据 → 考点与练习 → 错题复盘 → 复习行动
```

## 核心能力

### 1. 顺着授课逻辑整理可背诵笔记

按 PDF/PPTX 页码、讲义标题或笔记原始段落顺序输出“核心线索｜详细笔记｜证据”。每个单元附背诵版、命题角度和避坑点，保留老师的讲授主线。

### 2. 忠于原文，不瞎编

定义、公式、结论、分值和时间都必须标注 PPT 页码、真题题号、考纲章节或笔记关键词。资料找不到时明确写 `资料缺失` 或 `公式待确认`，不使用外部知识补写。

### 3. 基于证据生成模拟测验

模拟题、参考答案和评分点都要回指课程资料；材料不足以支持某个题型时，直接说明无法命题。作答后可进入错题记录、掌握度更新与 +1 / +3 / +7 天复习闭环。

### 4. 多资料自主编排

TeleAgent 自动完成资料盘点、文档解析、证据块建立、模式选择和结果校验。复合请求可串联“整理笔记 → 生成测验 → 错题复盘 → 复习计划”。

## 明文 Skill 结构

| 文件 | 评审可查看内容 |
| --- | --- |
| [`skill/system_prompt.md`](./skill/system_prompt.md) | 完整事实边界、模式路由、输出要求与自检规则 |
| [`skill/skill.json`](./skill/skill.json) | TeleAgent Skill 元数据、触发词与输入定义 |
| [`skill/input_output_schema.json`](./skill/input_output_schema.json) | 输入输出字段和必须满足的约束 |
| [`skill/workflow.md`](./skill/workflow.md) | TeleAgent 能力映射与任务自主拆解流程 |
| [`skill/references/output_templates.md`](./skill/references/output_templates.md) | 复习页、模拟卷和雷达表模板 |
| [`skill/scripts/`](./skill/scripts/) | PPTX 页级提取与文本清洗代码 |

## 完整评审核验流程

1. 下载并导入上述 Skill 包到 TeleAgent。
2. 上传一份脱敏课程 PDF/PPTX、笔记 TXT、题目或考纲。
3. 输入以下测试指令：

```text
请严格按课件授课顺序整理复习笔记。
每条结论标注资料证据；资料不足时标记“资料缺失”，不要补写外部知识。
公式使用规范数学格式排版，并保留 PDF/PPT 页码。
```

4. 继续输入：

```text
请仅依据现有资料生成 6 题期末模拟测验。
每题给出答案、评分点和资料依据；资料不足的考点不要命题。
```

## 隐私与边界

- 仅处理用户已授权的课程资料；演示时建议使用脱敏文件。
- 不将往年真题断言为本次考试范围。
- 不把资料外的通用知识伪装为课程结论。

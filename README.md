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

## 评审价值一览

| 评审维度 | 对应设计 | 评委可直接核验的证据 |
| --- | --- | --- |
| 选题契合与应用价值 | 面向“课件、笔记、真题割裂”的期末复习真实场景；不限定单一学科 | 导入任意课程 PPT/PDF/TXT 后先出资料体检与学习地图 |
| 功能实现与产品体验 | 以“资料体检 → 最短学习路径 → 整理/自测 → 盲区复盘”降低首次使用门槛 | 复制 [`study_map_prompt.txt`](./examples/study_map_prompt.txt) 即可体验 |
| 技术创新与实现质量 | 证据图谱、三级置信度、冲突隔离、禁剧透状态机、确定性审计 | 明文规则、审计脚本、14 条可复现 Benchmark 用例 |

所有“重点、分值、频率、考试范围”均以用户资料为边界；资料不足时明确提示补充项，不虚构学习效果数据。

## 核心能力

### 1. 顺着授课逻辑整理可背诵笔记

按 PDF/PPTX 页码、讲义标题或笔记原始段落顺序输出“核心线索｜详细笔记｜证据”。每个单元附背诵版、命题角度和避坑点，保留老师的讲授主线。

### 2. 忠于原文，不瞎编

定义、公式、结论、分值和时间采用三级置信度：`[确凿依据]` 保留精准页码，`[逻辑推导]` 列出全部前提与依赖，`[资料缺失]` 明确缺口和补救动作。生成前建立课程术语白名单，材料外的专业名词、定理、算子和符号体系会触发外部知识熔断。

### 3. 基于证据生成模拟测验

模拟题、参考答案和评分点都要回指课程资料；材料不足以支持某个题型时，直接说明无法命题。作答后可进入错题记录、掌握度更新与 +1 / +3 / +7 天复习闭环。

### 4. 多资料自主编排

TeleAgent 自动完成资料盘点、文档解析、证据块建立、模式选择和结果校验。复合请求可串联“整理笔记 → 生成测验 → 错题复盘 → 复习计划”。

### 5. 真题连环拷问

输入“考考我”“进入拷打模式”或“高压自测”即可进入 Grill-Me 状态机。系统坚持单题单发与禁剧透，根据学生回答执行 Challenge、Dig Deeper 或 Scaffolding；一道题结束后生成采分点核验、课件直连和盲区入库报告。

### 6. 资料冲突隔离与可见自省

当课件、笔记、考纲或题目对同一概念给出不同口径时，系统并列保留原文与来源，不依赖模型常识擅自选边。受冲突影响的推导、命题和评分会暂停，等待用户确认。每次交付末尾报告证据覆盖、资料缺失、冲突、公式核验和越界术语，让“没有瞎编”成为可检查的过程。

评委可上传 [`examples/sample_conflicting_sources.txt`](./examples/sample_conflicting_sources.txt)，并与 [`expected_conflict_output.md`](./examples/expected_conflict_output.md) 对照；生成结果可用 `skill/scripts/delivery_auditor.py` 检查结构完整性。

### 7. 资料体检与学习地图

首次上传资料时，不要求学生先理解复杂设置：系统先说明每份资料能做什么，识别授课主线、考试边界、题型线索和个人薄弱项是否缺失，再给出最多 3 个可以立即执行的动作。动作均通过“来源节点 → 考点/盲区节点 → 用途节点”的证据图谱回溯，避免泛泛的复习建议。

可复制 [`study_map_prompt.txt`](./examples/study_map_prompt.txt) 测试，并与 [`expected_study_map_output.md`](./examples/expected_study_map_output.md) 对照。

## 抗幻觉与命题质量定量对比基准

`TeleExam Contract Benchmark v1` 使用 7 个合规黄金样例和 7 个故意违规样例，直接运行证据审计器、Grill-Me 审计器、交付审计器和证据图谱审计器。结果可通过 [`benchmark/run_benchmark.py`](./benchmark/run_benchmark.py) 复现。

| 评测对象 | 样本数 | 目标 | 实测结果 |
| --- | ---: | --- | ---: |
| 合规黄金输出 | 7 | 正常通过审计门禁 | **7/7（100%）** |
| 故意违规输出 | 7 | 成功识别并拦截 | **7/7（100%）** |
| 三级证据标签 | 7 | 标签语法与依赖完整 | **7/7（100%）** |
| Grill-Me 未解锁回合 | 3 | 答案/解析/评分剧透次数 | **0 次** |
| Grill-Me 单题与问句收尾 | 3 | 单题单发且以 `？` 结束 | **3/3（100%）** |
| 题后透视报告 | 1 | 三个审计区块完整 | **3/3 区块** |
| 资料体检与证据图谱 | 2 | 图谱闭合与孤立节点拦截 | **2/2（100%）** |
| 原有脚本回归 | 184 | 文本清洗与 PPTX 解析 | **184/184（100%）** |

违规集覆盖：无证据结论、资料缺失但无补救动作、提前泄露答案、多题连发、题后审计字段不完整、资料冲突与自省字段缺失。完整口径与结果见 [`benchmark/`](./benchmark/) 和 [`results.json`](./benchmark/results.json)。

> 该基准衡量规则与确定性审计工具链的可执行性。在线 TeleAgent 模型在未知课程资料上的表现，需要通过真实导入与盲测单独报告。

## 明文 Skill 结构

| 文件 | 评审可查看内容 |
| --- | --- |
| [`skill/system_prompt.md`](./skill/system_prompt.md) | 完整事实边界、模式路由、输出要求与自检规则 |
| [`skill/skill.json`](./skill/skill.json) | TeleAgent Skill 元数据、触发词与输入定义 |
| [`skill/input_output_schema.json`](./skill/input_output_schema.json) | 输入输出字段和必须满足的约束 |
| [`skill/workflow.md`](./skill/workflow.md) | TeleAgent 能力映射与任务自主拆解流程 |
| [`skill/references/output_templates.md`](./skill/references/output_templates.md) | 复习页、模拟卷和雷达表模板 |
| [`skill/references/evidence_policy.md`](./skill/references/evidence_policy.md) | 术语白名单、三级置信度、推导链与公式保真协议 |
| [`skill/references/grill_me_mode.md`](./skill/references/grill_me_mode.md) | 单题单发、三阶追问、答案解锁与题后审计状态机 |
| [`skill/references/conflict_and_audit.md`](./skill/references/conflict_and_audit.md) | 多资料冲突隔离、冲突传播与交付前自省审计 |
| [`skill/references/learning_map.md`](./skill/references/learning_map.md) | 首次资料体检、最短学习路径与证据图谱模板 |
| [`skill/scripts/`](./skill/scripts/) | PPTX 页级提取、文本清洗与证据标签审计代码 |

评委可直接运行 [`examples/boundary_tests.md`](./examples/boundary_tests.md) 中的越界问题，检查 Skill 是否会拦截超纲术语、隐藏推导条件和模糊公式。

[`examples/grill_turns/`](./examples/grill_turns/) 提供发题、Challenge、Scaffolding 和题后审计四个独立回合，可用 `grill_turn_auditor.py` 验证禁剧透与单题规则。

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

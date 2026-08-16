# 每日作业报告：Day 0

## 1. 本日问题

- 里程碑：day-00
- 学生或小组：汤家齐
- 使用者：第一次完成真实编程项目、需要知道下一步做什么的学生小组
- 真实输入：课程仓库本身、真实 Day 1 课程文件、`learning-plan.json`
- 需要的输出：一份可执行、可检查、可解释的 Day 1 学习计划，以及验证该计划的学习计划检查器
- 与使用者最相关的错误：计划听起来专业，却引用不存在的文件、超过课堂时间、没有验证步骤、缺环节，或由智能体代替学生思考
- 本日产品边界：不要求学生独立设计新算法；不把 API 密钥写进文件；不批准看不懂的命令；不把智能体回答当作事实

## 2. 真实数据或真实课程输入

- 所有者/发布者：课程教师（GitHub: the-real-jushen/ai-summer-camp-2026）
- 标题：AI Engineering Summer Camp 2026（中文课程）
- 原始 URL：https://github.com/the-real-jushen/ai-summer-camp-2026
- 许可标签或使用许可：以课程仓库说明为准
- 下载/取得日期：2026-08-15 前已 clone，本地路径 `G:\ai-summer-camp-2026`
- 预期文件与结构：`course/zh-CN/day-01-prediction/` 的五个学生文件、starter README 与测试
- 检查命令：`python learning_plan_check.py learning-plan.json --course-root ..\...`
- 实际检查结果：`LEARNING PLAN CHECK PASSED`；Day: Day 1；Stages: 8；Total minutes: 180
- 已知缺失、偏差或限制：本日不使用 Kaggle 数据集；检查器只验证结构和路径，不验证命令安全性或学习顺序优劣

## 3. 可复现运行

```powershell
# 当前目录
G:\ai-summer-camp-2026\student-work\day-00-learning-plan

# 安装：无需安装，仅用 Python 标准库

# 测试
python -m unittest discover -s tests -v

# 真实计划检查
python learning_plan_check.py learning-plan.json --course-root ..\...

# 坏计划演示（预期失败，退出码 1）
python learning_plan_check.py evidence\bad-plan-example.json --course-root ..\..
```

- 测试实际输出：`evidence/tests-output.txt`（5 个测试全部 OK）
- 真实计划实际输出：`evidence/plan-check-passed.txt`（8 阶段、180 分钟）
- 坏计划实际输出：`evidence/bad-plan-check-output.txt`（3 条错误：文件不存在、超时 200 分钟、缺 candidate 环节）

## 4. 基线与候选

### 简单基线

- 方法：直接相信智能体生成的计划，不检查路径、时间、证据和环节完整性
- 为什么足够简单：零验证成本，是“听起来合理就照做”的最朴素做法
- 命令：无检查命令（对照 `evidence/bad-plan-example.json`）
- 结果：计划引用 `course/zh-CN/day-01-prediction/does-not-exist.md`（文件不存在）、总时长 200 分钟、purpose 缺少 `candidate` 关键词；一旦照做会浪费课堂时间并漏掉关键环节

### 候选方法

- 学生完成的核心改动：实现 `learning_plan_check.py` 的两个验证函数；把基于真实 Day 1 文件的学习计划保存为结构化 JSON
- 保持不变的数据、划分、指标或参数：测试文件保持课程原样；计划字段契约以 `tests/test_learning_plan_check.py` 为准
- 命令：`python -m unittest discover -s tests -v`；`python learning_plan_check.py learning-plan.json --course-root ..\...`
- 结果：5/5 测试通过；真实计划检查通过

| 项目 | 基线 | 候选 | 含义 |
| --- | ---: | ---: | --- |
| 测试 | 无 | 5/5 通过 | 检查器契约被自动验证 |
| 计划检查 | 未检查（含不存在文件） | PASSED，8 阶段 | 每条路径都在课程根下真实存在 |
| 总分钟 | 200（超时） | 180 | 能在课堂时间内完成 |
| 环节覆盖 | 缺 candidate | data/baseline/candidate/errors/finish 齐全 | 关键步骤没有被遗漏 |

## 5. 一个真实失败案例

- 样本位置/编号：`evidence/bad-plan-example.json`
- 真实结果：检查器退出码 1，打印 `LEARNING PLAN CHECK FAILED`
- 系统输出：三条错误——`course_file does not exist below course root: course/zh-CN/day-01-prediction/does-not-exist.md`；`total minutes must be 180 or less, got 200`；`no stage purpose mentions required word: candidate`
- 可以观察到什么：一个看似完整的智能体计划，依然可能引用不存在的文件、超出课时、缺少关键环节
- 说明的限制：检查器能抓结构和路径错误，不能证明学习顺序最优、命令安全或学生理解
- 不能证明什么：不能证明所有智能体计划都不可用；这个案例只证明“未经检查的计划不可直接执行”
- 下一项最小检查：对真实计划逐阶段打开所引用的课程文件，并人工复述每一步的目的和停止条件

## 6. 智能体与学生工作边界

- 智能体提出/生成/修改了什么：按用户要求生成学习计划 JSON 草稿、实现两个验证函数、运行测试与检查器、生成证据文件和本报告
- 学生怎样核对文件、来源、输出、测试和 diff：需要逐行阅读 `learning_plan_check.py`，打开 `learning-plan.json` 中 8 个阶段引用的课程文件，确认路径真实存在；重跑三条命令核对输出与 `evidence/` 一致
- 学生修改或拒绝了什么建议：应检查并确认坏计划演示文件是故意构造的反例，而不是正式计划的一部分
- 每名成员能独立解释的代码或证据：`validate_stage` 的六字段检查、`validate_plan` 的总时长与五个关键词检查、以及真实计划检查通过的含义

## 7. 结论与限制

证据支持的最小结论是：在真实 Day 1 课程文件上生成了一份 8 阶段、总时长 180 分钟的结构化学习计划，并实现了一个通过 5 项单元测试、能在真实计划上通过、能拒绝坏计划的学习计划检查器。数据限制：本日真实输入是课程仓库与 Day 1 文件，不是 Kaggle 数据集，检查器没有执行计划中的任何命令。方法限制：结构和路径通过不等于学习顺序最优，也不等于命令安全。使用边界：本工具只用于课程内部规划，不能替代学生对课程材料的阅读和理解，也不能证明“学生已经学会 Day 1 内容”。

## 8. 提交复核

- [x] README 从新环境可以开始运行
- [x] 数据检查、测试和主程序重新运行
- [x] 报告数字与保存输出一致
- [x] `presentation.pptx` 在 3 分钟内讲完（4 页：问题/方法/证据/失败与限制）
- [x] `submission.json` 路径正确
- [x] 无密钥、大数据、私人信息、虚拟环境或缓存
- [x] GitHub 仓库已创建并推送：https://github.com/Soup-Sky/ai-camp-2026-d0-tangjiaqi（public，分支 main；精确评阅 SHA 以教师工具记录为准）
- [ ] 邮件发送 URL（需要学生本人登录邮箱完成；若老师要求，先把老师 GitHub 账号加入仓库 collaborator）

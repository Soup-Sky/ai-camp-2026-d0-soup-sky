# Day 0：学习计划检查器

把智能体生成的 Day 1 学习计划保存为结构化 JSON，并用一个检查器验证：
计划中的课程文件真实存在、每个阶段有动作/预期结果/停止条件/分钟数、
总时间不超过 180 分钟，并且覆盖 data、baseline、candidate、errors、finish 五个必经环节。

## 问题

- 使用者：第一次完成真实编程项目、需要知道下一步做什么的学生小组；
- 真实输入：课程仓库本身、真实 Day 1 课程文件、以及 `learning-plan.json`；
- 输出：可执行、可检查、可解释的 Day 1 学习计划；
- 基线：只相信智能体的回答、不检查路径/时间/证据；
- 候选：把计划变成结构化 JSON，用测试和真实文件路径检查；
- 边界：检查器能证明结构和路径正确，不能证明“学习顺序最优”“命令安全”或“学生已经理解”。

## 环境

- Windows + Python 3（本仓库只用标准库，无需 pip 安装）；
- Git（提交仓库用）；
- 课程仓库：`G:\ai-summer-camp-2026`。

## 文件

| 文件 | 作用 |
| --- | --- |
| `learning_plan_check.py` | 学习计划检查器（两个 TODO 已实现） |
| `learning-plan.json` | 基于真实 Day 1 课程文件生成的学习计划 |
| `tests/test_learning_plan_check.py` | 检查器契约测试 |
| `evidence/bad-plan-example.json` | 一个会被检查器拒绝的坏计划（演示失败案例） |
| `evidence/tests-output.txt` | 测试通过的实际输出 |
| `evidence/plan-check-passed.txt` | 真实计划检查通过的实际输出 |
| `evidence/bad-plan-check-output.txt` | 坏计划被拒绝的实际输出 |

## 从零运行

在 `student-work/day-00-learning-plan` 目录打开 PowerShell：

```powershell
Get-Location
python -m unittest discover -s tests -v
```

预期输出：

```text
Ran 5 tests ... OK
```

再检查真实学习计划（`--course-root` 指课程仓库根，本目录向上两级）：

```powershell
python learning_plan_check.py learning-plan.json --course-root ..\..
```

预期输出：

```text
LEARNING PLAN CHECK PASSED
Day: Day 1
Stages: 8
Total minutes: 180
```

演示检查器拒绝一个坏计划：

```powershell
python learning_plan_check.py evidence\bad-plan-example.json --course-root ..\..
```

预期输出（退出码 1）：

```text
LEARNING PLAN CHECK FAILED
- stage 1 course_file does not exist below course root: course/zh-CN/day-01-prediction/does-not-exist.md
- total minutes must be 180 or less, got 200
- no stage purpose mentions required word: candidate
```

## 检查器验证了什么

- `day` 非空、`stages` 是列表且至少 5 个阶段；
- 每个阶段必须有非空的 `purpose`、`course_file`、`action`、`expected_result`、`stop_condition`、`minutes`；
- `minutes` 是正整数，全部阶段总和 ≤ 180；
- `course_file` 是课程根目录下真实存在的文件；
- 各阶段 `purpose` 覆盖 `data`、`baseline`、`candidate`、`errors`、`finish` 五个关键词。

## 限制

- 检查器不执行计划里的命令，不验证数据来源、命令安全性或学习顺序是否最优；
- 测试通过只证明检查器契约被满足，不证明学生理解；
- 本日不使用 Kaggle 数据集，真实输入是课程仓库和真实 Day 1 文件。

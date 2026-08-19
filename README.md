# Claude 智能体驾驭工程实战大师课
### Agent Harness Engineering Masterclass (Chinese Edition)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-在线演示课件-D97757?style=for-the-badge&logo=github)](https://kenhuangus.github.io/agent-harness-chinese/slides.html)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Anthropic Claude Code](https://img.shields.io/badge/Anthropic-Claude%20Code-D97757?style=for-the-badge)](https://claude.ai/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-2.x%20Standard-4A4A44?style=for-the-badge)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-BD5D3A?style=for-the-badge)](LICENSE)

> **为非确定性大模型构建确定性控制与工业级安全驾驭系统**  
> 全面掌握生产级 AI 编码智能体 智能体驾驭工程体系：深入 Claude Code 记忆架构、AST 语法与秘钥防护、TDA 自愈测试闭环、MCP 协议扩展及复合多智能体协同架构。

---

## 🌐 在线互动资源

* 🖥️ **47 页全景交互式课件**: [https://kenhuangus.github.io/agent-harness-chinese/slides.html](https://kenhuangus.github.io/agent-harness-chinese/slides.html)
* 🏠 **课程官方网站首页**: [https://kenhuangus.github.io/agent-harness-chinese/](https://kenhuangus.github.io/agent-harness-chinese/)
* 📦 **英文原版主仓库 (Packt Harness)**: [https://github.com/kenhuangus/packt-harness](https://github.com/kenhuangus/packt-harness)

---

## 🏛️ 核心论点：传统软件工程 vs. 智能体驾驭工程

| 维度 | 传统软件工程 (Traditional SE) | 智能体驾驭工程 (Harness Engineering) |
| :--- | :--- | :--- |
| **底层系统性质** | **确定性系统 (Deterministic)** | **非确定性概率系统 (Non-Deterministic)** |
| **开发管控范式** | SDLC, Agile, CI/CD, 测试金字塔, SRE | 记忆分层, 路径沙箱, AST 钩子, TDA 自愈闭环 |
| **行为产生方式** | 开发者明确编写的代码与逻辑分支 | 模型在提示词、记忆、工具与上下文中的概率涌现 |
| **工程核心使命** | 编写正确代码：**相同输入 ➔ 确定输出** | 构建外部刚性受控环境：**概率模型 ➔ 确定性受控运行** |

---

## 🛡️ 核心驾驭架构五大支柱 (Core Harness Stack)

1. **🧠 分层记忆系统 (Hierarchical Memory)**: `CLAUDE.md` / `AGENTS.md` 规范结合 Auto Memory (`MEMORY.md`)，实现多级作用域继承与压缩持久化。
2. **🔒 受限工具沙箱 (Scoped Tool Sandbox)**: 最小特权工具白名单结合 `Path.is_relative_to()` 路径穿越防御，将写入严格锁定在工作区内。
3. **🪝 确定性拦截钩子 (Deterministic Hooks)**: 覆盖 Claude Code 31 个生命周期事件，`PreToolUse` 拦截危险命令，`PostToolUse` 执行 AST 语法与多厂商秘钥扫描。
4. **📊 Token 预算管理 (Token Budgeting)**: 20/20/50/10 黄金预算分配策略与首尾保留压缩 (Head/Tail Compaction)，从根源防御上下文溢出与目标漂移。
5. **📜 结构化审计追踪 (Structured Event Tracing)**: 不可变追加式 `events.jsonl` 与 `telemetry.jsonl` 日志标准，提供全流程毫秒级可追溯审计。

---

## 📚 10 个实战模块课程大纲与源码

每个模块均配备标准架构设计、端到端 Python 代码实现与自动化 Pytest 校验套件：

| 模块编号 | 模块主题 | 核心实战代码与 Lab 链接 |
| :--- | :--- | :--- |
| **Module 01** | **为什么需要智能体驾驭工程** | [`course_implementation/module_01_why_harness_engineering/`](./course_implementation/module_01_why_harness_engineering/) |
| **Module 02** | **核心驾驭架构五大支柱 (Core Harness Stack)** | [`course_implementation/module_02_core_harness_stack/`](./course_implementation/module_02_core_harness_stack/) |
| **Module 03** | **规范驱动开发 (Spec-Driven Development)** | [`course_implementation/module_03_spec_driven_development/`](./course_implementation/module_03_spec_driven_development/) |
| **Module 04** | **确定性防护栏与生命周期拦截钩子** | [`course_implementation/module_04_guardrails_and_hooks/`](./course_implementation/module_04_guardrails_and_hooks/) |
| **Module 05** | **权限提权网关与分级审批矩阵** | [`course_implementation/module_05_break_and_qna/`](./course_implementation/module_05_break_and_qna/) |
| **Module 06** | **测试作为智能体的确定性可靠性层** | [`course_implementation/module_06_tests_as_reliability/`](./course_implementation/module_06_tests_as_reliability/) |
| **Module 07** | **智能体扩展机制：Skills、Plugins 与 MCP** | [`course_implementation/module_07_agent_extensions_mcp/`](./course_implementation/module_07_agent_extensions_mcp/) |
| **Module 08** | **复合工程与多智能体协同架构** | [`course_implementation/module_08_compound_engineering/`](./course_implementation/module_08_compound_engineering/) |
| **Module 09** | **五步端到端生产 SOP 流程** | [`course_implementation/module_09_practical_workflow_pattern/`](./course_implementation/module_09_practical_workflow_pattern/) |
| **Module 10** | **四大驾驭原则与五道生产就绪准入审查** | [`course_implementation/module_10_production_harness_principles/`](./course_implementation/module_10_production_harness_principles/) |

---

## 🔬 毕业设计项目：自主深度研究智能体 (Deep Research Agent)

毕业设计项目位于 [`deep_research_agent/`](./deep_research_agent/)，演示了如何将驾驭系统五大支柱与五步 SOP 应用于长周期学术调研：
* **阶段 1 (Spec First)**: 确立 `SPEC.md` 契约，严禁虚构文献与未经证实的推断。
* **阶段 2 (Sandbox Execution)**: 独立沙箱隔离文献与检索缓存。
* **阶段 3 (Deterministic Guardrails)**: PreToolUse 过滤低质内容与商业广告。
* **阶段 4 (Automated Evaluation)**: Pytest 验证字数、章节结构与引用完整性。
* **阶段 5 (Unified Diff Review)**: 交付 `FINAL_REPORT.md` 与 Token 消耗审计日志。

---

## ⚡ 快速开始与环境搭建

```bash
# 1. 克隆本仓库 (必须保留 .git 目录以支持 Worktree 隔离功能)
git clone https://github.com/kenhuangus/agent-harness-chinese.git
cd agent-harness-chinese

# 2. 创建并激活 Python 虚拟环境 (建议 Python 3.10+)
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. 安装依赖包
pip install -e .

# 4. 运行全套自动化测试套件
python run_all_modules.py
# 或使用 pytest:
pytest
```

---

## 🎓 课程主讲导师介绍

**黄健 (Ken Huang), CISSP**
* 🏛️ **旧金山大学兼职教授**: [旧金山大学学者主页 ↗](https://www.usfca.edu/faculty/ken-huang)
* 🚀 **DistributedApps.ai 创始人兼 CEO**: [DistributedApps.ai ↗](https://distributedapps.ai/)
* ✍️ **技术专栏**: [Substack 专栏 ↗](https://kenhuangus.substack.com/)
* 💼 **领英**: [LinkedIn 领英主页 ↗](https://www.linkedin.com/in/kenhuang8/)

黄健 (Ken Huang) 是 AI 安全与智能体驾驭工程领域的知名专家与学者。担任 OWASP AIVSS (AI 验证安全标准) 项目负责人、云安全联盟 (CSA) Fellow 兼两大 AI 安全工作组联合主席、OWASP Top 10 for LLM Applications 核心成员、AIUC-1 联盟成员以及施密特科学基金会 (Schmidt Sciences) 评审委员会成员。他在 Springer、Cambridge University Press、Wiley 和 Packt 出版了 7 部关于 Agentic AI、Web3 及生成式 AI 安全的权威学术著作，其中《Harness Engineering》荣登亚马逊领域畅销榜首。

---

## 📚 出版著作

* 📖 **Agentic AI: Theories and Practices** (Springer) — [Amazon ↗](https://www.amazon.com/dp/3031900251)
* 📖 **Securing AI Agents: Foundations, Frameworks, and Real-World Deployment** (Springer) — [Amazon ↗](https://www.amazon.com/dp/3031901002)
* 📖 **Generative AI Security: Theories and Practices** (Springer) — [Amazon ↗](https://www.amazon.com/dp/3031542517)
* 📖 **Beyond AI: ChatGPT, Web3, and the Business Landscape of Tomorrow** (Springer) — [Amazon ↗](https://www.amazon.com/dp/3031448839)
* 📖 **Web3: Blockchain, the New Economy, and the Self-Sovereign Internet** (Cambridge University Press) — [Amazon ↗](https://www.amazon.com/dp/1009384467)
* 📖 **Blockchain and Web3: Building Foundations of the Metaverse** (Wiley) — [Amazon ↗](https://www.amazon.com/dp/1394186524)
* 📖 **Harness Engineering** (Packt / 亚马逊 #1 畅销书) — [Amazon ↗](https://www.amazon.com/dp/B0HF3F86YM)

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源。

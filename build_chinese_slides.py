# -*- coding: utf-8 -*-
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, 'harness_course_presentation', 'slides_data.json')
TEMPLATE_FILE = os.path.join(ROOT_DIR, 'slides_template.html')


def highlight_python(code: str, highlight_lines: list[int] = None) -> str:
    if highlight_lines is None:
        highlight_lines = []

    keywords = {
        'class', 'def', 'return', 'if', 'else', 'elif', 'for', 'while',
        'import', 'from', 'as', 'try', 'except', 'finally', 'raise',
        'with', 'async', 'await', 'pass', 'break', 'continue', 'lambda',
        'yield', 'in', 'is', 'not', 'and', 'or', 'None', 'True', 'False',
        'self', 'cls'
    }

    builtins = {
        'print', 'len', 'range', 'str', 'int', 'float', 'bool', 'list',
        'dict', 'set', 'tuple', 'open', 'sum', 'min', 'max', 'enumerate',
        'zip', 'isinstance', 'issubclass', 'type', 'id', 'hasattr',
        'getattr', 'setattr', 'Path', 'subprocess', 'json', 're', 'sys',
        'hashlib', 'FastMCP', 'PermissionError', 'RuntimeError', 'Exception',
        'ZeroDivisionError'
    }

    lines = code.split('\n')
    highlighted_lines = []

    for idx, line in enumerate(lines, 1):
        is_hl = idx in highlight_lines
        hl_class = ' code-line-hl' if is_hl else ''
        key_badge = '<span class="key-badge">核心</span>' if is_hl else ''

        pos = 0
        n = len(line)
        line_out = []

        while pos < n:
            if line[pos] == '#':
                comment = line[pos:]
                comment_esc = comment.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                line_out.append(f'<span class="tok-com">{comment_esc}</span>')
                break

            if line[pos] in ('"', "'"):
                quote_char = line[pos]
                if line[pos:pos+3] == quote_char * 3:
                    end_idx = line.find(quote_char * 3, pos + 3)
                    if end_idx == -1:
                        str_lit = line[pos:]
                        pos = n
                    else:
                        str_lit = line[pos:end_idx+3]
                        pos = end_idx + 3
                else:
                    end_idx = pos + 1
                    while end_idx < n:
                        if line[end_idx] == '\\':
                            end_idx += 2
                            continue
                        if line[end_idx] == quote_char:
                            end_idx += 1
                            break
                        end_idx += 1
                    str_lit = line[pos:end_idx]
                    pos = end_idx

                str_esc = str_lit.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                line_out.append(f'<span class="tok-str">{str_esc}</span>')
                continue

            if line[pos] == '@':
                end_idx = pos + 1
                while end_idx < n and (line[end_idx].isalnum() or line[end_idx] in ('_', '.')):
                    end_idx += 1
                dec_lit = line[pos:end_idx]
                pos = end_idx
                dec_esc = dec_lit.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                line_out.append(f'<span class="tok-dec">{dec_esc}</span>')
                continue

            if line[pos].isalpha() or line[pos] == '_':
                end_idx = pos + 1
                while end_idx < n and (line[end_idx].isalnum() or line[end_idx] == '_'):
                    end_idx += 1
                word = line[pos:end_idx]
                pos = end_idx
                word_esc = word.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                if word in keywords:
                    line_out.append(f'<span class="tok-kw">{word_esc}</span>')
                elif word in builtins:
                    line_out.append(f'<span class="tok-typ">{word_esc}</span>')
                elif pos < n and line[pos] == '(':
                    line_out.append(f'<span class="tok-fn">{word_esc}</span>')
                elif word.isupper() and len(word) > 1:
                    line_out.append(f'<span class="tok-const">{word_esc}</span>')
                elif word[0].isupper() and not word.isupper():
                    line_out.append(f'<span class="tok-cls">{word_esc}</span>')
                else:
                    line_out.append(word_esc)
                continue

            ch = line[pos]
            if ch == '<': line_out.append('&lt;')
            elif ch == '>': line_out.append('&gt;')
            elif ch == '&': line_out.append('&amp;')
            else: line_out.append(ch)
            pos += 1

        formatted_line = ''.join(line_out)
        highlighted_lines.append(
            f'<div class="code-line{hl_class}"><span class="line-num">{idx:2d}</span>{key_badge}<span class="line-code">{formatted_line}</span></div>'
        )

    return '\n'.join(highlighted_lines)


def generate_svg_for_slide(num: int, title: str) -> str:
    title_upper = title.upper()

    if num == 2 or '关于讲师' in title_upper or 'ABOUT ME' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <defs>
    <clipPath id="headshot-circle">
      <circle cx="65" cy="55" r="32"/>
    </clipPath>
  </defs>
  <rect x="15" y="6" width="770" height="98" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <circle cx="65" cy="55" r="34" fill="#F5E6DF" stroke="#BD5D3A" stroke-width="2.5"/>
  <image href="assets/images/ken-head-shot.png" x="31" y="21" width="68" height="68" clip-path="url(#headshot-circle)" preserveAspectRatio="xMidYMid slice"/>
  <text x="115" y="44" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="16.5" font-weight="900">黄健 (KEN HUANG), CISSP — 讲师与 AI 安全学者</text>
  <text x="115" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="600">《Harness Engineering》与《MAESTRO》作者 | 旧金山大学兼职教授</text>
  <text x="115" y="88" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="750">CSA Fellow 兼联合主席 | OWASP AIVSS 项目负责人 | AIUC-1 联盟 | 施密特基金会</text>
</svg>'''
    elif num == 3 or '核心论点' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <rect x="20" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#6B6B63" stroke-width="2"/>
  <text x="202" y="34" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="14" font-weight="800" text-anchor="middle">传统软件工程 (确定性系统)</text>
  <text x="202" y="56" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="11.5" text-anchor="middle">SDLC · Agile · CI/CD · 测试金字塔 · SRE</text>
  <text x="202" y="78" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">相同输入 ➔ 产生 100% 确定性输出</text>
  <path d="M385 54 L415 54" stroke="#D97757" stroke-width="3.5" stroke-dasharray="4 4"/>
  <rect x="415" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <text x="597" y="34" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="14" font-weight="800" text-anchor="middle">智能体治理工程 (非确定性系统)</text>
  <text x="597" y="56" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="11.5" text-anchor="middle">记忆 · 路径沙箱 · 生命周期钩子 · TDA 测试自愈</text>
  <text x="597" y="78" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="750" text-anchor="middle">概率性大模型 ➔ 确定性受控与安全运行</text>
</svg>'''
    elif 'COURSE MASTER MAP' in title_upper or '全景知识大纲' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <rect x="20" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2.2"/>
  <text x="202" y="36" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="14" font-weight="800" text-anchor="middle">第一部分：基础架构与确定性控制</text>
  <text x="202" y="58" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="11" text-anchor="middle">模块 1–5: 记忆脚手架、SDD 规范与安全提权网关</text>
  <text x="202" y="78" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">确定性执行 · 路径沙箱 · 生命周期拦截</text>
  <path d="M385 54 L415 54" stroke="#BD5D3A" stroke-width="3.5" stroke-dasharray="4 4"/>
  <rect x="415" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.2"/>
  <text x="597" y="36" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="14" font-weight="800" text-anchor="middle">第二部分：生产级可靠性与团队协同</text>
  <text x="597" y="58" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="11" text-anchor="middle">模块 6–10: TDA 自愈、MCP 协议、多智能体与审计</text>
  <text x="597" y="78" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">五道生产就绪准入审计评分 (5-Gate Ready)</text>
</svg>'''
    elif '五大支柱' in title_upper or '5 CORE HARNESS' in title_upper or '模块 2' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">1. 分层记忆系统</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">CLAUDE.md 规范</text>
    <text x="72" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">Auto Memory</text>
  </g>
  <g transform="translate(170, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">2. 受限工具沙箱</text>
    <text x="72" y="52" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">最小特权白名单</text>
    <text x="72" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">is_relative_to()</text>
  </g>
  <g transform="translate(325, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">3. 确定性钩子</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">PreToolUse 拦截</text>
    <text x="72" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">AST 语法与秘钥扫描</text>
  </g>
  <g transform="translate(480, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">4. Token 预算</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">20/20/50/10 比例</text>
    <text x="72" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">首尾保留压缩</text>
  </g>
  <g transform="translate(635, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">5. 审计追踪</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">events.jsonl</text>
    <text x="72" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">不可变追加记录</text>
  </g>
</svg>'''
    elif '规范驱动' in title_upper or 'SPEC' in title_upper or '模块 3' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">1. SPEC.md 契约</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">明确锁定文件列表</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">机器可验证验收标准</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">2. 范围白名单校验</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">allowed_files 检查</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">阻断 database.py</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">3. 非目标过滤</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">过滤架构膨胀</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">ast.parse() 语法编译</text>
  </g>
  <g transform="translate(585, 6)">
    <rect x="0" y="0" width="195" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="97" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">4. 自动化测试闭环</text>
    <text x="97" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">test_auth.py 全部通过</text>
    <text x="97" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">零缺陷准入交付</text>
  </g>
</svg>'''
    elif '防护栏' in title_upper or 'HOOKS' in title_upper or '模块 4' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#6B6B63" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">第 1 层: 提示词记忆</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">CLAUDE.md / AGENTS.md</text>
    <text x="87" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">系统级规则引导</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">第 2 层: Schema 强校验</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">JSON Schema 参数约束</text>
    <text x="87" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">类型非法即阻断</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">第 3 层: 生命周期钩子</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">PreToolUse 拦截</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">AST 语法与秘钥扫描</text>
  </g>
  <g transform="translate(585, 6)">
    <rect x="0" y="0" width="195" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="97" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">第 4 层: OS 路径沙箱</text>
    <text x="97" y="50" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">is_relative_to() 隔离</text>
    <text x="97" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">进程级最小特权</text>
  </g>
</svg>'''
    elif '提权网关' in title_upper or 'PERMISSION' in title_upper or '模块 5' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#6B6B63" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">LOW (低风险)</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">read_file, list_dir</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700">自动放行 (Auto-approve)</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">MEDIUM (中风险)</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">write_file, run_test</text>
    <text x="87" y="70" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700">沙箱内记录并执行</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">HIGH (高风险)</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">pip_install, 网络请求</text>
    <text x="87" y="70" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700">增强型安全审计</text>
  </g>
  <g transform="translate(585, 6)">
    <rect x="0" y="0" width="195" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.5"/>
    <text x="97" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">CRITICAL (极高风险)</text>
    <text x="97" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="750" text-anchor="middle">git_push, db_drop</text>
    <text x="97" y="70" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="800">校验 approvals.json</text>
  </g>
</svg>'''
    elif '测试作为' in title_upper or 'TESTS AS' in title_upper or 'TDA' in title_upper or '模块 6' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">1. 编写代码</text>
    <text x="72" y="54" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">大模型提议实现</text>
  </g>
  <g transform="translate(170, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">2. 隔离运行测试</text>
    <text x="72" y="54" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">pytest 子进程执行</text>
  </g>
  <g transform="translate(325, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">3. 提取失败堆栈</text>
    <text x="72" y="54" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">精确 Traceback 注入</text>
  </g>
  <g transform="translate(480, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">4. 自愈闭环修复</text>
    <text x="72" y="54" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">定向修复缺陷</text>
  </g>
  <g transform="translate(635, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="72" y="30" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">5. 固化防回归</text>
    <text x="72" y="54" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">自动追加测试断言</text>
  </g>
</svg>'''
    elif 'MCP' in title_upper or 'SKILLS' in title_upper or 'PLUGINS' in title_upper or '模块 7' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(20, 6)">
    <rect x="0" y="0" width="220" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="110" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">Claude Code 客户端</text>
    <text x="110" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">Agent Skills &amp; Plugins</text>
    <text x="110" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">.claude-plugin/plugin.json</text>
  </g>
  <path d="M250 49 L320 49" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="3 3"/>
  <text x="285" y="40" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="800" text-anchor="middle">stdio / JSON-RPC</text>
  <g transform="translate(330, 6)">
    <rect x="0" y="0" width="440" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="220" y="26" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">Model Context Protocol (MCP 2.x) 服务器</text>
    <text x="75" y="52" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700">@mcp.tool()</text>
    <text x="75" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5">安全工具函数</text>
    <text x="215" y="52" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700">@mcp.resource()</text>
    <text x="215" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5">只读系统资源</text>
    <text x="355" y="52" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700">@mcp.prompt()</text>
    <text x="355" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5">预设交互模板</text>
  </g>
</svg>'''
    elif '复合工程' in title_upper or 'COMPOUND' in title_upper or 'MULTI-AGENT' in title_upper or '模块 8' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#6B6B63" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">1. 规划者 (Planner)</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10.5" text-anchor="middle">需求分析与任务切分</text>
    <text x="87" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">生成 SPEC-SUB-01.md</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">2. 执行者 (Implementer)</text>
    <text x="87" y="50" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Git Worktree 物理隔离</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">编写代码并自运行测试</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">3. 审查者 (Reviewer)</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Git Diff 补丁审查</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">验收标准合规准入</text>
  </g>
  <g transform="translate(585, 6)">
    <rect x="0" y="0" width="195" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="97" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="800" text-anchor="middle">4. 主分支安全合并</text>
    <text x="97" y="50" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">telemetry.jsonl 遥测</text>
    <text x="97" y="70" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">清理临时 Worktree</text>
  </g>
</svg>'''
    elif '五步' in title_upper or 'SOP' in title_upper or '模块 9' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">步骤 1: 规范契约</text>
    <text x="72" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">SPEC.md 范围定义</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">锁定验收标准</text>
  </g>
  <g transform="translate(170, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">步骤 2: 沙箱执行</text>
    <text x="72" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">隔离工作区写入</text>
    <text x="72" y="68" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">阻断跨目录穿越</text>
  </g>
  <g transform="translate(325, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">步骤 3: 确定性防护</text>
    <text x="72" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">AST 语法预检</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">凭证泄露扫描</text>
  </g>
  <g transform="translate(480, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">步骤 4: Pytest 验证</text>
    <text x="72" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">子进程自动化测试</text>
    <text x="72" y="68" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">100% 断言通过</text>
  </g>
  <g transform="translate(635, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">步骤 5: 审查归档</text>
    <text x="72" y="50" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">Git Diff 补丁输出</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">审计日志归档</text>
  </g>
</svg>'''
    elif '四大原则' in title_upper or '准入审查' in title_upper or '模块 10' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="800" text-anchor="middle">Gate 1: 记忆规范</text>
    <text x="72" y="48" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">CLAUDE.md / AGENTS</text>
    <text x="72" y="68" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="9.5" font-weight="700">记忆文件完整</text>
  </g>
  <g transform="translate(170, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="800" text-anchor="middle">Gate 2: 安全钩子</text>
    <text x="72" y="48" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">PreToolUse 拦截配置</text>
    <text x="72" y="68" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="9.5" font-weight="700">危险标志已阻断</text>
  </g>
  <g transform="translate(325, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="800" text-anchor="middle">Gate 3: 测试运行器</text>
    <text x="72" y="48" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">独立 Pytest 执行</text>
    <text x="72" y="68" fill="#D97757" font-family="Inter, system-ui, sans-serif" font-size="9.5" font-weight="700">自动化断言通过</text>
  </g>
  <g transform="translate(480, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="800" text-anchor="middle">Gate 4: MCP 声明</text>
    <text x="72" y="48" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">Tools / Resources</text>
    <text x="72" y="68" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="9.5" font-weight="700">标准 Schema 契约</text>
  </g>
  <g transform="translate(635, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="800" text-anchor="middle">Gate 5: 团队分工</text>
    <text x="72" y="48" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9.5" text-anchor="middle">Subagents &amp; Worktree</text>
    <text x="72" y="68" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="9.5" font-weight="750">5/5 生产就绪认证</text>
  </g>
</svg>'''
    return ''


def build():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        slides = json.load(f)

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    svg_map = {}
    for s in slides:
        num = s.get('number', 0)
        title = s.get('raw_lines', [''])[0]
        svg_html = generate_svg_for_slide(num, title)
        if svg_html:
            svg_map[num] = svg_html

        if s.get('slide_type') == 'code' and 'code_block' in s:
            s['highlighted_code'] = highlight_python(s['code_block'], s.get('highlight_lines', []))

    svg_json = json.dumps(svg_map, ensure_ascii=False)
    slides_json = json.dumps(slides, ensure_ascii=False)

    html_content = template.replace('__SLIDES_JSON__', slides_json).replace('__SVG_JSON__', svg_json)

    slides_path = os.path.join(ROOT_DIR, 'slides.html')
    docs_slides_path = os.path.join(ROOT_DIR, 'docs', 'slides.html')

    with open(slides_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open(docs_slides_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"SUCCESS: Built {len(slides)} Chinese slides to {slides_path} and {docs_slides_path}")


if __name__ == '__main__':
    build()

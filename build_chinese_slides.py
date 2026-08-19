# -*- coding: utf-8 -*-
"""
Build all 47 Chinese SVG Slides into an interactive, ultra-responsive HTML deck.
Look and feel perfectly matched with Packt Harness Masterclass.
Outputs:
  - slides.html
  - docs/slides.html
"""

import json
import re
import os

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

    if num == 2 or '关于讲师' in title_upper or 'ABOUT ME' in title_upper or '黄健' in title_upper:
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
    elif '深度研究' in title_upper or 'CAPSTONE' in title_upper or '毕业设计' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">阶段 1: 研报契约</text>
    <text x="72" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">SPEC.md 结构约束</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">禁止虚构引用</text>
  </g>
  <g transform="translate(170, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">阶段 2: 抓取沙箱</text>
    <text x="72" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">独立工作目录</text>
    <text x="72" y="68" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">隔离文献缓存</text>
  </g>
  <g transform="translate(325, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">阶段 3: 来源过滤</text>
    <text x="72" y="50" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="10" text-anchor="middle">过滤不可信网站</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">提取高质量学术源</text>
  </g>
  <g transform="translate(480, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">阶段 4: 研报评测</text>
    <text x="72" y="50" fill="#BD5D3A" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">Pytest 格式断言</text>
    <text x="72" y="68" fill="#4A4A44" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">字数与链接检查</text>
  </g>
  <g transform="translate(635, 6)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#141413" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">阶段 5: 交付归档</text>
    <text x="72" y="50" fill="#141413" font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">FINAL_REPORT.md</text>
    <text x="72" y="68" fill="#6B6B63" font-family="Inter, system-ui, sans-serif" font-size="9" text-anchor="middle">Token 消耗审计日志</text>
  </g>
</svg>'''
    return ''


def build_slides_html():
    json_path = os.path.join(os.path.dirname(__file__), 'harness_course_presentation', 'slides_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        slides = json.load(f)

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

    html_template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude 智能体 Harness 治理工程实战大师课</title>
  <meta name="description" content="为非确定性 AI 编码智能体构建确定性控制与安全治理系统 —— 全套 47 张交互式全景课件。">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" sizes="192x192" href="favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="favicon.png">
  <style>
    :root {
      --bg: #F0EEE6;
      --surface: #FAF9F5;
      --surface-card: #FFFFFF;
      --ink: #141413;
      --ink-muted: #6B6B63;
      --rule: #E3E0D6;
      --accent: #D97757;
      --accent-dk: #BD5D3A;
      --accent-sf: #F5E6DF;
      --font-display: ui-serif, Georgia, "Songti SC", "SimSun", serif;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      --font-code: ui-monospace, "JetBrains Mono", Menlo, Consolas, monospace;
      --code-bg: #24231F;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      height: 100%;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--font-sans);
      font-size: 16px;
      overflow: hidden;
    }

    header {
      height: 52px;
      background: var(--surface);
      border-bottom: 1px solid var(--rule);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.2rem;
      flex: 0 0 auto;
      z-index: 100;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }

    .brand-title {
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--ink);
      letter-spacing: -0.01em;
    }

    .controls {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .btn {
      background: var(--surface);
      border: 1px solid var(--rule);
      color: var(--ink);
      padding: 0.35rem 0.70rem;
      border-radius: 6px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      text-decoration: none;
      transition: all 0.15s ease-in-out;
    }
    .btn:hover {
      background: var(--accent-sf);
      border-color: var(--accent);
      color: var(--accent-dk);
    }
    .btn-primary {
      background: var(--accent);
      color: #FFFFFF !important;
      border-color: var(--accent-dk);
    }
    .btn-primary:hover {
      background: var(--accent-dk);
    }

    select.slide-select {
      background: var(--surface);
      border: 1px solid var(--rule);
      color: var(--ink);
      padding: 0.35rem 0.60rem;
      border-radius: 6px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      max-width: 280px;
    }

    .goto-group {
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .goto-input {
      width: 52px;
      padding: 0.35rem 0.40rem;
      border: 1px solid var(--rule);
      border-radius: 6px;
      background: var(--surface);
      font-size: 0.84rem;
      font-weight: 600;
      text-align: center;
      color: var(--ink);
    }
    .goto-input:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-sf);
    }
    .btn-goto {
      padding: 0.35rem 0.55rem;
      background: var(--accent-sf);
      border-color: var(--accent);
      color: var(--accent-dk);
    }

    main {
      height: calc(100vh - 55px);
      display: flex;
      flex-direction: column;
      padding: 0.85rem;
      overflow: hidden;
    }

    .slide-viewport {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 0;
    }

    .slide-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 12px;
      width: 100%;
      max-width: 1380px;
      height: 100%;
      display: flex;
      flex-direction: column;
      padding: 1.15rem 1.45rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
      overflow: hidden;
    }

    .slide-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.8rem;
      margin-bottom: 0.35rem;
      border-bottom: 1px solid var(--rule);
      padding-bottom: 0.35rem;
      flex: 0 0 auto;
    }
    .slide-title-wrap { min-width: 0; }
    .slide-title {
      font-family: var(--font-display);
      font-size: clamp(1.35rem, 2.1vw, 1.85rem);
      font-weight: 700;
      line-height: 1.15;
      letter-spacing: -0.015em;
      color: var(--ink);
    }
    .slide-header-right {
      display: flex;
      align-items: center;
      gap: 0.60rem;
      flex: 0 0 auto;
    }
    .packt-logo-link {
      display: inline-flex;
      align-items: center;
      padding: 0.18rem 0.50rem;
      background: #FAF8F2;
      border: 1.2px solid var(--rule);
      border-radius: 6px;
      transition: all 0.16s ease-in-out;
      text-decoration: none;
      box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .packt-logo-link:hover {
      background: var(--accent-sf);
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    .packt-title-logo {
      height: 22px;
      width: auto;
      display: block;
    }
    .slide-num-badge {
      background: var(--accent-sf);
      color: var(--ink);
      border: 1px solid var(--rule);
      padding: 0.22rem 0.60rem;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 750;
      white-space: nowrap;
      flex: 0 0 auto;
    }

    .slide-body {
      --fit-scale: 1;
      --slide-body-base-size: 1.28rem;
      flex: 1;
      min-height: 0;
      overflow-y: auto;
      padding-right: 0.20rem;
      font-size: calc(var(--slide-body-base-size) * var(--fit-scale));
      line-height: 1.55;
      color: var(--ink);
    }

    code {
      font-family: var(--font-code);
      background: var(--accent-sf);
      color: var(--accent-dk);
      padding: 0.08rem 0.32rem;
      border-radius: 4px;
      font-size: 0.90em;
      white-space: nowrap;
      border: 1px solid var(--rule);
    }
    pre code, .tree-block code, .code-editor-body code {
      white-space: pre !important;
      background: transparent !important;
      border: none !important;
      padding: 0 !important;
      color: inherit !important;
    }

    .slide-content-wrapper {
      width: 100%;
      display: block;
    }
    .slide-body > svg, .slide-svg {
      display: block;
      width: 100% !important;
      height: auto;
      max-width: 100%;
      margin: 0.35rem 0 0.65rem 0;
    }

    /* Comparison Table Styling */
    .slide-table {
      width: 100%;
      border-collapse: collapse;
      margin: 0.35rem 0 0.60rem 0;
      font-size: 0.88rem;
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .slide-table th {
      background: var(--accent-sf);
      color: var(--ink);
      font-weight: 750;
      text-align: left;
      padding: 0.45rem 0.70rem;
      border-bottom: 1.5px solid var(--rule);
      font-family: var(--font-display);
      font-size: 0.95rem;
    }
    .slide-table td {
      padding: 0.40rem 0.70rem;
      border-bottom: 1px solid var(--rule);
      color: var(--ink);
      vertical-align: middle;
    }
    .slide-table tr:last-child td { border-bottom: none; }
    .slide-table tr:nth-child(even) td { background: rgba(240, 238, 230, 0.4); }

    /* Bullet List & Hierarchies */
    .bullet-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.42rem;
      margin-top: 0.25rem;
    }
    .bullet-list.dense-columns {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      column-gap: 1.25rem;
      row-gap: 0.42rem;
    }
    .bullet-item {
      position: relative;
      padding-left: 1.35rem;
      line-height: 1.48;
    }
    .bullet-item::before {
      content: "•";
      position: absolute;
      left: 0.25rem;
      color: var(--accent);
      font-weight: 800;
      font-size: 1.15em;
    }
    .sub-bullet-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      margin-top: 0.25rem;
      padding-left: 1.10rem;
    }
    .sub-bullet-item {
      position: relative;
      padding-left: 1.10rem;
      font-size: 0.92em;
      color: var(--ink);
      line-height: 1.42;
    }
    .sub-bullet-item::before {
      content: "–";
      position: absolute;
      left: 0.20rem;
      color: var(--accent-dk);
      font-weight: 700;
    }

    /* Code Slide Split Layout */
    .code-slide-container {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 1.10rem;
      height: 100%;
      min-height: 0;
    }
    .code-editor-window {
      background: var(--code-bg);
      border-radius: 8px;
      border: 1px solid #383733;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .code-editor-header {
      background: #1C1B18;
      padding: 0.40rem 0.80rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #33322E;
      font-family: var(--font-code);
      font-size: 0.76rem;
      color: #A0A09A;
      flex: 0 0 auto;
    }
    .code-dots {
      display: flex;
      gap: 5px;
    }
    .code-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .dot-red { background: #FF5F56; }
    .dot-yellow { background: #FFBD2E; }
    .dot-green { background: #27C93F; }
    .code-lang-tag {
      background: #2D2B27;
      padding: 0.12rem 0.40rem;
      border-radius: 4px;
      font-size: 0.70rem;
      color: #D97757;
      font-weight: 700;
    }
    .cmd-copy-btn {
      background: #2D2B27;
      border: 1px solid #44433E;
      color: #ECEBE4;
      padding: 0.15rem 0.50rem;
      border-radius: 4px;
      font-size: 0.72rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      transition: background 0.12s;
    }
    .cmd-copy-btn:hover {
      background: #3E3C36;
      color: #FFFFFF;
    }
    .code-block {
      flex: 1;
      overflow: auto;
      padding: 0.75rem 0.90rem;
      font-family: var(--font-code);
      font-size: 0.84rem;
      line-height: 1.52;
      color: #F5F4EE;
    }
    .code-line {
      display: flex;
      align-items: flex-start;
      padding: 0.06rem 0;
    }
    .code-line-hl {
      background: rgba(217, 119, 87, 0.18);
      border-left: 3px solid var(--accent);
      padding-left: 0.25rem;
      margin-left: -0.25rem;
    }
    .line-num {
      width: 2.2rem;
      color: #6E6D66;
      text-align: right;
      padding-right: 0.75rem;
      user-select: none;
      flex-shrink: 0;
      font-size: 0.78rem;
    }
    .line-code {
      flex: 1;
      white-space: pre;
    }
    .key-badge {
      background: var(--accent);
      color: #FFFFFF;
      font-size: 0.60rem;
      font-weight: 800;
      padding: 0.05rem 0.25rem;
      border-radius: 3px;
      margin-right: 0.40rem;
      align-self: center;
      line-height: 1;
    }

    /* Syntax Highlighting Colors */
    .tok-kw { color: #FF7B72; font-weight: 700; }
    .tok-fn { color: #D2A8FF; font-weight: 600; }
    .tok-cls { color: #7EE787; font-weight: 700; }
    .tok-str { color: #A5D6FF; }
    .tok-com { color: #8B949E; font-style: italic; }
    .tok-typ { color: #FFA657; }
    .tok-dec { color: #79C0FF; font-weight: 600; }
    .tok-const { color: #79C0FF; font-weight: 700; }

    /* Code Concepts Column */
    .code-concepts-column {
      display: flex;
      flex-direction: column;
      gap: 0.50rem;
      overflow-y: auto;
    }
    .code-concept-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      border-left: 3px solid var(--accent);
    }
    .concept-card-head {
      display: flex;
      align-items: center;
      gap: 0.40rem;
      margin-bottom: 0.20rem;
    }
    .concept-tag {
      background: var(--accent-sf);
      color: var(--accent-dk);
      font-weight: 800;
      font-size: 0.72rem;
      padding: 0.10rem 0.40rem;
      border-radius: 4px;
      font-family: var(--font-code);
    }
    .concept-name {
      font-weight: 700;
      font-size: 0.90rem;
      color: var(--ink);
    }
    .concept-card-text {
      font-size: 0.82rem;
      line-height: 1.42;
      color: var(--ink-muted);
    }
    .invariant-card {
      background: #F4F1E8;
      border: 1.5px solid var(--accent);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      margin-top: auto;
    }
    .invariant-title {
      font-weight: 800;
      font-size: 0.86rem;
      color: var(--accent-dk);
      margin-bottom: 0.20rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    /* Instructor Slide (Slide 2) Layout */
    .instructor-slide-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 1.10rem;
      height: 100%;
      min-height: 0;
    }
    .instructor-info-col {
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }
    .author-books-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 10px;
      padding: 0.75rem 0.95rem;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }
    .author-books-header {
      font-family: var(--font-display);
      font-weight: 750;
      font-size: 0.96rem;
      color: var(--ink);
      margin-bottom: 0.60rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--rule);
      padding-bottom: 0.40rem;
    }
    .author-books-header a {
      font-size: 0.78rem;
      color: var(--accent-dk);
      text-decoration: none;
      font-weight: 600;
    }
    .author-books-header a:hover { text-decoration: underline; }
    .books-gallery-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.65rem;
      align-items: start;
    }
    .book-item-card {
      background: #FFFFFF;
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 0.35rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-decoration: none;
      color: var(--ink);
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    }
    .book-item-card:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
      box-shadow: 0 4px 10px rgba(217, 119, 87, 0.15);
    }
    .book-cover-img {
      width: 100%;
      height: 100px;
      object-fit: cover;
      border-radius: 4px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      margin-bottom: 0.30rem;
    }
    .book-item-title {
      font-size: 0.68rem;
      font-weight: 700;
      text-align: center;
      line-height: 1.2;
      max-height: 2.4em;
      overflow: hidden;
      color: var(--ink);
    }
    .book-publisher-tag {
      font-size: 0.58rem;
      color: var(--accent-dk);
      font-weight: 800;
      margin-top: 0.15rem;
      text-transform: uppercase;
    }

    /* Slide 1 Hero & Instructor Cover Layout */
    .slide-1-container {
      display: flex;
      flex-direction: column;
      gap: 0.70rem;
      height: 100%;
      justify-content: center;
    }
    .slide-1-hero-card {
      background: linear-gradient(135deg, rgba(245, 230, 223, 0.45) 0%, rgba(250, 249, 245, 0.90) 100%);
      border: 1.5px solid var(--accent);
      border-radius: 12px;
      padding: 0.95rem 1.45rem;
      box-shadow: 0 4px 14px rgba(217, 119, 87, 0.08);
    }
    .slide-1-hero-tagline {
      font-family: var(--font-display);
      font-size: clamp(1.20rem, 2.0vw, 1.65rem);
      font-weight: 800;
      color: var(--accent-dk);
      line-height: 1.25;
      margin-bottom: 0.30rem;
      letter-spacing: -0.015em;
    }
    .slide-1-hero-desc {
      font-size: clamp(0.88rem, 1.15vw, 1.02rem);
      line-height: 1.50;
      color: var(--ink-muted);
    }
    .slide-1-instructor-card {
      background: var(--surface-card);
      border: 1px solid var(--rule);
      border-radius: 12px;
      padding: 0.85rem 1.35rem;
      display: flex;
      align-items: center;
      gap: 1.25rem;
      box-shadow: 0 3px 12px rgba(0, 0, 0, 0.03);
    }
    .slide-1-avatar-wrap {
      flex-shrink: 0;
      width: 78px;
      height: 78px;
      border-radius: 50%;
      border: 2.5px solid var(--accent);
      padding: 2.5px;
      background: var(--accent-sf);
      box-shadow: 0 3px 8px rgba(217, 119, 87, 0.18);
    }
    .slide-1-avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      display: block;
    }
    .slide-1-instructor-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0.18rem;
    }
    .slide-1-instructor-badge {
      background: var(--accent-sf);
      color: var(--accent-dk);
      font-size: 0.72rem;
      font-weight: 750;
      padding: 0.18rem 0.55rem;
      border-radius: 6px;
      width: fit-content;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .slide-1-instructor-name {
      font-family: var(--font-display);
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.15;
    }
    .slide-1-instructor-titles {
      display: flex;
      flex-direction: column;
      gap: 0.30rem;
      margin-top: 0.20rem;
    }
    .slide-1-title-item {
      display: flex;
      align-items: center;
      gap: 0.50rem;
      font-size: 1.02rem;
      font-weight: 600;
      color: var(--ink);
    }
    .slide-1-title-item .title-icon {
      font-size: 1.15rem;
      flex-shrink: 0;
    }
    .slide-1-org-link {
      color: var(--accent-dk);
      font-weight: 750;
      text-decoration: underline;
      text-underline-offset: 3px;
      transition: color 0.15s ease-in-out;
    }
    .slide-1-org-link:hover {
      color: var(--accent);
    }
    .slide-1-social-links {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      margin-top: 0.30rem;
      flex-wrap: wrap;
    }
    .slide-1-social-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.40rem;
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 0.22rem 0.55rem;
      font-size: 0.86rem;
      color: var(--ink);
    }
    .slide-1-social-pill .social-icon {
      font-size: 0.95rem;
    }
    .slide-1-social-pill .social-label {
      font-weight: 600;
      color: var(--ink-muted);
    }
    .slide-1-social-link {
      color: var(--accent-dk);
      font-weight: 750;
      text-decoration: underline;
      text-underline-offset: 2.5px;
      transition: color 0.15s ease-in-out;
    }
    .slide-1-social-link:hover {
      color: var(--accent);
    }
    .slide-1-social-link .ext-arrow {
      color: var(--accent);
      font-weight: 800;
      font-size: 0.85em;
      text-decoration: none;
      display: inline-block;
    }
    .slide-1-pillars-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
    }
    @media (max-width: 900px) {
      .slide-1-pillars-row {
        grid-template-columns: repeat(2, 1fr);
      }
      .slide-1-instructor-card {
        flex-direction: column;
        text-align: center;
        align-items: center;
      }
      .slide-1-instructor-badge {
        margin: 0 auto;
      }
      .slide-1-title-item {
        justify-content: center;
      }
      .slide-1-social-links {
        justify-content: center;
      }
    }
    .slide-1-pillar-pill {
      background: var(--surface-card);
      border: 1px solid var(--rule);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      border-top: 3px solid var(--accent);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }
    .slide-1-pillar-title {
      font-weight: 750;
      font-size: 0.88rem;
      color: var(--ink);
      margin-bottom: 0.15rem;
    }
    .slide-1-pillar-desc {
      font-size: 0.76rem;
      color: var(--ink-muted);
      line-height: 1.35;
    }

    /* Grid View Mode */
    .grid-viewport {
      height: 100%;
      overflow-y: auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
      padding: 0.5rem;
    }
    .grid-slide-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 10px;
      padding: 1.15rem;
      height: 260px;
      display: flex;
      flex-direction: column;
      cursor: pointer;
      transition: border-color 0.16s, background-color 0.16s;
    }
    .grid-slide-card:hover {
      background: var(--accent-sf);
      border-color: var(--accent);
    }
    .grid-slide-title {
      font-family: var(--font-display);
      font-size: 1.05rem;
      line-height: 1.15;
      font-weight: 650;
      margin-bottom: 0.45rem;
      color: var(--ink);
    }
    .grid-slide-body {
      flex: 1;
      overflow: hidden;
      font-size: 0.80rem;
      line-height: 1.45;
      color: var(--ink-muted);
    }

    .progress-bar { height: 3px; background: var(--rule); width: 100%; }
    .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.3s; }

    @media (max-width: 980px) {
      header { padding: 0 0.6rem; }
      .brand-title { display: none; }
      select.slide-select { max-width: 200px; }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <img src="assets/images/harness_app_icon.png" alt="Harness 治理工程徽标" style="width:28px; height:28px; border-radius:6px; object-fit:cover; display:inline-block;" />
      <div class="brand-title">Claude 智能体 Harness 治理工程实战课</div>
    </div>
    <div class="controls">
      <a href="index.html" class="btn">🏠 课程主页</a>
      <button id="btn-grid" class="btn" onclick="toggleMode()"><span id="mode-icon">📜</span> <span id="mode-text">网格视图</span></button>
      <button id="btn-prev" class="btn" onclick="prevSlide()">❮ 上一页</button>
      <select id="slide-select" class="slide-select" onchange="goToSlide(this.value)"></select>
      <div class="goto-group">
        <input type="number" id="goto-input" min="1" max="''' + str(len(slides)) + '''" placeholder="#" class="goto-input" title="输入页码跳转 (1-''' + str(len(slides)) + ''')" onkeydown="if(event.key==='Enter') jumpToEnteredSlide()">
        <button id="btn-goto" class="btn btn-goto" onclick="jumpToEnteredSlide()" title="跳转到指定页码">跳转 ➔</button>
      </div>
      <button id="btn-next" class="btn" onclick="nextSlide()">下一页 ❯</button>
      <button id="btn-fullscreen" class="btn btn-primary" onclick="toggleFullscreen()">⛶ 全屏演示</button>
    </div>
  </header>

  <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>

  <main>
    <div id="presentation-mode" class="slide-viewport">
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-title-wrap">
            <div id="slide-title" class="slide-title">幻灯片标题</div>
          </div>
          <div class="slide-header-right">
            <div id="slide-packt-badge" style="display:none;">
              <a href="https://www.packtpub.com/" target="_blank" rel="noopener noreferrer" class="packt-logo-link" title="Packt Publishing 出版社">
                <img src="assets/images/packt_logo.svg" alt="Packt Publishing" class="packt-title-logo" />
              </a>
            </div>
            <div id="slide-num-badge" class="slide-num-badge">第 1 / ''' + str(len(slides)) + ''' 页</div>
          </div>
        </div>
        <div id="slide-body" class="slide-body"></div>
      </div>
    </div>

    <div id="grid-mode" class="grid-viewport" style="display:none;"></div>
  </main>

  <script>
    const slidesData = ''' + json.dumps(slides, ensure_ascii=False) + ''';
    const svgMap = ''' + svg_json + ''';

    let currentIdx = 0;
    let isGridMode = false;

    const DENSE_BULLET_MIN_LINES = 9;
    const bodyEl = document.getElementById('slide-body');

    const selectEl = document.getElementById('slide-select');
    slidesData.forEach((s, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      const rawTitle = s.raw_lines ? s.raw_lines[0] : `第 ${s.number} 页`;
      opt.textContent = `第 ${s.number} 页: ${rawTitle.substring(0, 38)}`;
      selectEl.appendChild(opt);
    });

    function cleanNumbers(text) {
      if (!text) return '';
      text = text.replace(/^(\d+[\.\)\:]|\d+\s*&\s*\d+[\.\)\:])\s+/, '');
      return text.trim();
    }

    function formatTextWithCode(text) {
      const keywords = ['CLAUDE.md', 'AGENTS.md', 'SPEC.md', 'MEMORY.md', 'CLAUDE.local.md', 'pytest', 'events.jsonl', 'telemetry.jsonl', 'rm -rf', 'write_file', 'read_file', '.claude-plugin/plugin.json', 'SKILL.md', 'mcp_client_runner.py', 'mcp_server_demo.py', 'core_harness_stack.py', 'guardrails_engine.py', 'spec_driven_verifier.py', 'tda_reliability_pipeline.py', 'multi_agent_team_simulator.py', 'five_step_sop_pipeline.py', 'production_harness_audit.py', 'is_relative_to()', 'ast.parse()', 'PreToolUse', 'PostToolUse', 'MCPServer', 'permissionDecision', 'approvals.json', 'ZeroDivisionError', 'pending_push.json', 'scripts/', 'references/', 'assets/', '.claude/workflows/'];
      
      text = text.replace(
        /\[(.*?)\]\(((?:https?:\/\/|file:\/\/\/)[^\s<>"']+)\)/g,
        (match, label, url) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`
      );

      text = text.replace(
        /(https?:\/\/[^\s<>"']+|file:\/\/\/[^\s<>"']+)/g,
        (match) => {
          let url = match.replace(/[.,;:)]+$/, '');
          let trailing = match.slice(url.length);
          return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>${trailing}`;
        }
      );
      
      keywords.forEach(kw => {
        text = text.replaceAll(kw, `<code>${kw}</code>`);
      });
      return text;
    }

    function copyCommand(btn, text) {
      if (!btn) return;
      const originalHtml = btn.innerHTML;
      
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          btn.innerHTML = '<span>✅</span> 已复制!';
          setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
        }).catch(() => {
          fallbackCopy(btn, text, originalHtml);
        });
      } else {
        fallbackCopy(btn, text, originalHtml);
      }
    }

    function fallbackCopy(btn, text, originalHtml) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy');
        btn.innerHTML = '<span>✅</span> 已复制!';
      } catch (e) {
        btn.innerHTML = '<span>❌</span> 复制失败';
      }
      document.body.removeChild(ta);
      setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
    }

    function copyCodeFromSlide(btn, slideIdx) {
      const slide = slidesData[slideIdx];
      if (slide && slide.code_block) {
        copyCommand(btn, slide.code_block);
      }
    }

    function formatCodeConcepts(lines) {
      if (!lines || lines.length === 0) return '';
      let html = '<div class="code-concepts-list">';
      
      lines.forEach(line => {
        let trimmed = line.trim();
        if (!trimmed) return;
        if (trimmed.startsWith('File:')) return;
        
        trimmed = trimmed.replace(/^[•\-�]\s*/, '').trim();
        
        const lineMatch = trimmed.match(/^\[(第?\s*[\d\-,\s]+行?)\]\s*([^:：]+)[:：]\s*(.*)$/i) || trimmed.match(/^\[(Lines?\s*[\d\-,\s]+)\]\s*([^:：]+)[:：]\s*(.*)$/i);
        if (lineMatch) {
          const lineTag = lineMatch[1];
          const title = lineMatch[2];
          const desc = formatTextWithCode(lineMatch[3]);
          html += `
            <div class="code-concept-card">
              <div class="concept-card-head">
                <span class="concept-tag">📌 ${lineTag}</span>
                <span class="concept-name">${formatTextWithCode(title)}</span>
              </div>
              <div class="concept-card-text">${desc}</div>
            </div>
          `;
        } else {
          const colonIdx = (trimmed.indexOf('：') !== -1) ? trimmed.indexOf('：') : trimmed.indexOf(':');
          if (colonIdx !== -1 && colonIdx < 40) {
            const title = trimmed.slice(0, colonIdx);
            const desc = formatTextWithCode(trimmed.slice(colonIdx + 1));
            html += `
              <div class="code-concept-card">
                <div class="concept-card-head">
                  <span class="concept-name">${formatTextWithCode(title)}</span>
                </div>
                <div class="concept-card-text">${desc}</div>
              </div>
            `;
          } else {
            html += `
              <div class="code-concept-card">
                <div class="concept-card-text">${formatTextWithCode(trimmed)}</div>
              </div>
            `;
          }
        }
      });
      
      html += '</div>';
      return html;
    }

    function parseMarkdownTable(lines) {
      const tableLines = lines.filter(l => l.trim().startsWith('|'));
      if (tableLines.length < 2) return null;

      let html = '<table class="slide-table">';
      let isHeader = true;

      tableLines.forEach(line => {
        const trimmed = line.trim();
        if (/^\|[\s\-:|]+\|$/.test(trimmed)) {
          isHeader = false;
          return;
        }

        const cells = trimmed.split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        if (cells.length === 0) return;

        html += '<tr>';
        cells.forEach(cell => {
          const tag = isHeader ? 'th' : 'td';
          html += `<${tag}>${formatTextWithCode(cell)}</${tag}>`;
        });
        html += '</tr>';
      });

      html += '</table>';
      return html;
    }

    function formatBullets(lines) {
      if (!lines || lines.length === 0) return '';
      
      const hasTable = lines.some(l => l.trim().startsWith('|'));
      if (hasTable) {
        const beforeTable = [];
        const tableLines = [];
        const afterTable = [];
        let state = 0;

        lines.forEach(line => {
          if (state === 0) {
            if (line.trim().startsWith('|')) { state = 1; tableLines.push(line); }
            else { beforeTable.push(line); }
          } else if (state === 1) {
            if (line.trim().startsWith('|')) { tableLines.push(line); }
            else { state = 2; afterTable.push(line); }
          } else {
            afterTable.push(line);
          }
        });

        let html = '';
        if (beforeTable.length > 0) html += formatBullets(beforeTable);
        const parsedTbl = parseMarkdownTable(tableLines);
        if (parsedTbl) html += parsedTbl;
        if (afterTable.length > 0) html += formatBullets(afterTable);
        return html;
      }

      const populatedLines = lines.filter(line => line.trim());
      if (populatedLines.length === 0) return '';

      const hasIndented = populatedLines.some(l => /^\s{2,}|	/.test(l));
      const denseClass = (!hasIndented && populatedLines.length >= DENSE_BULLET_MIN_LINES) ? ' dense-columns' : '';
      let html = '';
      let listOpen = false;
      let groupOpen = false;
      let subListOpen = false;

      populatedLines.forEach((line, idx) => {
        const isIndented = /^\s{2,}|	/.test(line);
        const trimmed = line.trim();
        const hasBullet = /^[•\-\*�]/.test(trimmed);

        let cleanText = trimmed.replace(/^[•\-\*�]\s*/, '').trim();
        cleanText = cleanNumbers(cleanText);

        const labUrl = cleanText.match(/^Lab demo:\s*(https:\/\/[^\s]+)/i) || cleanText.match(/^交互式实验[指南|演示]*[:：]\s*(https:\/\/[^\s]+)/i);
        if (labUrl) {
          cleanText = `<a href="${labUrl[1]}" target="_blank" rel="noopener noreferrer">🔗 实战代码 Lab 演示：在 GitHub 中打开该模块</a>`;
        } else {
          cleanText = formatTextWithCode(cleanText);
        }

        if (!cleanText) return;

        if (!isIndented) {
          if (subListOpen) { html += '</ul>'; subListOpen = false; }
          if (groupOpen) { html += '</li>'; groupOpen = false; }
          if (!listOpen) { html += `<ul class="bullet-list${denseClass}">`; listOpen = true; }

          const nextLine = populatedLines[idx + 1];
          const hasChildren = nextLine && /^\s{2,}|	/.test(nextLine);

          if (hasChildren) {
            html += `<li class="bullet-item"><span>${cleanText}</span>`;
            groupOpen = true;
          } else {
            html += `<li class="bullet-item"><span>${cleanText}</span></li>`;
          }
        } else {
          if (!groupOpen) {
            if (!listOpen) { html += `<ul class="bullet-list${denseClass}">`; listOpen = true; }
            html += `<li class="bullet-item">`;
            groupOpen = true;
          }
          if (!subListOpen) {
            html += '<ul class="sub-bullet-list">';
            subListOpen = true;
          }
          html += `<li class="sub-bullet-item"><span>${cleanText}</span></li>`;
        }
      });

      if (subListOpen) html += '</ul>';
      if (groupOpen) html += '</li>';
      if (listOpen) html += '</ul>';
      return html;
    }

    function renderSlide(idx) {
      if (idx < 0) idx = 0;
      if (idx >= slidesData.length) idx = slidesData.length - 1;
      currentIdx = idx;

      const slide = slidesData[idx];
      selectEl.value = idx;
      
      const gotoInput = document.getElementById('goto-input');
      if (gotoInput) {
        gotoInput.placeholder = String(slide.number);
      }

      const title = slide.raw_lines[0] || `第 ${slide.number} 页`;
      document.getElementById('slide-title').innerText = title;
      document.getElementById('slide-num-badge').innerText = `第 ${slide.number} / ${slidesData.length} 页`;

      const packtBadge = document.getElementById('slide-packt-badge');
      if (packtBadge) {
        packtBadge.style.display = (slide.number === 1) ? 'inline-flex' : 'none';
      }

      if (window.location.hash !== '#' + slide.number) {
        history.replaceState(null, '', '#' + slide.number);
      }

      const restLines = slide.raw_lines ? slide.raw_lines.slice(1) : [];
      const isCode = slide.slide_type === 'code';

      let bodyHtml = '';

      if (isCode && slide.highlighted_code) {
        const fileTag = slide.code_filename || 'source.py';
        const rawBullets = slide.raw_lines.slice(1);
        
        const primaryFile = fileTag.split(' & ')[0].trim();
        const pathParts = primaryFile.split('/');
        const moduleFolder = pathParts.slice(0, 2).join('/');
        
        let testsRelativePath = `${moduleFolder}/output/tests`;
        if (slide.number === 41 || moduleFolder.includes('module_09')) {
          testsRelativePath = 'course_implementation/module_09_practical_workflow_pattern/output/tests';
        } else if (slide.number === 46 || primaryFile.startsWith('deep_research_agent')) {
          testsRelativePath = 'deep_research_agent/tests';
        }
        
        const fileGithubUrl = `https://github.com/kenhuangus/agent-harness-chinese/blob/main/${primaryFile}`;
        const testsGithubUrl = `https://github.com/kenhuangus/agent-harness-chinese/tree/main/${testsRelativePath}`;
        
        bodyHtml += `
          <div class="code-slide-container">
            <div class="code-editor-window">
              <div class="code-editor-header">
                <div class="code-dots">
                  <div class="code-dot dot-red"></div>
                  <div class="code-dot dot-yellow"></div>
                  <div class="code-dot dot-green"></div>
                </div>
                <a href="${fileGithubUrl}" target="_blank" rel="noopener noreferrer" class="code-file-tag" title="在 GitHub 查看 ${primaryFile}" style="color:#A0A09A; text-decoration:none;">
                  📄 ${fileTag} ↗
                </a>
                <div style="display:flex; align-items:center; gap:0.45rem;">
                  <button class="cmd-copy-btn" onclick="copyCodeFromSlide(this, ${idx})" title="复制代码">
                    <span class="copy-icon">📋</span> 复制代码
                  </button>
                  <div class="code-lang-tag">${slide.code_language || 'PYTHON'}</div>
                </div>
              </div>
              <div class="code-block">${slide.highlighted_code}</div>
            </div>
            <div class="code-concepts-column">
              ${formatCodeConcepts(rawBullets)}
              <div class="invariant-card">
                <div class="invariant-title">🛡️ 确定性控制架构设计</div>
                <div style="margin-bottom:0.35rem; color:var(--ink); font-size:0.86rem;">通过 GitHub 真实可运行的自动化测试直接验证：</div>
                <div style="display:flex; flex-direction:column; gap:0.25rem; font-size:0.84rem;">
                  <div>📄 <strong>源码文件:</strong> <a href="${fileGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${primaryFile}</code> ↗</a></div>
                  <div>🧪 <strong>验证套件:</strong> <a href="${testsGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${testsRelativePath}</code> ↗</a></div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 1) {
        bodyHtml += `
          <div id="slide-content-wrap" class="slide-1-container">
            <div class="slide-1-hero-card">
              <div class="slide-1-hero-tagline">
                为非确定性 AI 智能体构建确定性控制与安全治理系统
              </div>
              <div class="slide-1-hero-desc">
                全面掌握生产级 AI 编码智能体 Harness 治理工程体系：深入 Claude Code 记忆架构、AST 语法与秘钥防护、TDA 自愈测试闭环、MCP 协议扩展及复合多智能体协同架构。
              </div>
            </div>

            <div class="slide-1-instructor-card">
              <div class="slide-1-avatar-wrap">
                <img src="assets/images/ken-head-shot.png" alt="黄健 (Ken Huang)" class="slide-1-avatar-img" />
              </div>
              <div class="slide-1-instructor-info">
                <div class="slide-1-instructor-badge">
                  <span>🎓 课程主讲导师</span>
                </div>
                <div class="slide-1-instructor-name">黄健 (Ken Huang)</div>
                <div class="slide-1-instructor-titles">
                  <div class="slide-1-title-item">
                    <span class="title-icon">🏛️</span>
                    <span>旧金山大学兼职教授, <a href="https://www.usfca.edu/faculty/ken-huang" target="_blank" rel="noopener noreferrer" class="slide-1-org-link" title="查看黄健教授在旧金山大学的学者主页">旧金山大学 (USF) ↗</a></span>
                  </div>
                  <div class="slide-1-title-item">
                    <span class="title-icon">🚀</span>
                    <span>创始人兼 CEO, <a href="https://distributedapps.ai/" target="_blank" rel="noopener noreferrer" class="slide-1-org-link" title="访问 DistributedApps.ai">DistributedApps.ai ↗</a></span>
                  </div>
                </div>

                <div class="slide-1-social-links">
                  <div class="slide-1-social-pill">
                    <span class="social-icon">✍️</span>
                    <span class="social-label">专栏 Substack:</span>
                    <a href="https://kenhuangus.substack.com/" target="_blank" rel="noopener noreferrer" class="slide-1-social-link" title="阅读黄健教授的技术专栏">kenhuangus.substack.com <span class="ext-arrow">↗</span></a>
                  </div>
                  <div class="slide-1-social-pill">
                    <span class="social-icon">💼</span>
                    <span class="social-label">领英 LinkedIn:</span>
                    <a href="https://www.linkedin.com/in/kenhuang8/" target="_blank" rel="noopener noreferrer" class="slide-1-social-link" title="在 LinkedIn 建立连接">linkedin.com/in/kenhuang8 <span class="ext-arrow">↗</span></a>
                  </div>
                </div>
              </div>
            </div>

            <div class="slide-1-pillars-row">
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🛡️ 确定性控制治理</div>
                <div class="slide-1-pillar-desc">记忆分层、沙箱隔离与 AST 钩子</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🧪 测试驱动可靠性</div>
                <div class="slide-1-pillar-desc">Pytest 动态反馈与防回归闭环</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🤖 复合多智能体系统</div>
                <div class="slide-1-pillar-desc">规划、执行与审查工作树隔离</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">📜 五道生产就绪准入表</div>
                <div class="slide-1-pillar-desc">100% 可靠性与安全性工程审计</div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 2) {
        bodyHtml += `
          <div id="slide-content-wrap" class="instructor-slide-grid">
            <div class="instructor-info-col">
              ${svgMap[slide.number] || ''}
              ${restLines.length > 0 ? formatBullets(restLines) : ''}
            </div>
            <div class="author-books-card">
              <div class="author-books-header">
                <span>📚 AI 领域学术专著与出版物 (Springer · Cambridge · Wiley · Packt)</span>
                <a href="https://www.amazon.com/stores/author/B0D3J7L7GN" target="_blank" rel="noopener noreferrer">亚马逊作者主页 ➔</a>
              </div>
              <div class="books-gallery-grid">
                <a href="https://www.amazon.com/dp/3031900251" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Agentic AI: Theories and Practices (Springer)">
                  <img src="assets/images/books/springer_agentic_ai.jpg" alt="Agentic AI (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Agentic AI</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031448839" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Beyond AI: ChatGPT, Web3, and the Business Landscape of Tomorrow (Springer)">
                  <img src="assets/images/books/springer_beyond_ai.jpg" alt="Beyond AI (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Beyond AI</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031542517" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Generative AI Security: Theories and Practices (Springer)">
                  <img src="assets/images/books/springer_generative_ai_security.jpg" alt="GenAI Security (Springer)" class="book-cover-img" />
                  <div class="book-item-title">GenAI Security</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031901002" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Securing AI Agents: Foundations, Frameworks, and Real-World Deployment (Springer)">
                  <img src="assets/images/books/springer_securing_ai_agents.jpg" alt="Securing AI Agents (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Securing Agents</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/1009384467" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Web3: Blockchain, the New Economy, and the Self-Sovereign Internet (Cambridge University Press)">
                  <img src="assets/images/books/cambridge_web3.jpg" alt="Web3 (Cambridge UP)" class="book-cover-img" />
                  <div class="book-item-title">Web3 &amp; Economy</div>
                  <div class="book-publisher-tag">CAMBRIDGE</div>
                </a>
                <a href="https://www.amazon.com/dp/1394186524" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Blockchain and Web3: Building Foundations of the Metaverse (Wiley)">
                  <img src="assets/images/books/wiley_blockchain_web3.jpg" alt="Blockchain & Web3 (Wiley)" class="book-cover-img" />
                  <div class="book-item-title">Blockchain Web3</div>
                  <div class="book-publisher-tag">WILEY</div>
                </a>
                <a href="https://www.amazon.com/dp/B0HF3F86YM" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Harness Engineering: Design Patterns for Securing Long-Horizon Multi-Agent AI Systems (Packt / 亚马逊 #1 畅销榜)">
                  <img src="assets/images/books/harness_engineering.jpg" alt="Harness Engineering" class="book-cover-img" />
                  <div class="book-item-title">Harness Engineering</div>
                  <div class="book-publisher-tag">PACKT</div>
                </a>
                <a href="https://www.amazon.com/stores/author/B0D3J7L7GN" target="_blank" rel="noopener noreferrer" class="book-item-card" title="查看更多学术著作">
                  <div style="width:100%; height:100px; background:var(--accent-sf); border-radius:4px; display:flex; align-items:center; justify-content:center; font-size:1.5rem; color:var(--accent-dk); margin-bottom:0.30rem;">📚</div>
                  <div class="book-item-title">更多学术专著</div>
                  <div class="book-publisher-tag">AMAZON ➔</div>
                </a>
              </div>
            </div>
          </div>
        `;
      } else {
        bodyHtml += '<div id="slide-content-wrap" class="slide-content-wrapper">';
        if (svgMap[slide.number]) {
          bodyHtml += svgMap[slide.number];
        }
        if (restLines.length > 0) {
          bodyHtml += formatBullets(restLines);
        }
        bodyHtml += '</div>';
      }

      bodyEl.innerHTML = bodyHtml;

      const progressPct = ((idx + 1) / slidesData.length) * 100;
      document.getElementById('progress-fill').style.width = progressPct + '%';

      if (!isCode && slide.number !== 2) {
        requestAnimationFrame(() => {
          fitSlideText();
        });
      } else {
        bodyEl.style.setProperty('--fit-scale', '1');
      }
    }

    function fitSlideText() {
      const container = bodyEl;
      const content = container.querySelector('#slide-content-wrap') || container.querySelector('.slide-1-container') || container.firstElementChild;
      if (!content) return;

      container.style.setProperty('--fit-scale', '1');
      const maxH = container.clientHeight - 8;
      if (maxH <= 0) return;

      let low = 0.55;
      let high = 1.35;
      let best = 1.0;

      for (let i = 0; i < 14; i++) {
        const mid = (low + high) / 2;
        container.style.setProperty('--fit-scale', mid.toFixed(3));
        const contentH = content.scrollHeight;

        if (contentH <= maxH) {
          best = mid;
          low = mid;
        } else {
          high = mid;
        }
      }

      const optimalScale = Math.max(0.60, Math.min(best * 0.98, 1.25));
      container.style.setProperty('--fit-scale', optimalScale.toFixed(3));
    }

    let resizeTimer = null;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        const slide = slidesData[currentIdx];
        if (slide && slide.slide_type !== 'code' && slide.number !== 2) {
          fitSlideText();
        }
      }, 100);
    });

    function nextSlide() {
      if (currentIdx < slidesData.length - 1) {
        renderSlide(currentIdx + 1);
      }
    }

    function prevSlide() {
      if (currentIdx > 0) {
        renderSlide(currentIdx - 1);
      }
    }

    function goToSlide(idx) {
      renderSlide(parseInt(idx, 10));
    }

    function jumpToEnteredSlide() {
      const input = document.getElementById('goto-input');
      if (!input) return;
      const val = parseInt(input.value.trim(), 10);
      if (!isNaN(val) && val >= 1 && val <= slidesData.length) {
        goToSlide(val - 1);
        input.value = '';
      } else {
        alert(`请输入有效的幻灯片页码 (1-${slidesData.length})`);
      }
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.warn('Fullscreen error:', err);
        });
      } else {
        document.exitFullscreen();
      }
    }

    function toggleMode() {
      isGridMode = !isGridMode;
      const presMode = document.getElementById('presentation-mode');
      const gridMode = document.getElementById('grid-mode');
      const modeText = document.getElementById('mode-text');
      const modeIcon = document.getElementById('mode-icon');

      if (isGridMode) {
        presMode.style.display = 'none';
        gridMode.style.display = 'grid';
        modeText.innerText = '幻灯片视图';
        modeIcon.innerText = '🖥️';
        renderGrid();
      } else {
        gridMode.style.display = 'none';
        presMode.style.display = 'flex';
        modeText.innerText = '网格视图';
        modeIcon.innerText = '📜';
        renderSlide(currentIdx);
      }
    }

    function renderGrid() {
      const gridContainer = document.getElementById('grid-mode');
      gridContainer.innerHTML = '';

      slidesData.forEach((slide, idx) => {
        const card = document.createElement('div');
        card.className = 'grid-slide-card';
        card.onclick = () => {
          toggleMode();
          goToSlide(idx);
        };

        const title = document.createElement('div');
        title.className = 'grid-slide-title';
        title.innerText = `第 ${slide.number} 页: ${slide.raw_lines[0] || ''}`;

        const body = document.createElement('div');
        body.className = 'grid-slide-body';
        
        if (slide.slide_type === 'code') {
          body.innerHTML = `<code>${slide.code_filename || 'Python 代码'}</code><div style="margin-top:0.4rem; color:var(--ink);">${slide.raw_lines.slice(1).join('<br>')}</div>`;
        } else {
          body.innerText = slide.raw_lines.slice(1).join('\n');
        }

        card.appendChild(title);
        card.appendChild(body);
        gridContainer.appendChild(card);
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      } else if (e.key === 'g' || e.key === 'G') {
        toggleMode();
      } else if (e.key === 'h' || e.key === 'H') {
        window.location.href = 'index.html';
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(slidesData.length - 1);
      }
    });

    window.addEventListener('DOMContentLoaded', () => {
      let initialSlide = 0;
      if (window.location.hash) {
        const hashNum = parseInt(window.location.hash.replace('#', ''), 10);
        if (!isNaN(hashNum) && hashNum >= 1 && hashNum <= slidesData.length) {
          initialSlide = hashNum - 1;
        }
      }
      renderSlide(initialSlide);
    });
  </script>
</body>
</html>
'''

    root_dir = os.path.dirname(__file__)
    slides_path = os.path.join(root_dir, 'slides.html')
    docs_slides_path = os.path.join(root_dir, 'docs', 'slides.html')

    with open(slides_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    with open(docs_slides_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"SUCCESSFULLY GENERATED {len(slides)} CHINESE SLIDES WITH DYNAMIC TEXT SIZING!")

if __name__ == '__main__':
    build_slides_html()

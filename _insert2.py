#!/usr/bin/env python3
"""Read article content from text file, escape newlines, insert into article.html."""
import sys

NL_ESCAPE = chr(0x5c) + 'n'  # literal \n (two bytes)

# Read article content
with open('/tmp/blog/_article_content.txt', 'r', encoding='utf-8') as f:
    raw = f.read().strip()

# Replace actual newlines with literal \n
escaped = raw.replace('\n', NL_ESCAPE)

# Count
literal_count = escaped.count(NL_ESCAPE)
actual_nl = escaped.count('\n') - literal_count
print(f"Escaped: {len(escaped)} chars, {literal_count} literal \\n, {actual_nl} real newlines remaining")

# Read article.html
with open('/tmp/blog/article.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find insertion point: just before the closing "    };" of articles object + related posts
marker = "    };\n\n    // Related posts data"
idx = html.find(marker)
if idx == -1:
    marker = "    };\n    // Related posts data"
    idx = html.find(marker)

if idx == -1:
    print("ERROR: Could not find insertion marker")
    sys.exit(1)

# Build the new entry
entry = f"""\
      'hot-20260725-1': {{
        id: 'hot-20260725-1', title: 'Kronos深度解读：金融市场的第一个「大语言模型」——33K星，AAAI 2026最佳论文',
        category: 'AI', date: '2026-07-25', readTime: '16 min', icon: '📈',
        tags: ['Kronos', 'AI金融', '时序预测', 'K线数据', 'Transformer', '开源', '基础模型'],
        description: 'Kronos是首个专为金融K线数据设计的开源基础模型——45家交易所、120亿条记录训练、价格预测RankK提升93%、AAAI 2026论文。我用投资+AI双重视角拆解：专用分词器如何把K线变成「语言」、自回归Transformer如何搞定非平稳金融时序、以及这对量化投资的深远影响...',
        content: '{escaped}'
      }},

    }};"""

# Insert
new_html = html[:idx] + entry + html[idx + len("    };"):]

with open('/tmp/blog/article.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Inserted at position {idx}, new size: {len(new_html)} bytes")

# Verify
with open('/tmp/blog/article.html', 'r', encoding='utf-8') as f:
    verify = f.read()

if 'hot-20260725-1' in verify:
    print("OK: Article found!")
else:
    print("FAIL: Article not found!")

# Check for double backslash-n (bad)
double_nl = verify.count(chr(0x5c) + chr(0x5c) + 'n')
print(f"Double \\\\n count: {double_nl}")

# Show a snippet around the new article
start = verify.find('hot-20260725-1')
if start > 0:
    snippet = verify[start:start+300]
    print(f"Snippet: {snippet[:200]}")

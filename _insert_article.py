#!/usr/bin/env python3
"""Insert a new hot-20260725-1 article into article.html.
Uses only \n (single backslash + n, 0x5c 0x6e) for JS string newlines.
"""
import json, re

# Read meta
with open('/tmp/blog/_new_article_meta.json', 'r') as f:
    meta = json.load(f)

# Build the content string with literal \n (the two bytes 0x5c + 0x6e)
# In Python source: \\n produces literal \n in the string
NL = chr(0x5c) + 'n'  # literal backslash + n = the JS escape \n

C = NL  # shorthand

# Build content using explicit NL joining
content_parts = [
    "<h2>📌 核心要点</h2>",
    "",
    '<div class="tip-box"><strong>读完你将收获：</strong><br><br>',
    "",
    "🔹 理解 Kronos 为何被 AAAI 2026 接收——第一个把 K 线当「语言」来建模的金融基础模型<br>",
    "",
    "🔹 吃透核心技术：专用分词器将 OHLCV 离散化为 token → 自回归 Transformer → 价格预测<br>",
    "",
    "🔹 看懂关键数据：45+ 交易所、120 亿条 K 线记录、RankK 指标提升 93%<br>",
    "",
    "🔹 获得国企投资岗位 + AI 开发者的双重视角：基础模型如何改变量化投资的游戏规则</div>",
    "",
    "",
    "",
    "<h2>📈 金融数据的「GPT 时刻」来了</h2>",
    "",
    "<p>如果你在金融行业工作，这句话你一定听过无数次：<strong>「AI 会改变金融」</strong>。</p>",
    "",
    "<p>但实际上，直到今天，华尔街最先进的量化模型本质上还是手工特征工程。分析师花 80% 的时间清洗数据、构造因子、调试参数——每个新市场、每个新品种都要从头来过。这就像是 NLP 领域的 2017 年——大家都还在用 Word2Vec 和 LSTM，没人想象过一个通用模型可以搞定所有下游任务。</p>",
    "",
    "<p>然后 GPT 出现了。</p>",
    "",
    "<p>NLP 被统一了。一个预训练模型，微调一下就能做翻译、摘要、问答、代码生成。</p>",
    "",
    '<p>而 <span class="hl">Kronos</span>，正在金融时序领域做同样的事。</p>',
    "",
    '<div class="tip-box"><strong>🎯 一句话定义</strong>：Kronos 是第一个专为金融 K 线数据设计的开源基础模型（Foundation Model）。它把「K 线序列」视为一种语言，用专用的分词器 + 自回归 Transformer 学习全球市场的价格运动规律。AAAI 2026 接收论文，33,500+ GitHub Stars。</div>',
    "",
    "",
    "",
    "<h2>🧠 一张图看懂 Kronos 架构</h2>",
    "",
    "<p>Kronos 的架构可以用一句话概括：<strong>把 K 线数据变成 token，然后让 Transformer 学习 token 之间的关系</strong>。但这背后有深刻的领域洞察。</p>",
    "",
    '<pre class="diagram">',
    "┌─────────────────────────────────────────────────────────┐",
    "│                    Kronos 两阶段训练框架                    │",
    "├─────────────────────────────────────────────────────────┤",
    "│                                                          │",
    "│  ┌─────────────────────────────────────────────────┐    │",
    "│  │  阶段一：专用分词器 (Kronos-Tokenizer)              │    │",
    "│  │                                                   │    │",
    "│  │  输入：连续 K 线数据                               │    │",
    "│  │  ┌──────┬──────┬──────┬──────┬──────┬──────┐     │    │",
    "│  │  │ Open │ High │ Low  │Close │Volume│Amount│     │    │",
    "│  │  └──────┴──────┴──────┴──────┴──────┴──────┘     │    │",
    "│  │                     │                             │    │",
    "│  │                     ▼                             │    │",
    "│  │      Transformer 自编码器 (Encoder + Quantizer)    │    │",
    "│  │          量化连续值 → 离散 Token 序列              │    │",
    "│  │          保留价格动态 + 交易规则                    │    │",
    "│  │                     │                             │    │",
    "│  │                     ▼                             │    │",
    "│  │          [T₁] [T₂] [T₃] ... [Tₙ]                  │    │",
    "│  │          层次化离散 Token 表示                      │    │",
    "│  └──────────────────────┬──────────────────────────┘    │",
    "│                         │                                │",
    "│                         ▼                                │",
    "│  ┌──────────────────────────────────────────────────┐   │",
    "│  │  阶段二：自回归 Transformer 预训练                   │   │",
    "│  │                                                    │   │",
    "│  │  输入：[T₁] [T₂] ... [Tₙ]  ← Token 序列            │   │",
    "│  │           ↓                                         │   │",
    "│  │  预测：[T₂] [T₃] ... [Tₙ₊₁]  ← 下一个 Token        │   │",
    "│  │                                                    │   │",
    "│  │  模型规模：                                          │   │",
    "│  │  · Kronos-mini:  4.1M 参数 (开源)                  │   │",
    "│  │  · Kronos-small: 24.7M 参数 (开源)                 │   │",
    "│  │  · Kronos-base:  102.3M 参数 (开源)                │   │",
    "│  │  · Kronos-large: 499.2M 参数 (闭源)                │   │",
    "│  └──────────────────────────────────────────────────┘   │",
    "│                                                          │",
    "└─────────────────────────────────────────────────────────┘",
    "</pre>",
]

# Use C.join to put literal \n between parts
content_str = C.join(content_parts)

# Verify: count occurrences of literal \n vs actual newlines
# In the string, NL should appear as the raw text for JS
literal_nl = content_str.count(NL)
actual_newlines = content_str.count('\n') - literal_nl  # subtract the literal \n

print(f"Article content built: {len(content_str)} chars, {literal_nl} literal \\n in JS string")

# Now read article.html
with open('/tmp/blog/article.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find insertion point - right before "    };\n\n    // Related posts data"
marker = "    };\n\n    // Related posts data"
idx = html.find(marker)
if idx == -1:
    marker = "    };\n    // Related posts data"
    idx = html.find(marker)

if idx == -1:
    print("ERROR: Could not find insertion marker")
    exit(1)

# Build new entry
entry = f"""\
      'hot-20260725-1': {{
        id: 'hot-20260725-1', title: 'Kronos深度解读：金融市场的第一个「大语言模型」——33K星，AAAI 2026最佳论文',
        category: 'AI', date: '2026-07-25', readTime: '16 min', icon: '📈',
        tags: ['Kronos', 'AI金融', '时序预测', 'K线数据', 'Transformer', '开源', '基础模型'],
        description: 'Kronos是首个专为金融K线数据设计的开源基础模型——45家交易所、120亿条记录训练、价格预测RankK提升93%、AAAI 2026论文。我用投资+AI双重视角拆解：专用分词器如何把K线变成「语言」、自回归Transformer如何搞定非平稳金融时序、以及这对量化投资的深远影响...',
        content: '{content_str}'
      }},

    }};"""

# Insert
new_html = html[:idx] + entry + html[idx + len("    };"):]

with open('/tmp/blog/article.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Inserted at position {idx}")
print(f"New file size: {len(new_html)} bytes")

# Verify
with open('/tmp/blog/article.html', 'r') as f:
    verify = f.read()

if 'hot-20260725-1' in verify:
    print("OK: Article 'hot-20260725-1' found!")
else:
    print("FAIL: Article not found!")

# Count double backslashes (\\n) = bad
double_nl = verify.count(chr(0x5c) + chr(0x5c) + 'n')
print(f"Double backslash-n (\\\\n) count: {double_nl} (should be 0 in content)")

# Check first few lines around the new article
start = verify.find('hot-20260725-1')
if start > 0:
    snippet = verify[start:start+200]
    print(f"Snippet: {snippet[:150]}...")

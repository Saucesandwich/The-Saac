"""
Script to apply macro catalog and automated news enhancements to build_terminal.py
"""

def update_build_terminal():
    with open('build_terminal.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update imports
    old_header = """import json
import datasets_json

# Prepare JSON data strings"""
    new_header = """import json
import datasets_json
from scripts.terminal_components import MACRO_NAV_CSS, MACRO_NAV_HTML, NEWS_CONTAINER_HTML, NEWS_SERVICE_JS, MACRO_NAV_JS

# Prepare JSON data strings"""

    if "from scripts.terminal_components" not in content:
        assert old_header in content, "old_header not found"
        content = content.replace(old_header, new_header)

    # Also load js_instruments
    old_load = """json_10m = json.dumps(datasets_json.RAW_10M, indent=2)

html_content = f'''<!DOCTYPE html>"""
    new_load = """json_10m = json.dumps(datasets_json.RAW_10M, indent=2)

with open('scripts/generated_instruments.js', encoding='utf-8') as f:
    js_instruments = f.read()

html_content = f'''<!DOCTYPE html>"""
    if "js_instruments = f.read()" not in content:
        assert old_load in content, "old_load not found"
        content = content.replace(old_load, new_load)

    # 2. Add MACRO_NAV_CSS before </style>
    old_style_end = """    footer {{ text-align: center; color: var(--text-dim); font-size: 0.74rem; font-family: var(--font-mono); padding: 16px 0; border-top: 1px solid var(--border-color); text-transform: uppercase; letter-spacing: 0.03em; }}
  </style>"""
    new_style_end = """    footer {{ text-align: center; color: var(--text-dim); font-size: 0.74rem; font-family: var(--font-mono); padding: 16px 0; border-top: 1px solid var(--border-color); text-transform: uppercase; letter-spacing: 0.03em; }}

{MACRO_NAV_CSS}
  </style>"""
    if "{MACRO_NAV_CSS}" not in content:
        assert old_style_end in content, "old_style_end not found"
        content = content.replace(old_style_end, new_style_end)

    # 3. Add MACRO_NAV_HTML after </header>
    old_header_end = """      </div>
    </div>
  </header>

  <!-- Real-World Market Cards -->"""
    new_header_end = """      </div>
    </div>
  </header>

{MACRO_NAV_HTML}

  <!-- Real-World Market Cards -->"""
    if "{MACRO_NAV_HTML}" not in content:
        assert old_header_end in content, "old_header_end not found"
        content = content.replace(old_header_end, new_header_end)

    # 4. Add NEWS_CONTAINER_HTML before <footer>
    old_footer = """    </div>
  </div>

  <footer>"""
    new_footer = """    </div>
  </div>

{NEWS_CONTAINER_HTML}

  <footer>"""
    if "{NEWS_CONTAINER_HTML}" not in content:
        assert old_footer in content, "old_footer not found"
        content = content.replace(old_footer, new_footer)

    # 5. Replace INSTRUMENTS definition with js_instruments + NEWS_SERVICE_JS + MACRO_NAV_JS
    instruments_start = "  // Universal Multi-Asset Registry & Instruments\n  const INSTRUMENTS = {{"
    instruments_end = "  }};\n\n  let currentInstrument = INSTRUMENTS.gold;"
    
    idx_start = content.find(instruments_start)
    assert idx_start != -1, "instruments_start not found"
    idx_end = content.find(instruments_end, idx_start)
    assert idx_end != -1, "instruments_end not found"
    
    # We replace from idx_start to idx_end + len("  }};")
    replacement = """{js_instruments}

{NEWS_SERVICE_JS}

{MACRO_NAV_JS}"""
    content = content[:idx_start] + replacement + content[idx_end + len("  }};"):]

    # 6. Update switchInstrument to invoke newsService.renderNewsSection
    old_switch_end = """      activeData = getSeriesForTimeframe(currentTimeframe, currentSamplingRate);
      updateHistChartData();
      updatePeriodSummaryBar();
    }}
  }}"""
    new_switch_end = """      activeData = getSeriesForTimeframe(currentTimeframe, currentSamplingRate);
      updateHistChartData();
      updatePeriodSummaryBar();
    }}

    // Auto-update bottom news headlines & market catalysts
    const newsContainer = document.getElementById('marketNewsContainer');
    if (newsContainer && window.newsService) {{
      window.newsService.renderNewsSection(newsContainer, inst);
    }}
  }}"""
    if "window.newsService.renderNewsSection" not in content:
        assert old_switch_end in content, "old_switch_end not found"
        content = content.replace(old_switch_end, new_switch_end)

    # 7. Update DOMContentLoaded
    old_dom_loaded = """  window.addEventListener('DOMContentLoaded', () => {{
    initLiveChart();
    refreshLiveData();
    updatePeriodSummaryBar();
  }});"""
    new_dom_loaded = """  window.addEventListener('DOMContentLoaded', () => {{
    initLiveChart();
    refreshLiveData();
    updatePeriodSummaryBar();
    if (typeof renderTickerPills === 'function') renderTickerPills('all');
    const newsContainer = document.getElementById('marketNewsContainer');
    if (newsContainer && window.newsService) {{
      window.newsService.renderNewsSection(newsContainer, currentInstrument);
    }}
  }});

  if (document.readyState === 'complete' || document.readyState === 'interactive') {{
    if (typeof renderTickerPills === 'function') renderTickerPills('all');
    const newsContainer = document.getElementById('marketNewsContainer');
    if (newsContainer && window.newsService && (!newsContainer.children || newsContainer.children.length === 0)) {{
      window.newsService.renderNewsSection(newsContainer, currentInstrument);
    }}
  }}"""
    if "renderTickerPills('all')" not in content:
        assert old_dom_loaded in content, "old_dom_loaded not found"
        content = content.replace(old_dom_loaded, new_dom_loaded)

    with open('build_terminal.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully updated build_terminal.py!")

if __name__ == '__main__':
    update_build_terminal()

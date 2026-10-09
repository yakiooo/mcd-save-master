#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_skill.py — 校验 SKILL.md 中引用的 mcd-mcp 工具名是否都在官方工具清单内。

麦当劳官方 MCP 工具清单（来自 https://github.com/M-China/mcd-mcp-server，版本 1.0.9）：
"""
import os
import re
import sys

# ---- 官方工具清单（与 mcd-mcp-server README 一致）----
OFFICIAL_TOOLS = {
    "list-nutrition-foods", "delivery-query-addresses", "delivery-create-address",
    "delivery-query-stores", "query-meal-assistance", "query-nearby-stores",
    "query-store-coupons", "query-meals", "query-meal-detail", "calculate-price",
    "create-order", "cancel-order", "query-order", "order-list", "campaign-calendar",
    "available-coupons", "auto-bind-coupons", "query-my-coupons", "query-my-account",
    "mall-points-products", "mall-product-detail", "mall-create-order", "now-time-info",
    "query-lottery-info", "draw-lottery", "query-my-prizes", "mall-order-list",
    "mall-order-detail", "query-party-city", "query-party-store",
    "query-partystore-date", "query-partystore-session", "party-order-create",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_PATH = os.path.join(ROOT, "SKILL.md")

# 形如 xxx-xxx 但不是工具名的已知标识符（如 MCP 连接器名），不参与工具合法性校验
KNOWN_NON_TOOLS = {"mcd-mcp"}


def extract_tools(text: str):
    """匹配反引号包裹的、形如 xxx-xxx 的工具名。"""
    return sorted(set(re.findall(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`", text)))


def main():
    if not os.path.exists(SKILL_PATH):
        print(f"[FAIL] 找不到 SKILL.md: {SKILL_PATH}")
        return 1

    with open(SKILL_PATH, encoding="utf-8") as f:
        content = f.read()

    referenced = [t for t in extract_tools(content) if t not in KNOWN_NON_TOOLS]
    if not referenced:
        print("[WARN] SKILL.md 中未检测到任何 `tool-name` 形式的引用。")
        return 0

    unknown = [t for t in referenced if t not in OFFICIAL_TOOLS]
    used = [t for t in referenced if t in OFFICIAL_TOOLS]

    print(f"检测到引用工具 {len(referenced)} 个，其中合法 {len(used)} 个。")
    for t in used:
        print(f"  [OK]   {t}")
    for t in unknown:
        print(f"  [??]   {t}  (不在官方清单，请核实是否为笔误或新版本工具)")

    if unknown:
        print(f"\n[FAIL] 存在 {len(unknown)} 个未识别工具名，请修正后再提交。")
        return 1

    print("\n[PASS] SKILL.md 引用的 mcd-mcp 工具全部合法。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

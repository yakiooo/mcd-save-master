---
name: mcd-save-master
description: 麦门省钱助手——基于麦当劳中国官方 MCP，自动查券、一键领券、比价并算出最省点餐组合。当用户说「怎么点麦当劳最划算 / 有哪些优惠券 / 帮我领券 / 算算这单多少钱 / 省钱点麦当劳 / 哪家店券多」时使用。
version: 1.0.0
author: 杨琦
license: MIT
---

# 麦门省钱助手（McDonald's Savings Assistant）

一个面向「点麦当劳想省钱」场景的 WorkBuddy Skill。它把麦当劳中国官方 MCP（`mcp.mcd.cn`）的
查询/领券/计价能力串成一套可复用的省钱工作流：**先拉券 → 再选品 → 算最省组合 → 输出省钱报告 → 可选下单**。

> 本 Skill 不自己实现任何网络请求，全部能力来自已连接的 `mcd-mcp` MCP Server。
> 所有餐品、价格、券状态均以 MCP 实时返回为准。

## 何时使用

- 用户想「省钱点麦当劳」「怎么点最划算」「有什么优惠券」
- 用户要「帮我领券」「查我有哪些券」「算算这单多少钱」
- 用户问「哪家店券多 / 附近哪家麦当劳划算」

## 前置条件

1. WorkBuddy 已连接 `mcd-mcp` 连接器（Streamable HTTP，`https://mcp.mcd.cn`，
   请求头 `Authorization: Bearer <MCP Token>`，Token 来自 `https://open.mcd.cn/mcp`）。
2. 若涉及下单/领券，需在用户已登录麦当劳账号的 Token 下进行，且先确认用户授权。

## 核心工作流

按顺序执行，每一步都基于上一步的真实返回；不要编造价格或券。

### Step 1 · 锁定场景与门店
- 问清用户：**到店自取 / 麦乐送外送 / 团餐**。
- 外送：先 `delivery-query-addresses` 列出已存地址；无地址则 `delivery-create-address` 引导新增；再用 `delivery-query-stores` 查附近可配送门店。
- 到店：`query-nearby-stores` 查附近门店。
- 记住选中的 `storeId`，后续查券/计价都用它。

### Step 2 · 拉满可用券
- `available-coupons`：查当前可领的「麦麦省」券列表。
- 征得用户同意后 `auto-bind-coupons`：**一键领走所有可领券**（节省逐步领的繁琐）。
- `query-my-coupons`：查账户里**已拥有**的券（含刚领的 + 历史存的）。
- `query-store-coupons`：用 Step1 的 `storeId` 查**该门店当前可用**的券（门店券常与账号券不同）。
- 汇总成「可用券池」，标注每张券的适用品类/门槛/有效期。

### Step 3 · 选品 + 看营养（按需）
- `query-meals`：按 `storeId` 拉当前在售菜单（分类、餐品编码、标签如「超值」「买一送一」）。
- `query-meal-detail`：对候选餐品查套餐组成、可替换项、特制项。
- 用户关注热量/蛋白时，`list-nutrition-foods` 给营养成分，辅助「好吃又不胖」的取舍。

### Step 4 · 算最省组合（核心省钱逻辑）
针对用户想买的清单，做**多方案比价**：
1. 方案 A：什么都不用券的原价（`calculate-price`，不带券）。
2. 方案 B：用账号券（`calculate-price`，传入 `query-my-coupons` 得到的券）。
3. 方案 C：用门店券（`calculate-price`，传入 `query-store-coupons` 得到的券）。
4. 若清单可拆单（如两张「满减券」各自凑单更省），给出拆单建议。
- `calculate-price` 会返回商品金额、配送费、优惠金额、应付总价——**以它为准**输出对比。
- 选省得最多的方案，并说明「为什么这单最省」（哪张券触发、门槛是否踩中）。

### Step 5 · 输出省钱报告
用清晰的分点/表格给出：
- 原价 vs 最优价、**省了多少、省在哪张券**；
- 本次没用上但「下次可凑单」的券（避免浪费）；
- 若 `campaign-calendar` 显示近期有大促，提示「可等 X 活动更划算」。

### Step 6 ·（可选）下单
- 用户确认后 `create-order` 用最优券组合下单，返回支付链接；
- 下单后 `query-order` 核对；如需取消 `cancel-order`。
- **默认不自动下单**，必须用户明确说「下单 / 帮我买」才走这一步。

## 工具映射表（均来自 mcd-mcp）

| 阶段 | MCP Tool | 用途 |
|---|---|---|
| 门店 | `query-nearby-stores` | 查附近门店 |
| 门店 | `delivery-query-addresses` / `delivery-create-address` / `delivery-query-stores` | 外送地址与门店 |
| 拉券 | `available-coupons` | 可领券列表 |
| 拉券 | `auto-bind-coupons` | 一键领券 |
| 拉券 | `query-my-coupons` | 我的券 |
| 拉券 | `query-store-coupons` | 门店可用券 |
| 选品 | `query-meals` / `query-meal-detail` | 菜单与详情 |
| 选品 | `list-nutrition-foods` | 营养热量 |
| 计价 | `calculate-price` | 多方案比价（核心） |
| 活动 | `campaign-calendar` | 近期大促提醒 |
| 下单 | `create-order` / `query-order` / `cancel-order` | 下单与核对 |
| 账户 | `query-my-account` | 积分（联动商城/抽奖时参考） |

## 输出示例（省钱报告）

```
🍔 麦门省钱报告
· 你想买：巨无霸套餐 ×1 + 麦辣鸡腿堡 ×1
· 原价：¥52.0
· 最优方案（用「满50减12」门店券 + 「麦辣买一送一」账号券）：
  应付 ¥33.0，省 ¥19.0（省 36.5%）
· 没用上但别浪费：「周二会员日券」下周二可用，建议那时再点
· 近期活动：10/15 有「半价分享盒」，囤货可等那天
```

## 合规与边界

- **绝不**在 Skill 或输出里写入/回显真实 Token、密钥、账号。
- 价格/券以 MCP 实时结果为准，输出明确标注「以官方实时为准」。
- 领券、下单属于敏感操作，**必须用户显式授权**才调用 `auto-bind-coupons` / `create-order`。
- 输出不构成营养/医疗建议；热量仅作参考。
- 非麦当劳官方产品，仅为创意开发大赛作品。

## 反模式（不要做）

- ❌ 编造价格或券面额——一切来自 `calculate-price` / `query-my-coupons` 的真实返回。
- ❌ 未经确认就 `auto-bind-coupons` / `create-order`。
- ❌ 把 Token 写进任何日志或回复。
- ❌ 忽略 `storeId` 一致性（用 A 店的券去算 B 店的单）。

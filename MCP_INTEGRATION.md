# 麦当劳 MCP 接入说明（MCP_INTEGRATION）

本项目**真实使用**麦当劳中国官方 MCP Server 提供的能力，所有查询、领券、计价、下单均通过该 MCP 完成。

## 1. 接入的 MCP Server

| 项 | 值 |
|---|---|
| 提供方 | 麦当劳中国（M-China，官方 GitHub 组织已验证） |
| Server 地址 | `https://mcp.mcd.cn` |
| 传输协议 | Streamable HTTP |
| 鉴权 | 请求头 `Authorization: Bearer <MCP Token>` |
| Token 获取 | <https://open.mcd.cn/mcp> 登录后「控制台 → 激活」复制 |
| 限流 | 每 Token 600 次/分钟（超了返回 429，需降频） |
| 官方指南 | <https://github.com/M-China/mcd-mcp-server> |

> Token **不入库、不写日志、不回显**；本仓库仅以环境变量占位符 `${MCD_MCP_TOKEN}` 出现（见 `mcp-config.example.json`）。

## 2. 实际使用的工具（Tool）

本 Skill 串联以下 `mcd-mcp` 工具（名称与官方一致）：

| Tool | 用途 | 在流程中的阶段 |
|---|---|---|
| `query-nearby-stores` | 查附近门店 | 门店定位 |
| `delivery-query-addresses` | 查已存配送地址 | 外送准备 |
| `delivery-create-address` | 新增配送地址 | 外送准备 |
| `delivery-query-stores` | 查可配送门店 | 外送准备 |
| `available-coupons` | 查可领「麦麦省」券 | 拉券 |
| `auto-bind-coupons` | 一键领走所有可领券 | 拉券（核心） |
| `query-my-coupons` | 查账户已有券 | 拉券 |
| `query-store-coupons` | 查指定门店可用券 | 拉券 |
| `query-meals` | 查在售菜单（分类/编码/标签） | 选品 |
| `query-meal-detail` | 查套餐组成/可替换项 | 选品 |
| `list-nutrition-foods` | 查营养热量 | 选品（健康参考） |
| `calculate-price` | 多方案计价（商品+券） | 比价（核心） |
| `campaign-calendar` | 查当月营销活动 | 大促提醒 |
| `create-order` | 创建订单并返回支付链接 | 下单（授权后） |
| `query-order` | 查订单详情 | 下单核对 |
| `cancel-order` | 取消订单 | 下单后 |
| `query-my-account` | 查积分（联动商城/抽奖参考） | 账户 |

> 以上为省钱主链路使用的工具；MCP 还提供团餐、派对预约、积分商城、抽奖等能力，本项目按场景可扩展调用。

## 3. 调用流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant A as WorkBuddy(AI)
    participant M as mcd-mcp
    U->>A: 怎么点麦当劳最划算？
    A->>M: query-nearby-stores / delivery-query-stores
    M-->>A: 门店列表 + storeId
    A->>M: available-coupons
    M-->>A: 可领券列表
    A->>M: auto-bind-coupons (授权后)
    M-->>A: 已领券
    A->>M: query-my-coupons + query-store-coupons
    M-->>A: 可用券池
    A->>M: query-meals / query-meal-detail
    M-->>A: 菜单与详情
    A->>M: calculate-price (多方案: 原价/账号券/门店券)
    M-->>A: 各方案金额/优惠/应付
    A-->>U: 省钱报告（最优方案 + 省多少 + 建议）
    U->>A: 帮我下单
    A->>M: create-order
    M-->>A: 支付链接
```

## 4. 业务价值

- **把零散优惠用满**：用户通常不知道自己有哪些券、哪家店券多。Skill 一次性拉满并汇总，避免「券过期才发现有」。
- **决策辅助**：用 `calculate-price` 真实比价，而非凭感觉，给出「为什么这单最省」的可解释结论。
- **降门槛**：自然语言即可完成「查券→领券→比价→下单」全链路，不需要用户逐屏翻 App。
- **可扩展**：同一套 MCP 连接可延伸到团餐凑单、派对预约、积分抽奖等场景，Skill 是统一入口。

## 5. 合规

- 严格遵循《麦当劳 MCP 服务规则》：非商业用途、Token 妥善保管、不超频。
- 领券/下单属敏感操作，Skill 内强制「用户显式授权」才调用，不做静默操作。
- 项目非麦当劳官方产品，输出以官方实时结果为准。

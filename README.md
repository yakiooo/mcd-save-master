# 麦门省钱助手（mcd-save-master）

> 基于 **麦当劳中国官方 MCP** 的省钱点餐 Skill · 麦当劳程序员节创意开发大赛参赛作品

<p align="center">
<b>查券 → 一键领券 → 比价 → 算出最省组合 → 省钱报告 → 可选下单</b>
</p>

一个面向「点麦当劳想省钱」场景的 [WorkBuddy](https://www.workbuddy.cn) Skill。它把麦当劳中国
MCP（`mcp.mcd.cn`）的查询 / 领券 / 计价能力，串成一套可复用的省钱工作流——你只管说「怎么点最划算」，
AI 自动拉券、比价、告诉你这单能省多少。

---

## ✨ 特性

- 🎟️ **拉满券**：查可领券 + 一键领走 + 查我的券 + 查门店券，汇总成「可用券池」
- 🧮 **多方案比价**：原价 / 用账号券 / 用门店券 / 拆单，四方案用 `calculate-price` 真实算出最优解
- 🍔 **选品辅助**：菜单、套餐组成、营养热量一键查，帮你「好吃又不贵」
- 📅 **大促提醒**：结合 `campaign-calendar` 提示「等 X 活动更划算」，别浪费券
- 🔒 **安全合规**：Token 走环境变量占位，敏感操作（领券/下单）需你显式授权

## 🎯 目标用户

- 经常点麦当劳、想少花钱的学生 / 上班族
- 团餐订餐负责人（帮部门凑最省方案）
- 任何想「用自然语言就能把优惠用满」的麦门信徒

---

## 📦 安装与使用

### 方式一：在 WorkBuddy 中加载（推荐，参与专项奖励）

1. 获取麦当劳 MCP Token：打开 <https://open.mcd.cn/mcp> → 登录（手机号验证）→ 控制台 → 激活 → 复制 Token。
2. 在 WorkBuddy 左侧【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】，填入：

   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": { "Authorization": "Bearer 你的MCP_Token" }
       }
     }
   }
   ```

   保存并**启用** `mcd-mcp`（首次需点「信任」）。
3. 将本仓库的 `SKILL.md`（连同 `references/`）放到 WorkBuddy 的技能目录：
   - 用户级：`~/.workbuddy/skills/mcd-save-master/`
   - 或项目级：`<你的工作区>/.workbuddy/skills/mcd-save-master/`
4. 在对话框直接说，例如：

   > 「帮我在成都春熙路附近点麦当劳，怎么最划算，我想吃巨无霸和麦辣鸡腿堡」

   AI 会按 `SKILL.md` 的流程自动调用 `mcd-mcp` 工具完成查券、比价并给出省钱报告。

### 方式二：直接用 MCP Client

不装 Skill 也能用——只要你的 MCP Client（WorkBuddy / Cherry Studio / Cursor / Trae 等）连上
`mcd-mcp`，把上面的自然语言需求发给 AI 即可。本 Skill 的价值在于**把零散工具固化成可复用的省钱流程**。

---

## 💬 使用示例

**用户**：帮我领一下麦当劳的券，看看今天点巨无霸套餐怎么最省

**助手（按 Skill 流程）**：
1. `available-coupons` → 列出 6 张可领券
2. `auto-bind-coupons`（已授权）→ 领走全部
3. `query-my-coupons` + `query-store-coupons` → 汇总可用券池
4. `query-meals` → 拉菜单
5. `calculate-price` × 多方案比价 →

```
🍔 麦门省钱报告
· 巨无霸套餐 ×1
· 原价 ¥34.5
· 最优：用「满30减8」门店券 → 应付 ¥26.5，省 ¥8.0（23%）
· 没用上：「麦辣买一送一」需凑单，建议加购麦辣堡更省
```

---

## 📁 项目结构

```
mcd-save-master/
├── SKILL.md                  # ★ 核心：省钱工作流（WorkBuddy Skill 定义）
├── README.md                 # 本文件
├── CONTEST_DECLARATION.md    # 参赛声明（官方模板，内容不可改）
├── MCP_INTEGRATION.md        # 麦当劳 MCP 接入说明（Server/Tool/流程/价值）
├── mcp-config.example.json   # 脱敏 MCP 配置示例（仅环境变量占位）
├── workbuddy.md              # WorkBuddy 对话上下文（联动专项奖励）
├── references/
│   └── save-strategy.md      # 省钱策略详解（券类型/组合优化思路）
└── scripts/
    └── verify_skill.py       # 校验 SKILL.md 引用的 tool 名都在官方清单内
```

## 🔧 本地校验

```bash
python scripts/verify_skill.py
# 输出 SKILL.md 中引用的 mcd-mcp 工具是否全部合法
```

## ⚠️ 免责声明

本项目为创意开发大赛作品，**非麦当劳官方产品**。所有餐品、价格、券状态以麦当劳官方渠道实时结果为准；
输出不构成营养/医疗建议。详见 `CONTEST_DECLARATION.md`。

## 📄 许可证

MIT · © 2026 杨琦

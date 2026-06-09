# 系統架構設計文件 (System Architecture Design)

## 專案名稱：任務管理系統 (Task Management System)

---

## 1. 技術架構說明

本系統採用經典的 **MVC (Model-View-Controller)** 設計模式，透過後端渲染 (Server-Side Rendering, SSR) 的方式運作。

### 選用技術與原因

*   **後端框架：Python Flask**
    *   **原因**：Flask 是一個輕量且高彈性的 Micro-framework，沒有過多強制的約束，非常適合小型專案快速開發，並且對於初學者理解 Web 運作原理非常有幫助。
*   **前端模板：Jinja2 模板引擎**
    *   **原因**：Jinja2 是 Flask 內建的模板引擎，讓開發者可以直接在 HTML 中編寫邏輯（如迴圈、條件判斷等）來渲染動態資料。不需建置複雜的前端打包工具 (如 Webpack, Vite)，省去前後端分離的 API 對接成本。
*   **資料庫：SQLite**
    *   **原因**：SQLite 是一個無伺服器 (Serverless) 的輕量級關聯式資料庫，資料庫就是一個單一檔案，不需安裝額外的資料庫服務（如 MySQL, PostgreSQL），非常適合本機開發與小型個人應用。
*   **資料庫連接：Flask-SQLAlchemy (ORM)**
    *   **原因**：透過 ORM (Object-Relational Mapping)，我們可以使用 Python 類別 (Class) 來定義資料表，並用物件導向的語法操作資料，避免撰寫繁瑣且容易出錯的原生 SQL 指令，同時自動防範 SQL 注入攻擊。
*   **前端樣式：原生 CSS (Vanilla CSS)**
    *   **原因**：本系統注重「精緻、現代且流暢」的視覺效果。使用原生 CSS 能讓我們擁有 100% 的設計掌控權，不需引入額外龐大的 CSS 框架即可刻劃出具備漸層、微動畫與玻璃磨砂 (Glassmorphic) 質感的進階 UI。

### Flask MVC 模式說明

在我們的專案中，MVC 職責劃分如下：

```
                    ┌─────────────────────────┐
                    │      瀏覽器 (Client)    │
                    └────────────┬────────────┘
                        ▲        │ HTTP 請求
               HTML 渲染│        ▼
                    ┌───┴────────┴────────────┐
             View   │      Jinja2 模板        │
          (Templates)└────────────────────────┘
                        ▲
                        │ 資料渲染
                    ┌───┴─────────────────────┐
          Controller│   Flask 路由 (Routes)   │
           (Routes) └────────────┬────────────┘
                        ▲        │
               查詢/更新│        ▼ 讀寫/操作
                    ┌───┴────────┴────────────┐
             Model  │    SQLAlchemy 模型      │
          (Database)└────────────┬────────────┘
                        ▲        │
               資料持久│        ▼ 存取實體
                    ┌───┴────────┴────────────┐
                    │    SQLite 資料庫檔案    │
                    └─────────────────────────┘
```

*   **Model (模型 — `app/models/`)**：
    負責定義資料表結構（如任務的欄位、資料型態），以及處理與資料庫的直接互動（CRUD）。
*   **View (視圖 — `app/templates/`)**：
    Jinja2 HTML 模板，負責將資料結構化呈現給使用者。當 Controller 傳入任務清單後，HTML 模板將之渲染為表格或列表。
*   **Controller (控制器 — `app/routes/`)**：
    Flask 路由處理器。負責接收使用者的 HTTP 請求 (GET, POST 等)，解析請求中的參數，呼叫 Model 取得或寫入資料，最後將資料交給相對應的 View 進行渲染，或執行重新導向 (Redirect)。

---

## 2. 專案資料夾結構

本專案結構經過精心設計，將職責分離，使得程式碼結構清晰、易於維護：

```text
web_app_development/
├── app/                       # 核心應用程式包 (Package)
│   ├── __init__.py            # 初始化應用程式、設定 Flask 與 SQLAlchemy
│   ├── models/                # 資料庫模型 (Model)
│   │   ├── __init__.py        # 匯出所有 Model
│   │   └── task.py            # 任務 (Task) 資料模型定義
│   ├── routes/                # 路由與控制器 (Controller)
│   │   ├── __init__.py        # 匯出所有 Blueprint 路由
│   │   └── task_routes.py     # 處理任務的新增、完成、刪除與篩選路由
│   ├── static/                # 靜態資源檔案
│   │   ├── css/
│   │   │   └── style.css      # 系統主要樣式表（含 RWD 與動畫效果）
│   │   └── js/
│   │       └── main.js        # 處理前端互動與非同步更新（可選）
│   └── templates/             # HTML 視圖模板 (View)
│       ├── base.html          # 共用基本配置模板（含導覽列、頁尾）
│       └── index.html         # 主頁面：任務清單、新增表單與篩選切換
├── docs/                      # 設計文件資料夾
│   ├── ARCHITECTURE.md        # 本系統架構設計文件
│   └── PRD.md                 # 產品需求文件
├── instance/                  # 執行實例資料夾 (Git 忽略，除初始化外)
│   └── database.db            # SQLite 資料庫實體檔案
├── .gitignore                 # Git 忽略檔案設定
├── app.py                     # 專案入口點檔案，啟動開發伺服器
├── README.md                  # 專案概覽說明
└── requirements.txt           # 專案相依 Python 套件清單
```

---

## 3. 元件關係圖

以下是使用者操作系統時，系統內部的元件互動流程：

### 流程 A：使用者請求顯示任務清單（含篩選）

```mermaid
sequenceDiagram
    actor User as 使用者/瀏覽器
    participant Route as Flask 路由 (task_routes.py)
    participant Model as Task Model (task.py)
    database DB as SQLite (database.db)
    participant Template as Jinja2 模板 (index.html)

    User->>Route: 發送 GET /?status=pending (附帶篩選參數)
    Route->>Model: 查詢狀態為 'pending' 的任務
    Model->>DB: 執行 SELECT * FROM tasks WHERE is_completed = 0
    DB-->>Model: 回傳任務資料集
    Model-->>Route: 回傳 Python 物件清單
    Route->>Template: 傳遞任務清單與當前篩選狀態
    Template->>Template: 依據資料渲染動態 HTML
    Template-->>User: 回傳完整 HTML 頁面
```

### 流程 B：使用者新增待辦任務

```mermaid
sequenceDiagram
    actor User as 使用者/瀏覽器
    participant Route as Flask 路由 (task_routes.py)
    participant Model as Task Model (task.py)
    database DB as SQLite (database.db)

    User->>Route: 發送 POST /add (攜帶任務標題)
    Route->>Route: 驗證欄位是否為空
    Route->>Model: 建立 Task 實例 (title="買牛奶", is_completed=False)
    Model->>DB: 執行 INSERT INTO tasks ...
    DB-->>Model: 確認寫入成功
    Route-->>User: 重導向 (Redirect) 至 GET / (重整頁面顯示新任務)
```

---

## 4. 關鍵設計決策

### 決策一：採用 Blueprint (藍圖) 進行路由模組化
*   **說明**：在 `app/routes/` 下，我們使用 Flask 的 Blueprint 機制來組織路由。
*   **優點**：這樣做可以避免把所有的路由程式碼都塞入單一的 `app.py` 中。未來如果需要新增「使用者管理」或「統計分析」等功能，只需在 `routes/` 下新增對應的 Blueprint 檔案，並在 `app/__init__.py` 中註冊即可，擴充性極佳。

### 決策二：以 URL 查詢參數 (?status=) 進行伺服器端篩選
*   **說明**：在實現「依完成狀態篩選」功能時，我們選擇透過 URL 參數（例如 `/?status=all`、`/?status=active`、`/?status=completed`）來觸發後端資料庫查詢，而非使用複雜的前端 JavaScript 篩選。
*   **優點**：
    1.  **符合 SSR 哲學**：每一次篩選都是一次乾淨的網頁請求，網址會隨著篩選狀態改變，使用者可以把特定狀態的頁面加入書籤或分享。
    2.  **效能佳**：只從資料庫撈取符合條件的資料，減少傳輸多餘資料的頻寬浪費。

### 決策三：使用 Flask-SQLAlchemy 進行 ORM 管理與自動化 Schema 建立
*   **說明**：使用 SQLAlchemy 設計 `Task` 模型，並在應用程式啟動時自動偵測資料庫，若不存在則自動初始化 Schema。
*   **優點**：
    1.  **無痛配置**：組員在 clone 專案後，直接啟動即可自動建立 SQLite 資料庫，不需手動匯入 SQL 腳本。
    2.  **安全防護**：ORM 對於變數插入進行自動轉義，天然防禦 SQL Injection，提升系統基本安全性。

### 決策四：採用響應式 Vanilla CSS 進行視覺風格包裝
*   **說明**：不使用 TailwindCSS 或 Bootstrap 等外部龐大 CSS 框架，改用精緻的原生 CSS Flexbox/Grid 進行排版，並搭配 CSS Variables 做色彩管理。
*   **優點**：
    1.  **高自由度**：能輕鬆設計圓角、磨砂玻璃效果、陰影以及按鈕 Hover 時的流暢過渡動畫，創造出讓人驚艷的現代感。
    2.  **無任何相依性**：專案極度乾淨，不需要載入額外的網頁 CDN，在網路受限的環境下也能迅速開啟。

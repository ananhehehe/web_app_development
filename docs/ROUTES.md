# 路由與頁面設計文件 (Route & Page Design)

## 專案名稱：任務管理系統 (Task Management System)

本文件規劃了系統的 URL 路由結構、HTTP 請求方法、資料流向以及對應的 HTML 模板，為前後端串接提供明確的規範。

---

## 1. 路由總覽表格

配合本專案採用 Flask + Jinja2 伺服器端渲染 (SSR) 且僅需單一主頁面的特性，路由規劃如下表所示。
由於原生 HTML 表單 (Form) 只支援 `GET` 與 `POST`，我們統一使用 `POST` 來處理狀態變更及刪除操作。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與任務列表** | `GET` | `/` | `app/templates/index.html` | 顯示所有或篩選後的任務列表，包含新增表單與篩選切換按鈕 |
| **新增任務** | `POST` | `/tasks/add` | *(無，重新導向)* | 接收表單提交的任務名稱，寫入資料庫後重導向回首頁 |
| **切換任務狀態** | `POST` | `/tasks/<int:id>/toggle` | *(無，重新導向)* | 將指定 ID 的任務狀態在已完成/未完成之間切換，完成後重導向回首頁 |
| **刪除任務** | `POST` | `/tasks/<int:id>/delete` | *(無，重新導向)* | 將指定 ID 的任務從資料庫中永久刪除，完成後重導向回首頁 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁與任務列表 (`GET /`)
*   **輸入**：
    *   Query String (URL 查詢參數): `status` (可選值: `all`, `pending`, `completed`。預設為 `all`)
*   **處理邏輯**：
    1.  讀取 `status` 參數。
    2.  呼叫 `Task.get_all(status)` 取得對應狀態的任務物件清單（最新建立的排在最前）。
    3.  將任務清單與當前 `status` 傳遞給 Jinja2 模板渲染。
*   **輸出**：
    *   渲染 [app/templates/index.html](file:///c:/Users/k0903/.gemini/web_app_development/app/templates/index.html) 頁面。
*   **錯誤處理**：
    *   若傳入非預期的 `status` 值，預設為 `all` 處理，避免出錯。

### 2.2 新增任務 (`POST /tasks/add`)
*   **輸入**：
    *   表單欄位 (Form Data): `title` (字串，必填，限制最多 100 字)
*   **處理邏輯**：
    1.  從 `request.form` 取得 `title` 並去除首尾空白 (`.strip()`)。
    2.  驗證 `title` 是否為空。
        *   **驗證失敗**：使用 Flask `flash()` 發送錯誤訊息：「任務名稱不可為空！」，並直接重導向回 `/`。
        *   **驗證成功**：呼叫 `Task.create(title=title)` 寫入資料庫。
*   **輸出**：
    *   `redirect(url_for('tasks.index'))` 重新導向至首頁。

### 2.3 切換任務完成狀態 (`POST /tasks/<int:id>/toggle`)
*   **輸入**：
    *   路徑參數 (Path Parameter): `id` (任務的唯一識別碼，整數)
*   **處理邏輯**：
    1.  呼叫 `Task.get_by_id(id)` 查詢任務。
    2.  若任務不存在，則拋出 404 錯誤或使用 `flash()` 提示。
    3.  呼叫 `task.update(is_completed=not task.is_completed)` 將任務的 `is_completed` 欄位取反。
*   **輸出**：
    *   `redirect(url_for('tasks.index'))` 重新導向至首頁。
*   **錯誤處理**：
    *   若任務不存在，呼叫 `abort(404)`。

### 2.4 刪除任務 (`POST /tasks/<int:id>/delete`)
*   **輸入**：
    *   路徑參數 (Path Parameter): `id` (任務的唯一識別碼，整數)
*   **處理邏輯**：
    1.  呼叫 `Task.get_by_id(id)` 查詢任務。
    2.  若任務不存在，則拋出 404 錯誤。
    3.  呼叫 `task.delete()` 將任務從資料庫中刪除並提交事務。
*   **輸出**：
    *   `redirect(url_for('tasks.index'))` 重新導向至首頁。
*   **錯誤處理**：
    *   若任務不存在，呼叫 `abort(404)`。

---

## 3. Jinja2 模板清單

專案採用模板繼承機制，主要包含以下二個 HTML 檔案：

1.  **`app/templates/base.html` (基本配置模板)**
    *   **用途**：定義所有頁面的共用骨架（如 `<!DOCTYPE html>`、`head` 設定、樣式表連結、導覽列、頁尾與 Flash 訊息區塊）。
    *   **預留 Block**：
        *   `{% block title %}{% endblock %}`
        *   `{% block content %}{% endblock %}`
2.  **`app/templates/index.html` (主頁面模板 — 繼承 `base.html`)**
    *   **用途**：
        *   繼承 `base.html`，並填入 `content` 區塊。
        *   包含任務新增表單（`<form action="/tasks/add" method="POST">`）。
        *   包含完成狀態篩選切換區塊（以帶有 URL 參數的連結或表單實現）。
        *   循環渲染傳入的任務清單（`tasks`），並依狀態顯示不同樣式。
        *   為每條任務提供狀態切換按鈕（`<form action="/tasks/id/toggle" method="POST">`）與刪除按鈕（`<form action="/tasks/id/delete" method="POST">`）。

from app import create_app

# 建立 Flask 應用實例
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器，啟用除錯模式
    app.run(debug=True)

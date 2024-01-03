# 画像分類アプリ

このプロジェクトは、画像分類モデルをAPI化し、ログイン機能とデータベースのCRUD操作を追加したものです。

## 技術スタック

- 環境構築: Docker
- フロントエンド: Streamlit
- バックエンド: FastAPI
- 画像分類モデル: PyTorch（CIFAR-10で学習）
- データベース: SQLite
- データベース操作: SQLAlchemy


## 主な機能

1. **ログイン認証:** ユーザーはログインしてAPIを利用できます。

2. **画像予測:** ユーザーは画像をアップロードして分類モデルによる予測を行えます。

3. **予測結果や画像の保存:** 予測結果やアップロードした画像はデータベースに保存されます。

4. **予測結果の履歴の閲覧:** ログインしたユーザーは過去の予測結果や画像の履歴を閲覧できます。

## ローカルでの実行方法

1. リポジトリをクローンする
   ```bash
   git clone https://github.com/Uyyuu/IC_Docker.git
   ```
2. dockerを起動
   ```bash
   docker compose up -d
   ```
3. アプリにアクセス
　　http://localhost:8501/

## デモ動画
https://github.com/Uyyuu/IC_Docker/assets/131258493/9f81d164-e935-4aaa-9726-9898ec37c721



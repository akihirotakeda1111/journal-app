# journal-app

会計仕訳の登録・訂正・取消、残高試算表、証憑ファイル管理を行う Web アプリケーション。

---

## 1. システム構成 (System Architecture)

### フロントエンド

| 項目              | 内容                                               |
| ----------------- | -------------------------------------------------- |
| フレームワーク    | React 19.2.5                                       |
| ビルドツール      | Vite 8.0.10                                        |
| 言語              | TypeScript 6.0.2                                   |
| HTTP クライアント | axios 1.15.2                                       |
| フォーム          | react-hook-form 7.75.0 + @hookform/resolvers 5.2.2 |
| バリデーション    | zod 4.4.2                                          |
| データ取得        | swr 2.4.1                                          |
| ID 生成           | uuidv7 1.2.1                                       |

### バックエンド

| 項目           | 内容                         |
| -------------- | ---------------------------- |
| 言語           | Python 3.12                  |
| フレームワーク | Django 6.0.4                 |
| API            | Django REST Framework 3.16.1 |
| DB ドライバ    | psycopg2-binary              |
| CORS           | django-cors-headers >= 4.0   |
| UUID           | uuid6                        |
| AWS SDK        | boto3                        |
| テスト         | pytest, pytest-django        |

### インフラ・IaC

| 項目             | 内容                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------- |
| IaC              | Terraform >= 1.6.0                                                                       |
| AWS Provider     | hashicorp/aws ~> 5.0                                                                     |
| リージョン       | ap-northeast-1（CloudFront 用 ACM 証明書は us-east-1）                                   |
| コンテナ         | Docker Compose（サーバー EC2: `docker-compose.dev.yml`、ローカル: `docker-compose.yml`） |
| リバースプロキシ | nginx:alpine + certbot（サーバー EC2）                                                   |

### データストア

| 環境              | エンジン   | バージョン |
| ----------------- | ---------- | ---------- |
| サーバー (RDS)    | PostgreSQL | 18.3       |
| ローカル (Docker) | PostgreSQL | 15         |

### 仕訳データモデルの方針

- Update / Delete を行わず、Insert のみで仕訳を管理する（Append Only）。
- 借方は正の金額、貸方は負の金額として `journal_lines.amount` に保存する。
- 取消・訂正は逆仕訳および新規仕訳の Insert で表現する。
- 仕訳登録 POST リクエストの UUID を検証し、冪等性を担保する。
- 取消・訂正時は `select_for_update` による排他制御を行う。

---

## 2. 機能仕様 (Features)

### 仕訳管理

- 仕訳ヘッダー（計上日・摘要）と仕訳明細（勘定科目・借方/貸方・金額）の新規登録
- 仕訳明細の借方・貸方を N:N 形式で入力する UI
- 仕訳取消（元仕訳に対する逆仕訳の Insert）
- 仕訳訂正（逆仕訳 Insert → 訂正後仕訳 Insert）
- 最新の正常仕訳（子仕訳が存在しない NORMAL タイプ）の一覧表示
- 指定仕訳の変更履歴表示（`original_journal` 自己参照チェーンを辿る）
- API 層で借方/貸方区分を符号付き金額へ変換

### 残高試算表

- 勘定科目ごとの残高集計（`start_date` / `end_date` クエリパラメータで期間指定）
- 勘定科目種別（資産・負債・純資産・収益・費用）に基づく借方/貸方残高の算出
- 借方合計・貸方合計の一致確認

### 勘定科目管理

- 勘定科目マスタの一覧参照（`management/fixtures/account.json` からロード）
- 勘定科目種別: ASSET / LIABILITY / EQUITY / REVENUE / EXPENSE
- 勘定科目の CRUD API は未実装（参照のみ）

### 証憑管理

- S3 署名付き URL（Presigned PUT）による証憑ファイルアップロード
- S3 `ObjectCreated:Put` イベント → Lambda → Django Webhook による証憑レコード非同期登録
- 仕訳に紐づく証憑一覧の取得
- S3 署名付き URL（Presigned GET）による証憑ダウンロード
- 証憑の手動登録 API（Webhook 経由以外の登録パス）

---

## 3. API エンドポイント一覧 (API Endpoints)

ベースパス: `/api/`

| パス                                        | メソッド | 用途                                                    |
| ------------------------------------------- | -------- | ------------------------------------------------------- |
| `/journal/`                                 | POST     | 仕訳（ヘッダー + 明細）の新規登録                       |
| `/journal/cancel/<journal_id>/`             | POST     | 仕訳取消（逆仕訳作成）                                  |
| `/journal/revise/<journal_id>/`             | POST     | 仕訳訂正（逆仕訳 + 新規仕訳作成）                       |
| `/journal/list/`                            | GET      | 最新正常仕訳の一覧取得                                  |
| `/journal/<journal_id>/history/`            | GET      | 指定仕訳の変更履歴取得                                  |
| `/journal/trial_balance/`                   | GET      | 残高試算表取得（`start_date`, `end_date` 任意）         |
| `/journal/evidence/upload/`                 | POST     | 証憑アップロード用 Presigned PUT URL 発行               |
| `/journal/evidence/webhook/`                | POST     | S3 アップロード完了通知（Lambda → Django、Bearer 認証） |
| `/journal/evidence/download/<evidence_id>/` | GET      | 証憑ダウンロード用 Presigned GET URL 発行               |
| `/journal/evidence/<journal_id>/`           | POST     | 証憑レコードの手動登録                                  |
| `/journal/evidence/list/<journal_id>/`      | GET      | 仕訳に紐づく証憑一覧取得                                |
| `/management/account/list/`                 | GET      | 勘定科目マスタ一覧取得                                  |

---

## 4. インフラ・デプロイメント構成 (Infrastructure & Deployment)

### AWS リソース一覧

| リソース             | 識別子 / 設定                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| VPC                  | `10.0.0.0/16`                                                                                       |
| サブネット           | public (`10.0.1.0/24`)、private_a (`10.0.2.0/24`)、private_c (`10.0.3.0/24`)                        |
| Internet Gateway     | public サブネット向け                                                                               |
| NAT Gateway          | private サブネット向け                                                                              |
| EC2                  | `t3.small`、Elastic IP 付与、Docker Compose で backend / nginx / certbot を稼働                     |
| RDS                  | PostgreSQL 18.3、`db.t3.micro`、private サブネット配置                                              |
| S3 (フロントエンド)  | `{project}-react-s3-bucket`、CloudFront OAC 経由で配信                                              |
| S3 (証憑)            | `{project}-file-uploads-s3-bucket`、CORS 設定あり                                                   |
| CloudFront           | フロントエンド配信、ACM 証明書（us-east-1）                                                         |
| Route53              | `{project}.{domain}` → CloudFront、`api.{project}.{domain}` → EC2 EIP                               |
| Lambda               | `{project}-evidence-webhook`（Python 3.12）、S3 uploads バケットの `evidence/` プレフィックスを監視 |
| IAM                  | EC2 ロール、Lambda ロール、GitHub Actions OIDC 用デプロイロール（frontend / backend）               |
| セキュリティグループ | EC2（SSH / HTTP / HTTPS）、RDS（EC2 から PostgreSQL 5432）                                          |

### デプロイ先 URL（Terraform 変数デフォルト値）

| 用途             | ホスト                                     |
| ---------------- | ------------------------------------------ |
| フロントエンド   | `https://journal-app.a-t-dev.com`          |
| バックエンド API | `https://api.journal-app.a-t-dev.com/api/` |

### GitHub Actions

#### Deploy Backend (`deploy-backend.yml`)

| 項目     | 内容                                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------ |
| トリガー | `main` ブランチへの push                                                                                                 |
| 対象パス | `backend/**`, `docker-compose.dev.yml`, `nginx/**`, `scripts/deploy-backend.sh`, `.github/workflows/deploy-backend.yml`  |
| 認証     | GitHub OIDC → IAM ロール (`AWS_BACKEND_DEPLOY_ROLE_ARN`)                                                                 |
| 処理     | SSM Run Command で EC2 に接続 → `git fetch/reset` → `scripts/deploy-backend.sh` 実行（Docker Compose 再ビルド、migrate） |

#### Deploy Frontend (`deploy-frontend.yml`)

| 項目             | 内容                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| トリガー         | `main` ブランチへの push                                                                                                           |
| 対象パス         | `frontend/**`, `.github/workflows/deploy-frontend.yml`                                                                             |
| 認証             | GitHub OIDC → IAM ロール (`AWS_FRONTEND_DEPLOY_ROLE_ARN`)                                                                          |
| 処理             | Node.js 22 で `npm ci && npm run build` → S3 sync (`REACT_S3_BUCKET`) → CloudFront キャッシュ無効化 (`CLOUDFRONT_DISTRIBUTION_ID`) |
| ビルド時環境変数 | `VITE_API_BASE_URL`                                                                                                                |

### 必要な GitHub Repository Variables

| Variable                       | 用途                                       |
| ------------------------------ | ------------------------------------------ |
| `AWS_BACKEND_DEPLOY_ROLE_ARN`  | バックエンドデプロイ用 IAM ロール ARN      |
| `AWS_FRONTEND_DEPLOY_ROLE_ARN` | フロントエンドデプロイ用 IAM ロール ARN    |
| `EC2_INSTANCE_ID`              | バックエンドデプロイ先 EC2 インスタンス ID |
| `REACT_S3_BUCKET`              | フロントエンド配置先 S3 バケット名         |
| `CLOUDFRONT_DISTRIBUTION_ID`   | CloudFront ディストリビューション ID       |
| `VITE_API_BASE_URL`            | フロントエンドビルド時の API ベース URL    |

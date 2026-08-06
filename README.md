# journal-app

システム概要: [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md)

# ER

```mermaid
erDiagram
    journals ||--o{ journal_lines : "has many (1:N)"
    journals ||--o{ evidence : "has many (1:N)"
    journals |o--o| journals : "cancels/modifies (1:1 自己参照)"
    accounts ||--o{ journal_lines : "used in (1:N)"


    journals {
        uuid id PK
        date recorded_date "計上日"
        text description "摘要"
        varchar type "NORMAL / CANCEL"
        uuid original_journal_id FK "元仕訳ID"
        timestamp created_at "作成日時"
    }

    journal_lines {
        bigserial id PK
        uuid journal_id FK "仕訳ID"
        varchar account_id FK "勘定科目ID"
        numeric amount "金額（符号付き: 借方+, 貸方-）"
    }

    evidence {
        bigserial id PK
        uuid journal_id FK "仕訳ID"
        varchar key "保存・参照キー"
        timestamp uploaded_at "アップロード日時"
    }

    accounts {
        varchar id PK "勘定科目コード"
        text name "科目名"
        varchar type "ASSET / LIABILITY / EQUITY / REVENUE / EXPENSE"
    }
```

# Infrastructure

<img src="./docs/images/infrastructure.png" width="800">

# Local Development

## 前提

- Docker / Docker Compose
- Node.js

## セットアップ手順

### 1. リポジトリクローン

```bash
git clone https://github.com/akihirotakeda1111/journal-app.git
```

### 2. 環境変数の設定

ルートディレクトリに.envを作成する。

```bash
cd journal-app
copy .env.example .env
```

### 3. Docker(backend, frontend, db)の起動

```bash
cd journal-app
docker compose up -d
```

## URL

- frontend: http://localhost:5173/
- backend: http://localhost:8000/api/

# Deployment

## backend

### migrate

```bash
ssh ec2-user@[EC2 Public DNS]
cd journal-app
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py loaddata account.json
```

### deploy

```bash
ssh ec2-user@[EC2 Public DNS]
cd journal-app
git pull origin main
docker-compose -f docker-compose.dev.yml up -d --build backend
```

## frontend

### deploy

```bash
cd journal-app
git fetch origin
git reset --hard origin/main
cd frontend
sed -i 's|http://[^"]*|https://api.journal-app.a-t-dev.com/api/|' src/utils/api/client.ts
npm run build
aws s3 sync dist/ s3://journal-app-react-s3-bucket --delete --region ap-northeast-1
```

## infra

### apply

```bash
cd journal-app/infra
terraform apply
```

### destroy

```bash
cd journal-app/infra
terraform destroy
```

# ER

```mermaid
erDiagram
    journals ||--o{ journal_lines : "has many (1:N)"
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

    accounts {
        varchar id PK "勘定科目コード"
        text name "科目名"
        varchar type "ASSET / LIABILITY / EQUITY / REVENUE / EXPENSE"
    }
```

# Infrastructure

<img src="./docs/images/infrastructure.png" width="800">

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

# GitCommit — Day 1

Repo: `llm-microservice` (tạo mới hôm nay, KHÁC với thư mục curriculum này).

## Bước tạo repo
```bash
mkdir llm-microservice && cd llm-microservice
uv init
uv add --dev ruff mypy pytest pre-commit
uv add httpx openai anthropic tiktoken
git init
```

## pyproject.toml — thêm cấu hình tối thiểu
```toml
[tool.mypy]
strict = true

[tool.ruff]
line-length = 100
```

## pre-commit (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks: [{id: ruff}, {id: ruff-format}]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks: [{id: mypy}]
```
Rồi: `uv run pre-commit install`

## .gitignore & secrets
- Thêm `.env` vào `.gitignore`. Tạo `.env.example` (không có key thật).
- KHÔNG commit key.

## Hai commit của ngày (theo roadmap)
1. `chore: scaffold project (uv, ruff, mypy, pytest, pre-commit)`
2. `feat: first LLM calls (OpenAI + Anthropic) with token accounting`

## Kiểm tra trước khi commit
```bash
uv run ruff check .
uv run mypy .
uv run pytest -q   # nếu đã có test
```

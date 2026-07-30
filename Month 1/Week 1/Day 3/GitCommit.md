# GitCommit — Day 3

Repo: `llm-microservice` (tiếp tục repo từ Day 1–2).

## Trước khi commit — chạy quality gate
```bash
uv add pydantic pydantic-settings   # nếu chưa có
uv run ruff check .
uv run ruff format .
uv run mypy --strict .
uv run pytest -q        # nếu đã có test
```
`mypy --strict` phải SẠCH trên cả 4 exercises. **KHÔNG commit `.env`** (đã gitignore từ Day 1).
Kiểm tra không có key thô nào lọt vào code hay log (`SecretStr` che khi print).

## Commit của ngày (1 commit chính)
```
feat: typed data boundary with Pydantic v2 + centralized settings
```
Nếu bạn tách mô hình dữ liệu và cầu nối client thành 2 mạch việc, có thể 2 commit:
1. `feat: add Pydantic v2 request/response models + validation at boundary`
2. `refactor: client takes Settings and returns typed ChatResponse/Usage`

## Gợi ý nội dung commit body (vì sao, không chỉ cái gì)
```
- introduce dataclass for trusted internal value objects (frozen, slots)
- Pydantic v2 models validate untrusted input at the boundary (Field constraints,
  field_validator + model_validator); ValidationError -> future 422
- pydantic-settings: one Settings source, SecretStr for keys, fail-fast at boot
- client now takes Settings + returns typed ChatResponse; defensively validates
  provider body (closes Day 2 bug: HTTP 200 with error body)
```

## Kiểm tra cuối
- [ ] `ruff check` + `mypy --strict` sạch
- [ ] `.env` KHÔNG bị commit; không hardcode/log key
- [ ] Dùng API Pydantic v2 (không `.dict()`/`@validator`/`class Config`)
- [ ] Commit message theo Conventional Commits

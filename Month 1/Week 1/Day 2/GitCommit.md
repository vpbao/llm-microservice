# GitCommit — Day 2

Repo: `llm-microservice` (tiếp tục repo đã tạo ở Day 1).

## Trước khi commit — chạy quality gate
```bash
uv run ruff check .
uv run ruff format .
uv run mypy --strict .
uv run pytest -q        # nếu đã có test
```
`mypy --strict` phải SẠCH trên cả 4 exercises. Không có key nào trong code (`.env` đã bị gitignore).

## Commit của ngày (1 commit chính)
```
feat: harden LLM client (timeout, retry+backoff, error taxonomy, usage logging)
```
Nếu bạn tách idioms và hardening thành 2 mạch việc, có thể 2 commit:
1. `refactor: idiomatic comprehensions + reusable decorators (retry/timed/log_usage)`
2. `feat: harden LLM client (timeout, retry+backoff, error taxonomy, usage logging)`

## Gợi ý nội dung commit body (vì sao, không chỉ cái gì)
```
- add @retry (exp backoff + jitter, bounded) + @timed + @log_usage decorators
- explicit httpx.Timeout (connect/read split) + reused Client (connection pool)
- classify transient (429/5xx/network) vs permanent (4xx) errors
- log model/tokens/cost/latency/attempts on every call (observability seed)
```

## Kiểm tra cuối
- [ ] `ruff check` + `mypy --strict` sạch
- [ ] Không hardcode key
- [ ] Commit message theo Conventional Commits

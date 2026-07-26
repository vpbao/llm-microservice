# Resources — Day 2 (primary sources, đọc bản gốc)

## Idioms Python
- Python docs — Comprehensions & generator expressions (tutorial §5, "Data Structures").
- Python docs — `yield`, generator functions ("More on Defining Functions" / language ref "Yield expressions").
- Python docs — `functools` (`wraps`, `lru_cache`).
- PEP 318 — Decorators for Functions and Methods (đọc lướt để hiểu lịch sử/ý niệm).
- *Fluent Python* (Ramalho) — ch.7 "Function decorators & closures", ch.14 "Iterables, iterators, generators" (đọc chương, bạn không phải beginner).

## Hardening / networking
- HTTPX docs — "Timeouts", "Clients" (connection pooling), "Exceptions".
- OpenAI/Anthropic docs — mục "Error codes" / "Rate limits" (xem status nào retry được, header `Retry-After`).
- Google SRE Book — ch. "Handling Overload" & "Addressing Cascading Failures" (backoff, jitter — đọc mục liên quan).
- AWS Architecture Blog — "Exponential Backoff And Jitter" (bài kinh điển về jitter).

## Ghi chú
- Vẫn KHÔNG động vào LangChain/LlamaIndex. Build tay trước.
- `tenacity` là thư viện retry phổ biến — HÔM NAY tự viết `@retry` bằng tay trước để hiểu cơ chế, rồi mới biết vì sao dùng lib sau.

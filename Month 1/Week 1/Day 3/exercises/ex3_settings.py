"""Exercise 3 — pydantic-settings: cấu hình tập trung, fail-fast, giấu secret.

Thay vì đọc os.environ["..."] rải rác (Day 1-2), dồn TẤT CẢ config vào một Settings,
validate MỘT LẦN lúc khởi động. Laravel: config/*.php + .env + config() — nhưng có kiểu + fail-fast.

Chuẩn bị: cp ../.env.example ../.env  (hoặc đặt .env cạnh file này) rồi điền APP_OPENROUTER_API_KEY.

Bạn TỰ viết phần thân ở chỗ `TODO`.

Acceptance:
- `Settings` đọc từ .env với env_prefix="APP_" (APP_MODEL -> field `model`).
- `openrouter_api_key` là SecretStr, BẮT BUỘC (thiếu -> ValidationError lúc khởi tạo).
- `request_timeout_s` > 0; `max_retries` trong [0, 10].
- `get_settings()` trả về MỘT instance dùng chung (fail-fast: gọi lúc boot).
- `demo_secret_hidden()`: chứng minh print(settings) KHÔNG lộ key; .get_secret_value() mới ra thật.
- `demo_fail_fast()`: thử tạo Settings thiếu key -> bắt ValidationError, in thông báo rõ ràng.
- Type hint đầy đủ; `mypy --strict` sạch; `ruff check` sạch.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )

    # TODO: openrouter_api_key: SecretStr   (BẮT BUỘC — không default -> thiếu là fail)
    openrouter_api_key: SecretStr
    model: str = "openai/gpt-4o-mini"
    base_url: str = "https://openrouter.ai/api/v1"
    # TODO: request_timeout_s: float = Field(default=60.0, gt=0)
    request_timeout_s: float = Field(default=60.0, gt=0)
    # TODO: max_retries: int = Field(default=3, ge=0, le=10)
    max_retries: int = Field(default=3, ge=0, le=10)


@lru_cache
def get_settings() -> Settings:
    """Trả về MỘT Settings dùng chung (cache). Tuần 2 cái này thành Depends(get_settings)."""
    return Settings()  # đọc env/.env + validate NGAY


def demo_secret_hidden() -> None:
    """Chứng minh SecretStr che key khỏi log/print; chỉ .get_secret_value() mới ra giá trị thật."""
    s = get_settings()
    print(s.openrouter_api_key)  # -> **********  (an toàn để log)
    print(s.openrouter_api_key.get_secret_value()[:6], "...")  # chỉ khi THỰC SỰ cần


def demo_fail_fast() -> None:
    """Chứng minh fail-fast: thiếu config bắt buộc -> lỗi NGAY lúc khởi tạo, không phải giữa request."""
    try:
        Settings(
            _env_file=None, openrouter_api_key=None
        )  # cố ý thiếu -> ValidationError
    except ValidationError as e:
        print("fail-fast lúc boot:", type(e).__name__)


def main() -> None:
    s = get_settings()
    print(
        "model:",
        s.model,
        "| timeout:",
        s.request_timeout_s,
        "| retries:",
        s.max_retries,
    )
    demo_secret_hidden()
    demo_fail_fast()


if __name__ == "__main__":
    main()

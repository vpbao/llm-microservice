# Interview — Day 1 (trả lời bằng lời của bạn, nói to được là đạt)

1. **Token là gì? Vì sao token count (không phải character count) chi phối cost & latency?**
   >

2. **Context window là gì? Chuyện gì xảy ra khi vượt quá?**
   >

3. **Vì sao LLM được gọi là stateless? Vậy chat "nhớ" các lượt trước bằng cách nào?**
   >

4. **Temperature vs top-p — mỗi cái điều khiển gì? Khi nào đặt temperature = 0?**
   >

5. **Logprobs là gì? Một ứng dụng production của nó?**
   >

## Follow-ups (khó hơn)
- Bạn gửi một tài liệu 50 trang mỗi lượt — ảnh hưởng cost & latency thế nào, và fix ra sao?
  >
- Temperature 0 vẫn không đảm bảo determinism tuyệt đối — vì sao?
  >

## Practical scenario
Đồng nghiệp nói "model quên mất những gì tôi vừa bảo nó." Chẩn đoán & giải thích thực chất đang xảy ra gì?
>

## Whiteboard
Vẽ vòng đời một chat request: HTTP in → tokens → model → tokens out → cost logged.
> (mô tả hoặc dán ảnh sketch)

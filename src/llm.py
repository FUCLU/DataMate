from config import MODEL_PATH

_tok = None
_model = None


def _load():
    global _tok, _model
    if _model is not None:
        return
    import torch                                  # import trong hàm để máy local không cần torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    _tok = AutoTokenizer.from_pretrained(MODEL_PATH)
    _model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16,                # T4 không có bf16
        device_map="auto",
    )
    _model.eval()


def generate(prompt: str, max_new_tokens: int = 512) -> str:
    if not MODEL_PATH:
        return "[MOCK] chua co model"
    import torch
    _load()
    messages = [{"role": "user", "content": prompt}]
    text = _tok.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
        enable_thinking=False,                    # riêng Qwen3; model khác thì bỏ dòng này
    )
    inputs = _tok(text, return_tensors="pt").to(_model.device)
    with torch.no_grad():
        out = _model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return _tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
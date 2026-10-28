import json, os, time
from config import DATA_DIR, OUT_PATH
import llm


def solve(question: dict, data_dir: str) -> dict:
    # Bản thử: gọi model để xem đường ống thông, nhưng vẫn abstain
    t = time.time()
    raw = llm.generate(f"Trả lời ngắn gọn bằng tiếng Việt: {question['question']}", max_new_tokens=128)
    debug_path = os.path.join(os.path.dirname(OUT_PATH), "debug.jsonl")
    with open(debug_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": question["id"], "raw": raw, "sec": round(time.time() - t, 1)},
                           ensure_ascii=False) + "\n")
    return {"id": question["id"], "type": "abstain"}


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["id"])
                except Exception:
                    pass
    return done


def main():
    os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
    done = load_done(OUT_PATH)
    limit = int(os.environ.get("LIMIT", "0"))      # LIMIT=5 để chỉ chạy 5 câu đầu
    n = 0
    with open(os.path.join(DATA_DIR, "questions.jsonl"), encoding="utf-8") as fin, \
         open(OUT_PATH, "a", encoding="utf-8") as fout:
        for line in fin:
            q = json.loads(line)
            if q["id"] in done:
                continue
            if limit and n >= limit:
                break
            try:
                res = solve(q, DATA_DIR)
            except Exception as e:
                print("LỖI", q["id"], repr(e))
                res = {"id": q["id"], "type": "abstain"}
            fout.write(json.dumps(res, ensure_ascii=False) + "\n")
            fout.flush()
            n += 1


if __name__ == "__main__":
    main()
import time
import llm

t = time.time()
print(llm.generate("Viết một dòng pandas để tính tổng cột doanh_thu của DataFrame df."))
print(f"[{time.time() - t:.1f}s]")
import os

DATA_DIR   = os.environ.get("DATA_DIR", "./data")
OUT_PATH   = os.environ.get("OUT_PATH", "./out/submission.jsonl")
MODEL_PATH = os.environ.get("MODEL_PATH", "")   
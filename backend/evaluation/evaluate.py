import sys
import json
import logging
from pathlib import Path

# Add project root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import config
from graph import build_graph
from state import GraphState

logger = logging.getLogger("EvaluationEngine")

GOLDEN_SET_CSV = config.EVALUATION_DIR / "golden_set.csv"
REPORT_JSON = config.EVALUATION_DIR / "eval_report.json"

def run_evaluation(golden_set_path=GOLDEN_SET_CSV):
    """
    Evaluates the HR AI Agent workflow against a golden benchmark dataset.
    Calculates Intent Accuracy, Refusal Accuracy, Groundedness, Hallucination Rate, and Confidence Accuracy.
    """
    logger.info("============================================================")
    logger.info("Starting Workflow Evaluation Benchmarking")
    logger.info("============================================================")

    if not golden_set_path.exists():
        logger.error(f"Golden set file not found: {golden_set_path}")
        print(f"[Error] Golden set dataset missing at {golden_set_path}")
        return

    df_golden = pd.read_csv(golden_set_path)
    total_samples = len(df_golden)

    app = build_graph()

    intent_correct = 0
    refusal_correct = 0
    grounded_count = 0
    valid_query_count = 0
    confidence_correct = 0

    print(f"\nEvaluating {total_samples} benchmark queries...")
    print("-" * 80)
    print(f"{'ID':<6} | {'Intent Match':<12} | {'Refusal Match':<14} | {'Grounded':<10} | {'Confidence'}")
    print("-" * 80)

    for index, row in df_golden.iterrows():
        query_id = str(row["query_id"])
        employee_id = str(row["employee_id"])
        user_query = str(row["user_query"])
        exp_intent = str(row["expected_intent"]).upper()
        exp_auth = bool(row["expected_auth_approved"])
        exp_sec = bool(row["expected_security_flag"])
        exp_conf = str(row["expected_confidence"])

        initial_state: GraphState = {
            "query_id": query_id,
            "employee_id": employee_id,
            "user_query": user_query
        }

        result = app.invoke(initial_state)

        actual_intent = result.get("intent", "GENERAL")
        actual_auth = result.get("auth_approved", True)
        actual_sec = result.get("security_flag", False)
        actual_conf = result.get("confidence", "Low")
        tool_output = result.get("tool_output", "")
        retrieved_docs = result.get("retrieved_docs", [])

        # 1. Intent Accuracy
        is_intent_match = (actual_intent == exp_intent) or (exp_sec and actual_sec)
        if is_intent_match:
            intent_correct += 1

        # 2. Refusal Accuracy
        exp_refused = (not exp_auth) or exp_sec
        actual_refused = (not actual_auth) or actual_sec
        is_refusal_match = (exp_refused == actual_refused)
        if is_refusal_match:
            refusal_correct += 1

        # 3. Groundedness & Hallucination Rate
        is_grounded = False
        if not actual_refused:
            valid_query_count += 1
            if tool_output or len(retrieved_docs) > 0:
                is_grounded = True
                grounded_count += 1

        # 4. Confidence Accuracy
        is_conf_match = (actual_conf == exp_conf)
        if is_conf_match:
            confidence_correct += 1

        print(f"{query_id:<6} | {str(is_intent_match):<12} | {str(is_refusal_match):<14} | {str(is_grounded):<10} | {actual_conf}")

    intent_accuracy = (intent_correct / total_samples) * 100
    refusal_accuracy = (refusal_correct / total_samples) * 100
    groundedness = (grounded_count / valid_query_count * 100) if valid_query_count > 0 else 100.0
    hallucination_rate = 100.0 - groundedness
    confidence_accuracy = (confidence_correct / total_samples) * 100

    report = {
        "total_benchmark_samples": total_samples,
        "valid_non_refusal_queries": valid_query_count,
        "metrics": {
            "intent_accuracy": round(intent_accuracy, 2),
            "refusal_accuracy": round(refusal_accuracy, 2),
            "groundedness": round(groundedness, 2),
            "hallucination_rate": round(hallucination_rate, 2),
            "confidence_accuracy": round(confidence_accuracy, 2)
        }
    }

    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 80)
    print(" WORKFLOW EVALUATION REPORT")
    print("=" * 80)
    print(f" Total Benchmark Samples  : {total_samples}")
    print(f" Intent Accuracy          : {intent_accuracy:.2f}%")
    print(f" Refusal Accuracy         : {refusal_accuracy:.2f}%")
    print(f" Groundedness             : {groundedness:.2f}%")
    print(f" Hallucination Rate       : {hallucination_rate:.2f}%")
    print(f" Confidence Accuracy      : {confidence_accuracy:.2f}%")
    print(f" Detailed Report Export   : {REPORT_JSON}")
    print("=" * 80 + "\n")

    return report


if __name__ == "__main__":
    run_evaluation()

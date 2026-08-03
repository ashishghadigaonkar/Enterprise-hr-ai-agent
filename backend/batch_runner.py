import time
import uuid
import logging
import pandas as pd
import config
from graph import build_graph
from state import GraphState

logger = logging.getLogger("BatchRunner")

def run_batch_processing(input_file=config.INPUT_QUERIES_CSV):
    """
    Reads batch input queries from CSV, executes the LangGraph workflow per query,
    saves output to results CSV, handles errors gracefully, and prints summary metrics.
    """
    logger.info("============================================================")
    logger.info("Starting Batch Processing Engine")
    logger.info("============================================================")

    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        print(f"[Error] Input queries file '{input_file}' missing.")
        return

    try:
        df_inputs = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df_inputs)} batch queries from '{input_file.name}'")
    except Exception as e:
        logger.error(f"Failed to read input CSV '{input_file}': {e}")
        return

    app = build_graph()

    start_time = time.time()
    total_queries = len(df_inputs)
    successful_count = 0
    security_flagged_count = 0
    auth_denied_count = 0
    error_count = 0

    print("\nExecuting Batch Queries...")
    print("-" * 75)
    print(f"{'Query ID':<10} | {'Emp ID':<8} | {'Intent':<10} | {'Auth':<8} | {'Sec Flag':<8} | {'Status'}")
    print("-" * 75)

    for index, row in df_inputs.iterrows():
        query_id = str(row.get("query_id", f"BQ-{index+1}")).strip()
        employee_id = str(row.get("employee_id", "")).strip()
        user_query = str(row.get("user_query", "")).strip()

        trace_id = str(uuid.uuid4())
        initial_state: GraphState = {
            "trace_id": trace_id,
            "query_id": query_id,
            "employee_id": employee_id,
            "user_query": user_query
        }

        try:
            result = app.invoke(initial_state)

            sec_flag = result.get("security_flag", False)
            auth_app = result.get("auth_approved", True)
            intent = result.get("intent", "UNKNOWN")

            if sec_flag:
                security_flagged_count += 1
                status_str = "SECURITY BLOCKED"
            elif not auth_app:
                auth_denied_count += 1
                status_str = "AUTH DENIED"
            else:
                successful_count += 1
                status_str = "SUCCESS"

            print(f"{query_id:<10} | {employee_id:<8} | {intent:<10} | {str(auth_app):<8} | {str(sec_flag):<8} | {status_str}")

        except Exception as e:
            error_count += 1
            logger.error(f"Failed processing query [{query_id}]: {e}", exc_info=True)
            print(f"{query_id:<10} | {employee_id:<8} | {'ERROR':<10} | {'N/A':<8} | {'N/A':<8} | ERROR: {str(e)[:25]}")

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 75)
    print(" BATCH PROCESSING SUMMARY STATISTICS")
    print("=" * 75)
    print(f" Total Queries Processed : {total_queries}")
    print(f" Successfully Processed : {successful_count}")
    print(f" Security Flagged       : {security_flagged_count}")
    print(f" Authorization Denied   : {auth_denied_count}")
    print(f" Errors Encountered     : {error_count}")
    print(f" Total Execution Time   : {elapsed_time:.2f} seconds")
    print(f" Audit Logs Destination : {config.RESULTS_CSV}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_batch_processing()

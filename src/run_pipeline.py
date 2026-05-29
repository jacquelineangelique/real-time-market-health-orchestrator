"""
PR 05: add end-to-end etl pipeline orchestration runner

Purpose:
Provide a single entry point for running the local ETL workflow.

Execution flow:
1. Run API extraction
2. Persist raw JSON responses
3. Run transformation workflow
4. Export Tableau-ready processed CSV
"""

import logging
from datetime import datetime
from pathlib import Path

from extract_market_data import main as run_extraction
from transform_market_data import run_transformation
from build_star_schema import build_star_schema

# =====================================================
# Logging Setup
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline_runner.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# =====================================================
# Pipeline Runner
# =====================================================

def run_pipeline():
    """
    Orchestrates the end-to-end ETL workflow.

    This lightweight runner simulates a production-style
    orchestration layer by enforcing execution order and
    logging each pipeline phase.
    """

    pipeline_start_time = datetime.utcnow()

    logging.info("Pipeline execution started.")

    try:
        # -------------------------------------------------
        # Step 1: Extraction
        # -------------------------------------------------
        # Calls the API extraction layer created in PR 03.
        # This retrieves raw source data and stores it in
        # data/raw/.
        # -------------------------------------------------

        logging.info("Starting extraction workflow.")
        print("Starting extraction workflow...")

        run_extraction()

        logging.info("Extraction workflow completed.")
        print("Extraction workflow completed.")

        # -------------------------------------------------
        # Step 2: Transformation
        # -------------------------------------------------
        # Calls the transformation layer created in PR 04.
        # This reads raw JSON, normalizes records, calculates
        # volatility metrics, and exports the processed CSV.
        # -------------------------------------------------

        logging.info("Starting transformation workflow.")
        print("Starting transformation workflow...")

        processed_file = run_transformation()

        logging.info("Transformation workflow completed.")
        print("Transformation workflow completed.")

        # -------------------------------------------------
        # Step 3: Build Star Schema
        # -------------------------------------------------

        logging.info("Starting star schema workflow.")
        print("Starting star schema workflow...")

        build_star_schema()

        logging.info("Star schema workflow completed.")
        print("Star schema workflow completed.")

        # -------------------------------------------------
        # Step 4: Completion Logging
        # -------------------------------------------------

        pipeline_end_time = datetime.utcnow()
        duration_seconds = (
            pipeline_end_time - pipeline_start_time
        ).total_seconds()

        logging.info(
            f"Pipeline execution completed successfully in "
            f"{duration_seconds:.2f} seconds."
        )

        print("\nPipeline completed successfully.")
        print(f"Processed output: {processed_file}")
        print(f"Duration: {duration_seconds:.2f} seconds")

        return processed_file

    except Exception as error:
        # -------------------------------------------------
        # Failure Handling
        # -------------------------------------------------
        # Any exception from extraction or transformation is
        # logged here so the full pipeline failure is visible
        # from one centralized log file.
        # -------------------------------------------------

        logging.exception(f"Pipeline execution failed: {error}")

        print("\nPipeline failed.")
        print(f"Error: {error}")

        raise


# =====================================================
# Script Entry Point
# =====================================================

if __name__ == "__main__":
    run_pipeline()

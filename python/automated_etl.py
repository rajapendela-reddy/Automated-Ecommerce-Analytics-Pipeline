from pathlib import Path
from datetime import datetime
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_FILE = OUTPUT_DIR / "ecommerce_reporting.csv"
LOG_FILE = LOG_DIR / "pipeline_log.csv"


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# PIPELINE LOGGING
# ============================================================

def write_log(status, rows_processed=0, invalid_revenue=0,
              invalid_quantity=0, invalid_price=0, error_message=""):

    log_record = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "rows_processed": rows_processed,
        "invalid_revenue": invalid_revenue,
        "invalid_quantity": invalid_quantity,
        "invalid_price": invalid_price,
        "error_message": error_message
    }])

    if LOG_FILE.exists():
        log_record.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        log_record.to_csv(
            LOG_FILE,
            index=False
        )


# ============================================================
# FIND INPUT EXCEL FILE
# ============================================================

def find_input_file():

    excel_files = list(INPUT_DIR.glob("*.xlsx"))

    if not excel_files:
        raise FileNotFoundError(
            "No Excel input file found in the input folder."
        )

    if len(excel_files) > 1:
        print("Multiple Excel files found. Using:", excel_files[0].name)

    return excel_files[0]


# ============================================================
# EXTRACT
# ============================================================

def extract_data(input_file):

    print(f"Reading input file: {input_file.name}")

    df = pd.read_excel(input_file)

    print(f"Rows extracted: {len(df):,}")
    print(f"Columns extracted: {len(df.columns)}")

    return df


# ============================================================
# VALIDATE
# ============================================================

def validate_data(df):

    print("\nRunning data validation...")

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    invalid_revenue = 0
    invalid_quantity = 0
    invalid_price = 0

    if "revenue" in df.columns:
        invalid_revenue = int((df["revenue"] < 0).sum())

    if "quantity" in df.columns:
        invalid_quantity = int((df["quantity"] < 0).sum())

    if "unit_price" in df.columns:
        invalid_price = int((df["unit_price"] < 0).sum())

    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print(f"Invalid revenue: {invalid_revenue}")
    print(f"Invalid quantity: {invalid_quantity}")
    print(f"Invalid unit price: {invalid_price}")

    if missing_values > 0:
        raise ValueError(
            f"Validation failed: {missing_values} missing values found."
        )

    if duplicate_rows > 0:
        raise ValueError(
            f"Validation failed: {duplicate_rows} duplicate rows found."
        )

    if invalid_revenue > 0:
        raise ValueError(
            f"Validation failed: {invalid_revenue} invalid revenue values found."
        )

    if invalid_quantity > 0:
        raise ValueError(
            f"Validation failed: {invalid_quantity} invalid quantity values found."
        )

    if invalid_price > 0:
        raise ValueError(
            f"Validation failed: {invalid_price} invalid unit price values found."
        )

    print("Validation passed.")

    return {
        "invalid_revenue": invalid_revenue,
        "invalid_quantity": invalid_quantity,
        "invalid_price": invalid_price
    }


# ============================================================
# TRANSFORM
# ============================================================

def transform_data(df):

    print("\nTransforming data...")

    df = df.copy()

    # Gross transaction value
    if "unit_price" in df.columns and "quantity" in df.columns:
        df["gross_value"] = (
            df["unit_price"] * df["quantity"]
        )

    # Conversion flag
    if "purchased" in df.columns:
        df["conversion_flag"] = (
            df["purchased"].astype(int)
        )

    # Abandonment flag
    if "cart_abandoned" in df.columns:
        df["abandonment_flag"] = (
            df["cart_abandoned"].astype(int)
        )

    # Convert session duration from seconds to minutes
    if "time_on_site_sec" in df.columns:
        df["time_on_site_min"] = (
            df["time_on_site_sec"] / 60
        )

    # Actual discount rate
    if "discount_amount" in df.columns and "gross_value" in df.columns:

        df["discount_rate_actual"] = (
            df["discount_amount"]
            .div(df["gross_value"].replace(0, pd.NA))
            .mul(100)
            .fillna(0)
        )

    # Date-based features
    if "visit_date" in df.columns:

        df["visit_date"] = pd.to_datetime(
            df["visit_date"]
        )

        df["year"] = df["visit_date"].dt.year
        df["month"] = df["visit_date"].dt.month
        df["month_name"] = df["visit_date"].dt.month_name()
        df["weekday_name"] = df["visit_date"].dt.day_name()
        df["week"] = df["visit_date"].dt.isocalendar().week.astype(int)

    print(f"Rows after transformation: {len(df):,}")
    print(f"Columns after transformation: {len(df.columns)}")

    return df


# ============================================================
# LOAD
# ============================================================

def load_data(df):

    print("\nGenerating reporting dataset...")

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Reporting file created: {OUTPUT_FILE}")
    print(f"Rows written: {len(df):,}")


# ============================================================
# MAIN ETL PIPELINE
# ============================================================

def automated_etl():

    start_time = datetime.now()

    print("=" * 60)
    print("AUTOMATED E-COMMERCE ETL PIPELINE")
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # EXTRACT
        # ----------------------------------------------------

        input_file = find_input_file()

        df = extract_data(input_file)

        # ----------------------------------------------------
        # VALIDATE
        # ----------------------------------------------------

        validation_results = validate_data(df)

        # ----------------------------------------------------
        # TRANSFORM
        # ----------------------------------------------------

        df_transformed = transform_data(df)

        # ----------------------------------------------------
        # LOAD
        # ----------------------------------------------------

        load_data(df_transformed)

        # ----------------------------------------------------
        # LOG SUCCESS
        # ----------------------------------------------------

        write_log(
            status="SUCCESS",
            rows_processed=len(df_transformed),
            invalid_revenue=validation_results["invalid_revenue"],
            invalid_quantity=validation_results["invalid_quantity"],
            invalid_price=validation_results["invalid_price"]
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Execution time: {duration:.2f} seconds")
        print("=" * 60)

    except Exception as error:

        error_message = str(error)

        print("\n" + "=" * 60)
        print("PIPELINE FAILED")
        print(f"Error: {error_message}")
        print("=" * 60)

        write_log(
            status="FAILED",
            error_message=error_message
        )

        raise


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    automated_etl()

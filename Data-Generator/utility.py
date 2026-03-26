import random
import rstr
import logging
import math
import datetime
import pandas as pd

# ---------------- LOGGER ---------------- #
def configure_logger():
    logging.basicConfig(
        filename="data_generation_logs.logs",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

logger = configure_logger()

# ---------------- HELPERS ---------------- #
def safe_str(value):
    """
    Converts value to string safely.
    Handles:
      - Python None
      - float NaN
      - pandas NA / pd.NA
    Returns empty string if value is "empty"
    """
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    if value is pd.NA:
        return ""
    return str(value)

def normalize_na(value):
    """Converts 'NA' or empty strings to None"""
    if value is None:
        return None
    value = str(value).strip()
    if value.upper() == "NA" or value == "":
        return None
    return value

def parse_range(range_val):
    """Parses numeric range like '1-1000', handling en-dash/em-dash"""
    try:
        if not range_val:
            return None, None
        range_val = str(range_val).replace("–", "-").replace("—", "-")
        start, end = range_val.split("-")
        return start.strip(), end.strip()
    except Exception as e:
        logger.error(f"Error parsing range '{range_val}': {str(e)}")
        return None, None

# ---------------- MAIN DISPATCHER ---------------- #
def generate_field(row, total_count):
    dtype = safe_str(row.get("Data Type")).lower()

    try:
        if dtype == "int":
            return generate_int(row, total_count)
        elif dtype == "float":
            return generate_float(row, total_count)
        elif dtype in ("string", "regex"):
            return generate_regex_string(row, total_count)
        elif dtype == "set":
            return generate_set(row, total_count)
        elif dtype == "datetime":
            return generate_datetime(row, total_count)
        else:
            logger.error(f"Unsupported data type: {dtype}")
            return [None] * total_count
    except Exception as e:
        logger.error(f"Error generating field [{row.get('Field')}]: {str(e)}")
        return [None] * total_count

# ---------------- GENERATORS ---------------- #
def generate_int(row, total_count):
    try:
        start, end = parse_range(row.get("Range"))
        start, end = int(start), int(end)
        logger.info(f"Generating INT field: {row.get('Field')}")
        return [random.randint(start, end) for _ in range(total_count)]
    except Exception as e:
        logger.error(f"Error generating INT field [{row.get('Field')}]: {str(e)}")
        return [None] * total_count

def generate_float(row, total_count):
    try:
        start, end = parse_range(row.get("Range"))
        start, end = float(start), float(end)
        precision = int(row.get("Size", 2))
        logger.info(f"Generating FLOAT field: {row.get('Field')}")
        return [round(random.uniform(start, end), precision) for _ in range(total_count)]
    except Exception as e:
        logger.error(f"Error generating FLOAT field [{row.get('Field')}]: {str(e)}")
        return [None] * total_count

def generate_regex_string(row, total_count):
    try:
        regex = normalize_na(row.get("Regex/Pattern"))
        prefix = safe_str(normalize_na(row.get("Prefix")))
        suffix = safe_str(normalize_na(row.get("Suffix")))

        logger.info(f"Generating REGEX/STRING field: {row.get('Field')}")

        # fallback if regex missing
        if not regex:
            example_value = safe_str(normalize_na(row.get("Example")))
            return [f"{prefix}{example_value}{suffix}" for _ in range(total_count)]

        return [f"{prefix}{rstr.xeger(regex)}{suffix}" for _ in range(total_count)]
    except Exception as e:
        logger.error(f"Error generating REGEX/STRING field [{row.get('Field')}]: {str(e)}")
        example_value = safe_str(normalize_na(row.get("Example")))
        return [example_value] * total_count

def generate_set(row, total_count):
    try:
        raw_set = normalize_na(row.get("Set"))
        if not raw_set:
            logger.warning(f"No set provided for field {row.get('Field')}")
            return [None] * total_count
        values = [x.strip() for x in raw_set.split(",") if x.strip()]
        logger.info(f"Generating SET field: {row.get('Field')}")
        return [random.choice(values) for _ in range(total_count)]
    except Exception as e:
        logger.error(f"Error generating SET field [{row.get('Field')}]: {str(e)}")
        return [None] * total_count

def generate_datetime(row, total_count):
    try:
        range_val = normalize_na(row.get("Range"))
        fmt = safe_str(row.get("Regex/Pattern")) or "%d/%m/%Y"

        if not range_val:
            logger.warning(f"No datetime range for field {row.get('Field')}")
            today = datetime.datetime.today()
            return [(today.strftime(fmt)) for _ in range(total_count)]

        from_line, to_line = range_val.split("\n")
        start_date = datetime.datetime.strptime(from_line.split(":")[1].strip(), "%d/%m/%Y")
        end_date = datetime.datetime.strptime(to_line.split(":")[1].strip(), "%d/%m/%Y")
        delta_days = (end_date - start_date).days

        logger.info(f"Generating DATETIME field: {row.get('Field')}")
        return [
            (start_date + datetime.timedelta(days=random.randint(0, delta_days))).strftime(fmt)
            for _ in range(total_count)
        ]
    except Exception as e:
        logger.error(f"Error generating DATETIME field [{row.get('Field')}]: {str(e)}")
        today = datetime.datetime.today()
        return [(today.strftime(fmt)) for _ in range(total_count)]

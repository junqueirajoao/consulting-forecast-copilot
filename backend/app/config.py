from dotenv import load_dotenv
import os

load_dotenv()

EXCEL_PATH    = os.getenv("EXCEL_PATH", "data/ficticio.xlsx")
DEFAULT_MONTH = int(os.getenv("DEFAULT_MONTH", "5"))
DEFAULT_YEAR  = int(os.getenv("DEFAULT_YEAR", "2026"))
APP_ENV       = os.getenv("APP_ENV", "dev")

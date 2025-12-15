import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-exp")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Data Paths
DOCUMENT_PATH = os.getenv("DOCUMENT_PATH", "data/data.jsonl")
USER_DATA_PATH = os.getenv("USER_DATA_PATH", "data/data.json")
COURSES_PATH = os.getenv("COURSES_PATH", "data/courses.json")
LEARNING_PATHS_PATH = os.getenv("LEARNING_PATHS_PATH", "data/learning_paths.json")
COURSE_LEVELS_PATH = os.getenv("COURSE_LEVELS_PATH", "data/course_levels.json")
TUTORIALS_PATH = os.getenv("TUTORIALS_PATH", "data/tutorials.json")

TOP_K = int(os.getenv("TOP_K", 3))
RETRIEVE_MIN_SCORE = float(os.getenv("RETRIEVE_MIN_SCORE", 0.4))
MAX_CONTEXT_WORDS = int(os.getenv("MAX_CONTEXT_WORDS", 400))

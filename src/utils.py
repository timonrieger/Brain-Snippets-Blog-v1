

def calculate_reading_time(text, words_per_minute=200):
    """Calculate the estimated reading time for a given text."""
    words = text.split()
    total_words = len(words)
    reading_time_minutes = total_words / words_per_minute
    minutes = int(reading_time_minutes)
    return minutes
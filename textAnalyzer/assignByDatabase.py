from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database_conn import Database

def assign_by_database(wordToAssign: str, DatabaseObject: 'Database', distanceProportion: int = 0.2) -> int | None:
    """if it is able to find similar word in database, it returns id of class it belongs to
    else it returns None"""
    candidates = DatabaseObject.find_candidates(wordToAssign)
    if candidates == []:
        return None
    distance = int(len(wordToAssign) * distanceProportion)
    # calculate Levenshtein distance
    for candidate in candidates:
        
        
        
        
        if normalized_distance <= distance:
            return candidate[0]
            
    return None

def calculate_levenshtein_distance(word1: str, word2: str, maxDistance: int) -> bool:
    m, n = len(word1), len(word2)
    if abs(m - n) > maxDistance:
        return False
    previous_row = list(range(n + 1))
    
    for i in range(1, m + 1):
        # The first element of the current row is the edit distance from word1[:i] to an empty string.
        current_row = [i] + [0] * n
        
        # Only iterate over the possible indices in word2.
        # Optionally, you can restrict the range further to [max(1, i-maxDistance), min(n, i+maxDistance)+1]
        # for an even more optimized solution. For clarity, we use the full range here.
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            current_row[j] = min(
                previous_row[j] + 1,      # Deletion
                current_row[j - 1] + 1,     # Insertion
                previous_row[j - 1] + cost  # Substitution
            )
        
        # Early termination: if the minimum edit distance in the current row is greater than maxDistance,
        # there is no need to process further.
        if min(current_row) > maxDistance:
            return False
        
        previous_row = current_row

    return previous_row[n] <= maxDistance


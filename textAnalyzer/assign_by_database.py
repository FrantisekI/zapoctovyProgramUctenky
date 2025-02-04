from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database_conn import Database

def assign_by_database(wordToAssign: str, DatabaseObject: 'Database', distanceProportion: int = 0.2) -> set[tuple[int, str]]:
    """if it is able to find similar word in database, it returns id of class it belongs to
    else it returns None"""
    candidates = DatabaseObject.find_candidates(wordToAssign)
    if candidates == []:
        return None
    distance = int(len(wordToAssign) * distanceProportion)
    # calculate Levenshtein distance
    matchingCandidates = {}
    for candidate in candidates:
        if candidate[1] == wordToAssign:
            return {(DatabaseObject.select_one_get_class_from_custom_name(candidate[0]),)}
        print(candidate[1])
        if calculate_levenshtein_distance(wordToAssign, candidate[1], distance):
            matchingCandidates.add((DatabaseObject.select_one_get_class_from_custom_name(candidate[0]),))
            
    print(matchingCandidates)    
    return matchingCandidates

def calculate_levenshtein_distance(word1: str, word2: str, maxDistance: int) -> bool:
    m, n = len(word1), len(word2)
    if abs(m - n) > maxDistance:
        return False
    previous_row = list(range(n + 1))
    
    for i in range(1, m + 1):
        current_row = [i] + [0] * n

        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            current_row[j] = min(
                previous_row[j] + 1,      
                current_row[j - 1] + 1,   
                previous_row[j - 1] + cost
            )
        
        if min(current_row) > maxDistance:
            return False
        
        previous_row = current_row

    return previous_row[n] <= maxDistance


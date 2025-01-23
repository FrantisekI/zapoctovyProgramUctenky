from sortNames import sortNames
from assignByDatabase import assignByDatabase

def analyzeText(text, DatabaseObject):
    sortedNamesJson = sortNames(text)
    if sortedNamesJson == {}:
        return
    assignedJson = assignByDatabase(sortedNamesJson, DatabaseObject)
    

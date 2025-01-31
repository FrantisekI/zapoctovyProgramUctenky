from random import randint, seed
import mmh3

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Database import Database

def _create_shingles(self: 'Database', text: str, shingle_size: int = 3) -> set[str]:
    if len(text) < shingle_size:
        return {text}
    
    shingles = set()
    for i in range(len(text) - shingle_size + 1):
        shingle = text[i:i + shingle_size]
        shingles.add(shingle)
    return shingles

def _create_signature(self: 'Database', shingles: set[str], number_of_functions: int = 5) -> list[int]:
    primarySeed = 123456
    seed(primarySeed)
    seeds = []
    seeds = [randint(0, 2**32 - 1) for _ in range(number_of_functions)]
    print(seeds)
    signature = []
    
    for i in range(number_of_functions):
        minimum = float('inf')
        for shingle in shingles:
            hashed_value = mmh3.hash(shingle, seeds[i])
            print(hashed_value)
            if hashed_value < minimum:
                minimum = hashed_value
        signature.append(minimum)
        
    return signature

def _store_custom_name_with_shingles(self: 'Database', customName: str, signature: list[int], classId: int) -> int:
    customNameId = self.insert_custom_product_name(customName, classId)
    
    for hashId, hash in enumerate(signature):
        self.insert_signature(customNameId, hashId, hash)
    
    return customNameId

def hash_insert_custom_name(self: 'Database', customName: str, classId: int) -> int:
    shingles = self._create_shingles(customName)
    signature = self._create_signature(shingles)
    return self._store_custom_name_with_shingles(customName, signature, classId)
    
        
        
    
    
    
if __name__ == "__main__":
    shingles = _create_shingles(None, 'Hello World!')
    print(_create_signature(None, shingles))
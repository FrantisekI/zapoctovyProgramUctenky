from random import randint, seed
import mmh3
import unicodedata

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Database

def _create_shingles(self: 'Database', text: str, shingle_size: int = 3) -> set[str]:
    """brakes text into smaller owerlaping parts of size shingle_size"""
    if len(text) < shingle_size:
        return {text}
    
    shingles = set()
    for i in range(len(text) - shingle_size + 1):
        shingle = text[i:i + shingle_size]
        shingles.add(shingle)
    # print(shingles) # comment
    return shingles

def _create_signature(self: 'Database', shingles: set[str], number_of_functions: int = 6) -> list[int]:
    """using minhash algorithm it creates signature from shingles
    returns list of integers"""
    primarySeed = 123456
    seed(primarySeed)
    seeds = []
    seeds = [randint(0, 2**32 - 1) for _ in range(number_of_functions)]
    signature = []
    
    for i in range(number_of_functions):
        minimum = float('inf')
        for shingle in shingles:
            hashed_value = mmh3.hash(shingle, seeds[i])
            # print(hashed_value)
            if hashed_value < minimum:
                minimum = hashed_value
        signature.append(minimum)
        
    return signature

def _store_custom_name_with_bands(self: 'Database', customName: str, bands: list[int], classId: int) -> int:
    customNameId = self.insert_custom_product_name(customName, classId)
    
    for bandId, hash in enumerate(bands):
        self.insert_band(customNameId, bandId, hash)
    
    return customNameId

def _compute_bands_hash(self: 'Database', signature: list[int], rowsPerBand: int = 2) -> list[int]:
    bands = []
    for i in range(0, len(signature), rowsPerBand):
        band = signature[i:min(i + rowsPerBand, len(signature)-1)]
        bands.append(hash(tuple(band)))
    
    return bands

def _marge_functions_to_compute_bands(self: 'Database', nameToIdentify: str, numberBands: int = 5, rowsPerBand: int = 2) -> list[int]:
    """helper function: creates shingles, signature and bands"""
    shingles = self._create_shingles(nameToIdentify)
    signature = self._create_signature(shingles, numberBands * rowsPerBand)
    bands = self._compute_bands_hash(signature, rowsPerBand)
    
    return bands

def hash_and_insert_custom_name(self: 'Database', customName: str, classId: int) -> int:
    """it takes name of product, computes bands and stores it in database
    also stores the bands returns custom_product_id"""
    customName = unicodedata.normalize('NFKD', customName.upper()).encode('ASCII', 'ignore').decode('ASCII')
    bands = self._marge_functions_to_compute_bands(customName)
    # print(bands)
    return self._store_custom_name_with_bands(customName, bands, classId)

def find_candidates(self: 'Database', inputName: str) -> list[tuple[int, str]]:
    """as an input it takes name of product and returns list of candidates
    that might be similar to it as a a list of tuples: (custom_product_id, name)"""
    inputName = unicodedata.normalize('NFKD', inputName.upper()).encode('ASCII', 'ignore').decode('ASCII')
    # print(inputName) # comment
    bands = self._marge_functions_to_compute_bands(inputName)
    keys = tuple([(id, band) for id, band in enumerate(bands)])
    
    return self._find_custom_names_by_bands(keys)
    

    
if __name__ == "__main__":
    shingles = _create_shingles(None, 'Hello World!')
    print(_create_signature(None, shingles))
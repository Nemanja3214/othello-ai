import random

from map import Map, MapElement


class HashMap(object):
    __slots__ = "_data", "_capacity", "_size", "prime", "_a", "_b"

    def __init__(self, capacity=1031):
        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 109345121

        # konstante heširanja
        self._a = 1 + random.randrange(self.prime-1)
        self._b = random.randrange(self.prime)

    def __len__(self):
        return self._size

    def clear(self):
        self._capacity = 8
        self._data = self._capacity * [None]
        self._size = 0

    def _hash(self, x):
        hashed_value = (hash(x)*self._a + self._b) % self.prime
        compressed = hashed_value % self._capacity
        return compressed

    def _resize(self, capacity):
        old_data = list(self.items())
        self._data = capacity * [None]
        self._size = 0

        # prepisivanje podataka u novu tabelu
        for (k, v) in old_data:
            self[k] = v

    def __getitem__(self, key):
        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

        # povećaj broj raspoloživih mesta
        current_capacity = len(self._data)
        if self._size > current_capacity // 2:
            self._resize(2*current_capacity - 1)

    def __delitem__(self, key):
        bucket_index = self._hash(key)
        self._bucket_delitem(bucket_index, key)

    def items(self):
        raise NotImplementedError()

    def _bucket_getitem(self, index, key):
        raise NotImplementedError()

    def _bucket_setitem(self, index, key, value):
        raise NotImplementedError()

    def _bucket_delitem(self, index, key):
        bucket = self._data[index]
        self._data[index][key]

    def get(self, key):
        bucket_index = self._hash(key)
        return self._bucket_getitem_get(bucket_index, key)

    def _bucket_getitem_get(self, bucket_index, key):
        raise NotImplementedError()


class ChainedHashMap(HashMap):
    def _bucket_getitem(self, i, key):
        bucket = self._data[i]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        return bucket[key]

    def _bucket_setitem(self, bucket_index, key, value):
        bucket = self._data[bucket_index]
        if bucket is None:
            self._data[bucket_index] = Map()

        # broj elemenata u mapi se menja samo u slučaju da je došlo do
        # dodavanja, dok ažuriranje ne menja broj elemenata
        current_size = len(self._data[bucket_index])
        self._data[bucket_index][key] = value
        if len(self._data[bucket_index]) > current_size:
            self._size += 1

    def _bucket_delitem(self, bucket_index, key):
        bucket = self._data[bucket_index]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        del bucket[key]
        self._size -= 1

    def __iter__(self):
        for bucket in self._data:
            if bucket is not None:
                for key in bucket:
                    yield key

    def items(self):
        for bucket in self._data:
            if bucket is not None:
                for key, value in bucket.items():
                    yield key, value



class LinearHashMap(HashMap):
    # sentinel koji označava lokaciju u mapi sa koje je obrisan element
    _MARKER = object()

    def _is_available(self, index):
        return self._data[index] is None or self._data[index] is self._MARKER

    def _find_bucket(self, bucket_index, key, check_deleted=False):
        available_slot = None
        while True:
            if self._is_available(bucket_index):
                if available_slot is None:
                    available_slot = bucket_index

                if self._data[bucket_index] is None:
                    return False, available_slot

                if check_deleted and self._data[bucket_index] is self._MARKER:
                    return False, available_slot

            elif key == self._data[bucket_index].key:
                return True, bucket_index

            bucket_index = (bucket_index+1) % len(self._data)

    def _bucket_getitem(self, bucket_index, key):
        found, index = self._find_bucket(bucket_index, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')
        return self._data[index].value

    def _bucket_setitem(self, bucket_index, key, value):
        found, available_bucket_index = self._find_bucket(bucket_index, key, True)
        if not found:
            self._data[available_bucket_index] = MapElement(key, value)
            self._size += 1
        else:
            self._data[available_bucket_index].value = value

    def _bucket_delitem(self, bucket_index, key):
        found, index = self._find_bucket(bucket_index, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')

        # označi element markerom
        self._data[index] = self._MARKER

    def _bucket_getitem_get(self, bucket_index, key):
        found, index = self._find_bucket(bucket_index, key)
        if not found:
            return None
        return self._data[index].value

    def __iter__(self):
        total_buckets = len(self._data)
        for i in range(total_buckets):
            if not self._is_available(i):
                yield self._data[i].key

    def items(self):
        total_buckets = len(self._data)
        for i in range(total_buckets):
            if not self._is_available(i):
                yield self._data[i].key, self._data[i].value

    def keys(self):
        total_buckets = len(self._data)
        for i in range(total_buckets):
            if not self._is_available(i):
                yield self._data[i].key




if __name__ == '__main__':
    # print("\nChained Hash Map\n---------------------")
    # hash_map = ChainedHashMap()
    #
    # print('Inicijalno dodavanje')
    # for item in hash_map:
    #     print(item, hash_map[item])
    #
    # print('Izmena vrednosti')
    # hash_map[3] = 5
    # for item in hash_map:
    #     print(item, hash_map[item])
    #
    # print('Brisanje elementa')
    # del hash_map[2]
    # for item in hash_map:
    #     print(item, hash_map[item])

    print("\nLinear Hash Map\n---------------------")
    hash_map = LinearHashMap()
    hash_map[3] = 10
    hash_map[2] = 11
    hash_map[55] = 11
    del hash_map[55]
    hash_map[43] = 11
    hash_map[24] = 11
    hash_map[19] = 11
    hash_map[190] = 11
    hash_map[13] = 10
    hash_map[12] = 11
    hash_map[155] = 11
    hash_map[143] = 11
    hash_map[124] = 11
    hash_map[119] = 11
    hash_map[1190] = 11

    print('Inicijalno dodavanje')
    for item in hash_map:
        print(item, hash_map[item])

    print('Izmena vrednosti')
    hash_map[3] = 5
    for item in hash_map:
        print(item, hash_map[item])

    print('Brisanje elementa')
    del hash_map[143]
    for item in hash_map:
        print(item, hash_map[item])




"""
Modul sadrži implementaciju asocijativnog niza
"""


class MapElement(object):
    """
    Klasa modeluje element asocijativnog niza
    """
    __slots__ = '_key', '_value'

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Map(object):
    def __init__(self):
        self._data = []

    def __getitem__(self, key):
        for item in self._data:
            if key == item.key:
                return item.value

        raise KeyError('Ne postoji element sa ključem %s' % str(key))

    def __setitem__(self, key, value):
        for item in self._data:
            if key == item.key:
                item.value = value
                return

        # element nije pronađen, zapiši ga u mapu
        self._data.append(MapElement(key, value))

    def __delitem__(self, key):
        length = len(self._data)
        for i in range(length):
            if key == self._data[i].key:
                self._data.pop(i)
                return

        raise KeyError('Ne postoji element sa ključem %s' % str(key))

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        for item in self._data:
            if key == item.key:
                return True

        return False

    def __iter__(self):
        for item in self._data:
            yield item.key

    def items(self):
        for item in self._data:
            yield item.key, item.value

    def keys(self):
        keys = []
        for key in self:
            keys.append(key)

        return keys

    def values(self):
        values = []
        for key in self:
            values.append(self[key])

        return values

    def clear(self):
        self._data = []


if __name__ == '__main__':
    table = Map()
    table[3] = 10
    table['x'] = 11
    table['asd'] = 'abcdefg'

    # pristup elementima
    print(table['asd'])
    print(table.values())
    print(table.keys())

    # metoda __contains__
    if 'y' in table:
        print('Tabela sadrži ključ y.')
    else:
        print('Tabela ne sadrži ključ y.')

    # iteracija kroz tabelu
    for item in table:
        print(item, table[item])

    # brisanje elementa
    del table['asd']
    print(len(table) == 2)

    # clear metoda
    table.clear()
    print(len(table) == 0)

class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity):
        
        self.min_capacity = MIN_CAPACITY
        if capacity > self.min_capacity:
            self.capacity = capacity
        else:
            self.capacity = self.min_capacity
        self.data = [None] * self.capacity
        self.size = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        Implement this.
        """
        return self.size/self.capacity


    def fnv1(self, key):
        hval = 0x811c9dc5
        fnv_32_prime = 0x01000193
        uint32_max = 2 ** 32
        for s in key:
            hval = hval ^ ord(s)
            hval = (hval * fnv_32_prime) % uint32_max
        return hval


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity

    def put(self, key, value):
       
        index = self.hash_index(key)
        if(self.data[index] == None):
            self.data[index] = HashTableEntry(key, value)
            self.size +=1
        else:
            curr = self.data[index]
            while curr.next != None and curr.key != key:
                curr = curr.next
            if curr.key == key:
                curr.value = value
            else:
                new_entry = HashTableEntry(key, value)
                new_entry.next = self.data[index]
                self.data[index] = new_entry
                self.size +=1
        if self.get_load_factor() > .7:
            self.resize(self.capacity * 2)


    def delete(self, key):

        index = self.hash_index(key)
        if self.data[index].key == key:
            if self.data[index].next == None:
                self.data[index] = None
                self.size -=1
            else:
                new_head = self.data[index].next
                self.data[index].next = None
                self.data[index] = new_head
                self.size -=1
        else:
            if self.data[index] == None:
                return None
            else:
                curr = self.data[index]
                prev = None
                while curr.next is not None and curr.key != key:
                    prev = curr
                    curr = curr.next
                if curr.key == key:
                    prev.next = curr.next
                    self.size -=1
                    return curr.value
                else:
                    return None
        
        if self.get_load_factor() < .2:
            if self.capacity/2 > 8:
                self.resize(self.capacity//2)
            elif self.capacity > 8:
                self.resize(8)


    def get(self, key):
        index = self.hash_index(key)
        if self.data[index] is not None and self.data[index].key == key:
            return self.data[index].value
        elif self.data[index] is None:
            return None
        else:
            curr = self.data[index]
            while curr.next != None and curr.key != key:
                curr = self.data[index].next
            if curr == None:
                return None
            else:
                return curr.value
 

    def resize(self, new_capacity):
        old_table = self.data[:]
        self.capacity = new_capacity
        self.data = [None] * new_capacity
        for i in range(len(old_table)):
            if old_table[i] is not None:
                if old_table[i].next is not None:
                    curr = old_table[i]
                    while curr.next is not None:
                        self.put(curr.key, curr.value)
                        curr = curr.next
                    self.put(curr.key, curr.value)
                else:
                    self.put(old_table[i].key, old_table[i].value)



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

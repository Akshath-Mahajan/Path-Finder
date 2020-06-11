class minHeap():
    def __init__(self):
        self.ID_TO_INDEX = {}
        self.arr = []
        #Example = [4,4,8,9,4,12,9,11,13]
        # parent(i) = i//2
        # children(i) = 2i, 2i+1
    def __str__(self):
        return str(self.arr)
    def __repr__(self):
        return self.arr
    def __len__(self):
        return len(self.arr)
    
    def get_parent_index(self, index):
        '''
            Input: Index of a node
            Result: Index of it's parent
            Note: For index of root, index of parent = -1
        '''
        if index == 0:
            return -1
        if index%2 == 0:
            return index//2 - 1
        if index%2 == 1:
            return index//2

    def get_children_indices(self, index):
        '''
            Input: Index of a node
            Result: Indices of its children
        '''
        s = [2*index+1, 2*index + 2]
        
        if s[0] >= len(self.arr):
            s[0] = -1
        if s[1] >= len(self.arr):
            s[1] = -1
        
        return s

    def swap(self, inda, indb):
        '''
            Input: Two indices
            Result: Swaps elements at those two indices in place
        '''
        self.ID_TO_INDEX[self.arr[inda][1]], self.ID_TO_INDEX[self.arr[indb][1]] = self.ID_TO_INDEX[self.arr[indb][1]], self.ID_TO_INDEX[self.arr[inda][1]]
        self.arr[inda], self.arr[indb] = self.arr[indb], self.arr[inda]
        
        return True


    def get_indexofsmallerchild(self, indPar):
        '''
            Input: Parent Index
            Result: Index of smaller child
        '''
        a,b = self.get_children_indices(indPar)
        if a == -1 and b == -1:
            return -1
        if a == -1:
            return b
        if b == -1:
            return a

        if self.arr[a] < self.arr[b]:
            return a
        else:
            return b


    def insert(self, item):
        '''
            Input: Item
            Result: Puts item in right place in heap while taking O(logN) time
        '''
        self.arr.append(item)
        indItem = len(self.arr) - 1
        self.ID_TO_INDEX[item[1]] = indItem
        indPar = self.get_parent_index(indItem)
        if indPar == -1:
            return True

        temp = self.arr[indPar]

        while(item < temp):
            self.swap(indItem, indPar)
            indItem = indPar
            indPar = self.get_parent_index(indItem)
            if indPar == -1:
                return True
            temp = self.arr[indPar]

        return True

    def extract_min(self):
        '''
            Input: None
            Result: Deletes and returns the smallest element in minheap while keeping heap structure intact
        '''
        ans = self.arr[0]
        self.swap(0, len(self.arr) - 1)
        del(self.arr[len(self.arr) - 1])
        #Bubble down
        indcurrent = 0
        indsmaller = self.get_indexofsmallerchild(indcurrent)
        if indsmaller == -1:
            return ans
        while self.arr[indcurrent] > self.arr[indsmaller]:
            self.swap(indcurrent, indsmaller)
            indcurrent = indsmaller
            indsmaller = self.get_indexofsmallerchild(indcurrent)
            if indsmaller == -1:
                break
        return ans
    def accessmin(self):
        if len(self.arr) == 0:
            return 0
        ans = self.arr[0]
        return ans
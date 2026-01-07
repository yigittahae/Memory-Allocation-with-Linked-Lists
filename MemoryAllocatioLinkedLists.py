class FreeBlock:   #a single free memory block in a linked list
    def __init__(self, start, size):
        self.start = start #starting address of the free block
        self.size = size #size of the free block
        self.next = None     #pointer to the next free block


class LinkedListAllocator:
    def __init__(self):
        self.head = FreeBlock(0, 100) 
        self.last = self.head # pointer for next fit allocation
        self.allocated = []

    def merge(self): #merge adjacent free blocks
        current = self.head
        while current and current.next: # while there is a next block
            if current.start + current.size == current.next.start: #adjacent blocks
                current.size += current.next.size #merge sizes
                current.next = current.next.next  #remove the next block
            else:
                current = current.next #move to the next block

    def free(self, start, size): #free a block of memory and add it back to the free list
        node = FreeBlock(start, size)  #create a new free block

        if self.head is None or start < self.head.start: #insert at the beginning
            node.next = self.head 
            self.head = node 
        else:
            current = self.head
            while current.next and current.next.start < start: #find the correct position to insert
                current = current.next 
            node.next = current.next
            current.next = node

        self.merge() #merge consecutive free blocks after the insertion operation

    #  BEST FIT 
    def allocate_bestfit(self, size):
        best = None
        best_prev = None
        prev = None
        current = self.head 
         # traverse the free list to find the best fit block

        while current: # traverse the free list
            if current.size >= size: # block is large enough
                if best is None or current.size < best.size: # check if it's the best fit so far
                    best = current      
                    best_prev = prev  # keep track of the previous block
            prev = current  # move to the next block
            current = current.next  # move to the next block

        if best is None:# no suitable block found
            return None # allocation fails

        start = best.start  # allocate memory from the best fit block
        best.start += size  # adjust the start of the free block
        best.size -= size # adjust the size of the free block

        if best.size == 0:# if the block is completely used up, remove it from the free list
            if best_prev: # if it's not the head
                best_prev.next = best.next # bypass the best block
            else: # if it's the head
                self.head = best.next

        self.allocated.append((start, size)) # keep track of allocated blocks
        return start  # return the starting address of the allocated block  

    #  WORST FIT 
    def allocate_worstfit(self, size): # allocate memory using the worst fit 
        worst = None  # the worst fit block
        worst_prev = None # the previous block of the worst fit
        prev = None # previous block during traversal
        current = self.head # start from the head of the free list

        # traverse the free list to find the worst fit block
        while current:
            if current.size >= size: # block is large enough
                if worst is None or current.size > worst.size: # check if it's the worst fit so far
                    worst = current
                    worst_prev = prev # keep track of the previous block
            prev = current # move to the next block
            current = current.next # move to the next block

        if worst is None: # no suitable block found
            return None # allocation fails

        start = worst.start # allocate memory from the worst fit block
        worst.start += size # adjust the start of the free block
        worst.size -= size # adjust the size of the free block

        if worst.size == 0: # if the block is completely used up, remove it from the free list
           if worst_prev: # if it's not the head
             worst_prev.next = worst.next # bypass the worst block
           else: # if it's the head
             self.head = worst.next

        self.allocated.append((start, size)) # keep track of allocated blocks
        return start # return the starting address of the allocated block

    #  NEXT FIT 
    def allocate_nextfit(self, size):
        current = self.last  # start from the last allocation point
        start_point = current  # save the starting point to detect full traversal
        prev = None  # previous block during traversal

        while True:
            if current.size >= size:  # block is large enough
                start = current.start  # allocate memory from the current block
                current.start += size  # adjust the start of the free block
                current.size -= size  # adjust the size of the free block
                self.last = current  # update the last allocation point

                if current.size == 0:  # if the block is completely used up, remove it from the free list
                    if prev:  # if it's not the head
                        prev.next = current.next  # bypass the current block
                    else:  # if it's the head
                        self.head = current.next

                self.allocated.append((start, size))  # keep track of allocated blocks
                return start  # return the starting address of the allocated block

            prev = current  # move to the next block
            current = current.next if current.next else self.head  # wrap around to head if at end
            if current == start_point:  # if we've wrapped around to the starting point
                break  # allocation fails, exit loop

        return None  # no suitable block found
    
def print_free_list(allocator, name): # print the current free list of the allocator
    current = allocator.head # start from the head
    blocks = [] # list to store block representations
    while current: # traverse all blocks
        blocks.append(f"[{current.start},{current.size}]") # format each block
        current = current.next # move to next block
    print(f"{name} Free List:", " -> ".join(blocks)) # print formatted free list


def run_allocation_trace(): # trace allocation/deallocation steps for all three strategies
    sequence = [10, 5, 20, -5, 12, -10, 8, 6, 7, 3, 10] # positive = allocate, negative = free

    print("\n BEST FIT TRACE ") # header for best fit test
    best = LinkedListAllocator() # create allocator instance
    allocated_best = [] # track allocated blocks

    for step in sequence: # process each operation
        if step > 0: # allocation operation
            addr = best.allocate_bestfit(step) # allocate using best fit
            allocated_best.append((addr, step)) # track allocation
            print(f"Allocate {step}") # log operation
        else: # deallocation operation
            size = -step # convert negative to positive size
            for i, (addr, s) in enumerate(allocated_best): # find matching block
                if s == size: # size matches
                    best.free(addr, s) # free the block
                    allocated_best.pop(i) # remove from tracking
                    print(f"Free {size}") # log operation
                    break # exit loop after freeing
        print_free_list(best, "Best Fit") # print current free list state

    print("\n WORST FIT TRACE ") # header for worst fit test
    worst = LinkedListAllocator() # create allocator instance
    allocated_worst = [] # track allocated blocks

    for step in sequence: # process each operation
        if step > 0: # allocation operation
            addr = worst.allocate_worstfit(step) # allocate using worst fit
            allocated_worst.append((addr, step)) # track allocation
            print(f"Allocate {step}") # log operation
        else: # deallocation operation
            size = -step # convert negative to positive size
            for i, (addr, s) in enumerate(allocated_worst): # find matching block
                if s == size: # size matches
                    worst.free(addr, s) # free the block
                    allocated_worst.pop(i) # remove from tracking
                    print(f"Free {size}") # log operation
                    break # exit loop after freeing
        print_free_list(worst, "Worst Fit") # print current free list state

    print("\n NEXT FIT TRACE ") # header for next fit test
    nextfit = LinkedListAllocator() # create allocator instance
    allocated_next = [] # track allocated blocks

    for step in sequence: # process each operation
        if step > 0: # allocation operation
            addr = nextfit.allocate_nextfit(step) # allocate using next fit
            allocated_next.append((addr, step)) # track allocation
            print(f"Allocate {step}") # log operation
        else: # deallocation operation
            size = -step # convert negative to positive size
            for i, (addr, s) in enumerate(allocated_next): # find matching block
                if s == size: # size matches
                    nextfit.free(addr, s) # free the block
                    allocated_next.pop(i) # remove from tracking
                    print(f"Free {size}") # log operation
                    break # exit loop after freeing
        print_free_list(nextfit, "Next Fit") # print current free list state

import random  # used to generate random allocation sizes

def run_fragmentation_test():
    print("\n FRAGMENTATION TEST ")

    # Tests how an allocation strategy behaves under fragmentation
    def test_allocator(name, alloc_func):
        allocator = LinkedListAllocator()  # create a new memory allocator
        allocated = []  # list to store allocated blocks (address, size)

        # 1️⃣ Perform 12 random allocations (sizes between 3 and 12)
        for _ in range(12):
            size = random.randint(3, 12)  # generate random size
            addr = alloc_func(allocator, size)  # allocate memory
            if addr is not None:
                allocated.append((addr, size))  # store successful allocation

        # 2️⃣ Free exactly 4 randomly chosen allocated blocks
        random.shuffle(allocated)  # randomize allocated blocks
        for _ in range(4):
            addr, size = allocated.pop()  # remove one allocated block
            allocator.free(addr, size)  # free the memory block

        # 3️⃣ Try to allocate one large block of size 25
        result = alloc_func(allocator, 25)

        # Print the final state of the free list
        print(f"\n{name} Final Free List:")
        current = allocator.head
        while current:
            print(f"[start={current.start}, size={current.size}]", end=" -> ")
            current = current.next
        print("NULL")

        # Print whether the large allocation succeeded
        if result is None:
            print(f"{name}: FAILED to allocate size 25")
        else:
            print(f"{name}: SUCCESS allocating size 25 at address {result}")

    random.seed(42)  # fixed seed for reproducible results

    # Run fragmentation test for each allocation strategy
    test_allocator("Best Fit", lambda a, s: a.allocate_bestfit(s))
    test_allocator("Worst Fit", lambda a, s: a.allocate_worstfit(s))
    test_allocator("Next Fit", lambda a, s: a.allocate_nextfit(s))


import time   # used to measure execution time
import random

def run_speed_test():
    print("\n SPEED TEST ")

    # Measures the speed of an allocation strategy
    def speed_test(name, alloc_func):
        allocator = LinkedListAllocator()  # create allocator
        allocated = []  # track allocated blocks

        start_time = time.time()  # start timing

        # Perform repeated allocation and deallocation
        for _ in range(200):
            size = random.randint(1, 10)  # random allocation size
            addr = alloc_func(allocator, size)  # allocate memory

            if addr is not None:
                allocated.append((addr, size))  # store allocated block

            # Free the oldest allocated block (FIFO)
            if allocated:
                addr, size = allocated.pop(0)
                allocator.free(addr, size)

        elapsed = time.time() - start_time  # calculate elapsed time
        print(f"{name} Time: {elapsed:.6f} seconds")
        return elapsed

    random.seed(1)  # fixed seed for consistent timing

    # Run speed test for each allocation strategy
    t1 = speed_test("Best Fit", lambda a, s: a.allocate_bestfit(s))
    t2 = speed_test("Worst Fit", lambda a, s: a.allocate_worstfit(s))
    t3 = speed_test("Next Fit", lambda a, s: a.allocate_nextfit(s))

    print("\nRESULT:")
    fastest = min((t1, "Best Fit"), (t2, "Worst Fit"), (t3, "Next Fit"))
    slowest = max((t1, "Best Fit"), (t2, "Worst Fit"), (t3, "Next Fit"))

    print(f"Fastest: {fastest[1]}")
    print(f"Slowest: {slowest[1]}")


if __name__ == "__main__":
    run_allocation_trace()
    run_fragmentation_test()
    run_speed_test()
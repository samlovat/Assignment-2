from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # initialize global variables
        self.cache = []
        self.page_frames = frames
        self.total_reads = 0
        self.total_writes = 0
        self.total_faults = 0
        self.debug = 0
        self.hand = 0

    def check_loaded(self, searched_page_number, action):
        """
        Checks if the cache has the given page number loaded, and if its a write action, sets the dirty bit to true.

        arguments:
            searched_page_number: number address of the page you check for
            action: 'w' or 'r'; write or read respectively

        returns:
            bool: true if the page number was found in the cache else false
        """
        
        # itterate through the pages in the cache
        for i, page in enumerate(self.cache):
            dirty, used, page_num = page
            # if the page of given number is found
            if page_num == searched_page_number:
                # if its a write action, mark it as dirty, in both cases set the use bit as true
                if action == "w":
                    self.cache[i] = (True, True, page_num)
                else:
                    self.cache[i] = (dirty, True, page_num)
                return True
            
        # report a page fault
        print("Page Fault! ") if self.debug == 1 else None
        self.total_faults += 1
        return False
    
    def insert_page(self, page_number, action):
        """
        insert the given page number into the cache using the clockMMU algorithm.

        arguments:
            page_number: page number to be inserted into the cache
            action: 'w' or 'r'; write or read respectively

        returns:
            ~void~
        """
        
        # dirty bit is true if action is write else false
        new_dirty = action == "w"

        # report a read
        self.total_reads += 1

        # if cache is full
        if len(self.cache) == self.page_frames:
            # while a space to insert the new page is not found
            space_found = False
            while not space_found:
                # itterate through pages cyclically, and insert the new page if a space with used = False, 
                # flipping used along the way if used = true.
                is_dirty, used, page_num = self.cache[self.hand]
                if used:
                    # flip used bit
                    self.cache[self.hand] = (is_dirty, False, page_num)
                else:
                    print("Victim: ", is_dirty, page_num) if self.debug == 1 else None
                    if is_dirty == 1:
                        # If the page was dirty, make the write before overwriting it
                        self.total_writes += 1
                        print("Had to write to disk!") if self.debug == 1 else None
                    # overwrite the page in the cache
                    self.cache[self.hand] = (new_dirty, True, page_number)
                    space_found = True
                # move the clock hand up one, cyclically.
                self.hand = (self.hand + 1) % len(self.cache)

        else:
            # if the cache wasnt full just push the page to the end of it.
            self.cache.append((new_dirty, True, page_number))

        print("updated: ", new_dirty, page_number) if self.debug == 1 else None

    def read_memory(self, page_number):
        """
        read a page of given address into the cache using the read action

        arguments:
            page_number: page number address to be inserted

        returns:
            ~void~
        """
        if self.debug == 1:
            print("\nRequested Action: Read ", page_number)
            self.print_cache()
        # if the page is not already in the cache
        if self.check_loaded(page_number, "r") == False:
            # load it into the cache with the read action
            self.insert_page(page_number, "r")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)
        
    def write_memory(self, page_number):
        """
        read a page of given address into the cache using the read action

        arguments:
            page_number: page number address to be inserted

        returns:
            ~void~
        """

        if self.debug == 1:
            print("\nRequested Action: Write ", page_number)
            self.print_cache()
        # if the page is not already in the cache
        if self.check_loaded(page_number, "w") == False:
            # write it into the cache with the write action
            self.insert_page(page_number, "w")
        else:
            # check_loaded also adjusts the dirty bit appropriately if found
            if self.debug == 1:
                print("Page Hit! ", page_number)

    def set_debug(self):
        self.debug = 1

    def reset_debug(self):
        self.debug = 0

    def print_cache(self):
        print("Current cache:")
        for dirty, used, page in self.cache:
            print(dirty, " , ", used, " , ", page)
        print("\n")

    def get_total_disk_reads(self):
        return self.total_reads

    def get_total_disk_writes(self):
        return self.total_writes

    def get_total_page_faults(self):
        return self.total_faults
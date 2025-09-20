from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # Use a cache (queue)
        self.cache = []
        self.page_frames = frames
        self.total_reads = 0
        self.total_writes = 0
        self.total_faults = 0
        self.debug = 0

    def check_loaded(self, searched_page_number, action):
        """
        Checks if the cache has the given page number loaded, and if its a write action, sets the dirty bit to true.
        Also if found, moves the item to the top of the queue as the most recently used page.

        arguments:
            searched_page_number: number address of the page you check for
            action: 'w' or 'r'; write or read respectively

        returns:
            bool: true if the page number was found in the cache else false
        """

        # itterate through the pages in the cache
        for page in self.cache:
            dirty, page_num = page
            if page_num == searched_page_number:
                # If writing, mark dirty
                if action == "w":
                    dirty = True
                # Move this entry to the end (most recently used)
                self.cache.remove(page)
                self.cache.append((dirty, page_num))
                return True
                    
        # report a page fault
        print("Page Fault! ") if self.debug == 1 else None
        self.total_faults += 1
        return False
    
    def insert_page(self, page_number, action):
        """
        insert the given page number into the cache using the LRUMMU algorithm.

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
            # get first entry in the cache and check if its dirty
            top_dirty, top_page = self.cache[0]
            print("Victim: ", top_dirty, top_page) if self.debug == 1 else None
            # if that least recently used page is dirty
            if top_dirty == 1:
                # If the page was dirty, make the write before overwriting it
                self.total_writes += 1
                print("Had to write to disk!") if self.debug == 1 else None
                
            # remove the least recently used page
            self.cache.pop(0) 
            # add our new page to the top of the cache as the new most recently used page
            self.cache.append((new_dirty, page_number))
        else:
            # Else just push to top of cache
            self.cache.append((new_dirty, page_number))

        print("Push_front: ", new_dirty, page_number) if self.debug == 1 else None

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
        for dirty, page in self.cache:
            print(dirty, " , ", page)
        print("\n")

    def get_total_disk_reads(self):
        return self.total_reads

    def get_total_disk_writes(self):
        return self.total_writes

    def get_total_page_faults(self):
        return self.total_faults
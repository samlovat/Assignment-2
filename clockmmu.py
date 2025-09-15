from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # Use a cache (queue)
        self.cache = []
        self.page_frames = frames
        self.total_reads = 0
        self.total_writes = 0
        self.total_faults = 0
        self.debug = 0
        self.hand = 0

    def check_loaded(self, searched_page_number, action):
        # Function which checks if requested page is already loaded 
        for i, page in enumerate(self.cache):
            dirty, used, page_num = page
            if page_num == searched_page_number:
                # If writing, mark dirty
                if action == "w":
                    self.cache[i] = (True, False, page_num)
                return True
            
        print("Page Fault! ") if self.debug == 1 else None
        self.total_faults += 1
        return False
    
    def insert_page(self, page_number, action):
        # Set inserted page's dirty bit according to action called
        new_dirty = action == "w"

        self.total_reads += 1
        # if cache is full
        if len(self.cache) == self.page_frames:
            clocked = False
            while not clocked:
                is_dirty, used, page_num = self.cache[self.hand]
                if used:
                    self.cache[self.hand] = (is_dirty, False, page_number)
                else:
                    print("Victim: ", is_dirty, page_num) if self.debug == 1 else None
                    if is_dirty == 1:
                        # If victim has dirty bit flipped, write to disk before popping from cache
                        print("Had to write to disk!") if self.debug == 1 else None
                        self.total_writes += 1
                    self.cache[self.hand] = (new_dirty, True, page_number)
                    clocked = True
                
                self.hand = (self.hand + 1) % len(self.cache)

        else:
            # Else just push to top of cache
            self.cache.append((new_dirty, True, page_number))

        print("updated: ", new_dirty, page_number) if self.debug == 1 else None

    def read_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Read ", page_number)
            self.print_cache()
        if self.check_loaded(page_number, "r") == False:
            self.insert_page(page_number, "r")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)
        
    def write_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Write ", page_number)
            self.print_cache()
        if self.check_loaded(page_number, "w") == False:
            self.insert_page(page_number, "w")
        else:
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
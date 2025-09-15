from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        # Use a cache (queue)
        self.cache = []
        self.page_frames = frames
        self.total_reads = 0
        self.total_writes = 0
        self.total_faults = 0
        self.debug = 0

    def check_loaded(self, searched_page_number, action):
        # Function which checks if requested page is already loaded 

        counter = 0
        for page in self.cache:
            dirty, page_num = page
            counter += 1
            if page_num == searched_page_number:

                
                dirty = 1 if action == "w" else None

                if counter != 1:
                    # Move to top of cache
                    self.cache.remove(page)
                    self.cache.append(page)
                    return True
        
        print("Page Fault! ") if self.debug == 1 else None
        return False
    
    def insert_page(self, page_number, action):
        # Set inserted page's dirty bit according to action called
        self.total_faults += 1
        new_dirty = not action == "r"

        # if cache is full
        if len(self.cache) == self.page_frames:
            # get first entry in the cache and check if its dirty
            top_dirty, top_page = self.cache[0]
            print("Victim: ", top_dirty, top_page) if self.debug == 1 else None
            if top_dirty == 1:
                # If victim has dirty bit flipped, write to disk before popping from cache
                print("Had to write to disk!") if self.debug == 1 else None
                
                self.cache.pop(0) 
                self.cache.append((new_dirty, page_number))
        else:
            # Else just push to top of cache
            self.cache.append((new_dirty, page_number))

        print("Push_front: ", new_dirty, page_number) if self.debug == 1 else None

    def read_memory(self, page_number):
        self.total_reads += 1
        if self.debug == 1:
            print("\nRequested Action: Read ", page_number)
            self.print_cache()
        if self.check_loaded(page_number, "r") == False:
            self.insert_page(page_number, "r")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)
        

    def write_memory(self, page_number):
        self.total_writes += 1
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
        for dirty, page in self.cache:
            print(dirty, " , ", page)
        print("\n")

    def get_total_disk_reads(self):
        return self.total_reads

    def get_total_disk_writes(self):
        return self.total_writes

    def get_total_page_faults(self):
        return self.total_faults
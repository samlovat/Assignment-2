from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        # Use a cache (queue)
        self.cache = []
        self.pageFrames = frames
        self.totalReads = 0
        self.totalWrites = 0
        self.totalFaults = 0
        self.debug = 0

    def check_load(self, searched_page_number, action):
        # Function which checks if requested page is already loaded
        if action == "w":
            self.totalWrites += 1  
        counter = 0
        for page in self.cache[:]:
            dirty, page_num = page
            counter += 1
            if page_num == searched_page_number:
                if action == "r":
                    if counter != 1:
                        # Move to top of cache
                        self.cache.remove(page)
                        self.cache.append(page)
                    return True
                dirty = 1
                if counter != 1:
                        # Move to top of cache
                        self.cache.remove(page)
                        self.cache.append(page)
                return True
        if self.debug == 1:
            print("Page Fault! ")
        # self.totalFaults += 1
        self.totalReads += 1
        return False
    
    def insert_page(self, page_number, action):
        # Set inserted page's dirty bit according to action called
        self.totalFaults += 1
        newDirty = 1
        if action == "r":
            newDirty = 0
        if len(self.cache) == self.pageFrames:
            # Need to replace top page
            # Grab top of cache to check dirty bit
            topDirty, topPage = self.cache[0]
            if self.debug == 1:
                print("Victim: ", topDirty, topPage)
            if topDirty == 1:
                # If victim has dirty bit flipped, write to disk before popping from cache
                self.totalWrites += 1
                if self.debug == 1:
                    print("Had to write to disk!")
            self.cache.pop(0) 
            self.cache.append((newDirty, page_number))
        else:
            # Else just push to top of cache
            self.cache.append((newDirty, page_number))
        if self.debug == 1:
            print("Push_front: ", newDirty, page_number)

    def read_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Read ", page_number)
            self.print_cache()
        if self.check_load(page_number, "r") == False:
            self.insert_page(page_number, "r")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)
        

    def write_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Write ", page_number)
            self.print_cache()
        if self.check_load(page_number, "w") == False:
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
        return self.totalReads

    def get_total_disk_writes(self):
        return self.totalWrites

    def get_total_page_faults(self):
        return self.totalFaults
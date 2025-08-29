from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        # Use a stack
        self.stack = []
        self.pageFrames = frames
        self.totalReads = 0
        self.totalWrites = 0
        self.totalFaults = 0
        self.debug = 0

    def check_load(self, searched_page_number, action):
        # Function which checks if requested page is already loaded
        counter = 0
        for page in self.stack[:]:
            dirty, page_num = page
            counter += 1
            if page_num == searched_page_number:
                if action == "r":
                    if counter != 1:
                        # Move to top of stack
                        self.stack.remove(page)
                        self.stack.append(page)
                    return True
                dirty = 1
                if counter != 1:
                        # Move to top of stack
                        self.stack.remove(page)
                        self.stack.append(page)
                return True
        self.totalFaults += 1
        self.totalReads += 1
        return False
    
    def insert_page(self, page_number, action):
        # Set inserted page's dirty bit according to action called
        if action == "r":
            newDirty = 0
        newDirty = 1
        if len(self.stack) == self.pageFrames:
            # Need to replace top page
            # Grab top of stack to check dirty bit
            topDirty, topPage = self.stack[-1]
            if topDirty == 1:
                # If victim has dirty bit flipped, write to disk before popping from stack
                self.totalWrites += 1
            self.stack.pop() 
            self.stack.append((newDirty, page_number))
        # Else just push to top of stack
        self.stack.append((newDirty, page_number))

    def read_memory(self, page_number):
        if self.check_load(page_number, "r") == False:
            self.insert_page(page_number, "r")
        

    def write_memory(self, page_number):
        if self.check_load(page_number, "w") == False:
            self.insert_page(page_number, "w")

    def set_debug(self):
        self.debug = 1

    def reset_debug(self):
        self.debug = 0

    def get_total_disk_reads(self):
        return self.totalReads

    def get_total_disk_writes(self):
        return self.totalWrites

    def get_total_page_faults(self):
        return self.totalFaults
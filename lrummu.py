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
        if self.debug == 1:
            print("Page Fault! ")
        self.totalFaults += 1
        self.totalReads += 1
        return False
    
    def insert_page(self, page_number, action):
        # Set inserted page's dirty bit according to action called
        newDirty = 1
        if action == "r":
            newDirty = 0
        if len(self.stack) == self.pageFrames:
            # Need to replace top page
            # Grab top of stack to check dirty bit
            topDirty, topPage = self.stack[0]
            if self.debug == 1:
                print("Victim: ", topDirty, topPage)
            if topDirty == 1:
                # If victim has dirty bit flipped, write to disk before popping from stack
                self.totalWrites += 1
                if self.debug == 1:
                    print("Had to write to disk!")
            self.stack.pop(0) 
            self.stack.append((newDirty, page_number))
        else:
            # Else just push to top of stack
            self.stack.append((newDirty, page_number))
        if self.debug == 1:
            print("Push_front: ", newDirty, page_number)

    def read_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Read ", page_number)
            self.print_stack()
        if self.check_load(page_number, "r") == False:
            self.insert_page(page_number, "r")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)
        

    def write_memory(self, page_number):
        if self.debug == 1:
            print("\nRequested Action: Write ", page_number)
            self.print_stack()
        if self.check_load(page_number, "w") == False:
            self.insert_page(page_number, "w")
        else:
            if self.debug == 1:
                print("Page Hit! ", page_number)

    def set_debug(self):
        self.debug = 1

    def reset_debug(self):
        self.debug = 0

    def print_stack(self):
        print("Current stack:")
        for dirty, page in self.stack:
            print(dirty, " , ", page)
        print("\n")

    def get_total_disk_reads(self):
        return self.totalReads

    def get_total_disk_writes(self):
        return self.totalWrites

    def get_total_page_faults(self):
        return self.totalFaults
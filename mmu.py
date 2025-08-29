'''
* Interface for Memory Management Unit.
* The memory management unit should maintain the concept of a page table.
* As pages are read and written to, this changes the pages loaded into the
* the limited number of frames. The MMU keeps records, which will be used
* to analyse the performance of different replacement strategies implemented
* for the MMU.
*
'''
class MMU:

    def __init__(self):
        self.totalReads = 0
        self.totalWrites = 0
        self.totalFaults = 0
        self.debug = 0

    def read_memory(self, page_number):
        self.totalReads += 1

    def write_memory(self, page_number):
        self.totalWrites += 1

    def page_fault(self):
        self.totalFaults += 1

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

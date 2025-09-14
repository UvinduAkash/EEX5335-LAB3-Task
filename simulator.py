# Memory System Simulator

PAGE_SIZE = 1024        # 1 KB
VIRTUAL_ADDR_SPACE = 2**16   # 64 KB
PHYSICAL_MEMORY_SIZE = 32 * 1024  # 32 KB
NUM_FRAMES = PHYSICAL_MEMORY_SIZE // PAGE_SIZE
PAGE_TABLE_ENTRIES =  VIRTUAL_ADDR_SPACE // PAGE_SIZE  # 64 entries
TLB_SIZE = 8
CACHE_SIZE = 8  # number of blocks

# Data Structures 
page_table = [-1] * PAGE_TABLE_ENTRIES   # -1 means not loaded
tlb = []   # list of (virtual_page, frame)
cache = [] # list of physical block numbers (FIFO)

next_free_frame = 0

# Functions 

def get_page_offset(virtual_address):
    page = virtual_address // PAGE_SIZE
    offset = virtual_address % PAGE_SIZE
    return page, offset

def tlb_lookup(vpage):
    for vp, frame in tlb:
        if vp == vpage:
            return frame, True
    return -1, False

def tlb_update(vpage, frame):
    global tlb
    if len(tlb) >= TLB_SIZE:
        tlb.pop(0)   # FIFO remove oldest
    tlb.append((vpage, frame))

def page_table_lookup(vpage):
    global next_free_frame
    if vpage >= PAGE_TABLE_ENTRIES:
        print(f" -> Page Fault: Virtual Page {vpage} not in page table (exceeds {PAGE_TABLE_ENTRIES} entries)")
        return -1   # invalid page
    
    frame = page_table[vpage]
    if frame == -1:
        # page fault: load into next free frame
        if next_free_frame >= NUM_FRAMES:
            print(" -> Out of physical memory frames!")
            return -1
        frame = next_free_frame
        page_table[vpage] = frame
        next_free_frame += 1
    return frame

def cache_lookup(physical_address):
    block_number = physical_address // PAGE_SIZE
    if block_number in cache:
        return True
    else:
        if len(cache) >= CACHE_SIZE:
            cache.pop(0)  # FIFO
        cache.append(block_number)
        return False

# Simulator Process 
def access_address(virtual_address):
    vpage, offset = get_page_offset(virtual_address)
    
    # Step 1: TLB lookup
    frame, tlb_hit = tlb_lookup(vpage)
    
    if not tlb_hit:
        # Page table lookup
        frame = page_table_lookup(vpage)
        if frame == -1:
            print(f"Virtual Addr: {virtual_address} (Page {vpage}, Offset {offset})")
            print(" -> Access aborted due to invalid page.")
            print("-"*40)
            return
        # Update TLB
        tlb_update(vpage, frame)
    
    # Step 2: Form physical address
    physical_address = frame * PAGE_SIZE + offset
    
    # Step 3: Cache lookup
    cache_hit = cache_lookup(physical_address)
    
    # Step 4: Print results
    print(f"Virtual Addr: {virtual_address} (Page {vpage}, Offset {offset})")
    print(f" -> TLB {'Hit' if tlb_hit else 'Miss'}")
    print(f" -> Physical Addr: {physical_address} (Frame {frame})")
    print(f" -> Cache {'Hit' if cache_hit else 'Miss'}")
    print("-"*40)

#  Main 
if __name__ == "__main__":
    # Example: read addresses from file
    with open("input_addresses.txt", "r") as f:
        addresses = [int(line.strip(), 0) for line in f.readlines()]
        # int(..., 0) allows both decimal (1000) and hex (0x0100)

    for addr in addresses:
        access_address(addr)

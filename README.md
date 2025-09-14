# Memory System Simulator

This project simulates a simple memory management unit (MMU) with virtual memory, TLB (Translation Lookaside Buffer), and a small cache. It provides a step-by-step demonstration of how virtual addresses are translated into physical addresses and how TLB, page tables, and caches interact.

## Features

- *Page Table*: Simulates virtual-to-physical address translation.
- *TLB*: Implements a FIFO TLB for fast page lookups.
- *Cache*: Small FIFO cache simulates block-level memory access.
- *Read-Only*: All memory operations are read only (no write/dirty/protection bits).
- *Single Process*: Simulates a single process environment.
- *Input*: Reads virtual addresses (in decimal or hexadecimal) from a text file.

## System Parameters

| Parameter                | Value                                  |
|--------------------------|----------------------------------------|
| Page Size                | 1 KB (1024 bytes)                      |
| Virtual Address Space    | 16-bit (0 to 65535)                    |
| Physical Memory Size     | 32 KB (32,768 bytes)                   |
| Number of Frames         | 32                                     |
| Page Table Entries       | 64                                     |
| TLB Size                 | 8 entries (FIFO)                       |
| Cache Size               | 8 blocks (FIFO)                        |

## Assumptions

- Only one process is simulated.
- All memory operations are read only.
- Address translation follows standard MMU logic.
- Input addresses can be decimal or hexadecimal (1000, 0x1000, etc).
- Output shows TLB hit/miss, physical address, and cache hit/miss for each access.

## Input Format

- Create a file named input_addresses.txt in the root directory.
- Each line contains a single virtual address (decimal or hexadecimal).

*Example:*

100
160
400
0x500
1024
0xFFFF


## Usage

1. *Prepare Input*
   - Place all virtual addresses to be tested in input_addresses.txt.

2. *Run the Simulator*
   - Execute the Python script:
     bash
     python memory_simulator.py
     
   - (Rename the provided code file to memory_simulator.py if needed.)

3. *Interpret Output*
   - For each address, you will see:
     - Virtual address, page, and offset
     - TLB hit/miss
     - Physical address and frame number
     - Cache hit/miss
     - Page faults and out-of-memory errors, if any

*Sample Output:*

Virtual Addr: 100 (Page 0, Offset 100)
 -> TLB Miss
 -> Physical Addr: 100 (Frame 0)
 -> Cache Miss
----------------------------------------
Virtual Addr: 160 (Page 0, Offset 160)
 -> TLB Hit
 -> Physical Addr: 160 (Frame 0)
 -> Cache Miss
----------------------------------------
...


## File Overview

- memory_simulator.py: Main simulator code.
- input_addresses.txt: List of virtual addresses to access.
- README.md: Documentation (this file).

## How Address Translation Works

1. *TLB Lookup*
   - If the virtual page is in TLB, get the frame directly (TLB hit).
   - Otherwise, check page table (TLB miss).

2. *Page Table Lookup*
   - If the page is not loaded (page fault), load into next free frame.
   - Update TLB with new mapping.

3. *Physical Address Formation*
   - Frame number combined with offset gives physical address.

4. *Cache Lookup*
   - Physical address block checked in cache.
   - FIFO replacement if cache is full.

## Customization

Modify system parameters (page size, cache size, TLB size, etc.) by editing the respective variables at the top of memory_simulator.py.

## License

This project is provided for educational purposes. No warranty or guarantee is implied.

---

# Memory Allocation with Linked Lists

In this project, I implemented three memory allocation strategies using a linked list:
Best Fit, Worst Fit, and Next Fit.

The main purpose of this project is to understand how different allocation algorithms
affect memory fragmentation and allocation performance through simple experiments.

---

## Experiments 
This project includes the following experiments:
1. Allocation Tracking (first 15 allocation outputs)
2. Speed ​​Test (time comparison)
3. Fragmentation Test (post-release block analysis)

The results are shown in the terminal for a summary of its outcome.
Tested with Python 3.10.

## Project Structure

This project is kept simple and consists of only two files:

- main.py: contains all allocation algorithms and test cases
- README.md: explains how to run and understand the project

---

## How the Program Works

The program simulates a memory of size 100 and manages free memory blocks using a
linked list. Memory is allocated and freed according to the selected allocation strategy.

I tested the behavior of each strategy using three experiments:

- allocation trace
- fragmentation test
- speed test

---

## How to Run

Make sure Python 3 is installed.

Then run the program using:

python main.py

No external libraries are required.

---



## Notes

This project was created for an Operating Systems assignment to better understand
dynamic memory allocation and external fragmentation.

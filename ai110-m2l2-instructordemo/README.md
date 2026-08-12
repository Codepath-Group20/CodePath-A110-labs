# AI110 Module 2 Lesson 2 - Python Optimization Demo

This repository contains a demonstration of Python code optimization techniques, specifically focusing on data structure performance comparisons for lookup operations.

## Overview

The demo showcases the performance difference between using lists and sets for membership testing in Python. This is a common optimization scenario where choosing the right data structure can dramatically improve performance.

## Code Structure

- `demo_optimization.py` - Main demonstration script containing performance comparison code

## What the Demo Shows

The application demonstrates:

1. **Inefficient List Lookup**: Using `in` operator on a list for membership testing
2. **Performance Measurement**: Using Python's `timeit` module to measure execution time
3. **Optimization Opportunity**: How data structure choice affects performance

### Key Concepts Demonstrated

- **Time Complexity**: List lookup is O(n) vs Set lookup is O(1) average case
- **Performance Profiling**: Measuring and comparing execution times
- **Memory vs Speed Trade-offs**: Understanding when to optimize for different metrics

## Sample Data

The demo uses:

- A large list of 10,000 random integers (0-100,000)
- 1,000 query integers for lookup operations

## Usage

```python
python demo_optimization.py
```

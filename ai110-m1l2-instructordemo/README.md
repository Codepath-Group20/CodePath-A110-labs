# Grade Parser

A simple Python application that processes student grades and calculates grade statistics.

## Overview

The Grade Parser is a utility tool designed to parse student grade data from formatted strings and provide statistical summaries including total scores, student count, and average grade.

## Features

- Parse student grades from "StudentName:Score" format
- Calculate total scores across all students
- Count number of students
- Compute average grade
- Simple and lightweight implementation

## Usage

### Basic Usage

The main function `process_grades()` takes a list of grade strings and returns a summary dictionary:

```python
from grade_parser import process_grades

# Example grade data
grades = [
    "Alice:85",
    "Bob:92", 
    "Charlie:78"
]

# Process the grades
result = process_grades(grades)
print(result)
```

### Expected Output

```python
{
    "total": 255,
    "count": 3,
    "average": 85.0
}
```

## Input Format

Grade entries should follow the format: `"StudentName:Score"`

- **StudentName**: The student's name (string)
- **Score**: The numerical grade (should be convertible to integer/float)

## File Structure

```text
├── grade_parser.py    # Main application file
└── README.md         # This documentation
```

## Running the Application

1. Ensure you have Python installed (Python 3.x recommended)
2. Navigate to the project directory
3. Run the script:

   ```bash
   python grade_parser.py
   ```

## Example

The application includes test data that demonstrates its functionality:

```python
class_data = [
    "Alice:85",
    "Bob:92", 
    "Charlie:78"
]

result = process_grades(class_data)
# Output: {'total': 255, 'count': 3, 'average': 85.0}
```

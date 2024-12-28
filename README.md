# Starship Programming Language

Welcome! This is a custom programming language designed for space-themed computation and data manipulation, featuring a unique syntax that combines readability with operability.

PLay around with the language [here](https://starship.streamlit.app).

Note: This project was inspired by the Muffin Programming Language.

## Overview

Starship is a domain-specific language that uses space-themed keywords and constructs to perform computations, handle data structures, and manage program flow. It features strong typing, array operations, quantum (random) number generation, and structured program organization.

### Why Starship?

I love space. I love programming. I love the idea of a space-themed programming language.

Plus, this was something new to me. My previous projects largely revolved around streamlit web apps and applying data anlysis tensorflow models to some aspect of our lives. Creating my own language led to many technical hurdles that I had to overcome. I also felt in-control: I could do whatever I wanted, and so felt more creative and motivated to continue.


## Language Structure

### Program Structure
Every Starship program follows this basic structure:

```
MISSION: ProgramName

    CARGO:
        # Variable declarations

    [QUANTUM:]
        # Optional quantum (random) variables

    FLIGHT_PLAN:
        # Numbered instructions

END_MISSION
```

### Data Types
- `METRIC`: Numbers (integers/floats)
- `SIGNAL`: Strings
- `CONSTELLATION`: Arrays
- `QUANTUM`: Random number generators

### Basic Operations

#### Variable Operations

```
EXTRACT source INTO target   # Assignment

BEAM value to DISPLAY        # Output to console
```

#### Mathematical Operations

```
BOOST x with y INTO z        # Multiplication: z = x * y

DOCK x with y INTO z         # Addition: z = x + y

UNDOCK x with y INTO z       # Subtraction: z = x - y

SPLIT x with y INTO z        # Division: z = x / y
```

#### Array Operations

```
EXTRACT array[0] INTO x      # Get array element

APPEND value TO array        # Add to array

array = [] as CONSTELLATION  # Create empty array
```

#### Control Flow

```
ORBIT count TIMES:           # Loop count times
    # Numbered instructions
```

## Example Programs

### 1. Factorial Calculator

```
MISSION: FactorialCalculator

    CARGO:
        number = 5 as METRIC
        result = 1 as METRIC
        counter = 1 as METRIC

    FLIGHT_PLAN:
        ORBIT number TIMES:
        BOOST result with counter INTO result
        DOCK counter with 1 INTO counter
        BEAM result to DISPLAY

END_MISSION
```

Output:

```
🚀 Mission completed successfully!

1

2

6

24

120
```

### 2. Random Number Generator

```
MISSION: RandomGenerator

    CARGO:
        results = [] as CONSTELLATION
        iterations = 2 as METRIC

    QUANTUM:
        random_range = UNCERTAIN(1, 100)

    FLIGHT_PLAN:
        1. ORBIT iterations TIMES:
            2. EXTRACT random_range INTO current
            3. APPEND current TO results
            4. BEAM current to DISPLAY

END_MISSION
```

Output:
(NOTE: The output is random and will vary.)

```
🚀 Mission completed successfully!

36.1470344818951

Quantum states stabilized.

-77.22467544708145

-92.61306865792709

6.876652546001278

Quantum states stabilized.

-25.271289187128154

28.33861312596064
```

### 3. Array Operations

```
MISSION: ArrayManipulator

    CARGO:
        numbers = [1, 2, 3, 4, 5] as CONSTELLATION
        squares = [] as CONSTELLATION

    FLIGHT_PLAN:
        1. BEAM "Original array:" to DISPLAY
        2. BEAM numbers to DISPLAY
        3. ORBIT 5 TIMES:
            4. EXTRACT numbers[index] INTO temp
            5. BOOST temp with temp INTO temp
            6. APPEND temp TO squares
        7. BEAM "Squared array:" to DISPLAY
        8. BEAM squares to DISPLAY

END_MISSION
```

Output:

```
🚀 Mission completed successfully!

Original array:
[1, 2, 3, 4, 5]

Squared array:
[1, 4, 9, 16, 25]

Sum of squares:
55
```

## Error Handling

The language includes comprehensive error handling with descriptive messages:
- Syntax errors
- Type mismatches
- Array index out of bounds
- Division by zero
- Invalid operations
- Missing required components

Errors include line numbers and detailed messages for easy debugging:

```
🚨 MISSION FAILURE at line 5: Cannot split by zero
```

## Interactive Environment

The language includes a Streamlit-based interactive environment with:
- Code editor with syntax highlighting
- Example program templates
- Real-time execution
- Quick reference documentation
- Visual output display

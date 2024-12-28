import streamlit as st
from lexer import StarshipLexer
from parser import StarshipParser
from interpreter import StarshipRuntime
from errors import StarshipError

FACTORIAL_EXAMPLE = """MISSION: FactorialCalculator

    CARGO:
        number = 5 as METRIC
        result = 1 as METRIC
        counter = 1 as METRIC

    FLIGHT_PLAN:
        1. ORBIT number TIMES:
            2. BOOST result with counter INTO result
            3. DOCK counter with 1 INTO counter
            4. BEAM result to DISPLAY

END_MISSION"""

QUANTUM_EXAMPLE = """MISSION: RandomGenerator

    CARGO:
        results = [] as CONSTELLATION
        iterations = 2 as METRIC
        current = 0 as METRIC

    QUANTUM:
        random_range = UNCERTAIN(1, 100)
        quantum_state = UNCERTAIN(-1, 1)

    FLIGHT_PLAN:
        1. ORBIT iterations TIMES:
            2. EXTRACT random_range INTO current
            3. APPEND current TO results
            4. BEAM current to DISPLAY

        5. BEAM "Quantum states stabilized." to DISPLAY

        6. ORBIT iterations TIMES:
            7. EXTRACT quantum_state INTO current
            8. BOOST current with 100 INTO current
            9. BEAM current to DISPLAY

END_MISSION"""

ARRAY_EXAMPLE = """MISSION: ArrayManipulator

    CARGO:
        numbers = [1, 2, 3, 4, 5] as CONSTELLATION
        squares = [] as CONSTELLATION
        sum = 0 as METRIC
        temp = 0 as METRIC
        index = 0 as METRIC

    FLIGHT_PLAN:
        1. BEAM "Original array:" to DISPLAY
        2. BEAM numbers to DISPLAY

        3. EXTRACT numbers[0] INTO temp
        4. BOOST temp with temp INTO temp
        5. APPEND temp TO squares

        6. EXTRACT numbers[1] INTO temp
        7. BOOST temp with temp INTO temp
        8. APPEND temp TO squares

        9. EXTRACT numbers[2] INTO temp
        10. BOOST temp with temp INTO temp
        11. APPEND temp TO squares

        12. EXTRACT numbers[3] INTO temp
        13. BOOST temp with temp INTO temp
        14. APPEND temp TO squares

        15. EXTRACT numbers[4] INTO temp
        16. BOOST temp with temp INTO temp
        17. APPEND temp TO squares

        18. BEAM "Squared array:" to DISPLAY
        19. BEAM squares to DISPLAY

        20. EXTRACT squares[0] INTO temp
        21. DOCK sum with temp INTO sum
        22. EXTRACT squares[1] INTO temp
        23. DOCK sum with temp INTO sum
        24. EXTRACT squares[2] INTO temp
        25. DOCK sum with temp INTO sum
        26. EXTRACT squares[3] INTO temp
        27. DOCK sum with temp INTO sum
        28. EXTRACT squares[4] INTO temp
        29. DOCK sum with temp INTO sum

        30. BEAM "Sum of squares:" to DISPLAY
        31. BEAM sum to DISPLAY

END_MISSION"""


def run_starship_program(code):
    try:
        lexer = StarshipLexer(code)
        tokens = lexer.tokenize()

        parser = StarshipParser(tokens)
        ast = parser.parse()

        runtime = StarshipRuntime()
        runtime.execute(ast)

        output = ["🚀 Mission completed successfully!"]
        output.extend(runtime.output_buffer)
        print(output)
        return "\n\n".join(str(line) for line in output)

    except StarshipError as e:
        return f"🚨 MISSION FAILURE at line {e.line}: {e.message}"

    except Exception as e:
        return f"🔥 Critical system failure: {str(e)}"


def main():
    st.title("🚀 Starship Language Text Editor")

    example_choice = st.selectbox(
        "Choose an example program:",
        [
            "Custom Program",
            "Factorial Calculator",
            "Random Generator (Quantum)",
            "Array Manipulator",
        ],
    )

    if example_choice == "Factorial Calculator":
        initial_code = FACTORIAL_EXAMPLE
    elif example_choice == "Random Generator (Quantum)":
        initial_code = QUANTUM_EXAMPLE
    elif example_choice == "Array Manipulator":
        initial_code = ARRAY_EXAMPLE
    else:
        initial_code = """MISSION: FactorialCalculator

            CARGO:
                # Add variables here

            [OPTIONAL] QUANTUM:
                # Add uncertain variables here

            FLIGHT_PLAN:
                # Add numbered steps here

END_MISSION"""

    code = st.text_area("Code Editor", initial_code, height=400)

    if st.button("Launch Mission"):
        st.write("### Output:")
        output = run_starship_program(code)
        if "Mission completed successfully" in output:
            st.success(output)
        else:
            st.error(output)

    st.sidebar.header("Quick Reference")

    st.sidebar.subheader("Basic Commands")
    st.sidebar.code(
        """
    BEAM value to DISPLAY     # Print output
    EXTRACT source INTO target    # Get/assign value
    APPEND value TO array     # Add to array
    """
    )

    st.sidebar.subheader("Math Operations")
    st.sidebar.code(
        """
    BOOST x with y INTO z     # Multiply: z = x * y
    DOCK x with y INTO z      # Add: z = x + y
    UNDOCK x with y INTO z    # Subtract: z = x - y
    SPLIT x with y INTO z     # Divide: z = x / y
    """
    )

    st.sidebar.subheader("Array Operations")
    st.sidebar.code(
        """
    array[index]             # Access array element
    EXTRACT array[0] INTO x  # Get array element
    APPEND value TO array    # Add to end of array
    array = [] as CONSTELLATION      # Create empty array
    array = [1,2,3] as CONSTELLATION # Create with values
    """
    )

    st.sidebar.subheader("Variable Declaration")
    st.sidebar.code(
        """
    x = 0 as METRIC         # Number (int/float)
    msg = "hello" as SIGNAL # String
    arr = [] as CONSTELLATION # Array
    """
    )

    st.sidebar.subheader("Control Flow")
    st.sidebar.code(
        """
    ORBIT count TIMES:      # Loop count times
        <numbered steps>    # Steps must be numbered
    """
    )

    st.sidebar.subheader("Quantum Operations")
    st.sidebar.code(
        """
    QUANTUM:
        x = UNCERTAIN(min, max)  # Random float
    EXTRACT x INTO target    # Get random value
    """
    )

    st.sidebar.subheader("Program Structure")
    st.sidebar.code(
        """
    MISSION: name
        CARGO:              # Variables
            <declarations>
        [QUANTUM:]          # Optional quantum vars
            <declarations>
        FLIGHT_PLAN:        # Instructions
            <numbered steps>
    END_MISSION
    """
    )


if __name__ == "__main__":
    main()

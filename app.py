from lexer import StarshipLexer
from parser import StarshipParser, ASTNode
from interpreter import StarshipRuntime
from errors import StarshipError


def run_starship_program(code):
    try:
        lexer = StarshipLexer(code)
        tokens = lexer.tokenize()

        print("Tokens:")
        for token in tokens:
            print(f"  {token}")

        parser = StarshipParser(tokens)
        ast = parser.parse()

        runtime = StarshipRuntime()
        runtime.execute(ast)

        print("🚀 Mission completed successfully!")
        return runtime.output_buffer

    except StarshipError as e:
        print(f"🚨 MISSION FAILURE at line {e.line}: {e.message}")
        return []
    except Exception as e:
        print(f"🔥 Critical system failure at line {getattr(e, 'line', '?')}: {str(e)}")
        return []


if __name__ == "__main__":
    code = """
    MISSION: ArrayManipulator
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
    END_MISSION
    """

    output = run_starship_program(code)
    for line in output:
        print(line)

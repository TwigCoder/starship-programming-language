from typing import Dict, Any
from parser import StarshipParser, ASTNode
from lexer import StarshipLexer
from errors import StarshipError
import random


class StarshipRuntime:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.quantum_space: Dict[str, Any] = {}
        self.output_buffer = []

    def execute(self, ast):
        if ast.type == "MISSION":
            self.execute_mission(ast)
        else:
            raise Exception(f"Unknown node type: {ast.type}")

    def execute_mission(self, mission_node):
        for node in mission_node.children:
            if node.type == "CARGO":
                self.execute_cargo(node)
            elif node.type == "QUANTUM":
                self.execute_quantum(node)
            elif node.type == "FLIGHT_PLAN":
                self.execute_flight_plan(node)

    def execute_cargo(self, cargo_node):
        for item in cargo_node.children:
            name = item.value
            value_node = item.children[0]
            type_node = item.children[1]

            print(
                f"DEBUG: Cargo - name: {name}, value_node: {value_node.type}, value: {value_node.value}"
            )

            if value_node.type == "VALUE":
                if (
                    isinstance(value_node.value, ASTNode)
                    and value_node.value.type == "ARRAY"
                ):
                    value = [
                        self.evaluate_expression(x) for x in value_node.value.children
                    ]
                else:
                    value = self.evaluate_expression(value_node.value)
            else:
                value = self.evaluate_expression(value_node)

            print(f"DEBUG: Evaluated value: {value}")
            type_name = type_node.value

            if type_name == "METRIC" and not isinstance(value, (int, float)):
                raise TypeError(f"Expected METRIC, got {type(value)}")
            elif type_name == "SIGNAL" and not isinstance(value, str):
                raise TypeError(f"Expected SIGNAL, got {type(value)}")
            elif type_name == "CONSTELLATION" and not isinstance(value, list):
                raise TypeError(f"Expected CONSTELLATION, got {type(value)}")

            self.variables[name] = {"value": value, "type": type_name}

    def execute_flight_plan(self, plan_node):
        for step in plan_node.children:
            print(f"DEBUG: Flight plan step type: {step.type}")

            if step.type == "STEP":
                instruction = step.children[0]
                self.execute_instruction(instruction)

            elif step.type == "BEAM":
                value = self.evaluate_expression(step.children[0])
                self.output_buffer.append(str(value))

            elif step.type == "EXTRACT":
                print(f"DEBUG: Executing EXTRACT")
                source = self.evaluate_expression(step.children[0])
                target_var = step.children[1].value
                print(f"DEBUG: EXTRACT - source: {source}, target: {target_var}")
                self.variables[target_var] = {"value": source, "type": "METRIC"}

            elif step.type == "BOOST":
                print(f"DEBUG: Executing BOOST")
                val1 = self.evaluate_expression(step.children[0])
                val2 = self.evaluate_expression(step.children[1])
                target_var = step.children[2].value
                print(
                    f"DEBUG: BOOST - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                result = val1 * val2
                print(f"DEBUG: BOOST result: {result}")
                self.variables[target_var] = {"value": result, "type": "METRIC"}

            elif step.type == "APPEND":
                print(f"DEBUG: Executing APPEND")
                value = self.evaluate_expression(step.children[0])
                target_list = step.children[1].value
                print(
                    f"DEBUG: APPEND - value: {value}, target: {target_list}, current list: {self.variables[target_list]['value']}"
                )

                if target_list not in self.variables:
                    raise StarshipError(f"List {target_list} not found", step.line)
                if self.variables[target_list]["type"] != "CONSTELLATION":
                    raise StarshipError(
                        f"{target_list} is not a CONSTELLATION", step.line
                    )

                self.variables[target_list]["value"].append(value)
                print(f"DEBUG: After APPEND: {self.variables[target_list]['value']}")

            elif step.type == "DOCK":
                print(f"DEBUG: Executing DOCK")
                val1 = self.evaluate_expression(step.children[0])
                val2 = self.evaluate_expression(step.children[1])
                target_var = step.children[2].value
                print(f"DEBUG: DOCK - val1: {val1}, val2: {val2}, target: {target_var}")
                result = val1 + val2
                print(f"DEBUG: DOCK result: {result}")
                if (
                    target_var not in self.variables
                    or target_var == step.children[0].value
                ):
                    self.variables[target_var] = {"value": result, "type": "METRIC"}

            elif step.type == "ORBIT":
                count = self.evaluate_expression(step.children[0])
                loop_body = step.children[1:]
                for _ in range(count):
                    for instruction in loop_body:
                        self.execute_instruction(instruction)

            elif step.type == "SPLIT":
                print(f"DEBUG: Executing SPLIT")
                val1 = self.evaluate_expression(step.children[0])
                val2 = self.evaluate_expression(step.children[1])
                target_var = step.children[2].value
                print(
                    f"DEBUG: SPLIT - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                if val2 == 0:
                    raise StarshipError("Cannot split by zero", step.line)
                result = val1 // val2
                self.variables[target_var] = {"value": result, "type": "METRIC"}
                print(f"DEBUG: SPLIT result: {result}")

            elif step.type == "UNDOCK":
                print(f"DEBUG: Executing UNDOCK")
                val1 = self.evaluate_expression(step.children[0])
                val2 = self.evaluate_expression(step.children[1])
                target_var = step.children[2].value
                print(
                    f"DEBUG: UNDOCK - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                result = max(0, val1 - val2)
                self.variables[target_var] = {"value": result, "type": "METRIC"}
                print(f"DEBUG: UNDOCK result: {result}")

    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float, str)):
            return expr

        elif expr.type == "IDENTIFIER":
            if expr.value in self.quantum_space:
                quantum_node = self.quantum_space[expr.value]
                if quantum_node.type == "UNCERTAIN":
                    min_val = self.evaluate_expression(quantum_node.children[0])
                    max_val = self.evaluate_expression(quantum_node.children[1])
                    return random.uniform(min_val, max_val)
                return self.evaluate_expression(quantum_node)
            return self.variables[expr.value]["value"]

        elif expr.type == "ARRAY_ACCESS":
            array = self.variables[expr.value]["value"]
            index = int(self.evaluate_expression(expr.children[0]))
            if index < 0 or index >= len(array):
                raise StarshipError(
                    f"Array index {index} out of range for array of size {len(array)}",
                    expr.line,
                )
            return array[index]

        elif expr.type == "NUMBER":
            return expr.value

        elif expr.type == "STRING":
            return expr.value

        elif expr.type == "ARRAY":
            return [self.evaluate_expression(e) for e in expr.children]

        elif expr.type == "UNCERTAIN":
            min_val = self.evaluate_expression(expr.children[0])
            max_val = self.evaluate_expression(expr.children[1])
            return random.uniform(min_val, max_val)

        else:
            raise StarshipError(f"Invalid expression type: {expr.type}", expr.line)

    def execute_instruction(self, instruction):
        try:
            print(f"DEBUG: Executing instruction type: {instruction.type}")

            if instruction.type == "EXTRACT":
                print(f"DEBUG: Executing EXTRACT")
                source = self.evaluate_expression(instruction.children[0])
                target_var = instruction.children[1].value
                print(f"DEBUG: EXTRACT - source: {source}, target: {target_var}")
                self.variables[target_var] = {"value": source, "type": "METRIC"}

            elif instruction.type == "SPLIT":
                print(f"DEBUG: Executing SPLIT")
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value

                print(
                    f"DEBUG: SPLIT - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                if val2 == 0:
                    raise StarshipError("Cannot split by zero", instruction.line)
                result = val1 // val2
                self.variables[target_var] = {"value": result, "type": "METRIC"}
                print(f"DEBUG: SPLIT result: {result}")

            elif instruction.type == "UNDOCK":
                print(f"DEBUG: Executing UNDOCK")
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value
                print(
                    f"DEBUG: UNDOCK - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                result = max(0, val1 - val2)
                self.variables[target_var] = {"value": result, "type": "METRIC"}
                print(f"DEBUG: UNDOCK result: {result}")

            elif instruction.type == "BOOST":
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value
                print(
                    f"DEBUG: BOOST - val1: {val1}, val2: {val2}, target: {target_var}"
                )
                result = val1 * val2
                print(f"DEBUG: BOOST result: {result}")
                self.variables[target_var] = {"value": result, "type": "METRIC"}

            elif instruction.type == "APPEND":
                value = self.evaluate_expression(instruction.children[0])
                target_list = instruction.children[1].value
                print(
                    f"DEBUG: APPEND - value: {value}, target: {target_list}, current list: {self.variables[target_list]['value']}"
                )

                if target_list not in self.variables:
                    raise StarshipError(
                        f"List {target_list} not found", instruction.line
                    )
                if self.variables[target_list]["type"] != "CONSTELLATION":
                    raise StarshipError(
                        f"{target_list} is not a CONSTELLATION", instruction.line
                    )

                self.variables[target_list]["value"].append(value)
                print(f"DEBUG: After APPEND: {self.variables[target_list]['value']}")

            elif instruction.type == "BEAM":
                value = self.evaluate_expression(instruction.children[0])
                self.output_buffer.append(str(value))

            elif instruction.type == "ORBIT":
                count = self.evaluate_expression(instruction.children[0])
                loop_body = instruction.children[1:]
                for _ in range(int(count)):
                    for sub_instruction in loop_body:
                        self.execute_instruction(sub_instruction)

            elif instruction.type == "DOCK":
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value
                print(f"DEBUG: DOCK - val1: {val1}, val2: {val2}, target: {target_var}")
                result = val1 + val2
                print(f"DEBUG: DOCK result: {result}")
                self.variables[target_var] = {"value": result, "type": "METRIC"}

            elif instruction.type == "UNDOCK":
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value
                if target_var not in self.variables:
                    self.variables[target_var] = {"value": 0, "type": "METRIC"}
                result = max(0, val1 - val2)
                self.variables[target_var] = {"value": result, "type": "METRIC"}

            elif instruction.type == "SPLIT":
                val1 = self.evaluate_expression(instruction.children[0])
                val2 = self.evaluate_expression(instruction.children[1])
                target_var = instruction.children[2].value

                if target_var not in self.variables:
                    self.variables[target_var] = {"value": 0, "type": "METRIC"}
                if val2 == 0:
                    raise StarshipError("Cannot split by zero", instruction.line)
                result = val1 // val2

                self.variables[target_var] = {"value": result, "type": "METRIC"}

            else:
                raise StarshipError(
                    f"Unknown instruction type: {instruction.type}", instruction.line
                )
        except Exception as e:
            if not isinstance(e, StarshipError):
                raise StarshipError(str(e), instruction.line)
            raise

    def execute_quantum(self, quantum_node):
        for item in quantum_node.children:
            name = item.value
            value_node = item.children[0]
            self.quantum_space[name] = value_node


class StarshipInterpreter:
    def __init__(self, parser):
        self.parser = parser
        self.runtime = StarshipRuntime()

    def interpret(self):
        ast = self.parser.parse()
        self.runtime.execute(ast)
        return self.runtime.output_buffer

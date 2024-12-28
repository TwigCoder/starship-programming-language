from dataclasses import dataclass
from typing import List, Any
from errors import StarshipError


@dataclass
class ASTNode:
    type: str
    value: Any
    children: List["ASTNode"] = None
    line: int = 0

    def __init__(self, type, value, children=None, line=0):
        self.type = type
        self.value = value
        self.children = children if children else []
        self.line = line


class StarshipParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def error(self, message="Invalid syntax"):
        token_info = (
            f"'{self.current_token.value}'" if self.current_token else "end of file"
        )
        line = self.current_token.line if self.current_token else 0
        raise StarshipError(f"{message} at {token_info}", line)

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.pos]

    def parse(self):
        return self.parse_mission()

    def parse_mission(self):
        if self.current_token.value != "MISSION:":
            self.error("Program must start with MISSION:")

        self.advance()
        mission_name = self.current_token.value
        self.advance()

        nodes = []
        found_end_mission = False

        while self.current_token:
            if self.current_token.value == "END_MISSION":
                found_end_mission = True
                break

            if self.current_token.value == "CARGO:":
                nodes.append(self.parse_cargo())
            elif self.current_token.value == "QUANTUM:":
                nodes.append(self.parse_quantum())
            elif self.current_token.value == "FLIGHT_PLAN:":
                nodes.append(self.parse_flight_plan())
            else:
                self.advance()

        if not found_end_mission:
            self.error("Program must end with END_MISSION")

        self.advance()
        return ASTNode("MISSION", mission_name, nodes)

    def parse_cargo(self):
        self.advance()
        cargo_items = []

        while self.current_token and self.current_token.type == "IDENTIFIER":
            name = self.current_token.value
            self.advance()

            if self.current_token.value != "=":
                self.error()
            self.advance()

            value = self.parse_expression()

            if self.current_token.value != "as":
                self.error()
            self.advance()

            type_name = self.current_token.value
            self.advance()

            cargo_items.append(
                ASTNode(
                    "CARGO_ITEM",
                    name,
                    [ASTNode("VALUE", value), ASTNode("TYPE", type_name)],
                )
            )

        return ASTNode("CARGO", "cargo_section", cargo_items)

    def parse_flight_plan(self):
        self.advance()
        steps = []

        while self.current_token and self.current_token.type == "NUMBER":
            step_number = int(float(self.current_token.value))
            self.advance()

            if self.current_token.type != "DOT":
                self.error("Expected '.' after step number")
            self.advance()

            step = self.parse_step()
            steps.append(step)

        return ASTNode("FLIGHT_PLAN", "flight_plan_section", steps)

    def parse_step(self):
        if not self.current_token:
            self.error("Unexpected end of flight plan")

        if self.current_token.type == "NUMBER":
            self.advance()
            if self.current_token.type == "DOT":
                self.advance()

        if self.current_token.type == "KEYWORD":
            if self.current_token.value == "BEAM":
                return self.parse_beam_command()

            elif self.current_token.value == "ORBIT":
                return self.parse_orbit_command()

            elif self.current_token.value == "DOCK":
                return self.parse_operation_command("DOCK")

            elif self.current_token.value == "UNDOCK":
                return self.parse_operation_command("UNDOCK")

            elif self.current_token.value == "BOOST":
                return self.parse_operation_command("BOOST")

            elif self.current_token.value == "SPLIT":
                return self.parse_operation_command("SPLIT")

            elif self.current_token.value == "EXTRACT":
                return self.parse_extract_command()

            elif self.current_token.value == "APPEND":
                return self.parse_append_command()

        self.error(f"Unknown command: {self.current_token.value}")

    def parse_beam_command(self):
        self.advance()
        value = self.parse_expression()

        if self.current_token.value != "to":
            self.error("Expected 'to' after BEAM value")
        self.advance()

        if self.current_token.value != "DISPLAY":
            self.error("Expected 'DISPLAY' after 'to'")
        self.advance()

        return ASTNode("BEAM", None, [value])

    def parse_orbit_command(self):
        self.advance()
        count = self.parse_expression()

        if self.current_token.value not in ["TIMES", "TIMES:"]:
            self.error("Expected 'TIMES' after ORBIT count")
        self.advance()

        if self.current_token.value == ":":
            self.advance()

        body = []
        while self.current_token and self.current_token.type == "NUMBER":
            step = self.parse_step()
            body.append(step)

        return ASTNode("ORBIT", None, [count] + body)

    def parse_quantum(self):
        self.advance()
        quantum_items = []

        while self.current_token and self.current_token.type == "IDENTIFIER":
            name = self.current_token.value
            self.advance()

            if self.current_token.value != "=":
                self.error()
            self.advance()

            value = self.parse_quantum_expression()
            quantum_items.append(ASTNode("QUANTUM_ITEM", name, [value]))

        return ASTNode("QUANTUM", "quantum_section", quantum_items)

    def parse_quantum_expression(self):
        if self.current_token.value == "UNCERTAIN":
            self.advance()

            if self.current_token.value != "(":
                self.error()
            self.advance()
            min_val = self.parse_expression()

            if self.current_token.value != ",":
                self.error()
            self.advance()
            max_val = self.parse_expression()

            if self.current_token.value != ")":
                self.error()
            self.advance()
            return ASTNode("UNCERTAIN", None, [min_val, max_val])

        self.error()

    def parse_expression(self):
        if self.current_token.type == "NUMBER":
            value = self.current_token.value
            self.advance()
            return ASTNode("NUMBER", value)

        elif self.current_token.type == "MINUS":
            self.advance()

            if self.current_token.type == "NUMBER":
                value = -self.current_token.value
                self.advance()
                return ASTNode("NUMBER", value)
            self.error("Expected number after '-'")

        elif self.current_token.type == "STRING":
            value = self.current_token.value
            self.advance()
            return ASTNode("STRING", value)

        elif self.current_token.type == "IDENTIFIER":
            value = self.current_token.value
            self.advance()

            if self.current_token and self.current_token.value == "[":
                self.advance()
                index = self.parse_expression()

                if not self.current_token or self.current_token.value != "]":
                    self.error("Expected ']'")
                self.advance()
                return ASTNode("ARRAY_ACCESS", value, [index])

            return ASTNode("IDENTIFIER", value)

        elif self.current_token.value == "[":
            return self.parse_array()
        self.error()

    def parse_array(self):
        self.advance()
        elements = []

        while self.current_token and self.current_token.value != "]":
            elements.append(self.parse_expression())
            if self.current_token.value == ",":
                self.advance()

        if self.current_token.value != "]":
            self.error()
        self.advance()

        return ASTNode("ARRAY", None, elements)

    def parse_launch_command(self):
        self.advance()
        value = self.parse_expression()
        return ASTNode("LAUNCH", None, [value])

    def parse_return_command(self):
        self.advance()
        return ASTNode("RETURN", None, [])

    def parse_extract_command(self):
        self.advance()
        source = self.parse_expression()

        if self.current_token.value != "INTO":
            self.error("Expected 'INTO' after EXTRACT expression")
        self.advance()

        target = self.parse_expression()
        return ASTNode("EXTRACT", None, [source, target])

    def parse_dock_command(self):
        self.advance()
        val1 = self.parse_expression()

        if self.current_token.value != "with":
            self.error("Expected 'with' after first DOCK value")
        self.advance()

        val2 = self.parse_expression()

        if self.current_token.value != "INTO":
            self.error("Expected 'INTO' after second DOCK value")
        self.advance()

        target = self.parse_expression()
        return ASTNode("DOCK", None, [val1, val2, target])

    def parse_append_command(self):
        self.advance()
        value = self.parse_expression()

        if self.current_token.value != "TO":
            self.error("Expected 'TO' after APPEND value")
        self.advance()

        target = self.parse_expression()
        return ASTNode("APPEND", None, [value, target])

    def parse_operation_command(self, op_type):
        self.advance()
        val1 = self.parse_expression()

        if self.current_token.value != "with":
            self.error(f"Expected 'with' after first {op_type} value")
        self.advance()

        val2 = self.parse_expression()

        if self.current_token.value != "INTO":
            self.error(f"Expected 'INTO' after second {op_type} value")
        self.advance()

        target = self.parse_expression()
        return ASTNode(op_type, None, [val1, val2, target])

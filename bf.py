
class InvalidLoopError(BaseException):
    pass


class BrainfuckInstance:
    @staticmethod
    def decode_instruction_string(instruction_string: str):
        instructions = []
        loop_stack = []
        for i in instruction_string:
            if i in '><+-.,':
                instructions.append(i)
            elif i == '[':
                instructions.append(None)
                loop_stack.append(len(instructions) - 1)
            elif i == ']':
                if not loop_stack:
                    raise
                instructions.append(loop_stack.pop())
                instructions[instructions[-1]] = len(instructions) - 1
            else:
                pass
        if loop_stack:
            raise InvalidLoopError(f'Unclosed loop(s) at {loop_stack}')
        instructions.append(None)
        return instructions

    def __init__(self, code: str):
        self.instructions = self.decode_instruction_string(code)
        self.memory = []
        self.memory_pointer = 0
        self.instruction_pointer = 0
    
    def ensure_memory_pointer(self):
        if self.memory_pointer >= len(self.memory):
            self.memory.append(0)
        elif self.memory_pointer < 0:
            raise IndexError('Memory pointer is out of bounds')

    def right(self):
        self.memory_pointer += 1
        if self.memory_pointer > len(self.memory):
            self.memory.append(0)

    def left(self):
        self.memory_pointer -= 1
        if self.memory_pointer < 0:
            self.memory_pointer = 0  

    def increment(self):
        self.memory[self.memory_pointer] += 1

    def decrement(self):
        self.memory[self.memory_pointer] -= 1

    def output(self):
        print(chr(self.memory[self.memory_pointer]), end='')

    def input(self):
        self.memory[self.memory_pointer] = ord(input())

    def loop_start(self):
        if self.memory[self.memory_pointer] == 0:
            self.instruction_pointer = self.instructions[self.instruction_pointer] - 1

    def loop_end(self):
        if self.memory[self.memory_pointer] != 0:
            self.instruction_pointer = self.instructions[self.instruction_pointer] - 1

    def advance(self):
        self.instruction_pointer
        self.ensure_memory_pointer()
        match (self.instructions[self.instruction_pointer]):
            case '>':
                self.right()
            case '<':
                self.left()
            case '+':
                self.increment()
            case '-':
                self.decrement()
            case '.':
                self.output()
            case ',':
                self.input()
            case None:
                pass
            case int as x:
                if x > self.instruction_pointer:
                    self.loop_start()
                else:
                    self.loop_end()
        self.instruction_pointer += 1

    def run(self):
        while self.instructions[self.instruction_pointer] is not None:
            if self.instruction_pointer < 0:
                raise IndexError('Instruction pointer is out of bounds')
            self.advance()

    def __repr__(self) -> str:
        return f'BrainuckInstance<memory={self.memory} memory_pointer={self.memory_pointer} instructions={self.instructions} instruction_pointer={self.instruction_pointer}>'

def main():
    import sys
    BrainfuckInstance(sys.argv[1])


if __name__ == '__main__':
    main()

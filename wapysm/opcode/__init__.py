# 2.4 Instructions
# This defines structure of all instructions and action itself,
# and not responsible for parsing binaries or texts.

class InstructionBase(object):
    def execute(self):
        pass

# 2.4.5 Control Instructions

class Unreachable(InstructionBase):
    "unreachable"
    def execute(self):
        raise Exception('Unreachable!')

class Nop(InstructionBase):
    "nop"
    def execute(self):
        pass

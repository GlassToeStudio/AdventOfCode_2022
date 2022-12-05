"""


--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from
the ships. Supplies are stored in stacks of marked crates, but because the
needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To
ensure none of the crates get crushed or fall over, the crane operator will
rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her which crate will end up where, and they
want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the
rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates:
crate Z is on the bottom, and crate N is on top. Stack 2 contains three
crates; from bottom to top, they are crates M, C, and D. Finally, stack 3
contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a
quantity of crates is moved from one stack to a different stack. In the first
step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

In the second step, three crates are moved from stack 1 to stack 3. Crates are
moved one at a time, so the first crate to be moved (D) ends up below the
second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are
moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in
this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each
stack?


"""


from collections import deque
from io import TextIOWrapper


def format_data(in_file: TextIOWrapper) -> list[str]:
    """Return a list of str from the given text."

    Args:
        in_file (TextIOWrapper): text file

    Returns:
        list[str]: input data as list[str]
    """
    temp = [x.replace("\n", " ") for x in in_file.readlines()]
    crates = []
    instructions = []
    for _, x in enumerate(temp):
        crates.append(list())
        if "1" in x:
            instructions = [
                int(y.strip())
                for z in temp[_ + 1 :]
                for y in (z.replace("move ", "").replace(" from ", "-").replace(" to ", "-").split("-"))
                if y != " "
            ]
            instructions = [instructions[j : j + 3] for j in range(0, len(instructions) - 2, 3)]
            break
        crates[_] = [x[i : i + 3] for i in range(0, len(x) - 3, 4)]

    crates = [deque(x[i] for x in reversed(crates[:-1])) for i in range(len(crates[0]))]
    for x in crates:
        to_remove = 0
        for y in x:
            if y == "   ":
                to_remove += 1
        for i in range(to_remove):
            x.pop()
    return crates, instructions


def move_crates(crates, instructions):
    for mov, fr, to in instructions:
        for i in range(mov):
            crates[to - 1].append(crates[fr - 1].pop())


if __name__ == "__main__":
    with open("Day_05/input.txt", "r", encoding="utf-8") as f:
        crates, instructions = format_data(f)
        move_crates(crates, instructions)
        ans = ""
        for x in crates:
            ans += x.pop().replace("[", "").replace("]", "")
        print(ans)

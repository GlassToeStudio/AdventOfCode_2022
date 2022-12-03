"""Get the stuff from AoC"""

import argparse
import os
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from gts_colors.colors import BLUE, BOLD, RESET, YELLOW


def get_args() -> argparse.Namespace:
    """Setup arg parser and return optional and required args.

    Returns:
        argparse.Namespace: args
    """

    parser = argparse.ArgumentParser(
        f"\n{BLUE}{BOLD}"
        "********************************************************************************\n"  # noqa: E501
        "********************************************************************************\n"  # noqa: E501
        "**                                                                            **\n"  # noqa: E501
        "**  Will get the input file and create a boilerplate python file for a given  **\n"  # noqa: E501
        "**                           Advent of Code problem.                          **\n"  # noqa: E501
        "**                                                                            **\n"  # noqa: E501
        "********************************************************************************\n"  # noqa: E501
        "********************************************************************************\n"  # noqa: E501
        f"{RESET}"
    )

    parser.add_argument("day", help="Enter the day for the problem you are working on.")  # noqa: E501
    parser.add_argument("-i", "--input", help="Create the input file.", action="store_true")  # noqa: E501
    parser.add_argument("-p", "--python", help="Create the python template.", action="store_true")  # noqa: E501
    return parser.parse_args()


def get_session_id() -> str:
    """Get the session ID from the .env file.

    Returns:
        str: session id for logged in user
    """

    load_dotenv()
    return os.getenv("SESSION_ID")


def get_input_data(url: str, session_id: str) -> list[str]:
    """Get the input data for the given url (day of advent of code)

    Args:
        url (str): url of the advent of code problem for a specific day
        ID (str): session id for logged in user

    Returns:
        list[str]: the input for a given advent of code problem
    """

    cookies = {
        "session": session_id,
    }
    res = requests.get(f"{url}/input", cookies=cookies)
    data = res.content.decode("UTF-8")

    return data


def get_instruction_data(url: str, session_id: str) -> str:
    """Get the instruction text from the given url (day of advent of code)

    Args:
        url (str): url of the advent of code problem for a specific day
        ID (str): session id for logged in user

    Returns:
        str: html text from the given url
    """

    cookies = {
        "session": session_id,
    }
    res = requests.get(f"{url}", cookies=cookies).text
    html_text = BeautifulSoup(res, "html.parser").get_text()

    return html_text


def format_instruction_text(html_text: str) -> str:
    """Get a pep8 formatted version of the given html_text.

    Args:
        html_text (str): all text from html object

    Returns:
        str: pep8 formatted set of instruction text
    """

    # Save the text and format it.
    # Not sure why it differs so much after saving and reading
    # back from a file versus just doing html_text.split('\n')[18:-11]
    with open("temp", "a+", encoding="utf-8") as python_file:
        max_line_length = 79
        instructions = []

        # Checks for '--- message ---' and keeps a match of the inner text
        # '--- message ---'
        # 'message'
        # [-]{3}[\s]{1} '--- '
        # ([\s\w:!]*) 'any characters, whitespace, colon, exclamation'
        # [\s]{1}[-]{3} ' ---'
        regex_str = r"([-]{3}[\s]{1}([\s\w:!]*)[\s]{1}[-]{3})"
        regex = re.compile(regex_str)
        matches = regex.findall(html_text)
        title = matches[0][1]
        for match in matches:
            html_text = html_text.replace(match[0], f"\n\n--- {match[1]} ---\n")

        # TODO: Prefer to format the html_text directly and not
        # write to, and read back from, a file.
        python_file.write(html_text)
        python_file.seek(0)  # back to the beginning.
        lines = python_file.readlines()[18:-11]  # Cut out the junk.

        # Break the lines up such that they are never longer
        # than MAX_LINE_LENGTH, for pep8
        for line in lines:
            start = 0
            end = max_line_length
            if max_line_length >= len(line):
                instructions.append(line)
                continue
            while end < len(line):
                while line[end] != " ":
                    end -= 1
                instructions.append(line[start:end] + "\n")
                start = end + 1
                end += max_line_length
                if end >= len(line):
                    instructions.append(line[start:] + "\n")

    os.remove("temp")
    return "".join(instructions), title


def fix_day(day: str) -> str:
    """Append a zero [0] in front of day if day is one digit.\n
    1 -> 01

    Args:
        day (str): 1, 21, etc.

    Returns:
        str: 01, 21, etc.
    """

    return f"0{day}" if len(day) == 1 else day


def try_make_dir(day: str) -> None:
    """Try to make a new directory for the given day.\n
    ./Day_01,\n
    ./Day_21,\n
    etc.\n
    If it exists, just print to console.

    Args:
        day (str): 01, 21, etc.
    """

    if os.path.isdir(f"Day_{day}"):
        print(f"{YELLOW}{BOLD}* Directory exists.{RESET}")
    else:
        os.mkdir(f"Day_{day}")


def make_input_file(day: str, data: list[str]) -> None:
    """Save the input data to a file for the given day in its
    corresponding directory.

    Args:
        day (str): 01, 21, etc.
        file (str): file name to save as
        data (list[str]): the data to save to file
    """

    if os.path.exists(f"Day_{day}/input.txt"):
        print(f"{YELLOW}{BOLD}* Input file exists.{RESET}")
        return

    with open(f"Day_{day}/input.txt", "w", encoding="utf-8") as input_file:
        input_file.write(data)

    with open(f"Day_{day}/sample.txt", "a", encoding="utf-8"):
        pass


def make_python_file(day: str, instructions: str) -> None:
    """Save the instruction string to a python file for the given
    day in its corresponding directory. If the file exists, just
    overwrite the previous instructions with new instructions that
    include part 2.

    Args:
        day (str): 01, 21, etc.
        instructions (str): instructions to be added at the top of python file
    """

    # If we already made the file, just overwrite the instructions,
    # keep the code we already wrote.
    if os.path.exists(f"Day_{day}/day_{day}_problems.py"):
        print(f"{YELLOW}{BOLD}python file exists, editing current file.{RESET}")
        with open(f"Day_{day}/day_{day}_problems.py", "r+", encoding="utf-8") as python_file:
            data = python_file.read()
            previous_contents = data.split('"""', 2)
            output = f"\"\"\"\n{instructions}\"\"\"{''.join(previous_contents[2:])}"
            python_file.seek(0)
            python_file.truncate(0)
            python_file.write(output)
    else:
        with open(f"Day_{day}/day_{day}_problems.py", "w", encoding="utf-8") as python_file:
            with open("py_template.txt", "r", encoding="utf-8") as template:
                output = (template.read().replace("{day}", day).replace("{instructions}", instructions))  # noqa E501
            python_file.write(output)


def update_readme(title: str) -> None:
    """Update readme

    Args:
        title (str: title extracted from isntruction text.
    """
    with open("README.md", "a", encoding="utf-8") as readme_file:
        with open("readme_template.txt", "r", encoding="utf-8") as template:
            output = template.read().replace("{title}", title)
        readme_file.write(output)


def main():
    """Main method"""

    args = get_args()
    aoc_url = f"https://adventofcode.com/2022/day/{args.day}"
    session_id = get_session_id()

    day = fix_day(args.day)
    try_make_dir(day)

    if args.input:
        input_data = get_input_data(aoc_url, session_id)
        make_input_file(day, input_data)
    if args.python:
        instruction_data = get_instruction_data(aoc_url, session_id)
        instructions, title = format_instruction_text(instruction_data)
        make_python_file(day, instructions)
        update_readme(title)


if __name__ == "__main__":
    main()

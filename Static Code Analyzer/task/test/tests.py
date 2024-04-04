from hstest.stage_test import *
from hstest.test_case import TestCase
import os, re

TOO_LONG_LINE = 'Too long line is not mentioned. '
error_code_long = "s001"

INDENTATION = "Invalid check of indentation. "
error_code_indention = "s002"

UNNECESSARY_SEMICOLON = "Your program passed the line with an unnecessary semicolon or has an incorrect format. "
error_code_semicolon = "s003"

TWO_SPACES_BEFORE_COMMENT = "The program should warn about the line with less than 2 spaces before a comment."
error_code_comments = "s004"

TODO = "Your program passed the line with TODO comment or has an incorrect format. "
error_code_todo = "s005"

TOO_MANY_BLANK_LINES = "Your program didn't warn about more than two blank lines between lines."
error_code_blank_lines = "s006"

error_code_class_def_spaces = "s007"
SPACES_AFTER_CLASS_FUNC = "Your program should warn about multiple spaces after keyword 'class' and 'def'"

error_code_class_name = "s008"
CLASS_NAME = "The program should warn about incorrect class name. "

error_code_func_name = "s009"
FUNC_NAME = "The program passed the function with the name not in snake_case style."

FALSE_ALARM = "False alarm. Your program warned about correct line."

cur_dir = os.path.abspath(os.curdir)


class AnalyzerTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase(args=[f"test{os.sep}test_1.py"], check_function=self.test_1),
                TestCase(args=[f"test{os.sep}test_2.py"], check_function=self.test_2),
                TestCase(args=[f"test{os.sep}test_3.py"], check_function=self.test_3),
                TestCase(args=[f"test{os.sep}test_4.py"], check_function=self.test_4),
                TestCase(args=[f"test{os.sep}test_5.py"], check_function=self.test_5),
                TestCase(args=[f"test{os.sep}test_6.py"], check_function=self.test_6),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_7.py"], check_function=self.test_7),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_8.py"], check_function=self.test_8),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_9.py"], check_function=self.test_9),
                TestCase(args=[cur_dir + f"{os.sep}test{os.sep}this_stage"], check_function=self.test_common)]

    # Check of correct indention
    def test_1(self, output: str, attach):
        if output.strip() != "":
            return CheckResult.wrong("Your program warned a style error in the correct file."
                                     "There was no any rows with string length more than 79 symbols.")
        return CheckResult.correct()

    # Test of semicolon violation
    def test_2(self, output: str, attach):
        file_path = f"test{os.sep}test_2.py"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for issue in output:
            if issue.startswith(f"{file_path}: line 1: {error_code_semicolon}"):
                return CheckResult.wrong(FALSE_ALARM + "There was no any semicolons at all.")
            if issue.startswith(f"{file_path}: line 5: {error_code_semicolon}") or issue.startswith(
                    f"line 8 {error_code_semicolon}"):
                return CheckResult.wrong(FALSE_ALARM + "The semicolon was a part of comment block")
            if issue.startswith(f"{file_path}: line 6: {error_code_semicolon}") or issue.startswith(
                    f"line 7 {error_code_semicolon}"):
                return CheckResult.wrong(FALSE_ALARM + "The semicolon was a part of string")

        # positive tests
        if not len(output) == 3:
            return CheckResult.wrong("Incorrect number of warning messages.")
        for i, j in enumerate([2, 3, 4]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_semicolon}"):
                return CheckResult.wrong(UNNECESSARY_SEMICOLON)
        return CheckResult.correct()

    # Test of todo_comments
    def test_3(self, output: str, attach):
        file_path = f"test{os.sep}test_3.py"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for issue in output:
            if issue.startswith(f"{file_path}: line 1: {error_code_todo}") or issue.startswith(
                    f"line 8 {error_code_todo}") or \
                    issue.startswith(f"line 9: {error_code_todo}"):
                return CheckResult.wrong(FALSE_ALARM + "There was no any TODO comments")
            if issue.startswith(f"{file_path}: line 6: {error_code_todo}") or issue.startswith(
                    f"line 7 {error_code_todo}"):
                return CheckResult.wrong(FALSE_ALARM + "TODO is inside of string")

        # positive tests
        if not len(output) == 4:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about 4 lines with mistakes in this test case.\n"
                                     "4 lines that include TODO comments should be found")
        for i, j in enumerate([2, 3, 4, 5]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_todo}"):
                return CheckResult.wrong(TODO)

        return CheckResult.correct()

    # Blank lines test
    def test_4(self, output, attach):
        file_path = f"test{os.sep}test_4.py"
        output = output.strip().lower().splitlines()
        if len(output) != 1:
            if len(output) == 0:
                return CheckResult.wrong(TOO_MANY_BLANK_LINES)
            if output[0].startswith(f"{file_path}: line 4: {error_code_blank_lines}"):
                return CheckResult.wrong(FALSE_ALARM)
            if not output[0].startswith(f"{file_path}: line 8: {error_code_blank_lines}"):
                return CheckResult.wrong(TOO_MANY_BLANK_LINES)
            else:
                return CheckResult.wrong(TOO_MANY_BLANK_LINES)
        return CheckResult.correct()

    # Test of comments style
    def test_5(self, output, attach):
        file_path = f"test{os.sep}test_5.py"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for issue in output:
            if issue.startswith(f"{file_path}: line 1: {error_code_comments}"):
                return CheckResult.wrong(FALSE_ALARM + "There is no comments at all.")
            if issue.startswith(f"{file_path}: line 2: {error_code_comments}"):
                return CheckResult.wrong(FALSE_ALARM + "There is a correct line with comment")
            if issue.startswith(f"{file_path}: line 3: {error_code_comments}" or
                                issue.startswith(f"{file_path}: line 4: {error_code_comments}")):
                return CheckResult.wrong(FALSE_ALARM + "It is a correct line with a comment after code.")

        # positive test
        if not len(output) == 2:
            return CheckResult.wrong("Incorrect number of warning messages. "
                                     "Your program should warn about two mistakes in this test case.")
        for i, j in enumerate([6, 7]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_comments}"):
                return CheckResult.wrong(TWO_SPACES_BEFORE_COMMENT)

        return CheckResult.correct()

    def test_6(self, output, attach):
        file_path = f"test{os.sep}test_6.py"
        output = output.strip().lower().splitlines()

        if len(output) != 9:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        if not (output[0].startswith(f"{file_path}: line 1: s004") or
                output[7].startswith(f"{file_path}: line 13: s004")):
            return CheckResult.wrong(TWO_SPACES_BEFORE_COMMENT)

        if not (output[1].startswith(f"{file_path}: line 2: s003") or
                output[3].startswith(f"{file_path}: line 3: s003") or
                output[6].startswith(f"{file_path}: line 13: s003")):
            return CheckResult.wrong(UNNECESSARY_SEMICOLON)

        if not (output[2].startswith(f"{file_path}: line 3: s001") or
                output[4].startswith(f"{file_path}: line 6: s001")):
            return CheckResult.wrong(TOO_LONG_LINE)

        if not (output[5].startswith(f"{file_path}: line 11: s006")):
            return CheckResult.wrong(TOO_MANY_BLANK_LINES)

        if not output[8].startswith(f"{file_path}: line 13: s005"):
            return CheckResult.wrong(TODO)

        return CheckResult.correct()

    # Class name test
    def test_7(self, output, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_7.py"
        output = output.strip().lower().splitlines()

        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if (issue.startswith(f"{file_path}: line 1: {error_code_class_name}") or
                    issue.startswith(f"{file_path}: line 13: {error_code_class_name}")):
                return CheckResult.wrong(FALSE_ALARM)

        if not len(output) == 2:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about two mistakes in this test case")

        if not output[0].startswith(f"{file_path}: line 5: {error_code_class_name}") or \
                not output[1].startswith(f"{file_path}: line 9: {error_code_class_name}"):
            return CheckResult.wrong(CLASS_NAME + "The class had name in snake_case style.")

        return CheckResult.correct()

    # "Spaces after keywords 'class' and 'def'" test
    def test_8(self, output, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_8.py"
        output = output.strip().lower().splitlines()

        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if issue.startswith(f"{file_path}: line 5: {error_code_class_def_spaces}"):
                return CheckResult.wrong(FALSE_ALARM)

        if not len(output) == 2:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about two mistakes in this test case")

        for i, j in enumerate([1, 7]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_class_def_spaces}"):
                return CheckResult.wrong(SPACES_AFTER_CLASS_FUNC)

        return CheckResult.correct()

    # function name test
    def test_9(self, output, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_9.py"
        output = output.strip().lower().splitlines()

        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if (issue.startswith(f"{file_path}: line 1: {error_code_func_name}") or
                    issue.startswith(f"{file_path}: line 2: {error_code_func_name}")):
                return CheckResult.wrong(FALSE_ALARM)

        if not len(output) == 2:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about 2 lines with mistakes in this test case.\n"
                                     "2 function names not in snake_case style should be found.")

        for i, j in enumerate([8, 12]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_func_name}"):
                return CheckResult.wrong(FUNC_NAME)

        return CheckResult.correct()

    def test_common(self, output, attach):
        file_1 = f"test{os.sep}this_stage{os.sep}test_7.py"
        file_2 = f"test{os.sep}this_stage{os.sep}test_8.py"
        file_3 = f"test{os.sep}this_stage{os.sep}test_9.py"

        output = output.strip().lower().splitlines()

        if not len(output) == 6:
            return CheckResult.wrong("It looks like there is an incorrect number of error messages. "
                                     f"Expected 6 lines, found {len(output)}")

        if file_1 not in output[0] or file_2 not in output[2] or file_3 not in output[4]:
            return CheckResult.wrong("Incorrect output format.\n"
                                     "Make sure that the files in the output are sorted "
                                     "according to the file name, line number, and issue code.")

        # negative tests
        for issue in output:
            if f"{file_1}: line 1: {error_code_class_name}" in issue or \
                    f"{file_1}: line 13: {error_code_class_name}" in issue:
                return CheckResult.wrong(FALSE_ALARM)
            if f"{file_2}: line 5: {error_code_class_def_spaces}" in issue:
                return CheckResult.wrong(FALSE_ALARM)
            if f"{file_3}: line 1: {error_code_func_name}" in issue or \
                    f"{file_3}: line 2: {error_code_func_name}" in issue:
                return CheckResult.wrong(FALSE_ALARM)

        # test_7 file
        if f"{file_1}: line 5: {error_code_class_name}" not in output[0] or \
                f"{file_1}: line 9: {error_code_class_name}" not in output[1]:
            return CheckResult.wrong(CLASS_NAME + "The class had name in snake_case style.")

        # test_8 file
        for i, j in enumerate([1, 7]):
            if f"{file_2}: line {j}: {error_code_class_def_spaces}" not in output[i+2]:
                return CheckResult.wrong(SPACES_AFTER_CLASS_FUNC)

        # test_9 file
        for i, j in enumerate([8, 12]):
            if f"{file_3}: line {j}: {error_code_func_name}" not in output[i+4]:
                return CheckResult.wrong(FUNC_NAME)

        return CheckResult.correct()


if __name__ == '__main__':
    AnalyzerTest("analyzer.code_analyzer").run_tests()

import editdistance
import re
from difflib import SequenceMatcher
from suffix_trees import STree
from difflib import get_close_matches

class Evaluation:
    def __init__(self, buggy_code, expected: str, codex: str, warning_line: str):
        self.expected_orig = expected.strip().lower()
        self.codex_orig = codex.strip().lower()
        self.buggy_code = buggy_code.strip().lower()
        self.warning_line = warning_line.strip().lower()

    def is_exact_match(self):
        expected = ''
        for line in self.expected_orig.split('\n'):
            expected += re.sub(' +', ' ', line.strip()).replace(' ', '').replace('(', '').replace(')', '')
        
        codex = ''
        for line in self.codex_orig.split('\n'):
            codex += re.sub(' +', ' ', line.strip()).replace(' ', '').replace('(', '').replace(')', '')

        return expected == codex or expected in codex

    def is_match(self):
        if self.is_exact_match():
            return True
        
        splitted_buggy_code = self.buggy_code.split('\n')
        splitted_expected_code = self.expected_orig.split('\n')
        splitted_codex_code = self.codex_orig.split('\n')

        expected = ''
        for line in self.expected_orig.split('\n'):
            expected += re.sub(' +', ' ', line.strip())
        
        codex = ''
        for line in self.codex_orig.split('\n'):
            codex += re.sub(' +', ' ', line.strip())

        if len(splitted_buggy_code) > len(splitted_expected_code):
            closest_match_expected = get_close_matches(self.warning_line, splitted_expected_code, n=1)
            if not len(closest_match_expected): ## The warning line was completely removed
                if self.warning_line not in expected and self.warning_line not in codex:
                    return True
            else: ## The warning line exists but is modified
                closest_match_codex = get_close_matches(self.warning_line, splitted_codex_code, n=1)
                if len(closest_match_codex) == len(closest_match_expected) == 1:
                    if closest_match_expected[0] \
                        .replace(' ', '') \
                        .replace('==', '===') \
                        .replace('(', '').replace(')', '') == closest_match_codex[0] \
                        .replace(' ', '') \
                        .replace('==', '===') \
                        .replace('(', '').replace(')', ''):
                        return True
        
        elif len(splitted_buggy_code) == len(splitted_expected_code) == len(splitted_codex_code):
            i = 0
            buggy_line_num = -1
            for line in splitted_buggy_code:
                if line.strip() == self.warning_line:
                    buggy_line_num = i
                i += 1
            
            if buggy_line_num != -1 and splitted_codex_code[buggy_line_num] \
                .replace(' ', '') \
                .replace('==', '===') \
                .replace('(', '').replace(')', '') == splitted_expected_code[buggy_line_num] \
                .replace(' ', '') \
                .replace('==', '===') \
                .replace('(', '').replace(')', ''):
                return True 

        return False

    def calc_lcs(self):
        """
        https://stackoverflow.com/questions/18715688/find-common-substring-between-two-strings
        """
        input_list = [self.expected_orig, self.codex_orig]
        st = STree.STree(input_list)
        longest_lcs = st.lcs()

        return longest_lcs

    def edit_distance(self):
        return editdistance.eval(self.expected_orig, self.codex_orig)

    def calculate(self):
        return {
            "is_exact_match": self.is_exact_match(),
            "is_match": self.is_match(),
            "calc_lcs": self.calc_lcs(),
            "edit_distance": self.edit_distance()
        }

import editdistance
import re
from difflib import SequenceMatcher
from suffix_trees import STree

class Evaluation:
    def __init__(self, expected: str, actual: str):
        self.expected_orig = expected.strip()
        self.actual_orig = actual.strip()

        self.expected = expected.strip()
        self.actual = actual.strip()

    def is_exact_match(self):
        return self.expected == self.actual

    def _strip_full_form(self, assertion):
        listical = list(assertion.split())
        final_str = ''
        found_assertion = False
        for i in range(len(listical)):
            if listical[i].startswith('assert'):
                found_assertion = True
            if found_assertion:
                final_str += listical[i] + ' '
        return final_str

    def _strip_extra_parenthesis(self):
        if '( (' in self.expected and ') )' in self.expected:
            self.expected = self.expected.replace('( (', '(')
            self.expected = self.expected.replace(') )', ')')

    def _replace_assert_true_false_assert_equal(self):
        ASSERT_EQUALS_TRUE = 'assertEquals ( true ,'
        ASSERT_EQUALS_FALSE = 'assertEquals ( false ,'
        ASSERT_TRUE = 'assertTrue ('
        ASSERT_FALSE = 'assertFalse ('
        if (ASSERT_EQUALS_TRUE in self.expected and ASSERT_TRUE in self.actual) or \
                ASSERT_EQUALS_TRUE in self.actual and ASSERT_TRUE in self.expected:
            self.expected = self.expected.replace(ASSERT_EQUALS_TRUE, ASSERT_TRUE)
            self.actual = self.actual.replace(ASSERT_EQUALS_TRUE, ASSERT_TRUE)
        elif (ASSERT_EQUALS_FALSE in self.expected and ASSERT_FALSE in self.actual) or \
                ASSERT_EQUALS_FALSE in self.actual and ASSERT_FALSE in self.expected:
            self.expected = self.expected.replace(ASSERT_EQUALS_FALSE, ASSERT_FALSE)
            self.actual = self.actual.replace(ASSERT_EQUALS_FALSE, ASSERT_FALSE)

    def _match_args(self):
        def find_match(text):
            x = re.findall("\(\s*([^)]+?)\s*\)", text)
            if len(x):
                return [a.strip() for a in x[0].split(',')]
            return []

        def get_assertion_type(text):
            for c in text.split():
                if c.startswith('assert'):
                    return c

        expected_args = sorted(find_match(self.expected))
        actual_args = sorted(find_match(self.actual))

        expected_assertion_type = get_assertion_type(self.expected)
        actual_assertion_type = get_assertion_type(self.actual)
        return len(expected_args) and len(actual_args) and \
               expected_args == actual_args and expected_assertion_type == actual_assertion_type

    def is_match(self):
        if self.expected == self.actual:
            return True

        self.expected = self._strip_full_form(self.expected)
        self.actual = self._strip_full_form(self.actual)

        self._strip_extra_parenthesis()

        if self.expected == self.actual:
            return True

        self._replace_assert_true_false_assert_equal()
        if self.expected == self.actual:
            return True

        if self._match_args():
            return True

        return False

    def calc_lcs(self):
        """
        https://stackoverflow.com/questions/18715688/find-common-substring-between-two-strings
        """
        try:
            input_list = [self.expected_orig, self.actual_orig]
            st = STree.STree(input_list)
            longest_lcs = st.lcs()
        except RecursionError as e:
            print(e)
            print(f"error in calc_lcs for {self.expected_orig} and {self.actual_orig}")
            match = SequenceMatcher(None, self.expected_orig, self.actual_orig)\
                .find_longest_match(0, len(self.expected_orig), 0, len(self.actual_orig))
            longest_lcs = self.expected_orig[match.a:match.a + match.size]


        return longest_lcs

    def edit_distance(self):
        return editdistance.eval(self.expected_orig, self.actual_orig)

    def calculate(self):
        return {
            "is_exact_match": self.is_exact_match(),
            "is_match": self.is_match(),
            "calc_lcs": self.calc_lcs(),
            "edit_distance": self.edit_distance()
        }

# e = Evaluation('org . junit . Assert . assertEquals ( true , result )', 'org . junit . Assert . assertTrue ( result )')
# print(e.is_match())
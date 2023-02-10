from collections import namedtuple
from enum import Enum

atlas_datapoint = namedtuple('Datapoint',
                             "focal_method "
                             "test_method "
                             "assertion "
                             "assertion_type "
                             "method_name "
                             "test_name "
                             "complexity")

class atlas_datapoint_with_demo_length:
    def __init__(self, datapoint: atlas_datapoint, token_count: int):
        self.datapoint = datapoint
        self.token_count = token_count

atlas_mode = Enum('atlas_mode',
                  'zero_shot '
                  'random_1_shot '
                  'random_n_shot '
                  'random_n_shot_until_context_window '
                  'random_assertion_by_category_n_shot '
                  'bm_25 '
                  'semantic_search')

atlas_result = namedtuple('AtlasResult',
                          "prompt expected actual "
                          "is_exact_match is_match "
                          "lcs edit_distance "
                          "inference_time "
                          "gpt_token_count "
                          "word_count "
                          "response_completion_tokens "
                          "response_prompt_tokens "
                          "response_total_tokens")

atlas_stat = namedtuple('AtlasStat',
                        "query "
                        "assertion_type "
                        "gpt_token_count_focal_method "
                        "gpt_token_count_test_method "
                        "gpt_token_count_assertion_completion "
                        "gpt_token_count_demo "
                        "word_count_demo")

tfix_datapoint = namedtuple('Datapoint',
                            "source_code "
                            "target_code "
                            "source_file "
                            "target_file "
                            "linter_report_evidence linter_report_message linter_report_rule_id "
                            "warning_line "
                            "repo")

tfix_mode = Enum('tfix_mode',
                 'zero_shot '
                 'random_1_shot '
                 'random_52_shot '
                 'random_52_shot_1_example_per_category '
                 'random_assertion_by_category_n_shot_util_8000_tokens '
                 'random_n_shot_until_context_window '
                 'bm_25 '
                 'semantic_search_st_n_shot '
                 'semantic_search_unixcoder_n_shot')

tfix_result = namedtuple('TFixResult',
                          "prompt warning_line "
                          "linter_report_rule_id linter_report_message "
                          "expected codex "
                          "is_exact_match is_match "
                          "lcs edit_distance "
                          "inference_time "
                          "gpt_token_count "
                          "word_count "
                          "response_completion_tokens "
                          "response_prompt_tokens "
                          "response_total_tokens")

tfix_result_without_prompt = namedtuple('TFixResult',
                         "buggy_code warning_line "                         
                         "linter_report_rule_id linter_report_message "
                         "expected codex "
                         "is_exact_match is_match "
                         "lcs edit_distance "
                         "inference_time "
                         "gpt_token_count "
                         "word_count "
                         "response_completion_tokens "
                         "response_prompt_tokens "
                         "response_total_tokens")

tfix_result_top_n = namedtuple('TFixResult',
                         "prompt expected "
                         "codex_1 codex_2 codex_3 codex_4 codex_5 "
                         "is_exact_match is_match "
                         "lcs edit_distance "
                         "inference_time "
                         "gpt_token_count "
                         "word_count "
                         "response_completion_tokens "
                         "response_prompt_tokens "
                         "response_total_tokens")

tufano_datapoint = namedtuple('tufano_datapoint',
                              "source_code_abstracted "
                              "target_code_abstracted "
                              "source_code "
                              "target_code ")

tufano_result = namedtuple('tufano_result',
                           "prompt  "
                           "expected codex "
                           "is_exact_match is_match "
                           "lcs edit_distance "
                           "inference_time "
                           "gpt_token_count "
                           "word_count "
                           "response_completion_tokens "
                           "response_prompt_tokens "
                           "response_total_tokens")

tufano_result_without_prompt = namedtuple('tufano_result_without_prompt',
                                          "buggy_code "
                                          "expected codex "
                                          "is_exact_match is_match "
                                          "lcs edit_distance "
                                          "inference_time "
                                          "gpt_token_count "
                                          "word_count "
                                          "response_completion_tokens "
                                          "response_prompt_tokens "
                                          "response_total_tokens")


sequencer_datapoint = namedtuple('sequencer_datapoint',
                              "buggy_method_context "
                              "buggy_code "
                              "correct_code "
                              "complexity")

sequencer_result = namedtuple('sequencer_result',
                           "prompt  "
                           "expected codex "
                           "is_exact_match is_match "
                           "lcs edit_distance "
                           "inference_time "
                           "gpt_token_count "
                           "word_count "
                           "response_completion_tokens "
                           "response_prompt_tokens "
                           "response_total_tokens")

sequencer_result_without_prompt = namedtuple('sequencer_result_without_prompt',
                                          "buggy_code "
                                          "expected codex "
                                          "is_exact_match is_match "
                                          "lcs edit_distance "
                                          "inference_time "
                                          "gpt_token_count "
                                          "word_count "
                                          "response_completion_tokens "
                                          "response_prompt_tokens "
                                          "response_total_tokens")


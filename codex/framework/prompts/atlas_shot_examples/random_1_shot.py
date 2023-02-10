import models
import random
from models import atlas_datapoint_with_demo_length
from util import utils

from demonstration.atlas_demonstrations import MAX_ATLAS_COMPLETION_LENGTH_TRAIN

def random_1_shot_example(query: str,
                          training_data_with_length:list[atlas_datapoint_with_demo_length]) -> models.atlas_datapoint:
    """
    Returns a random 1-shot example.
        This example was chosen randomly from the set of training examples.
        This random example is taken from line number 72916 in the "dataset/atlas-dataset/Training/testMethods.txt".
    :return:
    """
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_sample: atlas_datapoint_with_demo_length = random.choice(training_data_with_length)
    if random_sample.token_count <= max_demo_length:
        return [random_sample.datapoint]
    else:
        print("WARNING: demo length exceeded. Selecting random example with the max_demo_length.")
        filtered_samples = [x for x in training_data_with_length
                            if x.token_count <= max_demo_length]
        if len(filtered_samples) == 0:
            return []
        return [random.choice(filtered_samples).datapoint]

    #random_example = models.atlas_datapoint(
    #    focal_method='hasAValidHash ( ) { if ( ( this . fileToCheck ) == null ) throw new java . io . FileNotFoundException ( "File<sp>to<sp>check<sp>has<sp>not<sp>been<sp>set!" ) ; if ( ( ( this . expectedFileHash ) == null ) || ( ( this . typeOfHash ) == null ) ) throw new java . lang . NullPointerException ( "Hash<sp>details<sp>have<sp>not<sp>been<sp>set!" ) ; java . lang . String actualFileHash = "" ; boolean isHashValid = false ; switch ( this . typeOfHash ) { case MD5 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . md5Hex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; case SHA1 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . shaHex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; } return isHashValid ; }',
    #    test_method='checkValidMD5Hash ( ) { main . java . actions . CheckFileHash fileToCheck = new main . java . actions . CheckFileHash ( ) ; fileToCheck . fileToCheck ( new java . io . File ( java . lang . System . getProperty ( "java.io.tmpdir" ) ) ) ; fileToCheck . hashDetails ( "617bfc4b78b03a0f61c98188376d2a6d" , HashType . MD5 ) ; "<AssertPlaceHolder>" ; }',
    #    assertion='org . junit . Assert . assertTrue ( fileToCheck . hasAValidHash ( ) )',
    #    assertion_type='assertTrue',
    #    method_name='hasAValidHash',
    #    test_name='checkValidMD5Hash'
    #)
    #return random_example

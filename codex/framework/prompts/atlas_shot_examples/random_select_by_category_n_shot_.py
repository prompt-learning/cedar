import models
import random
from util import utils
from models import atlas_datapoint
from demonstration.atlas_demonstrations import MAX_ATLAS_COMPLETION_LENGTH_TRAIN

def random_select_by_category_n_shot_example() -> models.atlas_datapoint:
    """
    Returns random n-shot example per category.
        This example was chosen randomly from the set of training examples.
        This random example is taken from random line numbers from the "dataset/atlas-dataset/Training/testMethods.txt".
        random numbers were chosen after running the chose_random_number.py script.
    :return:
    """
    # assertEquals - randomly selected from line 101909
    random_assert_equals = models.atlas_datapoint(
        focal_method='size ( ) { return neighbors . size ( ) ; }',
        test_method='testFetchLimit ( ) { createFourArtistsTwoPaintings ( ) ; java . lang . String ejbql = "select<sp>a<sp>FROM<sp>Artist<sp>a" ; org . apache . cayenne . query . EJBQLQuery query = new org . apache . cayenne . query . EJBQLQuery ( ejbql ) ; query . setFetchLimit ( 2 ) ; java . util . List < ? > artists = context . performQuery ( query ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertEquals ( 2 , artists . size ( ) )',
        assertion_type='assertEquals',
        method_name='size',
        test_name='testFetchLimit'
    )

    # assertTrue
    random_assert_true = models.atlas_datapoint(
        focal_method='hasAValidHash ( ) { if ( ( this . fileToCheck ) == null ) throw new java . io . FileNotFoundException ( "File<sp>to<sp>check<sp>has<sp>not<sp>been<sp>set!" ) ; if ( ( ( this . expectedFileHash ) == null ) || ( ( this . typeOfHash ) == null ) ) throw new java . lang . NullPointerException ( "Hash<sp>details<sp>have<sp>not<sp>been<sp>set!" ) ; java . lang . String actualFileHash = "" ; boolean isHashValid = false ; switch ( this . typeOfHash ) { case MD5 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . md5Hex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; case SHA1 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . shaHex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; } return isHashValid ; }',
        test_method='checkValidMD5Hash ( ) { main . java . actions . CheckFileHash fileToCheck = new main . java . actions . CheckFileHash ( ) ; fileToCheck . fileToCheck ( new java . io . File ( java . lang . System . getProperty ( "java.io.tmpdir" ) ) ) ; fileToCheck . hashDetails ( "617bfc4b78b03a0f61c98188376d2a6d" , HashType . MD5 ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertTrue ( fileToCheck . hasAValidHash ( ) )',
        assertion_type='assertTrue',
        method_name='hasAValidHash',
        test_name='checkValidMD5Hash'
    )

    # assertNotNull - randomly selected from line 112375
    random_assert_not_null = models.atlas_datapoint(
        focal_method='getPort ( ) { return port ; }',
        test_method='testCreate ( ) { com . ctrip . xpipe . simpleserver . Server server = startEmptyServer ( ) ; com . ctrip . xpipe . redis . proxy . monitor . stats . PingStats pingStats = manager . create ( new com . ctrip . xpipe . redis . core . proxy . endpoint . DefaultProxyEndpoint ( java . lang . String . format ( "%s://%s:%d" , ProxyEndpoint . PROXY_SCHEME . TCP . name ( ) , "127.0.0.1" , server . getPort ( ) ) ) ) ; "<AssertPlaceHolder>" ; server . stop ( ) ; }',
        assertion='org . junit . Assert . assertNotNull ( pingStats )',
        assertion_type='assertNotNull',
        method_name='getPort',
        test_name='testCreate'
    )

    # assertThat - randomly selected from line 36916
    random_assert_that = models.atlas_datapoint(
        focal_method='is ( java . lang . String ) { return ( com . threewks . thundr . configuration . Environment . environment ) == null ? environment == null : com . threewks . thundr . configuration . Environment . environment . equals ( environment ) ; }',
        test_method='shouldReturnNegotiatedViewRespectingQualityParameters ( ) { viewNegotiatorRegistry . addNegotiator ( "application/json" , jsonNegotiator ) ; viewNegotiatorRegistry . addNegotiator ( "application/javascript" , jsonpNegotiator ) ; req . withHeader ( Header . Accept , "application/json;q=0.7,application/javascript;q=0.8" ) ; com . threewks . thundr . view . negotiating . Negotiator < ? > result = strategy . findNegotiator ( req , view , viewNegotiatorRegistry ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertThat ( result , is ( jsonpNegotiator ) )',
        assertion_type='assertThat',
        method_name='is',
        test_name='shouldReturnNegotiatedViewRespectingQualityParameters'
    )

    # assertNull - chosen randomly from line 87057
    random_assert_null = models.atlas_datapoint(
        focal_method='next ( ) { checkClosed ( ) ; if ( hasNext ( ) ) { return batchResults . next ( ) ; } batchResults . next ( ) ; return false ; }',
        test_method='testDefaultResponse ( ) { java . lang . String query = "exec<sp>logoutUser();" ; java . lang . String expectedURL = "http://petstore.swagger.io/v2/user/logout" ; java . lang . String response = "" ; org . teiid . translator . ProcedureExecution excution = helpProcedureExecute ( query , response , expectedURL , 200 , true , "GET" , null , getHeaders ( ) ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertNull ( excution . next ( ) )',
        assertion_type='assertNull',
        method_name='next',
        test_name='testDefaultResponse'
    )

    # assertFalse - randomly selected from line 110481
    random_assert_false = models.atlas_datapoint(
        focal_method='iterator ( ) { return createFieldList ( ) . iterator ( ) ; }',
        test_method='interfaceTest ( ) { nl . jqno . equalsverifier . internal . reflection . FieldIterable iterable = nl . jqno . equalsverifier . internal . reflection . FieldIterable . of ( nl . jqno . equalsverifier . internal . reflection . Interface . class ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertFalse ( iterable . iterator ( ) . hasNext ( ) )',
        assertion_type='assertFalse',
        method_name='iterator',
        test_name='interfaceTest'
    )

    # assertArrayEquals - randomly selected from line 150201
    random_assert_array_equals = models.atlas_datapoint(
        focal_method='getFileNames ( ) { if ( ( returnCode ) == ( org . eclipse . swt . SWT . OK ) ) { java . lang . String [ ] completedFileNames = getCompletedFileNames ( ) ; if ( ( isMulti ( ) ) || ( ( completedFileNames . length ) == 0 ) ) { return completedFileNames ; } return new java . lang . String [ ] { completedFileNames [ ( ( completedFileNames . length ) - 1 ) ] } ; } return org . eclipse . swt . widgets . FileDialog . EMPTY_ARRAY ; }',
        test_method='testGetFileNames_returnsAllCompletedFileNames_forMulti ( ) { completedFileNames = new java . lang . String [ ] { "foo.gif" , "bar.doc" , "baz.txt" } ; getOKButton ( ) . notifyListeners ( SWT . Selection , null ) ; java . lang . String [ ] fileNames = dialog . getFileNames ( ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertArrayEquals ( new java . lang . String [ ] { "foo.gif" , "bar.doc" , "baz.txt" } , fileNames )',
        assertion_type='assertArrayEquals',
        method_name='getFileNames',
        test_name='testGetFileNames_returnsAllCompletedFileNames_forMulti'
    )

    # assertSame - randomly selected from line 34373
    random_assert_same = models.atlas_datapoint(
        focal_method='parse ( java . lang . String ) { if ( line == null ) { return null ; } if ( line . equals ( org . metricssampler . daemon . ControlCommandParser . CMD_SHUTDOWN ) ) { return factory . shutdown ( ) ; } else if ( line . equals ( org . metricssampler . daemon . ControlCommandParser . CMD_STATUS ) ) { return factory . status ( ) ; } else { if ( line . startsWith ( "sampler<sp>" ) ) { final org . metricssampler . daemon . commands . ControlCommand result = processSamplerCommand ( line ) ; if ( result != null ) { return result ; } } else if ( line . startsWith ( "resource<sp>" ) ) { final org . metricssampler . daemon . commands . ControlCommand result = processResourceCommand ( line ) ; if ( result != null ) { return result ; } } return factory . invalidSyntax ( line , "could<sp>not<sp>parse<sp>command" ) ; } }',
        test_method='parseEnableSamplerForDurationHourRegExp ( ) { final org . metricssampler . daemon . commands . ControlCommand expected = mock ( org . metricssampler . daemon . commands . ControlCommand . class ) ; when ( factory . enableSamplerForDuration ( "^what.*ever.+$" , 3600L ) ) . thenReturn ( expected ) ; final org . metricssampler . daemon . commands . ControlCommand result = testee . parse ( "sampler<sp>^what.*ever.+$<sp>enable<sp>for<sp>1<sp>hour" ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertSame ( expected , result )',
        assertion_type='assertSame',
        method_name='parse',
        test_name='parseEnableSamplerForDurationHourRegExp'
    )

    return [random_assert_equals, random_assert_true,
            random_assert_not_null, random_assert_that,
            random_assert_null, random_assert_false,
            random_assert_array_equals, random_assert_same]

def random_select_by_category_n_shot_example(query: str,
                                             training_data: list[models.atlas_datapoint],
                                             training_data_with_length: list[models.atlas_datapoint_with_demo_length],
                                             with_commands: bool,
                                             how_many_examples: int = 1) -> list[models.atlas_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    datapoints_by_atlas_assertion_type = {}

    for r in training_data_with_length:
        dp = r.datapoint
        if dp.assertion_type in datapoints_by_atlas_assertion_type:
            datapoints_by_atlas_assertion_type[dp.assertion_type].append(r)
        else:
            datapoints_by_atlas_assertion_type[dp.assertion_type] = [r]

    how_many_assertion_categories = len(datapoints_by_atlas_assertion_type.keys())
    print(f"how_many_assertion_categories: {how_many_assertion_categories}")

    random_samples = []
    random_samples_length = 0
    for _, datapoints in datapoints_by_atlas_assertion_type.items():
        random_choice = random.choice(datapoints)
        random_samples.append(random_choice)
        random_samples_length += random_choice.token_count

    results = []
    if random_samples_length <= max_demo_length:
        results = random_samples
    else:
        print("Check: this should not happen. random_samples_length > max_demo_length")
        random_samples = []
        random_samples_length = 0
        avg_length_per_example = max_demo_length / (how_many_examples * 1)
        for _, datapoints in datapoints_by_atlas_assertion_type.items():
            filtered_samples = [x for x in datapoints
                                if x.token_token_count <= avg_length_per_example]

            if len(filtered_samples) == 0:
                datapoints_sorted = sorted(datapoints, key = lambda x: x.token_count)
                choice = datapoints_sorted[0]
                random_samples.append(choice)
                random_samples_length += choice.token_count
            else:
                random_choice = random.choice(filtered_samples)
                random_samples.append(random_choice)
                random_samples_length += random_choice.token_count
        results = random_samples

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [x.datapoint for x in results]
    return results
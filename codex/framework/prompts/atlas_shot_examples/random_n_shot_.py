import models
from models import atlas_datapoint
from util import utils
import random
from demonstration.atlas_demonstrations import MAX_ATLAS_COMPLETION_LENGTH_TRAIN

def random_n_shot_example_() -> list[models.atlas_datapoint]:
    """
    Returns random n-shot example.
        This example was chosen randomly from the set of training examples.
        This random example is taken from random line numbers from the "dataset/atlas-dataset/Training/testMethods.txt".
        random numbers were chosen after running the chose_random_number.py script.
    :return:
    """
    # random example - line 72963
    random_example_1 = models.atlas_datapoint(
        focal_method='isEmpty ( ) { return ( simpleProperties . isEmpty ( ) ) && ( nestedProperties . isEmpty ( ) ) ; }',
        test_method='availableExtensionsShouldReportNoExtensionsWhenNoFactoriesAvailable ( ) { org . kaazing . gateway . transport . nio . internal . socket . TcpExtensionFactory factory = org . kaazing . gateway . transport . nio . internal . socket . TcpExtensionFactory . newInstance ( new org . kaazing . gateway . transport . nio . internal . TcpExtensionFactoryTest . TestClassLoader ( ) ) ; java . util . Collection < org . kaazing . gateway . transport . nio . TcpExtensionFactorySpi > extensions = factory . availableExtensions ( ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertTrue ( extensions . isEmpty ( ) )',
        assertion_type='assertTrue',
        method_name='isEmpty',
        test_name='availableExtensionsShouldReportNoExtensionsWhenNoFactoriesAvailable'
    )

    # random example - line 28527
    random_example_2 = models.atlas_datapoint(
        focal_method='getPublicationStatuses ( ) { if ( ( this . publicationStatuses ) == null ) { this . publicationStatuses = new java . util . ArrayList ( ) ; } return this . publicationStatuses ; }',
        test_method='testSetPublicationStatuses4 ( ) { this . statuses = null ; this . solrSearchResult . setPublicationStatuses ( this . statuses ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertEquals ( new java . util . ArrayList ( ) , solrSearchResult . getPublicationStatuses ( ) )',
        assertion_type='assertEquals',
        method_name='getPublicationStatuses',
        test_name='testSetPublicationStatuses4'
    )

    # random example - line 46005
    random_example_3 = models.atlas_datapoint(
        focal_method='size ( ) { return ( rawValues . size ( ) ) + 2 ; }',
        test_method='size_null ( ) { com . psddev . dari . util . ObjectMapTest . ObjValues obj = new com . psddev . dari . util . ObjectMapTest . ObjValues ( ) ; obj . field_pub = null ; com . psddev . dari . util . ObjectMap objmap = new com . psddev . dari . util . ObjectMap ( obj ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertEquals ( 3 , objmap . size ( ) )',
        assertion_type='assertEquals',
        method_name='size',
        test_name='size_null'
    )

    # random example - line 65709
    random_example_4 = models.atlas_datapoint(
        focal_method='getSql ( ) { return sql ; }',
        test_method='testCreateSqlQuery ( ) { java . lang . String sql = "select<sp>*<sp>from<sp>dictionaries" ; org . dayatang . persistence . jpa . SqlQuery query = repository . createSqlQuery ( sql ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertEquals ( sql , query . getSql ( ) )',
        assertion_type='assertEquals',
        method_name='getSql',
        test_name='testCreateSqlQuery'
    )

    # random example - line 61729
    random_example_5 = models.atlas_datapoint(
        focal_method="""diff ( com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNode , com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNode , java . util . Comparator ) { com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference nodeDifference ; if ( ( originalNode == null ) && ( newNode == null ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . NONE ; } else if ( originalNode == null ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . NEW_NODE ; } else if ( newNode == null ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . REMOVED_NODE ; } else if ( ( dimensionComparator . compare ( originalNode . getDimension ( ) , newNode . getDimension ( ) ) ) != 0 ) { throw new java . lang . IllegalArgumentException ( "Original<sp>node<sp>and<sp>new<sp>node<sp>are<sp>not<sp>for<sp>the<sp>same<sp>product<sp>dimension" ) ; } else if ( ( originalNode . isUnit ( ) ) != ( newNode . isUnit ( ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . PARTITION_TYPE_CHANGE ; } else if ( ( originalNode . isExcludedUnit ( ) ) != ( newNode . isExcludedUnit ( ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . EXCLUDED_UNIT_CHANGE ; } else if ( ( ( ! ( originalNode . isExcludedUnit ( ) ) ) && ( originalNode . isUnit ( ) ) ) && ( newNode . isUnit ( ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . NONE ; if ( ! ( java . util . Objects . equals ( originalNode . getBid ( ) , newNode . getBid ( ) ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . BIDDABLE_UNIT_CHANGE ; } if ( ! ( java . util . Objects . equals ( originalNode . getTrackingUrlTemplate ( ) , newNode . getTrackingUrlTemplate ( ) ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . BIDDABLE_UNIT_CHANGE ; } if ( ! ( java . util . Objects . equals ( originalNode . getCustomParameters ( ) , newNode . getCustomParameters ( ) ) ) ) { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . BIDDABLE_UNIT_CHANGE ; } } else { nodeDifference = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference . NONE ; } return nodeDifference ; }""",
        test_method='testFindNodeDifference_origNull ( ) { com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNode newNode = new com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNode ( null , null , ( - 1L ) , dimensionComparator ) ; com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . NodeDifference diff = com . google . api . ads . adwords . axis . utils . v201809 . shopping . ProductPartitionNodeDiffer . diff ( null , newNode , dimensionComparator ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertEquals ( NodeDifference . NEW_NODE , diff )',
        assertion_type='assertEquals',
        method_name='diff',
        test_name='testFindNodeDifference_origNull'
    )

    # random example - line 106064
    random_example_6 = models.atlas_datapoint(
        focal_method='toLong ( java . lang . Long ) { return value != null ? new java . lang . Long ( value ) : null ; }',
        test_method="""convertToLongNull ( ) { java . lang . Double df = null ; java . lang . Long l = converter . toLong ( df ) ; "<AssertPlaceHolder>" ; }""",
        assertion='org . junit . Assert . assertNull ( l )',
        assertion_type='assertNull',
        method_name='toLong',
        test_name='convertToLongNull'
    )

    # random example - line 988
    random_example_7 = models.atlas_datapoint(
        focal_method='getNextAvailable ( int ) { if ( ( fromPort < ( org . apache . camel . test . AvailablePortFinder . currentMinPort . get ( ) ) ) || ( fromPort > ( org . apache . camel . test . AvailablePortFinder . MAX_PORT_NUMBER ) ) ) { throw new java . lang . IllegalArgumentException ( ( "From<sp>port<sp>number<sp>not<sp>in<sp>valid<sp>range:<sp>" + fromPort ) ) ; } for ( int i = fromPort ; i <= ( org . apache . camel . test . AvailablePortFinder . MAX_PORT_NUMBER ) ; i ++ ) { if ( org . apache . camel . test . AvailablePortFinder . available ( i ) ) { org . apache . camel . test . AvailablePortFinder . LOG . info ( "getNextAvailable({})<sp>-><sp>{}" , fromPort , i ) ; return i ; } } throw new java . util . NoSuchElementException ( ( "Could<sp>not<sp>find<sp>an<sp>available<sp>port<sp>above<sp>" + fromPort ) ) ; }',
        test_method="""testGetNextAvailablePortInt ( ) { int p1 = org . apache . camel . test . AvailablePortFinder . getNextAvailable ( 9123 ) ; int p2 = org . apache . camel . test . AvailablePortFinder . getNextAvailable ( 9123 ) ; "<AssertPlaceHolder>" ; }""",
        assertion='org . junit . Assert . assertEquals ( p1 , p2 )',
        assertion_type='assertEquals',
        method_name='getNextAvailable',
        test_name='testGetNextAvailablePortInt'
    )

    # random example - line 84055
    random_example_8 = models.atlas_datapoint(
        focal_method='homeResources ( ) { if ( ( home . get ( ) ) == null ) { home . compareAndSet ( null , new com . smartsheet . api . internal . HomeResourcesImpl ( this ) ) ; } return home . get ( ) ; }',
        test_method="""testHome ( ) { "<AssertPlaceHolder>" ; }""",
        assertion='org . junit . Assert . assertNotNull ( smartsheet . homeResources ( ) )',
        assertion_type='assertNotNull',
        method_name='homeResources',
        test_name='testHome'
    )






    # random example - line 48619
    random_example_9 = models.atlas_datapoint(
        focal_method='checkSetEquality ( edu . illinois . cs . cogcomp . datalessclassification . Set , edu . illinois . cs . cogcomp . datalessclassification . Set ) { if ( ( goldLabels . size ( ) ) != ( predictedLabels . size ( ) ) ) return false ; for ( java . lang . String goldLabel : goldLabels ) { if ( ( predictedLabels . contains ( goldLabel ) ) == false ) return false ; } return true ; }',
        test_method="""testPredictions ( ) { try { configFile = "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 0 ; edu . illinois . cs . cogcomp . core . utilities . configuration . ResourceManager nonDefaultRm = new edu . illinois . cs . cogcomp . core . utilities . configuration . ResourceManager ( configFile ) ; edu . illinois . cs . cogcomp . core . utilities . configuration . ResourceManager rm = new edu . illinois . cs . cogcomp . datalessclassification . config . ESADatalessConfigurator ( ) . getConfig ( nonDefaultRm ) ; dataless = new edu . illinois . cs . cogcomp . datalessclassification . ta . ESADatalessAnnotator ( rm ) ; documents = new edu . illinois . cs . cogcomp . datalessclassification . ArrayList ( ) ; java . lang . String doc1 = "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 6 + ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 5 + "<sp>and<sp>hijaak<sp>for<sp>windows<sp>anyone<sp>have<sp>any<sp>experience<sp>with<sp>those<sp>or<sp>some<sp>others" ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 2 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 8 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 3 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" ) + "yes<sp>i<sp>know<sp>it<sp>s<sp>nowhere<sp>near<sp>christmas<sp>time<sp>but<sp>i<sp>m<sp>gonna<sp>loose<sp>net<sp>access<sp>in<sp>a<sp>few<sp>days<sp>maybe<sp>" 0 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 5 ) + "rec.autos" 2 ) + "rec.autos" 9 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 2 ) + "rec.autos" 6 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 0 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 5 ) + "other<sp>parts<sp>of<sp>the<sp>window<sp>if<sp>you<sp>understood<sp>my<sp>description<sp>can<sp>you<sp>tell<sp>me<sp>if<sp>another<sp>" ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 9 ) + "what<sp>lies<sp>behind<sp>us<sp>and<sp>what<sp>lies<sp>technically<sp>a<sp>writer<sp>before<sp>us<sp>are<sp>tiny<sp>matters<sp>compared<sp>" ) + "delgreco<sp>rahul<sp>net<sp>to<sp>what<sp>lies<sp>within<sp>us<sp>oliver<sp>wendell<sp>holmes<sp>david<sp>f<sp>delgreco<sp>delgreco<sp>rahul<sp>" ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" ) ; documents . add ( doc1 ) ; java . lang . String doc2 = "yes<sp>i<sp>know<sp>it<sp>s<sp>nowhere<sp>near<sp>christmas<sp>time<sp>but<sp>i<sp>m<sp>gonna<sp>loose<sp>net<sp>access<sp>in<sp>a<sp>few<sp>days<sp>maybe<sp>" + ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( "rec.autos" 1 + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 8 ) + "rec.autos" 8 ) + "rec.autos" 3 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 9 ) + "rec.autos" 0 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 0 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 3 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 7 ) + "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 4 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 4 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 6 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 2 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 1 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 7 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 6 ) + "rec.autos" 7 ) + "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 8 ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 1 ) ; documents . add ( doc2 ) ; docLabels = new edu . illinois . cs . cogcomp . datalessclassification . ArrayList ( ) ; edu . illinois . cs . cogcomp . datalessclassification . Set < java . lang . String > docLabels1 = new edu . illinois . cs . cogcomp . datalessclassification . HashSet ( edu . illinois . cs . cogcomp . datalessclassification . Arrays . asList ( "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 4 , "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 9 ) ) ; docLabels . add ( docLabels1 ) ; edu . illinois . cs . cogcomp . datalessclassification . Set < java . lang . String > docLabels2 = new edu . illinois . cs . cogcomp . datalessclassification . HashSet ( edu . illinois . cs . cogcomp . datalessclassification . Arrays . asList ( "net<sp>recommendation<sp>for<sp>screen<sp>capture<sp>program" 7 , "rec.autos" ) ) ; docLabels . add ( docLabels2 ) ; } catch ( java . io . IOException e ) { e . printStackTrace ( ) ; System . out . println ( ( "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 1 + ( e . getMessage ( ) ) ) ) ; org . junit . Assert . fail ( ( "driving<sp>me<sp>crazy<sp>tonight<sp>it<sp>decided<sp>that<sp>for<sp>any<sp>graphic<sp>it<sp>writes<sp>out<sp>as<sp>a<sp>tiff<sp>" 1 + ( e . getMessage ( ) ) ) ) ; } try { for ( int i = 0 ; i < ( documents . size ( ) ) ; i ++ ) { java . lang . String docText = documents . get ( i ) ; edu . illinois . cs . cogcomp . datalessclassification . Set < java . lang . String > docPredictions = getPredictions ( getTextAnnotation ( docText ) , dataless ) ; System . out . println ( ( ( "Doc" + i ) + "rec.autos" 4 ) ) ; for ( java . lang . String goldLabel : docLabels . get ( i ) ) { System . out . println ( goldLabel ) ; } System . out . println ( ( ( "Doc" + i ) + "resistor<sp>if<sp>you<sp>can<sp>get<sp>one<sp>caution<sp>do<sp>not<sp>replace<sp>with<sp>a<sp>standard<sp>c<sp>bulb<sp>as<sp>these<sp>" 3 ) ) ; for ( java . lang . String predictedLabel : docPredictions ) { System . out . println ( predictedLabel ) ; } "<AssertPlaceHolder>" ; System . out . println ( ) ; } } catch ( edu . illinois . cs . cogcomp . annotation . AnnotatorException e ) { e . printStackTrace ( ) ; System . out . println ( ( "rec.autos" 5 + ( e . getMessage ( ) ) ) ) ; org . junit . Assert . fail ( ( "rec.autos" 5 + ( e . getMessage ( ) ) ) ) ; } }""",
        assertion='org . junit . Assert . assertTrue ( checkSetEquality ( docLabels . get ( i ) , docPredictions ) )',
        assertion_type='assertTrue',
        method_name='checkSetEquality',
        test_name='testPredictions'
    )

    # random example - line 20218
    random_example_10 = models.atlas_datapoint(
        focal_method='resolvers ( com . betfair . cougar . api . export . Protocol ) { if ( protocol == ( com . betfair . cougar . api . export . Protocol . SOAP ) ) { return new com . betfair . cougar . transport . api . DehydratedExecutionContextResolver [ ] { ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . SoapIdentityTokenResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpLocationResolver ( geoIPLocator , geoLocationDeserializer , inferredCountryResolver ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpReceivedTimeResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpRequestedTimeResolver ( requestTimeResolver ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpRequestUuidResolver ( uuidHeader , uuidParentsHeader ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpTraceLoggingResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpTransportStrengthResolver ( unknownCipherKeyLength ) ) ) } ; } if ( protocol . underlyingTransportIsHttp ( ) ) { return new com . betfair . cougar . transport . api . DehydratedExecutionContextResolver [ ] { ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpIdentityTokenResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpLocationResolver ( geoIPLocator , geoLocationDeserializer , inferredCountryResolver ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpReceivedTimeResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpRequestedTimeResolver ( requestTimeResolver ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpRequestUuidResolver ( uuidHeader , uuidParentsHeader ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpTraceLoggingResolver ( ) ) ) , ( ( com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < T , B > ) ( new com . betfair . cougar . transport . impl . protocol . http . HttpTransportStrengthResolver ( unknownCipherKeyLength ) ) ) } ; } return null ; }',
        test_method='otherHttp ( ) { com . betfair . cougar . transport . impl . protocol . http . DefaultExecutionContextResolverFactory factory = new com . betfair . cougar . transport . impl . protocol . http . DefaultExecutionContextResolverFactory ( ) ; com . betfair . cougar . transport . api . DehydratedExecutionContextResolver < com . betfair . cougar . transport . api . protocol . http . HttpCommand , java . lang . Void > [ ] resolvers = factory . resolvers ( Protocol . RESCRIPT ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertTrue ( ( ( resolvers [ 0 ] ) instanceof com . betfair . cougar . transport . impl . protocol . http . HttpIdentityTokenResolver ) )',
        assertion_type='assertTrue',
        method_name='resolvers',
        test_name='otherHttp'
    )

    # random example - line 72916
    random_example_11 = models.atlas_datapoint(
        focal_method='hasAValidHash ( ) { if ( ( this . fileToCheck ) == null ) throw new java . io . FileNotFoundException ( "File<sp>to<sp>check<sp>has<sp>not<sp>been<sp>set!" ) ; if ( ( ( this . expectedFileHash ) == null ) || ( ( this . typeOfHash ) == null ) ) throw new java . lang . NullPointerException ( "Hash<sp>details<sp>have<sp>not<sp>been<sp>set!" ) ; java . lang . String actualFileHash = "" ; boolean isHashValid = false ; switch ( this . typeOfHash ) { case MD5 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . md5Hex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; case SHA1 : actualFileHash = org . apache . commons . codec . digest . DigestUtils . shaHex ( new java . io . FileInputStream ( this . fileToCheck ) ) ; if ( this . expectedFileHash . equals ( actualFileHash ) ) isHashValid = true ; break ; } return isHashValid ; }',
        test_method='checkValidMD5Hash ( ) { main . java . actions . CheckFileHash fileToCheck = new main . java . actions . CheckFileHash ( ) ; fileToCheck . fileToCheck ( new java . io . File ( java . lang . System . getProperty ( "java.io.tmpdir" ) ) ) ; fileToCheck . hashDetails ( "617bfc4b78b03a0f61c98188376d2a6d" , HashType . MD5 ) ; "<AssertPlaceHolder>" ; }',
        assertion='org . junit . Assert . assertTrue ( fileToCheck . hasAValidHash ( ) )',
        assertion_type='assertTrue',
        method_name='hasAValidHash',
        test_name='checkValidMD5Hash'
    )

    # random example - line 61716
    random_example_12 = models.atlas_datapoint(
        focal_method='toString ( ) { return ( ( ( ( ( "Annotation<sp>[start=" + ( start ) ) + ",<sp>end=" ) + ( end ) ) + ",<sp>data=" ) + ( data ) ) + "]" ; }',
        test_method="""testReplace ( com . joliciel . talismane . lexicon . Diacriticizer ) { new mockit . NonStrictExpectations ( ) { { diacriticizer . diacriticize ( "VEUX" ) ; returns ( new java . util . HashSet ( java . util . Arrays . asList ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 3 ) ) ) ; diacriticizer . diacriticize ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 6 ) ; returns ( new java . util . HashSet ( java . util . Arrays . asList ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 7 ) ) ) ; diacriticizer . diacriticize ( "src/test/resources/test.conf" 2 ) ; returns ( new java . util . HashSet ( java . util . Arrays . asList ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 1 ) ) ) ; diacriticizer . diacriticize ( "AMERIQUE" ) ; returns ( new java . util . HashSet ( java . util . Arrays . asList ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 4 ) ) ) ; } } ; java . lang . System . setProperty ( "config.file" , "src/test/resources/test.conf" ) ; com . typesafe . config . ConfigFactory . invalidateCaches ( ) ; final com . typesafe . config . Config config = com . typesafe . config . ConfigFactory . load ( ) ; final com . joliciel . talismane . TalismaneSession session = new com . joliciel . talismane . TalismaneSession ( config , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 0 ) ; session . setDiacriticizer ( diacriticizer ) ; com . joliciel . talismane . tokeniser . filters . UppercaseSeriesFilter filter = new com . joliciel . talismane . tokeniser . filters . UppercaseSeriesFilter ( session ) ; java . lang . String text = "src/test/resources/test.conf" 9 ; com . joliciel . talismane . rawText . Sentence sentence = new com . joliciel . talismane . rawText . Sentence ( text , session ) ; com . joliciel . talismane . tokeniser . TokenSequence tokenSequence = new com . joliciel . talismane . tokeniser . TokenSequence ( sentence , session ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 3.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 2.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>" . length ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 9.le ngth ( ) ) ; tokenSequence . addToken ( "src/test/resources/test.conf" 4.le ngth ( ) , "src/test/resources/test.conf" 0.le ngth ( ) ) ; tokenSequence . addToken ( "src/test/resources/test.conf" 5.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 8.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" . length ( ) , "src/test/resources/test.conf" 7.le ngth ( ) ) ; tokenSequence . addToken ( "src/test/resources/test.conf" 7.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 7.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 6.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 0.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 8.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>" 5.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 1.le ngth ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 2.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 4.le ngth ( ) , "src/test/resources/test.conf" 3.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>" . length ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" 5.le ngth ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>" . length ( ) , "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur" . length ( ) ) ; tokenSequence . addToken ( "Je<sp>VEUX<sp>SAVOIR<sp>la<sp>VERITE,<sp>je<sp>VEUX<sp>SAVOIR<sp>LA<sp>VERITE<sp>sur<sp>" . length ( ) , "src/test/resources/test.conf" 8.le ngth ( ) ) ; tokenSequence . addToken ( "src/test/resources/test.conf" 8.le ngth ( ) , "src/test/resources/test.conf" 6.le ngth ( ) ) ; tokenSequence . addToken ( "src/test/resources/test.conf" 6.le ngth ( ) , "src/test/resources/test.conf" 9.le ngth ( ) ) ; filter . apply ( tokenSequence ) ; System . out . println ( tokenSequence ) ; java . lang . StringBuilder sb = new java . lang . StringBuilder ( ) ; for ( com . joliciel . talismane . tokeniser . Token token : tokenSequence ) { sb . append ( token . getText ( ) ) ; sb . append ( ' | ' ) ; } "<AssertPlaceHolder>" ; }""",
        assertion='org . junit . Assert . assertEquals ( "src/test/resources/test.conf" 1 , sb . toString ( ) )',
        assertion_type='assertEquals',
        method_name='toString',
        test_name='testReplace'
    )

    return [random_example_1, random_example_2,
            random_example_3, random_example_4,
            random_example_5, random_example_6,
            random_example_7, random_example_8]


def random_n_shot_example(query: str,
                          training_data: list[atlas_datapoint],
                          training_data_with_length: list[models.atlas_datapoint_with_demo_length],
                          with_commands:bool,
                          n=8) -> list[models.atlas_datapoint]:
    length_of_query = utils.count_codex_tokens(query)
    length_of_completion = MAX_ATLAS_COMPLETION_LENGTH_TRAIN
    max_demo_length = 8000 - (length_of_query + length_of_completion)

    random_samples: list[models.atlas_datapoint_with_demo_length] = random.sample(training_data_with_length, n)

    results = []
    random_samples_length = 0
    for sample in random_samples:
        random_samples_length += sample.token_count
        if random_samples_length > max_demo_length:
            break
        else:
            results.append(sample.datapoint)

    if len(results) != n:
        average_dmeo_length = max_demo_length / n
        random_samples:list[models.atlas_datapoint_with_demo_length] = random.sample(training_data_with_length, 5000)

        chose_samples_that_fits_within_context_window = []
        for sample in random_samples:
            if sample.token_count <= average_dmeo_length:
                chose_samples_that_fits_within_context_window.append(sample)
                if len(chose_samples_that_fits_within_context_window) == n:
                    break

        if len(chose_samples_that_fits_within_context_window) < n:
            raise Exception("Could not find enough samples that fits within the context window")
        results = chose_samples_that_fits_within_context_window

    length_so_far = 0
    for r in results:
        length_so_far += r.token_count
        if length_so_far > max_demo_length:
            raise Exception("Demo length exceeded")

    results = [r.datapoint for r in results]
    print(f"number of demonstrations: {len(results)}")
    return results
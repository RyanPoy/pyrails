#coding: utf8
import unittest
from pyactive.tests.test_criteria_insert import CriteriaInsertTestCase
from pyactive.tests.test_criteria_delete import CriteriaDeleteTestCase
from pyactive.tests.test_criteria_update import CriteriaUpdateTestCase
from pyactive.tests.test_criteria_query import CriteriaQueryTestCase
from pyactive.tests.test_criteria_aggregate_functions import CriteriaAggregateFunctionTestCase 

from pyactive.tests.test_record import RecordTestCase
from pyactive.tests.test_record_base import RecordBaseTestCase
from pyactive.tests.test_record_insert import RecordInsertTestCase
from pyactive.tests.test_record_update import RecordUpdateTestCase
from pyactive.tests.test_record_delete import RecordDeleteTestCase
from pyactive.tests.test_record_query import RecordQueryTestCase
from pyactive.tests.test_record_method_missing import RecordMethodMissingTestCase

from pyactive.tests.test_relation_belongs_to import RelationBelongsToTestCase
from pyactive.tests.test_relation_has_one import RelationHasOneTestCase
from pyactive.tests.test_relation_has_many import RelationHasManyTestCase
from pyactive.tests.test_relation_has_and_belongs_to_many import RelationHasAndBelongsToManyTestCase


tests = [
    CriteriaAggregateFunctionTestCase,
    CriteriaInsertTestCase,
    CriteriaDeleteTestCase,
    CriteriaUpdateTestCase,
    CriteriaQueryTestCase,

    RecordBaseTestCase,
    RecordUpdateTestCase,
    RecordInsertTestCase,
    RecordDeleteTestCase,
    RecordQueryTestCase,
    RecordMethodMissingTestCase,

    RelationBelongsToTestCase,
    RelationHasOneTestCase,
    RelationHasManyTestCase,
    RelationHasAndBelongsToManyTestCase,
]


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(t))
    unittest.TextTestRunner().run(suite)

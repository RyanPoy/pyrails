# -*- coding: utf-8 -*-
from ..record import ActiveRecord
import unittest
import fudge


class OrmRecord(ActiveRecord):
    pass


class RecordTestCase(unittest.TestCase):
    
    def setUp(self):
        self.tbname = OrmRecord.__table_name__
    
    def tearDown(self):
        OrmRecord.__table_name__ = self.tbname 
        
    def test_table_name(self):
        self.assertEqual('orm_records', OrmRecord.table_name) 
        self.assertEqual('orm_records', OrmRecord.__table_name__)
        OrmRecord.__table_name__ = 'records'
        self.assertEqual('records', OrmRecord.table_name) 
        
    def test_init(self):
        r = OrmRecord({'a':1, 'b':2}, c=3, d=4, b=5)
        self.assertEquals(1, r.a)
        self.assertEquals(3, r.c)
        self.assertEquals(4, r.d)
        self.assertEquals(5, r.b)
        
    def test_dirty_attributes(self):
        model = OrmRecord(foo='1', bar=2, baz=3)
        model.foo = 1
        model.bar = 20
        model.baz = 30
  
        self.assertTrue(model.is_dirty())
        self.assertTrue(model.is_dirty('foo'))
        self.assertTrue(model.is_dirty('bar'))
        self.assertTrue(model.is_dirty('baz'))
        self.assertTrue(model.is_dirty('foo', 'bar', 'baz'))
#  
#     def test_calculated_attributes(self):
#         model = OrmRecord()
#         model.password = 'secret'
#         attributes = model.get_attributes()
# 
#         self.assertFalse('password' in attributes)
#         self.assertEqual('******', model.password)
#         self.assertEqual('5ebe2294ecd0e0f08eab7690d2a6ee69', attributes['password_hash'])
#         self.assertEqual('5ebe2294ecd0e0f08eab7690d2a6ee69', model.password_hash)
# 
#     def test_new_instance_returns_instance_wit_attributes_set(self):
#         model = OrmRecord()
#         instance = model.new_instance({'name': 'john'})
#         self.assertIsInstance(instance, OrmRecord)
#         self.assertEqual('john', instance.name)
# 
#     def test_hydrate_creates_collection_of_models(self):
#         data = [
#             {'name': 'john'},
#             {'name': 'jane'}
#         ]
#         collection = OrmRecord.hydrate(data, 'foo_connection')
# 
#         self.assertIsInstance(collection, Collection)
#         self.assertEqual(2, len(collection))
#         self.assertIsInstance(collection[0], OrmRecord)
#         self.assertIsInstance(collection[1], OrmRecord)
#         self.assertEqual(collection[0].get_attributes(), collection[0].get_original())
#         self.assertEqual(collection[1].get_attributes(), collection[1].get_original())
#         self.assertEqual('john', collection[0].name)
#         self.assertEqual('jane', collection[1].name)
#         self.assertEqual('foo_connection', collection[0].get_connection_name())
#         self.assertEqual('foo_connection', collection[1].get_connection_name())
# 
#     def test_hydrate_raw_makes_raw_query(self):
#         model = OrmModelHydrateRawStub()
#         connection = MockConnection().prepare_mock()
#         connection.select.return_value = []
#         model.get_connection = mock.MagicMock(return_value=connection)
# 
#         def _set_connection(name):
#             model.__connection__ = name
# 
#             return model
# 
#         OrmModelHydrateRawStub.set_connection = mock.MagicMock(side_effect=_set_connection)
#         collection = OrmModelHydrateRawStub.hydrate_raw('SELECT ?', ['foo'])
#         self.assertEqual('hydrated', collection)
#         connection.select.assert_called_once_with(
#             'SELECT ?', ['foo']
#         )
# 
#     def test_create_saves_new_model(self):
#         model = OrmModelSaveStub.create(name='john')
#         self.assertTrue(model.get_saved())
#         self.assertEqual('john', model.name)
# 
#     def test_find_method_calls_query_builder_correctly(self):
#         result = OrmModelFindStub.find(1)
# 
#         self.assertEqual('foo', result)
# 
#     def test_find_use_write_connection(self):
#         OrmModelFindWithWriteConnectionStub.on_write_connection().find(1)
# 
#     def test_find_with_list_calls_query_builder_correctly(self):
#         result = OrmModelFindManyStub.find([1, 2])
# 
#         self.assertEqual('foo', result)
# 
#     def test_destroy_method_calls_query_builder_correctly(self):
#         OrmModelDestroyStub.destroy(1, 2, 3)
# 
#     def test_with_calls_query_builder_correctly(self):
#         result = OrmModelWithStub.with_('foo', 'bar')
#         self.assertEqual('foo', result)
# 
#     def test_update_process(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'name': 'john'})
# 
#         model = OrmRecord()
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updating: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updated: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('saved: %s' % model.__class__.__name__, model)\
#             .and_return(True)
# 
#         model.id = 1
#         model.foo = 'bar'
#         model.sync_original()
#         model.name = 'john'
#         model.set_exists(True)
#         self.assertTrue(model.save())
# 
#         model.new_query.assert_called_once_with()
#         model._update_timestamps.assert_called_once_with()
# 
#     def test_update_process_does_not_override_timestamps(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'created_at': 'foo', 'updated_at': 'bar'})
# 
#         model = OrmRecord()
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
# 
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updating: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updated: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('saved: %s' % model.__class__.__name__, model)\
#             .and_return(True)
# 
#         model.id = 1
#         model.sync_original()
#         model.created_at = 'foo'
#         model.updated_at = 'bar'
#         model.set_exists(True)
#         self.assertTrue(model.save())
# 
#         model.new_query.assert_called_once_with()
#         self.assertTrue(model._update_timestamps.called)
# 
#     def test_creating_with_only_created_at_column(self):
#         query_builder = flexmock(QueryBuilder)
#         query_builder.should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
# 
#         model = flexmock(OrmModelCreatedAt())
#         model.should_receive('new_query').and_return(Builder(QueryBuilder(None, None, None)))
#         model.should_receive('set_created_at').once()
#         model.should_receive('set_updated_at').never()
#         model.name = 'john'
#         model.save()
# 
#     def test_creating_with_only_updated_at_column(self):
#         query_builder = flexmock(QueryBuilder)
#         query_builder.should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
# 
#         model = flexmock(OrmModelUpdatedAt())
#         model.should_receive('new_query').and_return(Builder(QueryBuilder(None, None, None)))
#         model.should_receive('set_created_at').never()
#         model.should_receive('set_updated_at').once()
#         model.name = 'john'
#         model.save()
# 
#     def test_updating_with_only_created_at_column(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'name': 'john'})
# 
#         model = flexmock(OrmModelCreatedAt())
#         model.id = 1
#         model.sync_original()
#         model.set_exists(True)
#         model.should_receive('new_query').and_return(Builder(QueryBuilder(None, None, None)))
#         model.should_receive('set_created_at').never()
#         model.should_receive('set_updated_at').never()
#         model.name = 'john'
#         model.save()
# 
#     def test_updating_with_only_updated_at_column(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'name': 'john'})
# 
#         model = flexmock(OrmModelUpdatedAt())
#         model.id = 1
#         model.sync_original()
#         model.set_exists(True)
#         model.should_receive('new_query').and_return(Builder(QueryBuilder(None, None, None)))
#         model.should_receive('set_created_at').never()
#         model.should_receive('set_updated_at').once()
#         model.name = 'john'
#         model.save()
# 
#     def test_update_is_cancelled_if_updating_event_returns_false(self):
#         model = flexmock(OrmRecord())
#         query = flexmock(Builder(flexmock(QueryBuilder(None, None, None))))
#         model.should_receive('new_query_without_scopes').once().and_return(query)
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updating: %s' % model.__class__.__name__, model)\
#             .and_return(False)
#         model.set_exists(True)
#         model.foo = 'bar'
# 
#         self.assertFalse(model.save())
# 
#     def test_update_process_without_timestamps(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'name': 'john'})
# 
#         model = flexmock(OrmRecord())
#         model.__timestamps__ = False
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
# 
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         model.should_receive('_fire_model_event').and_return(True)
# 
#         model.id = 1
#         model.sync_original()
#         model.name = 'john'
#         model.set_exists(True)
#         self.assertTrue(model.save())
# 
#         model.new_query.assert_called_once_with()
#         self.assertFalse(model._update_timestamps.called)
# 
#     def test_update_process_uses_old_primary_key(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'id': 2, 'name': 'john'})
# 
#         model = OrmRecord()
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
# 
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updating: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('updated: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('saved: %s' % model.__class__.__name__, model)\
#             .and_return(True)
# 
#         model.id = 1
#         model.sync_original()
#         model.id = 2
#         model.name = 'john'
#         model.set_exists(True)
#         self.assertTrue(model.save())
# 
#         model.new_query.assert_called_once_with()
#         self.assertTrue(model._update_timestamps.called)
# 
#     def test_timestamps_are_returned_as_objects(self):
#         model = Model()
#         model.set_raw_attributes({
#             'created_at': '2015-03-24',
#             'updated_at': '2015-03-24'
#         })
# 
#         self.assertIsInstance(model.created_at, Arrow)
#         self.assertIsInstance(model.updated_at, Arrow)
# 
#     def test_timestamps_are_returned_as_objects_from_timestamps_and_datetime(self):
#         model = Model()
#         model.set_raw_attributes({
#             'created_at': datetime.datetime.utcnow(),
#             'updated_at': time.time()
#         })
# 
#         self.assertIsInstance(model.created_at, Arrow)
#         self.assertIsInstance(model.updated_at, Arrow)
# 
#     def test_timestamps_are_returned_as_objects_on_create(self):
#         model = Model()
#         model.unguard()
# 
#         timestamps = {
#             'created_at': datetime.datetime.now(),
#             'updated_at': datetime.datetime.now()
#         }
# 
#         instance = model.new_instance(timestamps)
# 
#         self.assertIsInstance(instance.created_at, Arrow)
#         self.assertIsInstance(instance.updated_at, Arrow)
# 
#         model.reguard()
# 
#     def test_timestamps_return_none_if_set_to_none(self):
#         model = Model()
#         model.unguard()
# 
#         timestamps = {
#             'created_at': datetime.datetime.now(),
#             'updated_at': datetime.datetime.now()
#         }
# 
#         instance = model.new_instance(timestamps)
#         instance.created_at = None
# 
#         self.assertIsNone(instance.created_at)
# 
#         model.reguard()
# 
#     def test_insert_process(self):
#         query = flexmock(Builder)
# 
#         model = OrmRecord()
#         query_builder = flexmock(QueryBuilder)
#         query_builder.should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
# 
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('creating: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('created: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('saved: %s' % model.__class__.__name__, model)\
#             .and_return(True)
# 
#         model.name = 'john'
#         model.set_exists(False)
#         self.assertTrue(model.save())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
#         self.assertTrue(model._update_timestamps.called)
# 
#         model = OrmRecord()
#         query_builder.should_receive('insert').once().with_args({'name': 'john'})
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
#         model._update_timestamps = mock.MagicMock()
#         model.set_incrementing(False)
# 
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('creating: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('created: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('saved: %s' % model.__class__.__name__, model)\
#             .and_return(True)
# 
#         model.name = 'john'
#         model.set_exists(False)
#         self.assertTrue(model.save())
#         self.assertFalse(hasattr(model, 'id'))
#         self.assertTrue(model.exists)
#         self.assertTrue(model._update_timestamps.called)
# 
#     def test_insert_is_cancelled_if_creating_event_returns_false(self):
#         model = flexmock(OrmRecord())
#         query = flexmock(Builder(flexmock(QueryBuilder(None, None, None))))
#         model.should_receive('new_query_without_scopes').once().and_return(query)
#         events = flexmock(Event())
#         model.__dispatcher__ = events
#         events.should_receive('fire').once()\
#             .with_args('saving: %s' % model.__class__.__name__, model)\
#             .and_return(True)
#         events.should_receive('fire').once()\
#             .with_args('creating: %s' % model.__class__.__name__, model)\
#             .and_return(False)
# 
#         self.assertFalse(model.save())
#         self.assertFalse(model.exists)
# 
#     def test_delete_properly_deletes_model(self):
#         model = OrmRecord()
#         builder = flexmock(Builder(QueryBuilder(None, None, None)))
#         builder.should_receive('where').once().with_args('id', 1).and_return(builder)
#         builder.should_receive('delete').once()
#         model.new_query = mock.MagicMock(return_value=builder)
#         model.touch_owners = mock.MagicMock()
# 
#         model.set_exists(True)
#         model.id = 1
#         model.delete()
# 
#         self.assertTrue(model.touch_owners.called)
# 
#     def test_push_no_relations(self):
#         model = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.should_receive('new_query').once().and_return(builder)
#         model.should_receive('_update_timestamps').once()
# 
#         model.name = 'john'
#         model.set_exists(False)
# 
#         self.assertTrue(model.push())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
# 
#     def test_push_empty_one_relation(self):
#         model = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.should_receive('new_query').once().and_return(builder)
#         model.should_receive('_update_timestamps').once()
# 
#         model.name = 'john'
#         model.set_exists(False)
#         model.set_relation('relation_one', None)
# 
#         self.assertTrue(model.push())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
#         self.assertIsNone(model.relation_one)
# 
#     def test_push_one_relation(self):
#         related1 = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'related1'}, 'id').and_return(2)
#         related1.should_receive('new_query').once().and_return(builder)
#         related1.should_receive('_update_timestamps').once()
# 
#         related1.name = 'related1'
#         related1.set_exists(False)
# 
#         model = flexmock(Model())
#         model.should_receive('resolve_connection').and_return(MockConnection().prepare_mock())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.should_receive('new_query').once().and_return(builder)
#         model.should_receive('_update_timestamps').once()
# 
#         model.name = 'john'
#         model.set_exists(False)
#         model.set_relation('relation_one', related1)
# 
#         self.assertTrue(model.push())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
#         self.assertEqual(2, model.relation_one.id)
#         self.assertTrue(model.relation_one.exists)
#         self.assertEqual(2, related1.id)
#         self.assertTrue(related1.exists)
# 
#     def test_push_empty_many_relation(self):
#         model = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.should_receive('new_query').once().and_return(builder)
#         model.should_receive('_update_timestamps').once()
# 
#         model.name = 'john'
#         model.set_exists(False)
#         model.set_relation('relation_many', Collection([]))
# 
#         self.assertTrue(model.push())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
#         self.assertEqual(0, len(model.relation_many))
# 
#     def test_push_many_relation(self):
#         related1 = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'related1'}, 'id').and_return(2)
#         related1.should_receive('new_query').once().and_return(builder)
#         related1.should_receive('_update_timestamps').once()
# 
#         related1.name = 'related1'
#         related1.set_exists(False)
# 
#         related2 = flexmock(Model())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'related2'}, 'id').and_return(3)
#         related2.should_receive('new_query').once().and_return(builder)
#         related2.should_receive('_update_timestamps').once()
# 
#         related2.name = 'related2'
#         related2.set_exists(False)
# 
#         model = flexmock(Model())
#         model.should_receive('resolve_connection').and_return(MockConnection().prepare_mock())
#         query = flexmock(QueryBuilder(MockConnection().prepare_mock(), QueryGrammar(), QueryProcessor()))
#         builder = Builder(query)
#         builder.get_query().should_receive('insert_get_id').once().with_args({'name': 'john'}, 'id').and_return(1)
#         model.should_receive('new_query').once().and_return(builder)
#         model.should_receive('_update_timestamps').once()
# 
#         model.name = 'john'
#         model.set_exists(False)
#         model.set_relation('relation_many', Collection([related1, related2]))
# 
#         self.assertTrue(model.push())
#         self.assertEqual(1, model.id)
#         self.assertTrue(model.exists)
#         self.assertEqual(2, len(model.relation_many))
#         self.assertEqual([2, 3], model.relation_many.lists('id'))
# 
#     def test_new_query_returns_orator_query_builder(self):
#         conn = flexmock(Connection)
#         grammar = flexmock(QueryGrammar)
#         processor = flexmock(QueryProcessor)
#         conn.should_receive('get_query_grammar').and_return(grammar)
#         conn.should_receive('get_post_processor').and_return(processor)
#         resolver = flexmock(DatabaseManager)
#         resolver.should_receive('connection').and_return(Connection(None))
#         OrmRecord.set_connection_resolver(DatabaseManager({}))
# 
#         model = OrmRecord()
#         builder = model.new_query()
#         self.assertIsInstance(builder, Builder)
# 
#     def test_get_key_returns_primary_key_value(self):
#         model = OrmRecord()
#         model.id = 1
#         self.assertEqual(1, model.get_key())
#         self.assertEqual('id', model.get_key_name())
# 
#     def test_connection_management(self):
#         resolver = flexmock(DatabaseManager)
#         resolver.should_receive('connection').once().with_args('foo').and_return('bar')
# 
#         OrmRecord.set_connection_resolver(DatabaseManager({}))
#         model = OrmRecord()
#         model.set_connection('foo')
# 
#         self.assertEqual('bar', model.get_connection())
# 
#     def test_to_dict(self):
#         model = OrmRecord()
#         model.name = 'foo'
#         model.age = None
#         model.password = 'password1'
#         model.set_hidden(['password'])
#         model.set_relation('names', Collection([OrmRecord(bar='baz'), OrmRecord(bam='boom')]))
#         model.set_relation('partner', OrmRecord(name='jane'))
#         model.set_relation('group', None)
#         model.set_relation('multi', Collection())
# 
#         d = model.to_dict()
# 
#         self.assertIsInstance(d, dict)
#         self.assertEqual('foo', d['name'])
#         self.assertEqual('baz', d['names'][0]['bar'])
#         self.assertEqual('boom', d['names'][1]['bam'])
#         self.assertEqual('jane', d['partner']['name'])
#         self.assertIsNone(d['group'])
#         self.assertEqual([], d['multi'])
#         self.assertIsNone(d['age'])
#         self.assertNotIn('password', d)
# 
#         model.set_appends(['appendable'])
#         d = model.to_dict()
#         self.assertEqual('appended', d['appendable'])
# 
#     def test_to_dict_includes_default_formatted_timestamps(self):
#         model = Model()
#         model.set_raw_attributes({
#             'created_at': '2015-03-24',
#             'updated_at': '2015-03-25'
#         })
# 
#         d = model.to_dict()
# 
#         self.assertEqual('2015-03-24T00:00:00+00:00', d['created_at'])
#         self.assertEqual('2015-03-25T00:00:00+00:00', d['updated_at'])
# 
#     def test_to_dict_includes_custom_formatted_timestamps(self):
#         class Stub(Model):
# 
#             def get_date_format(self):
#                 return 'DD-MM-YY'
# 
#         flexmock(Stub).should_receive('_boot_columns').and_return(['created_at', 'updated_at'])
# 
#         model = Stub()
#         model.set_raw_attributes({
#             'created_at': '2015-03-24',
#             'updated_at': '2015-03-25'
#         })
# 
#         d = model.to_dict()
# 
#         self.assertEqual('24-03-15', d['created_at'])
#         self.assertEqual('25-03-15', d['updated_at'])
# 
#     def test_visible_creates_dict_whitelist(self):
#         model = OrmRecord()
#         model.set_visible(['name'])
#         model.name = 'John'
#         model.age = 28
#         d = model.to_dict()
# 
#         self.assertEqual({'name': 'John'}, d)
# 
#     def test_hidden_can_also_exclude_relationships(self):
#         model = OrmRecord()
#         model.name = 'John'
#         model.set_relation('foo', ['bar'])
#         model.set_hidden(['foo', 'list_items', 'password'])
#         d = model.to_dict()
# 
#         self.assertEqual({'name': 'John'}, d)
# 
#     def test_to_dict_uses_mutators(self):
#         model = OrmRecord()
#         model.list_items = [1, 2, 3]
#         d = model.to_dict()
# 
#         self.assertEqual([1, 2, 3], d['list_items'])
# 
#         model = OrmRecord(list_items=[1, 2, 3])
#         d = model.to_dict()
# 
#         self.assertEqual([1, 2, 3], d['list_items'])
# 
#     def test_hidden_are_ignored_when_visible(self):
#         model = OrmRecord(name='john', age=28, id='foo')
#         model.set_visible(['name', 'id'])
#         model.set_hidden(['name', 'age'])
#         d = model.to_dict()
# 
#         self.assertIn('name', d)
#         self.assertIn('id', d)
#         self.assertNotIn('age', d)
# 
#     def test_fillable(self):
#         model = OrmRecord()
#         model.fillable(['name', 'age'])
#         model.fill(name='foo', age=28)
#         self.assertEqual('foo', model.name)
#         self.assertEqual(28, model.age)
# 
#     def test_fill_with_dict(self):
#         model = OrmRecord()
#         model.fill({'name': 'foo', 'age': 28})
#         self.assertEqual('foo', model.name)
#         self.assertEqual(28, model.age)
# 
#     def test_unguard_allows_anything(self):
#         model = OrmRecord()
#         model.unguard()
#         model.guard(['*'])
#         model.fill(name='foo', age=28)
#         self.assertEqual('foo', model.name)
#         self.assertEqual(28, model.age)
#         model.reguard()
# 
#     def test_underscore_properties_are_not_filled(self):
#         model = OrmRecord()
#         model.fill(_foo='bar')
#         self.assertEqual({}, model.get_attributes())
# 
#     def test_guarded(self):
#         model = OrmRecord()
#         model.guard(['name', 'age'])
#         model.fill(name='foo', age='bar', foo='bar')
#         self.assertFalse(hasattr(model, 'name'))
#         self.assertFalse(hasattr(model, 'age'))
#         self.assertEqual('bar', model.foo)
# 
#     def test_fillable_overrides_guarded(self):
#         model = OrmRecord()
#         model.guard(['name', 'age'])
#         model.fillable(['age', 'foo'])
#         model.fill(name='foo', age='bar', foo='bar')
#         self.assertFalse(hasattr(model, 'name'))
#         self.assertEqual('bar', model.age)
#         self.assertEqual('bar', model.foo)
# 
#     def test_global_guarded(self):
#         model = OrmRecord()
#         model.guard(['*'])
#         self.assertRaises(
#             MassAssignmentError,
#             model.fill,
#             name='foo', age='bar', foo='bar'
#         )
# 
#     # TODO: test relations
# 
#     def test_models_assumes_their_name(self):
#         model = OrmModelNoTableStub()
# 
#         self.assertEqual('orm_model_no_table_stubs', model.get_table())
# 
#     def test_mutator_cache_is_populated(self):
#         model = OrmRecord()
# 
#         expected_attributes = sorted([
#             'list_items',
#             'password',
#             'appendable'
#         ])
# 
#         self.assertEqual(expected_attributes, sorted(list(model._get_mutated_attributes().keys())))
# 
#     def test_fresh_method(self):
#         model = flexmock(OrmRecord())
#         model.id = 1
#         model.set_exists(True)
#         flexmock(Builder)
#         q = flexmock(QueryBuilder(None, None, None))
#         query = flexmock(Builder(q))
#         query.should_receive('where').and_return(query)
#         query.get_query().should_receive('take').and_return(query)
#         query.should_receive('get').and_return(Collection([]))
#         model.should_receive('with_').once().with_args('foo', 'bar').and_return(query)
# 
#         model.fresh(['foo', 'bar'])
# 
#         model.should_receive('with_').once().with_args().and_return(query)
# 
#         model.fresh()
# 
#     def test_clone_model_makes_a_fresh_copy(self):
#         model = OrmRecord()
#         model.id = 1
#         model.set_exists(True)
#         model.first = 'john'
#         model.last = 'doe'
#         model.created_at = model.fresh_timestamp()
#         model.updated_at = model.fresh_timestamp()
#         # TODO: relation
# 
#         clone = model.replicate()
# 
#         self.assertFalse(hasattr(clone, 'id'))
#         self.assertFalse(clone.exists)
#         self.assertEqual('john', clone.first)
#         self.assertEqual('doe', clone.last)
#         self.assertFalse(hasattr(clone, 'created_at'))
#         self.assertFalse(hasattr(clone, 'updated_at'))
#         # TODO: relation
# 
#         clone.first = 'jane'
# 
#         self.assertEqual('john', model.first)
#         self.assertEqual('jane', clone.first)
# 
#     def test_get_attribute_raise_attribute_error(self):
#         model = OrmRecord()
# 
#         try:
#             relation = model.incorrect_relation
#             self.fail('AttributeError not raised')
#         except AttributeError:
#             pass
# 
#     def test_increment(self):
#         query = flexmock()
#         model_mock = flexmock(OrmRecord, new_query=lambda: query)
#         model = OrmRecord()
#         model.set_exists(True)
#         model.id = 1
#         model.sync_original_attribute('id')
#         model.foo = 2
# 
#         model_mock.should_receive('new_query').and_return(query)
#         query.should_receive('where').and_return(query)
#         query.should_receive('increment')
# 
#         model.public_increment('foo')
# 
#         self.assertEqual(3, model.foo)
#         self.assertFalse(model.is_dirty())
# 
#     # TODO: relationship touch_owners is propagated
# 
#     # TODO: relationship touch_owners is not propagated if no relationship result
# 
#     def test_timestamps_are_not_update_with_timestamps_false_save_option(self):
#         query = flexmock(Builder)
#         query.should_receive('where').once().with_args('id', 1)
#         query.should_receive('update').once().with_args({'name': 'john'})
# 
#         model = OrmRecord()
#         model.new_query = mock.MagicMock(return_value=Builder(QueryBuilder(None, None, None)))
# 
#         model.id = 1
#         model.sync_original()
#         model.name = 'john'
#         model.set_exists(True)
#         self.assertTrue(model.save({'timestamps': False}))
#         self.assertFalse(hasattr(model, 'updated_at'))
# 
#         model.new_query.assert_called_once_with()
# 
#     def test_casts(self):
#         model = OrmModelCastingStub()
#         model.first = '3'
#         model.second = '4.0'
#         model.third = 2.5
#         model.fourth = 1
#         model.fifth = 0
#         model.sixth = {'foo': 'bar'}
#         model.seventh = ['foo', 'bar']
#         model.eighth = {'foo': 'bar'}
# 
#         self.assertIsInstance(model.first, int)
#         self.assertIsInstance(model.second, float)
#         self.assertIsInstance(model.third, basestring)
#         self.assertIsInstance(model.fourth, bool)
#         self.assertIsInstance(model.fifth, bool)
#         self.assertIsInstance(model.sixth, dict)
#         self.assertIsInstance(model.seventh, list)
#         self.assertIsInstance(model.eighth, dict)
#         self.assertTrue(model.fourth)
#         self.assertFalse(model.fifth)
#         self.assertEqual({'foo': 'bar'}, model.sixth)
#         self.assertEqual({'foo': 'bar'}, model.eighth)
#         self.assertEqual(['foo', 'bar'], model.seventh)
# 
#         d = model.to_dict()
# 
#         self.assertIsInstance(d['first'], int)
#         self.assertIsInstance(d['second'], float)
#         self.assertIsInstance(d['third'], basestring)
#         self.assertIsInstance(d['fourth'], bool)
#         self.assertIsInstance(d['fifth'], bool)
#         self.assertIsInstance(d['sixth'], dict)
#         self.assertIsInstance(d['seventh'], list)
#         self.assertIsInstance(d['eighth'], dict)
#         self.assertTrue(d['fourth'])
#         self.assertFalse(d['fifth'])
#         self.assertEqual({'foo': 'bar'}, d['sixth'])
#         self.assertEqual({'foo': 'bar'}, d['eighth'])
#         self.assertEqual(['foo', 'bar'], d['seventh'])
# 
#     def test_casts_preserve_null(self):
#         model = OrmModelCastingStub()
#         model.first = None
#         model.second = None
#         model.third = None
#         model.fourth = None
#         model.fifth = None
#         model.sixth = None
#         model.seventh = None
#         model.eighth = None
# 
#         self.assertIsNone(model.first)
#         self.assertIsNone(model.second)
#         self.assertIsNone(model.third)
#         self.assertIsNone(model.fourth)
#         self.assertIsNone(model.fifth)
#         self.assertIsNone(model.sixth)
#         self.assertIsNone(model.seventh)
#         self.assertIsNone(model.eighth)
# 
#         d = model.to_dict()
# 
#         self.assertIsNone(d['first'])
#         self.assertIsNone(d['second'])
#         self.assertIsNone(d['third'])
#         self.assertIsNone(d['fourth'])
#         self.assertIsNone(d['fifth'])
#         self.assertIsNone(d['sixth'])
#         self.assertIsNone(d['seventh'])
#         self.assertIsNone(d['eighth'])
# 
#     def test_get_foreign_key(self):
#         model = OrmRecord()
#         model.set_table('stub')
# 
#         self.assertEqual('stub_id', model.get_foreign_key())
# 
#     def test_default_values(self):
#         model = OrmModelDefaultAttributes()
# 
#         self.assertEqual('bar', model.foo)
# 
# 
# class OrmModelHydrateRawStub(Model):
# 
#     @classmethod
#     def hydrate(cls, items, connection=None):
#         return 'hydrated'
# 
# 
# class OrmModelWithStub(Model):
# 
#     def new_query(self):
#         mock = flexmock(Builder(None))
#         mock.should_receive('with_').once().with_args('foo', 'bar').and_return('foo')
# 
#         return mock
# 
# 
# class OrmModelSaveStub(Model):
# 
#     __table__ = 'save_stub'
# 
#     __guarded__ = []
# 
#     def save(self, options=None):
#         self.__saved = True
# 
#     def set_incrementing(self, value):
#         self.__incrementing__ = value
# 
#     def get_saved(self):
#         return self.__saved
# 
# 
# class OrmModelFindStub(Model):
# 
#     def new_query(self):
#         flexmock(Builder).should_receive('find').once().with_args(1, ['*']).and_return('foo')
# 
#         return Builder(None)
# 
# 
# class OrmModelFindWithWriteConnectionStub(Model):
# 
#     def new_query(self):
#         mock = flexmock(Builder)
#         mock_query = flexmock(QueryBuilder)
#         mock_query.should_receive('use_write_connection').once().and_return(flexmock)
#         mock.should_receive('find').once().with_args(1).and_return('foo')
# 
#         return Builder(QueryBuilder(None, None, None))
# 
# 
# class OrmModelFindManyStub(Model):
# 
#     def new_query(self):
#         mock = flexmock(Builder)
#         mock.should_receive('find').once().with_args([1, 2], ['*']).and_return('foo')
# 
#         return Builder(QueryBuilder(None, None, None))
# 
# 
# class OrmModelDestroyStub(Model):
# 
#     def new_query(self):
#         mock = flexmock(Builder)
#         model = flexmock()
#         mock_query = flexmock(QueryBuilder)
#         mock_query.should_receive('where_in').once().with_args('id', [1, 2, 3]).and_return(flexmock)
#         mock.should_receive('get').once().and_return([model])
#         model.should_receive('delete').once()
# 
#         return Builder(QueryBuilder(None, None, None))
# 
# 
# class OrmModelNoTableStub(Model):
# 
#     pass
# 
# 
# class OrmModelCastingStub(Model):
# 
#     __casts__ = {
#         'first': 'int',
#         'second': 'float',
#         'third': 'str',
#         'fourth': 'bool',
#         'fifth': 'boolean',
#         'sixth': 'dict',
#         'seventh': 'list',
#         'eighth': 'json'
#     }
# 
# class OrmModelCreatedAt(Model):
# 
#     __timestamps__ = ['created_at']
# 
# 
# class OrmModelUpdatedAt(Model):
# 
#     __timestamps__ = ['updated_at']
# 
# 
# class OrmModelDefaultAttributes(Model):
# 
#     __attributes__ = {
#         'foo': 'bar'
#     }
#

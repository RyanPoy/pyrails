#coding: utf8
from __future__ import with_statement
from sweet.criteria import Criteria
from sweet.relation import Relation
from sweet.utils import *


class ActiveRecordMetaClass(type):
    
    def __init__(cls, name, bases, attr):
        model_instance = type.__init__(cls, name, bases, attr)
        if name != 'ActiveRecord':
            # set __table_name__ to Record Class
            if not hasattr(cls, '__table_name__'):
                setattr(cls, '__table_name__', tableize(cls.__name__))

            for relation in Relation.iter():
                relation.inject(cls)

            # id column must in columns validate
            if cls.__pk__ not in cls.__columns__:
                raise PKColumnNotInColumns()
            for c, err in [
                (cls.__pk__, PKColumnNotInColumns),
                (cls.__created_at__, CreatedAtColumnNotInColumns), 
                (cls.__updated_at__, UpdatedAtColumnNotInColumns),
                (cls.__created_on__, CreatedOnColumnNotInColumns),
                (cls.__updated_on__, UpdatedOnColumnNotInColumns),
            ]:
                if c and  c not in cls.__columns__:
                    raise err()

        return model_instance
    
    def __getattribute__(self, name):
        try:
            return type.__getattribute__(self, name)
        except AttributeError, _:
            if MethodMissing.match(name):
                return MethodMissing(self, name)
            raise


class ActiveRecord(object):
    """
    A ORM. You can use it like this:
    - Query with chain 
        - where:
          User.where(name='pengyi').where('age != ?', 28).where('birthday between ? and ?', '1982-01-01', '1986-01-01')
         # => SELECT FROM users WHERE name = 'pengyi' AND age != 28 AND birthday between '1982-01-01' and '1986-01-01'
        
        - limit 
          User.where(name='pengyi').limit(10, 1) 
         # => SELECT FROM users WHERE name = 'pengyi' LIMIT 10 OFFSET 1
         
        - group/order/having ....
          User.where(name='pengyi').order('name DESC').group('name').having(age = 10)
         # => SELECT users.* FROM users WHERE `users`.`name` = 'pengyi' GROUP BY `users`.`name` HAVING `users`.`age` = 10 ORDER BY name DESC LIMIT 10 OFFSET 1
    
    - Query with method missing
      User.find_by_name('pengyi')
     # => SELECT FROM users WHERE name = 'pengyi'

      User.find_by_name_and_age('pengyi', 28)
     # => SELECT FROM users WHERE name = 'pengyi' AND age = 28
     
    - Create a record in database
      User.create(name = 'pengyi', age = 28)
     # => INSERT INTO users (name, age) VALUES ('pengyi', 28)
      
      User(name = 'pengyi', age = 28).save()
     # => INSERT INTO users (name, age) VALUES ('pengyi', 28)
     
    - Update
      u = User.find(1)  # 1 meams id
      u.update_attributes(name = 'poy', age = 30)
     # => UPDATE users SET name = 'poy', age = 30 WHERE id = 1
    
      User.where(age=20).update_all(name='poy', age='40)
     # => UPDATE users SET name = 'poy', age = 40 WHERE age = 20

    - Delete
      u = User.find(1)
      u.delete()
     # => DELETE FROM users WHERE id = 1
     
      u = User.where(age=20).delete_all()
     # => DELETE FROM users WHERE age = 20
    """
    __db__ = None
    __metaclass__ = ActiveRecordMetaClass
    __columns__ = set([])
    __pk__ = 'id'
    __created_at__ = 'created_at'
    __updated_at__ = 'updated_at'
    __created_on__ = None
    __updated_on__ = None
    __relations__  = []

    def __init__(self, dict_args={}, **kwargs):
        self.__dict__.update(dict_args)
        self.__dict__.update(kwargs)
        self.__is_persisted = False
        self.__origin_attrs = {}

    def _get_origin(self, attr):
        return self.__origin_attrs.get(attr)
    
    def is_dirty(self, *attrs):
        dirty_attrs = {}
        for k, v in self.__origin_attrs.iteritems():
            dirty_v = getattr(self, k, v) 
            if dirty_v != v:
                dirty_attrs[k] = (dirty_v, v)
        if not dirty_attrs:
            return False
        for a in attrs:
            if a not in dirty_attrs:
                return False
        return True

    @property
    def is_persisted(self):
        return self.__is_persisted
    
    def _sync_attrs(self):
        for col in self.__columns__:
            self.__origin_attrs[col] = getattr(self, col, None)
        return self
    
    def __getattr__(self, name):
        try:
            return super(ActiveRecord, self).__getattribute__(name)
        except AttributeError, _:
            if name in self.__columns__:
                return None
            raise

    @classproperty
    def table_name(cls):
        return cls.__table_name__

    def persist_attrs(self, contains_id=False):
        relt = dict([ (c, getattr(self, c, None)) for c in self.__columns__ ])
        if not contains_id:
            relt.pop(self.__pk__)
        return relt

    @classmethod
    def all(cls):
        """ find all records
        @return a record array
        eg.
            User.all
            User.where(age=10).all
        """
        return cls._new_criteria().all()
     
    @classmethod
    def first(cls):
        """ find the first record
        @return a record
        eg.
            User.first
            User.where(age=10).first
        """
        return cls._new_criteria().first()

    @classmethod
    def last(cls):
        """ find the last record
        @return a record
        eg.
            User.last
            User.where(age=10).last
        """
        return cls._new_criteria().last()
 
    @classmethod
    def count(cls, column='*'):
        return cls._new_criteria().count(column) 
    
    @classmethod
    def sum(cls, column):
        return cls._new_criteria().sum(column)
    
    @classmethod
    def max(cls, column):
        return cls._new_criteria().max(column)
    
    @classmethod
    def min(cls, column):
        return cls._new_criteria().min(column)
    
    @classmethod
    def avg(cls, column):
        return cls._new_criteria().avg(column)
    
    @classmethod  
    def distinct(cls):
        return cls._new_criteria().distinct()
    
    @classmethod
    def where(cls, *args, **kwargs):
        """ condition query
        eg.
            User.where(username="abc").where(password="123")
            User.where("username='abc' and password='123'")
            User.where("username=? and password=?", 'abc', '123')
        """
        return cls._new_criteria().where(*args, **kwargs)
    
    @classmethod
    def find(cls, *ids):
        """ find record by ids
        @return:    if there is a id and found it will return a record
                    if there are many ids and found them will return a record array
                    if any id not found, throw RecordNotFound exception
        """
        c = cls._new_criteria().where(id=ids)
        if len(ids) == 1:
            relt = c.first()
            if relt is None:
                raise RecordNotFound()
        else:
            relt = c.all()
        return relt
 
    @classmethod
    def limit(cls, limit):
        """ limit query
        eg. 
            User.limit(10)
            User.limit(10, 1)
        """
        return cls._new_criteria().limit(limit)
    
    @classmethod
    def offset(cls, offset):
        """ limit query
        eg. 
            User.limit(10)
            User.limit(10, 1)
        """
        return cls._new_criteria().offset(offset)
    
    @classmethod
    def page(cls, page_num, limit):
        return cls._new_criteria().page(page_num, limit)
    
    @classmethod
    def group_by(cls, *args):
        """ group query
        eg. 
            User.group_by('username')
        """
        return cls._new_criteria().group_by(*args)
    
    @classmethod
    def order_by(cls, *args):
        """ order query
        eg.
            User.order_by('age')
            User.order_by('age ASC')
            User.order_by('age DESC')
        """
        return cls._new_criteria().order_by(*args)
    
    @classmethod
    def having(cls, *args, **kwargs):
        """ having query when group
        Note: if there is not use group, the having will be not useful
        eg.
            User.group('username').having(age=1)
        """
        return cls._new_criteria().having(*args, **kwargs)
    
    @classmethod
    def select(cls, *select_columns):
        return cls._new_criteria().select(*select_columns)
    
    @classmethod
    def join(cls, tablename, *args):
        return cls._new_criteria().join(tablename, *args)
    
    @classmethod
    def left_join(cls, tablename, *args):
        return cls._new_criteria().left_join(tablename, *args)
    
    @classmethod
    def right_join(cls, tablename, *args):
        return cls._new_criteria().right_join(tablename, *args)

    def valid(self):
        return True

    def _get_attr(self, attrname, default=None):
        return getattr(self, attrname, default)

    @classmethod
    def create(cls, attr_dict={}, **attributes):
        """ persist a active record. 
        @return：record instance if successful, else return None. 
                it will throw exception when any exception occur
        eg. 
            User.create(username='abc', password='123')
        """
        record = cls(attr_dict, **attributes)
        return record if record.save() else None
    
    def  _prepare_at_or_on(self, attrs_dict):
        def _build_at_or_on(at_or_on_attrname, attrs_dict, is_at=True):
            str_2_datetime_or_date = str2datetime if is_at else str2date
            cur_datetime_or_date = datetime.now if is_at else datetime.today
            if at_or_on_attrname:
                value = attrs_dict.get(at_or_on_attrname, None) or self._get_attr(at_or_on_attrname)
                value = str_2_datetime_or_date(value)
                if value is None:
                    value = cur_datetime_or_date() 
                setattr(self, at_or_on_attrname, value)
                attrs_dict[at_or_on_attrname] = self._get_attr(at_or_on_attrname)
        for at in (self.__created_at__, self.__updated_at__):
            _build_at_or_on(at, attrs_dict)
        for on in (self.__created_on__, self.__updated_on__):
            _build_at_or_on(on, attrs_dict, False)
        return self

    def save(self):
        """ persist a record instance.
        @return：record instace if successful, else return None. 
                it will throw exception when any exception occur
        eg.
            u = User(username="abc", password="123456").save()
        """
        criteria = self._new_criteria()
        if self.is_persisted: # update
            attrs = self.persist_attrs()
            self._prepare_at_or_on(attrs)
            criteria.where(**{self.__pk__:self.pk}).update(**attrs)
        else: # insert
            attrs = self.persist_attrs()
            self._prepare_at_or_on(attrs)
            setattr(self, self.__pk__, criteria.insert(**attrs))
            self.__is_persisted = True
        self._sync_attrs()
        return self

    @classmethod
    def _new_criteria(cls):
        return Criteria().from_(cls.table_name)

#     def relate(self, *models):
#         Collection(self.__class__).save(self)
#         return self

    def update_attributes(self, **attributes):
        """ update attributes
        eg. 
            u = User(username="abc", password="123").save().update_attributes(username="efg", password="456")
        return: self if update successful else False
        """
        if not self.is_persisted:
            raise RecordHasNotBeenPersisted()
        self._prepare_at_or_on(attributes)
        criteria = self._new_criteria().where(**{self.__pk__:self.pk})
        criteria.update(attributes)

        for name, value in attributes.iteritems():
            setattr(self, name, value)
        return self

    @classmethod
    def update_all(cls, **attributes):
        cls._new_criteria().update(**attributes)
        return True

    @property
    def pk(self):
        return getattr(self, self.__pk__)

    def delete(self):
        """delete a record instance.
        eg.
            u = User.find(1)
            u.delete()
        """
        if not self.is_persisted:
            raise RecordHasNotBeenPersisted()
        
        for r in self.__relations__:
            r._delete(self)

        # @TODO: 需要按照关系再次删除相关的数据
        c = self._new_criteria()
        return c.where(**{self.__pk__:self.pk}).delete()

    @classmethod
    def delete_all(cls):
        """ delete all records
        eg.
            User.delete_all()
            User.find(1, 2, 3).delete_all()
        """
        c = cls._new_criteria()
        return c.delete()

#     @classmethod
#     def _get_db(cls):
#         if cls.__db__ is None:
#             cls.__db__ = pyrails.get_database()
#         return cls.__db__
#     
#     @classproperty
#     @contextmanager
#     def transaction(cls):
#         try:
#             database = cls._get_db()
#             database.set_autocommit(False)
#             yield None
#             database.commit()
#         except ValidationError:
#             database.rollback()
#         except:
#             database.rollback()
#             raise
#         finally:
#             try:
#                 database.set_autocommit(True)
#             except:
#                 pass
# 
#     def add_error(self, attr_name, msg):
#         self.errors.setdefault(attr_name, []).append(msg)
#         return self
# 
#     def validate(self, on='save'):
#         return all([ valid(record=self) for valid in self.__class__.validate_func_dict.get(on, {}) ])
#
    
    @classproperty
    def columns(cls):
        return cls.__columns__

    @classmethod
    def has_column(cls, column_name):
        return column_name in cls.__columns__

    def to_dict(self, contain_relations=False):
        d = dict([ (c, getattr(self, c)) for c in self.__columns__ ])
        self._prepare_at_or_on(d)
        if contain_relations:
            pass
        return d


####### method missing ########
class MethodMissing(object):

    FIND_BY_P = re.compile('^find_(all_by|by)_([_a-zA-Z]\w*)$')
    FIND_OR_BY_P = re.compile('^find_or_(init|create)_by_([_a-zA-Z]\w*)$')

    def __init__(self, instance, method_name):
        self.name = method_name
        self.record = instance

    @classmethod
    def match(cls, name):
        return cls.FIND_BY_P.match(name) or cls.FIND_OR_BY_P.match(name)

    def __call__(self, *args):
        def extract_scope_or_method_and_arguments(match, args):
            groups = match.groups()
            scope = groups[0]
            args_name = groups[1].split('_and_')
            return scope, dict(zip(args_name, args))

        r = None
        match = self.FIND_BY_P.match(self.name)
        if match:
            scope, argments = extract_scope_or_method_and_arguments(match, args)
            if scope == 'all_by':
                r = self.record.where(**argments).all()
            else: # must 'by'
                r = self.record.where(**argments).first()
        else:
            match = self.FIND_OR_BY_P.match(self.name)
            if match:
                scope, argments = extract_scope_or_method_and_arguments(match, args)
                r = self.record.where(**argments).first()
                if r is None:
                    if scope == 'create':
                        r = self.record.create(**argments)
                    else: # must 'init'
                        r = self.record(**argments)
        return r

# class CreateOrBuildMethodMissing(object):
# 
#     __pattern = re.compile('^(create|build)_([_a-zA-Z]\w*)$')
# 
#     def __init__(self, instance, method_name):
#         self.name = method_name
#         self.record = instance
# 
#     @classmethod
#     def match(cls, name):
#         return cls.__pattern.match(name)
#             
#     def __call__(self, *args, **kwargs):
#         r = None
#         match = self.__class__.__pattern.match(self.name)
#         if match:
#             scope, association_propert_name = match.groups()
#             association = self.record.association_of(association_propert_name) # belongs_to or has_one
#             if not association: #or association.is_belongs_to():
#                 raise AttributeError("'%s' object has no attribute '%s'" % (self.record.__class__.__name__, self.name))
#             foreign_key = association.foreign_key
#             if foreign_key not in kwargs:
#                 kwargs[foreign_key] = self.record.id
#             if scope == 'create':
#                 r = association.target.create(*args, **kwargs)
#             else: # must 'build'
#                 r = association.target(*args, **kwargs)
#             setattr(self.record, association_propert_name, r)
#         return r
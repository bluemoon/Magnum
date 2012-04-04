from .field import Field

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        metaclass = attrs.get('__metaclass__')
        super_new = super(ModelMetaclass, cls).__new__
        if metaclass and issubclass(metaclass, ModelMetaclass):
            return super_new(cls, name, bases, attrs)
            
        doc_fields = {}
        class_name = [name]
        superclasses = {}
        simple_class = True
        for base in bases:
            if hasattr(base, '_fields'):
                doc_fields.update(base._fields)
                superclasses[base._class_name] = base
                superclasses.update(base._superclasses)
            else:
                attrs.update(dict([(k,v) for k,v in base.__dict__.items()
                                    if issubclass(v.__class__, Field)]))
                                                
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and \
               issubclass(attr_value.__class__, Field):
                attr_value.name = attr_name
                doc_fields[attr_name] = attr_value
        attrs['_fields'] = doc_fields
        new_class = super_new(cls, name, bases, attrs)
        for field in new_class._fields.values():
            field.owner_document = new_class
            print field.name
            
        if not hasattr(new_class, '_unbound_fields'):
            new_class._unbound_fields = new_class._fields
        
        return new_class

class Model(object):
    __metaclass__ = ModelMetaclass
    """docstring for Document"""
    def __init__(self, **values):
        self._data = {}
        self._initialised = False
        # Assign default values to instance
        for attr_name, field in self._fields.items():
            value = getattr(self, attr_name, None)
            setattr(self, attr_name, value)
        # Assign initial values to instance
        for attr_name in values.keys():
            try:
                value = values.pop(attr_name)
                setattr(self, attr_name, value)
            except AttributeError:
                pass
        
    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, name):
        try:
            if name in self._fields:
                return getattr(self, name)
        except AttributeError:
            pass
        raise KeyError(name)

    def __setitem__(self, name, value):
        # Ensure that the field exists before settings its value
        if name not in self._fields:
            raise KeyError(name)
        return setattr(self, name, value)

    def __contains__(self, name):
        try:
            val = getattr(self, name)
            return val is not None
        except AttributeError:
            return False

    def __len__(self):
        return len(self._data)
        
    def __html__(self):
        """docstring for form"""
        for field_name, field in self._fields.items():
            yield field.html()
    
    def fields(self):
        for field_name, field in self._fields.items():
            print getattr(self, field_name)
            yield idx, field
            
    def to_db(self):
        data = {}
        for field_name, field in self._fields.items():
            value = getattr(self, field_name, None)
            if value is not None:
                data[field.name] = field.to_db(value)
        # Only add _cls and _types if allow_inheritance is not False
        if not (hasattr(self, '_meta') and
                self._meta.get('allow_inheritance', True) == False):
            #data['_cls'] = self._class_name
            #data['_types'] = self._superclasses.keys() + [self._class_name]
            pass
        if '_id' in data and data['_id'] is None:
            del data['_id']
        return data

class Field(object):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance._data.get(self.name)
        if value is None:
            value = self.default
            # Allow callable default values
            if callable(value):
                value = value()
                
        return value
        
    def __set__(self, instance, value):
        self.data = value
        instance._data[self.name] = value
        
    def html(self, **kwargs):
        return self.widget(self, **kwargs)
        
    def prepare_value(self):
        """docstring for prepare_value"""
        pass
        
    def to_python(self):
        """docstring for to_python"""
        pass
        
    def to_db(self, value):
        """docstring for to_db"""
        pass
        
    def validate(self):
        """docstring for validate"""
        pass
        
    def db_type(self):
        """docstring for db_type"""
        pass
    
    def get_choices(self):
        """docstring for get_choices"""
        pass

    def formfield(self, **kwargs):
        """docstring for formfield"""
        #return form_class(**defaults)
        pass
        
    def _value(self):
        return self.to_python(self.data)

class StringField(Field):
    pass
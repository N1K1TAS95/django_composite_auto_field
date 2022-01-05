import warnings

from django.db import models
from django.db.models import Max
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class CompositeAutoField(models.CharField):
    warning = ("You passed an argument to CodeField that will be "
               "ignored. Avoid args and following kwargs: max_length, unique, editable, null.")
    description = _('custom auto incrementing field')
    defaults = dict(max_length=255, unique=True, editable=False, null=True)

    def __init__(self, *args, db_collation=None, prefix='CC', use_year=False, zeros=4, **kwargs):
        self.prefix = prefix
        self.use_year = use_year
        self.zeros = zeros
        self._warn_for_shadowing_args(*args, **kwargs)
        kwargs['max_length'] = 255
        kwargs['unique'] = True
        kwargs['editable'] = False
        kwargs['null'] = True
        kwargs.update(self.defaults)
        super().__init__(*args, db_collation=db_collation, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CompositeAutoField, self).deconstruct()
        if self.prefix != 'CC':
            kwargs['prefix'] = self.prefix
        kwargs['use_year'] = self.use_year
        if self.zeros != 4:
            kwargs['zeros'] = self.zeros
        del kwargs['max_length']
        del kwargs['unique']
        del kwargs['editable']
        del kwargs['null']
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if self.prefix and self.zeros and add:
            max_res = self.model.objects.aggregate(**{self.name + '_max': Max(self.name)})[self.name + '_max']
            next_num = 1
            cur_year = str(now().year)[2:]
            if max_res:
                if self.use_year:
                    last_year = int(max_res[len(self.prefix):4])
                    if last_year == int(cur_year):
                        next_num = int(max_res[len(self.prefix) + 2:]) + 1
                else:
                    next_num = int(max_res[len(self.prefix):]) + 1
            next_num = str(next_num).zfill(self.zeros)
            value = f'{self.prefix}{cur_year if self.use_year else str()}{next_num}'
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def _warn_for_shadowing_args(self, *args, **kwargs):
        if args:
            warnings.warn(self.warning)
        else:
            for key in set(kwargs).intersection(set(self.defaults.keys())):
                if not kwargs[key] == self.defaults[key]:
                    warnings.warn(self.warning)
                    break

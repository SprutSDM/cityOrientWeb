from django.conf import settings
from django.core import checks
from django.core.files.storage import get_storage_class
from django.db.models.fields.files import ImageFieldFile, ImageField


class DefaultStaticImageFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.name or self.name == self.field.default_image_path:
            self.name = self.field.default_image_path
            self.storage = get_storage_class(settings.STATICFILES_STORAGE)()


class DefaultStaticImageField(ImageField):
    attr_class = DefaultStaticImageFieldFile

    def __init__(self, default_image_path=None, *args, **kwargs):
        self.default_image_path = default_image_path
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_default_image_path_attribute(**kwargs),
        ]

    def _check_default_image_path_attribute(self, **kwargs):
        if self.max_length is None:
            return [
                checks.Error(
                    "DefaultStaticImageField must define a 'default_image_path' attribute.",
                    obj=self,
                )
            ]
        return []

from django.db.models import Model
from django.shortcuts import _get_queryset


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def create_breadcrumbs(
    obj: Model, root_path: str = "/catalog", disable_last: bool = True
) -> list[dict]:
    last_item = {
        "level": obj.depth,
        "name": obj.name,
        "href": f"{root_path}/{obj.slug}",
        "disabled": disable_last,
    }
    if obj.is_root():
        return [last_item]

    breadcrumbs = []
    for anccestor in obj.get_ancestors():
        item = {
            "level": anccestor.depth,
            "name": anccestor.name,
            "href": f"{root_path}/{anccestor.slug}",
            "disabled": False,
        }
        breadcrumbs.append(item)
    breadcrumbs.append(last_item)

    return breadcrumbs

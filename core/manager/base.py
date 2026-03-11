def _soft_delete(instance):
    """Mark an instance as deleted (soft delete)."""
    instance.is_deleted = True
    instance.save()
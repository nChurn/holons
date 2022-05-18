def duplicate_object(self):
    """
    this is taken from https://stackoverflow.com/questions/437166/duplicating-model-instances-and-their-related-objects-in-django-algorithm-for
    Duplicate a model instance, making copies of all foreign keys pointing to it.
    There are 3 steps that need to occur in order:

        1.  Enumerate the related child objects and m2m relations, saving in lists/dicts
        2.  Copy the parent object per django docs (doesn't copy relations)
        3a. Copy the child objects, relating to the copied parent object
        3b. Re-create the m2m relations on the copied parent object

    """
    related_objects_to_copy = []
    relations_to_set = {}
    # Iterate through all the fields in the parent object looking for related fields
    for field in self._meta.get_fields():
        if field.one_to_many:
            # One to many fields are backward relationships where many child 
            # objects are related to the parent. Enumerate them and save a list 
            # so we can copy them after duplicating our parent object.
            # print(f'Found a one-to-many field: {field.name}')

            # 'field' is a ManyToOneRel which is not iterable, we need to get
            # the object attribute itself.
            related_object_manager = getattr(self, field.name)
            related_objects = list(related_object_manager.all())
            if related_objects:
                # print(f' - {len(related_objects)} related objects to copy')
                related_objects_to_copy += related_objects

        elif field.many_to_one:
            # In testing, these relationships are preserved when the parent
            # object is copied, so they don't need to be copied separately.
            # print(f'Found a many-to-one field: {field.name}')
            pass

        elif field.many_to_many:
            # Many to many fields are relationships where many parent objects
            # can be related to many child objects. Because of this the child
            # objects don't need to be copied when we copy the parent, we just
            # need to re-create the relationship to them on the copied parent.
            # print(f'Found a many-to-many field: {field.name}')
            related_object_manager = getattr(self, field.name)
            relations = list(related_object_manager.all())
            if relations:
                # print(f' - {len(relations)} relations to set')
                relations_to_set[field.name] = relations

    # Duplicate the parent object
    self.pk = None
    self.save()
    # print(f'Copied parent object ({str(self)})')

    # Copy the one-to-many child objects and relate them to the copied parent
    for related_object in related_objects_to_copy:
        # Iterate through the fields in the related object to find the one that 
        # relates to the parent model.
        for related_object_field in related_object._meta.fields:
            if related_object_field.related_model == self.__class__:
                # If the related_model on this field matches the parent
                # object's class, perform the copy of the child object and set
                # this field to the parent object, creating the new
                # child -> parent relationship.
                related_object.pk = None
                setattr(related_object, related_object_field.name, self)
                related_object.save()

                text = str(related_object)
                text = (text[:40] + '..') if len(text) > 40 else text
                # print(f'|- Copied child object ({text})')

    '''
    # Right now we do not need M2M relations here
    # Set the many-to-many relations on the copied parent
    for field_name, relations in relations_to_set.items():
        # Get the field by name and set the relations, creating the new
        # relationships.
        field = getattr(self, field_name)
        field.set(relations)
        text_relations = []
        for relation in relations:
            text_relations.append(str(relation))
        print(f'|- Set {len(relations)} many-to-many relations on {field_name} {text_relations}')
    '''

    return self

class IdTable:
    def add_entity(self, entity_name):
        self.entity_counters[entity_name] = 0
        self.entity_objects[entity_name] = {}

    def add_object(self, entity_name, object_name):
        self.entity_counters[entity_name] += 1
        new_id = self.entity_counters[entity_name]
        self.entity_objects[entity_name][object_name] = new_id

    def get_id(self, entity_name, object_name):
        return self.entity_objects \
            .get(entity_name) \
            .get(object_name)

ID_TABLE = IdTable()
ID_TABLE.add_entity("genre")
ID_TABLE.add_entity("movie")
ID_TABLE.add_entity("composer")
ID_TABLE.add_entity("actor")
ID_TABLE.add_entity("director")

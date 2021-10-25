This project requires at least python3.8. (maybe?)

# TODOs

- [ ] Maybe some `as_list` parameter for `XML_Config`
- [ ] Docstrings + type annotations + marking methods as private
- [x] Type casting
- [x] Type casting for complex types
- [ ] Add a license
- [ ] Some functionality needs to be moved to a generic mixin (like data casting)
- [ ] Reorder methods
- [ ] Implement some sort of validation of the `Config` objects
- [ ] For now, only "basic" Python types are supported. Would working with full annotations be useful?
- [ ] Is type casting properly tested everywhere?
- [ ] What's the best way of handling types with JSON (standard ones, non-standard ones, "1" crap responses etc.)
- [ ] Handle nested dataclasses?
- [ ] DRY some of the methods (e.g. data casting from the mixins)

# Thoughts on architecture

- Some functionality can be mutualized between the JSON and XML mixins, mainly data casting.
- There is always a process of checking if a field is "configured" or not
- The XML processign and JSON processing are very different (it is hard to name the JSON processing, and I am not sure if processing in the XML just using the standard lib it the best way to go)

Basic data flow of the `from_*` functions:

- Check if the field was configured or not (configuration only relates to finding the object, **not** casting)
- Find the field if necessary and extract it as a text value (XML) or its actual value (JSON)
- Cast the text value using the casting functions
- Return the value and cast the dataclass

This project requires at least python3.8. (maybe?)

# TODOs

- [x] Type casting
- [x] Type casting for complex types
- [x] Some functionality needs to be moved to a generic mixin (like data casting)
- [x] Docstrings + type annotations + marking methods as private
- [x] Add a license
- [x] For now, only "basic" Python types are supported. Would working with full annotations be useful?
- [x] Warnings for no match found
- [x] Add a flag to pass in deserialized data directly
- [x] Rename `fieldwrapper` to something shorter/better
- [x] Rename/regroup the modules
- [x] Move test file paths to constants
- [ ] Reorder methods
- [ ] Implement some sort of validation of the `Config` objects
- [ ] Would using abc make for the mixins make sense?
- [ ] Is type casting properly tested everywhere?
- [ ] Handle nested dataclasses?
- [ ] Add a method for getting only the attributes needed for instatiating a dataclass
- [ ] Add options to skip fields (to the method above?)
- [ ] The `hasattr(cls, "config")` in mixins check can probably be DRYed
- [ ] Test exceptions like `TooManyErrors`
- [ ] Be careful with the whole lxml xpath support like using `text()` (breaks things)
- [ ] Update licenses to properly includes licenses of dependencies
- [ ] Make the classes available as decorators
- [ ] Expand documentation
- [ ] Package properly to be able to make a Python package out of it

# Thoughts on architecture

Basic data flow of the `from_*` functions:

- Check if the field was configured or not (configuration only relates to finding the object, **not** casting)
- Find the field if necessary and extract it as a text value (XML) or its actual value (JSON)
- Cast the text value using the casting functions
- Return the value and cast the dataclass

This project requires at least python3.8. (maybe?)

# TODOs

- [ ] Docstrings + type annotations + marking methods as private
- [x] Type casting
- [x] Type casting for complex types
- [ ] Add a license
- [x] Some functionality needs to be moved to a generic mixin (like data casting)
- [ ] Reorder methods
- [ ] Implement some sort of validation of the `Config` objects
- [ ] For now, only "basic" Python types are supported. Would working with full annotations be useful?
- [ ] Is type casting properly tested everywhere?
- [ ] What's the best way of handling types with JSON (standard ones, non-standard ones, "1" crap responses etc.)
- [ ] Handle nested dataclasses?
- [ ] Add a method for getting only the attributes needed for instatiating a dataclass
- [ ] Add options to skip fields (to the method above?)
- [ ] Maybe move (most) `classmethod` to being `staticmethod`
- [ ] The `hasattr(cls, "config")` in mixins check can probably be DRYed
- [ ] Test exceptions like `TooManyErrors`
- [ ] Be careful with the whole lxml xpath support like using `text()` (breaks things)
- [ ] Warnings for no match found
- [ ] Add a flag to pass in deserialized data directly

# Thoughts on architecture

Basic data flow of the `from_*` functions:

- Check if the field was configured or not (configuration only relates to finding the object, **not** casting)
- Find the field if necessary and extract it as a text value (XML) or its actual value (JSON)
- Cast the text value using the casting functions
- Return the value and cast the dataclass

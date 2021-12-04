# Dataclaster

Dataclaster (contraction of **dataclass** and **casting**) helps you, well, cast data into dataclasses. It adds methods like `from_json` or `from_xml` to your dataclasses so that you can do things like `person = Person.from_json(json_dict)`.

## Motivation

When writing data/ETL pipelines, you can easily lose track of which entities/fields your are manipulating. A fairly new (python3.7+) but very effective way of solving this problem is to use dataclasses.

You can cast your raw data into dataclasses; not only does this make it easier to manipulate the data, the dataclasses themselves will serve as a single-source-of-truth for entities you're working with in your pipelines.

```python
# entities.py
@dataclass
class Person:
    first_name: str
    # ...


# pipeline01.py
import pandas as pd
from entities import Person

persons = [
    {
        "first_name": "Pierre",
        # ...
    },
    # ...
]

persons = [Person(**person_dict) for person_dict in persons]
df = pd.DataFrame(persons)
# ...
```

This makes the code much more readable and self-documenting. But how about the instantiation of the `Person` dataclass from the `persons` list?

While this works well for structured/simple data, things can get very messy when dealing with complex and/or nested data. Not only will you have to write and maintain functions to pick the right field in the response for you, you'll also need to make sure to cast fields that e.g. use `yes/no` instead of proper booleans; let alone handling things like extracting XML attributes.

Let's say you're making an API call that returns following JSON response:

```json
{
  "category": "pastry",
  "name": "Donut",
  "rating": {
    "average": 4.5,
    "count": 1345
  }
}
```

If you want to cast this into a dataclass, you'd have to write something along the lines of:

```python
@dataclass
class Pastry:
    category: str
    name: str
    average_rating: float

def cast_pastry_dataclass(json_response):
    json_dict = json.loads(json_response)
    attribs = { k: json_dict[k] for k in ["category", "name"] }
    attribs["average_rating"] = float(json_dict["rating"]["average"])
    return Pastry(**attribs)

pastry = cast_pastry_dataclass(json_string)
```

Doing this not only is repetitive and time-consuming, it will bloat your entity files with function code and decorrelate the fields from their origin. While decoupling is usually a good practice in Software Engineering, we believe that for the extraction part of a data pipeline there is clear benefit in having a given dataclass tied to a specific source.

Dataclaster aims to solve this problem by allowing you to store both things - the fields you will manipulate and where to get them - in the same place: the dataclass itself.

## Simple usage

The example above can be easily rewritten using dataclaster.

```python
from dataclaster.json_mixin import JSONMixin, JSONConfig
from dataclaster.common import field as dcfield

@dataclass
class Pastry(JSONMixin):
    category: str
    name: str
    average_rating: float = dcfield(config=JSONConfig(path="rating.average"))

pastry = Pastry.from_json(json_string)

```

For fields without a configuration, dataclaster assumes that those live at the top level. The `JSONConfig` `path` attribute is a simple [jsonpath_rw](https://github.com/kennknowles/python-jsonpath-rw) path.

## Roadmap

Dataclaster hasn't even reached the alpha stage.

The approach of using dataclasses as a single-source-of-truth for entities in ETL pipelines has been applied in production projects in which we wrote utility classes/code to be able to consistently parse messy responses.

The dataclaster project is an attempt to consolidate this utility code into a proper Python package.

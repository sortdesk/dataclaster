# Dataclaster

Dataclaster (contraction of **dataclass** and **casting**) helps you, well, cast data into dataclasses. It adds methods like `from_json` or `from_xml` to your dataclasses so that you can do things like `person = Person.from_json(json_dict)`.

## Motivation

When writing data/ETL pipelines, you can easily lose track of which entities/fields your are manipulating. A fairly new (python3.7+) but very effective way of solving this problem is to use dataclasses.

Describing the entities and their fields is now as simple as writing dataclasses in a separate `entities.py` (or similar) file. This does not only make the codebase much more readable for developers, it also acts as an intermediate step between the extraction and further transformation of data within your data/ETL pipelines. Instances of dataclasses can be easily manipulated, sorted, and e.g. used to instantiate a pandas `DataFrame`.

But how do you instantiate dataclasses from raw data?

While this is usually very easy when extracting structured data from a database or when dealing with a flat JSON dictionary, things get a little harder when you're dealing with API responses in XML/JSON that have complex and/or nested structures. You would have to write functions that parses the specific data response and picks the right field corresponding to your dataclass entity. Writing and maintaining these functions is time-consuming, bloats your code, and breaks the principle of having simple, readable dataclasses that define what entities/fields your are manipulating and where they come from. In addition, you'll also have to handle casting the data type, e.g. when the API returns `yes/no` instead of a proper boolean or when manipulatin XMl.

Dataclaster aims to solve this problem by allowing you to store both things - the fields you will manipulate and where to get them - in the same place: the dataclass itself.

## Simple usage

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

We'll name this JSON string `json_string` in the following snippets.

Before further manipulating it in your data pipelines, you want to cast it into a dataclass.

Instead of doing:

```python
@dataclass
class Pastry:
    category: str
    name: str
    average_rating: float

def cast_pastry_dataclass(json_response):
    json_dict = json.loads(json_response)
    attribs = { k: json_dict[k] for k in ["category", "name"] }
    attribs["average_rating"] = json_dict["rating"]["average"]
    return Pastry(**attribs)

pastry = cast_pastry_dataclass(json_string)
```

with dataclaster you can simply write:

```python
from dataclaster.json_mixin import JSONMixin, JSONConfig
from dataclaster.common import fieldwrapper

class Pastry(JSONMixin):
    category: str
    name: str
    average_rating: float = fieldwrapper(config=JSONConfig(path="rating.average"))

pastry = Pastry.from_json(json_string)

```

For fields without a configuration, dataclaster assumes that those live at the top level. The `JSONConfig` `path` attribute is a simple [jsonpath_rw](https://github.com/kennknowles/python-jsonpath-rw) path.

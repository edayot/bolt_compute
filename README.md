# Bolt Compute

A [beet](https://github.com/mcbeet/beet) plugin that allows to use expressions instead of inline [number providers](https://minecraft.wiki/w/Number_provider).


## Installation

In a beet project, use `uv add bolt_compute` and add the module in the require phase in your beet config:

```yaml
require:
  - bolt
  - bolt_compute # <-- Add this line
pipeline:
  - mecha
```

## Usage

Any place where the `compute` command/subcommand is used, you can use the `bolt` subcommand to use an expression instead of a number provider. For example, instead of:

```mcfunction 
compute default {type:"minecraft:sum",operands:[1,1]}
data modify storage namespace:path path set compute default {type:"minecraft:sum",operands:[1,1]}
```
You can use:

```mcfunction
compute bolt (1 + 1)
data modify storage namespace:path path set compute bolt (1 + 1)
```

### Literals values

Bolt compute supports the following literal values:
```mcfunction
compute bolt (storage namespace:path path) # compute default {type:"minecraft:storage",storage:"namespace:path",path:"path"}

x = 1 # bolt variable assignment
compute bolt (x + 1) # compute default {type:"minecraft:sum",operands:[1,1]}

y = "namespace:path_to_number_provider"
compute bolt (y * y) # compute default {type:"minecraft:product",operands:["namespace:path_to_number_provider","namespace:path_to_number_provider"]}

```

### Operators

'+', '-', '*', are supported, as well as parentheses for grouping.

### Functions

Built-in functions are supported, such as : 
- `average` expect a list using square brackets, e.g. `average([1,2,3])`
- `binomial` expect N and P, can be expressions, e.g. `binomial(10, 0.5)`
- `conditional` currently not implemented
- `maximum` expect a list using square brackets, e.g. `maximum([1,2,3])`
- `minimum` expect a list using square brackets, e.g. `minimum([1,2,3])`
- `uniform` expect two number providers, can be expressions, e.g. `uniform(1, 10)`
- `sum` expect a list using square brackets, e.g. `sum([1,2,3])`
- `product` expect a list using square brackets, e.g. `product([1,2,3])`

### Multiline expressions

Expressions can be multiline, for example:

```mcfunction
x = 1
y = 2
compute bolt (
    x + y
)
```

### Full example

```mcfunction

x = "namespace:path_to_number_provider"
y = 256*256

data modify storage example:main result_bolt set compute bolt (
    (storage example:main prod1)*(storage example:main prod2)*(storage example:main prod3)*2
    *
    2485*52+
    maximum([0,1,(storage example:main prod2),1])+(143)-
    (y*x) + x
)
```

More examples can be found in the [examples](examples) folder.
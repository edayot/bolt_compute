# Bolt Compute

A [beet](https://github.com/mcbeet/beet) plugin that lets you write expressions instead of inline [number providers](https://minecraft.wiki/w/Number_provider) in the `compute` command.


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

Anywhere the `compute` command or subcommand is used, you can write an expression in parentheses instead of a number provider. For example, instead of:

```mcfunction
compute default float {type: "minecraft:add", inputs: [{type: "minecraft:storage", storage: "demo:main", path: "a"}, 1.0f]}
data modify storage demo:main result set compute default float {type: "minecraft:add", inputs: [{type: "minecraft:storage", storage: "demo:main", path: "a"}, 1.0f]}
```

You can write:

```mcfunction
compute default float (storage demo:main a + 1)
data modify storage demo:main result set compute default float (storage demo:main a + 1)
```

`compute entity <target>` and `compute block <pos>` work the same way:

```mcfunction
compute entity @s float (storage demo:main a + 1)
compute block ~ ~ ~ integer (score this my_objective * 2)
```

Expressions are compiled into vanilla number providers during mecha's transform step. The generated NBT is then validated against the game's schema in the check step, like any hand-written number provider, so mistakes are reported on the expression itself.

### The `bolt` subcommand

`compute bolt`, `compute bolt_entity <target>` and `compute bolt_block <pos>` always parse their argument as a bolt_compute expression:

```mcfunction
compute bolt float (storage demo:main a + 1)
compute bolt_entity @s float (storage demo:main a + 1)
compute bolt_block ~ ~ ~ integer (score this my_objective * 2)
```

They compile to `compute default`, `compute entity @s` and `compute block ~ ~ ~` respectively.

With the default `default_command: true` option, the vanilla argument is tried first. A parenthesized expression that is also valid Python, such as `(1 + 1)` or `(x * 2)`, is evaluated by bolt at compile time and inlined as a constant. Use the `bolt` subcommand when you need a bolt_compute expression in that case:

```mcfunction
x = 1
compute default float (x + 1)  # compute default float 2
compute bolt float (x + 1)     # compute default float {type: "minecraft:add", inputs: [1.0f, 1.0f]}
```

Set `default_command: false` to only enable expressions through the `bolt` subcommand:

```yaml
meta:
  bolt_compute:
    default_command: false
```

### Literal values

| Expression | Number provider |
| --- | --- |
| `1.5`, `3` | constant |
| `"demo:my_provider"` | reference to a number provider file |
| `storage demo:main path.to.value` | `minecraft:storage` |
| `score this my_objective` | `minecraft:score` on a context entity (`this`, `attacker`, `direct_attacker`, `attacking_player`, `target_entity`, `interacting_entity`) |
| `score fixed jeb_ my_objective` | `minecraft:score` on a fixed name or UUID |
| `x` | value of the bolt variable `x`: a number becomes a constant, a string becomes a reference |

```mcfunction
compute default float (storage demo:main path)
# compute default float {type: "minecraft:storage", storage: "demo:main", path: "path"}

compute default integer (score fixed jeb_ my_objective)
# compute default integer {type: "minecraft:score", target: {type: "fixed", name: "jeb_"}, score: "my_objective"}

y = "demo:my_provider"
compute bolt float (y * y)
# compute default float {type: "minecraft:mul", inputs: ["demo:my_provider", "demo:my_provider"]}
```

A score used in a `float` expression is wrapped in `minecraft:from_int`.

### Operators

| Operator | `float` | `integer` |
| --- | --- | --- |
| `+` | `add` | `add` |
| `-` | `sub` | `sub` |
| `*` | `mul` | `mul` |
| `/` | `div` | |
| `//` | | `div` |
| `%` | `mod` | `mod` |
| `**` | `pow` | `pow` |
| unary `-` | `negate` | `negate` |

Operator precedence follows Python, and parentheses can be used for grouping.

### Functions

Every vanilla number provider type can be called as a function. Arguments can be passed by position or by name, and can themselves be expressions:

```mcfunction
compute default float (uniform(0, 10))
compute default float (uniform(min=0, max=storage demo:main a))
compute default integer (binomial(10, 0.5))
compute default float (sin(storage demo:main angle))
```

Functions taking a list of inputs accept either a list or the inputs as separate arguments: `max([1, 2, storage demo:main a])` or `max(1, 2, storage demo:main a)`.

| Type | Functions |
| --- | --- |
| `float` | `abs`, `add`, `avg`, `ceil`, `conditional`, `constant`, `cos`, `div`, `enchantment_level`, `environment_attribute`, `floor`, `from_int`, `length`, `max`, `min`, `mod`, `mul`, `negate`, `number_dispatcher`, `pow`, `round`, `sin`, `sqrt`, `storage`, `sub`, `truncate`, `uniform`, `weighted_list` |
| `integer` | `abs`, `add`, `avg`, `binomial`, `conditional`, `constant`, `div`, `environment_attribute`, `floor_div`, `floor_mod`, `from_float`, `max`, `min`, `mod`, `mul`, `negate`, `number_dispatcher`, `pow`, `storage`, `sub`, `uniform`, `weighted_list` |

### Conditions

`on_true if condition else on_false` is equivalent to the `conditional` function. The condition is a predicate: either a predicate id, an inline predicate (26.3 format, with a `type` key), or a list of inline predicates that must all pass.

```mcfunction
compute default float (1 if demo:my_predicate else 0)
compute default float (conditional(demo:my_predicate, 1, 0))

compute default float (
    220210 if {type: "minecraft:random_chance", chance: 0.5} else 23
#    ^        ^                                                ^
#    |        |                                                |
#  on_true    |                                             on_false
#         condition
)
```

Inline predicates are validated in mecha's check step. A predicate id is only checked to be a string.

### Multiline expressions

Expressions can span several lines:

```mcfunction
compute default float (
    storage demo:main a
    + storage demo:main b
)
```

### Full example

```mcfunction
x = "demo:my_provider"
y = 256*256

data modify storage demo:main result set compute bolt float (
    (storage demo:main prod1)*(storage demo:main prod2)*(storage demo:main prod3)*2
    *
    2485*52+
    max([0,1,(storage demo:main prod2),1])+(143)-
    (y*x) + x
)
```

More examples can be found in the [examples](examples) folder.

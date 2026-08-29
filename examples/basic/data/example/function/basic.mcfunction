

data modify storage example:main prod1 set value 2
data modify storage example:main prod2 set value 4



data modify storage example:main result set compute default {
    "type": "minecraft:product",
    "operands": [
        {
            "type": f"minecraft:storage",
            "storage": "example:main",
            "path": "prod1"
        },
        {
            "type": "minecraft:storage",
            "storage": "example:main",
            "path": "prod2"
        }
    ]
}

# dataa = "coucoi"

data modify storage example:main result_bolt set compute bolt (1)
data modify storage example:main result_bolt set compute bolt (4+7*2+8)
data modify storage example:main result_bolt set compute bolt (1+1+1)
data modify storage example:main result_bolt set compute bolt (21-78)
data modify storage example:main result_bolt set compute bolt (21*78)

x = 1.25

data modify storage example:main result_bolt set compute bolt (x)
data modify storage example:main result_bolt set compute bolt (x*x)

y = "eee:aaaaaa"
data modify storage example:main result_bolt set compute bolt (y)

for z in range(15):
    data modify storage example:main result_bolt set compute bolt (f"minecraft:{z}")


data modify storage example:main result_bolt set compute bolt (maximum([1]))
data modify storage example:main result_bolt set compute bolt (maximum([1,2,3,4,5,6]))

data modify storage example:main result_bolt set compute bolt (sum([1]))
data modify storage example:main result_bolt set compute bolt (sum([1,2,3,4,5,6]))

data modify storage example:main result_bolt set compute bolt (sum(["1"]))
data modify storage example:main result_bolt set compute bolt (sum(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt (average(["1"]))
data modify storage example:main result_bolt set compute bolt (average(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt (binomial(5, 2,))
data modify storage example:main result_bolt set compute bolt (uniform(5, 2,))

data modify storage example:main result_bolt set compute bolt ("aaa:bbb")
data modify storage example:main result_bolt set compute bolt ("aaa:bbb" + "ccc:ddd")
data modify storage example:main result_bolt set compute bolt ("aaa:bbb" * "ccc:ddd")

data modify storage example:main result_bolt set compute bolt ((storage f"example:{'main'}" f"prod{1}")*(storage example:main prod2))
data modify storage example:main result_bolt set compute bolt (2*(storage example:main prod1)*(storage example:main prod2)+1)

x = 25
y = 85
data modify storage example:main result_bolt set compute bolt (x*y)



data modify storage example:main result_bolt set compute bolt (
    (storage example:main prod1)*(storage example:main prod2)*2
)


data modify storage example:main result_bolt set compute bolt (
    (storage example:main prod1)*(storage example:main prod2)*(storage example:main prod3)*2
    *
    2485*52+
    maximum([0,1,(storage example:main prod2),1])+(143)
)

data modify storage example:main result_bolt set compute bolt (
    (storage example:main prod1)*2
)


data modify storage example:main result_bolt set compute bolt ("aaa:bbb")
data modify storage example:main result_bolt set compute bolt ("aaa:bbb" + "ccc:ddd")
data modify storage example:main result_bolt set compute bolt (1)
data modify storage example:main result_bolt set compute bolt (1+1)


compute bolt (1+1)

compute bolt (conditional({
    "type": "minecraft:value_check",
    "value": {
        "type": "minecraft:uniform",
        "min": 0,
        "max": 1
    },
    "range": 0
}, 1, 0))

compute bolt (
    1 if {
        "type": "minecraft:value_check",
        "value": {
            "type": "minecraft:uniform",
            "min": 0,
            "max": 1
        },
        "range": 0
    } else 0
)

compute bolt (
    220210 if {} else 23
#    ^        ^       ^
#    |        |       |
#  on_true    |       on_false
#         condition
)

scoreboard players set @s dummy 1
compute bolt (
    (score this minecraft.dummy)
)
compute bolt (
    (score this minecraft.dummy 42)
)

my_score = "minecarft.dummy"
my_thing = "attacker"

compute bolt (
    (score my_thing my_score)
)
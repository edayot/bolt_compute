

data modify storage example:main prod1 set value 2
data modify storage example:main prod2 set value 4



data modify storage example:main result set compute default float {
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

data modify storage example:main result_bolt set compute bolt float (1)
data modify storage example:main result_bolt set compute bolt float (4+7*2+8)
data modify storage example:main result_bolt set compute bolt float (1+1+1)
data modify storage example:main result_bolt set compute bolt float (21-78)
data modify storage example:main result_bolt set compute bolt float (21*78)

x = 1.25

data modify storage example:main result_bolt set compute bolt float (x)
data modify storage example:main result_bolt set compute bolt float (x*x)

y = "eee:aaaaaa"
data modify storage example:main result_bolt set compute bolt float (y)

for z in range(15):
    data modify storage example:main result_bolt set compute bolt float (f"minecraft:{z}")


data modify storage example:main result_bolt set compute bolt float (maximum([1]))
data modify storage example:main result_bolt set compute bolt float (maximum([1,2,3,4,5,6]))

data modify storage example:main result_bolt set compute bolt float (sum([1]))
data modify storage example:main result_bolt set compute bolt float (sum([1,2,3,4,5,6]))

data modify storage example:main result_bolt set compute bolt float (sum(["1"]))
data modify storage example:main result_bolt set compute bolt float (sum(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt float (average(["1"]))
data modify storage example:main result_bolt set compute bolt float (average(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt float (binomial(5, 2,))
data modify storage example:main result_bolt set compute bolt float (uniform(5, 2,))

data modify storage example:main result_bolt set compute bolt float ("aaa:bbb")
data modify storage example:main result_bolt set compute bolt float ("aaa:bbb" + "ccc:ddd")
data modify storage example:main result_bolt set compute bolt float ("aaa:bbb" * "ccc:ddd")

data modify storage example:main result_bolt set compute bolt float ((storage f"example:{'main'}" f"prod{1}")*(storage example:main prod2))
data modify storage example:main result_bolt set compute bolt float (2*(storage example:main prod1)*(storage example:main prod2)+1)

x = 25
y = 85
data modify storage example:main result_bolt set compute bolt float (x*y)



data modify storage example:main result_bolt set compute bolt float (
    (storage example:main prod1)*(storage example:main prod2)*2
)


data modify storage example:main result_bolt set compute bolt float (
    (storage example:main prod1)*(storage example:main prod2)*(storage example:main prod3)*2
    *
    2485*52+
    maximum([0,1,(storage example:main prod2),1])+(143)
)

data modify storage example:main result_bolt set compute bolt float (
    (storage example:main prod1)*2
)


data modify storage example:main result_bolt set compute bolt float ("aaa:bbb")
data modify storage example:main result_bolt set compute bolt float ("aaa:bbb" + "ccc:ddd")
data modify storage example:main result_bolt set compute bolt float (1)
data modify storage example:main result_bolt set compute bolt float (1+1)


compute bolt float (1+1)

compute bolt float (conditional({
    "type": "minecraft:value_check",
    "value": {
        "type": "minecraft:uniform",
        "min": 0,
        "max": 1
    },
    "range": 0
}, 1, 0))

compute bolt float (
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

compute bolt float (
    220210 if {} else 23
#    ^        ^       ^
#    |        |       |
#  on_true    |       on_false
#         condition
)

scoreboard players set @s dummy 1
# this = "aaa"
compute bolt float (
    (score this minecraft.dummy)
)
compute bolt float (
    (score this minecraft.dummy 42)
)

my_score = "minecarft.dummy"
my_thing = "attacker"

compute bolt float (
    (score my_thing my_score)
)
compute bolt float (
    (score fixed my_thing my_score)
)


compute bolt float (
    (score fixed jeb_ my_score)
)

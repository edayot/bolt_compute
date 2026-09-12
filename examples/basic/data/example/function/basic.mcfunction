

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

data modify storage example:main result_bolt set compute bolt float 143.221
data modify storage example:main result_bolt set compute bolt float (4+7*2+2)
data modify storage example:main result_bolt set compute bolt float (1+1+1)
data modify storage example:main result_bolt set compute bolt float (21-78)
data modify storage example:main result_bolt set compute bolt float (21*78)

x = 1.25

data modify storage example:main result_bolt set compute bolt float x
data modify storage example:main result_bolt set compute bolt float x*x

y = "eee:aaaaaa"
data modify storage example:main result_bolt set compute bolt float (y)

for z in range(15):
    data modify storage example:main result_bolt set compute bolt float (f"minecraft:{z}")


data modify storage example:main result_bolt set compute bolt float -(21*78)


data modify storage example:main result_bolt set compute bolt float (sin(input=1))
data modify storage example:main result_bolt set compute bolt float (sin(1))
data modify storage example:main result_bolt set compute bolt float (max(inputs=[1,2,3,4,5,6]))
data modify storage example:main result_bolt set compute bolt float (max([1,2,3,4,5,6]))
data modify storage example:main result_bolt set compute bolt float (max(1,2,3,4,5,6))

data modify storage example:main result_bolt set compute bolt float (add([1]))
data modify storage example:main result_bolt set compute bolt float (add([1,2,3,4,5,6]))

data modify storage example:main result_bolt set compute bolt float (add(["1"]))
data modify storage example:main result_bolt set compute bolt float (add(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt float (avg(["1"]))
data modify storage example:main result_bolt set compute bolt float (avg(["1","2","3","4","5","6"]))


data modify storage example:main result_bolt set compute bolt integer (binomial(n=5, p=2,))
data modify storage example:main result_bolt set compute bolt integer (binomial(5, 2))
data modify storage example:main result_bolt set compute bolt integer (uniform(5, 2,))

data modify storage example:main result_bolt set compute bolt float ("aaa:bbb")
data modify storage example:main result_bolt set compute bolt float ("aaa:bbb" + "ccc:ddd")
data modify storage example:main result_bolt set compute bolt float ("aaa:bbb" * "ccc:ddd")

x = "blblba"
data modify storage example:main result_bolt set compute bolt float (storage(example:main, a."a:b"))

data modify storage example:main result_bolt set compute bolt float ((storage f"example:{'main'}" f"prod{1}")*(storage example:main prod2))
data modify storage example:main result_bolt set compute bolt float (storage example:main prod1)

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
    max([0,1,(storage example:main prod2),1])+(143)
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
    (score fixed this minecraft.dummy)
)
compute bolt float (
    (score context this minecraft.dummy)
)

compute bolt integer (
    (score this minecraft.dummy)
)
compute bolt integer (
    (score fixed this minecraft.dummy)
)
compute bolt integer (
    (score context this minecraft.dummy)
)


compute bolt integer from_float(43/7)
compute bolt float from_int(43//7)


compute bolt float (
    (score this this)
)
compute bolt float (
    (score fixed this this)
)
compute bolt float (
    (score context this this)
)

compute bolt integer (
    (score this this)
)
compute bolt integer (
    (score fixed this this)
)
compute bolt integer (
    (score context this this)
)
compute bolt integer (
    (score context this this 15)
)

compute bolt integer (
    (score context this this 15)
)

# arg1 = "fixed"
# arg2 = "this"
# arg3 = "score"
# arg4 = "minecraft:callback"

# compute bolt float (
#     score arg1 arg2 arg3 arg4
# )


# arg1 = "fixed"
# arg2 = "this"
# arg3 = "score"

# compute bolt float (
#     storage arg1 arg2 arg3
# )



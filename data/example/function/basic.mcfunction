

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

data modify storage example:main result_bolt set compute bolt 1

# data modify storage example:main result_bolt set compute bolt (
#     (storage example:main prod1)*(storage example:main prod2)
#     *max([0,1,(storage example:main prod2),1])+(143)

# )

compute bolt float (score "context" 'this' "average")


# showcase
compute default float (
    2*sin(storage namespace:test div) + max(score this namespace.data, score this namespace.money)
    
)

# calculate distance between two entities
execute on origin run data modify storage namespace:temp pos1 set from entity @s Pos
data modify storage namespace:temp pos2 set from entity @s Pos

data modify storage namespace:temp distance set compute default float (
    sqrt(
        (storage namespace:temp pos1[0] - storage namespace:temp pos2[0])**2 +
        (storage namespace:temp pos1[1] - storage namespace:temp pos2[1])**2 +
        (storage namespace:temp pos1[2] - storage namespace:temp pos2[2])**2
    )
)

# conditional
compute bolt float (
    220210 if {} else 23
#    ^        ^       ^
#    |        |       |
#  on_true    |       on_false
#         condition 
#        (predicate)
)




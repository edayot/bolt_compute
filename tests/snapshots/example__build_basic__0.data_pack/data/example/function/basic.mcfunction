data modify storage example:main prod1 set value 2
data modify storage example:main prod2 set value 4
data modify storage example:main result set compute default float {type: "minecraft:mul", inputs: [{type: "minecraft:storage", storage: "example:main", path: "prod1"}, {type: "minecraft:storage", storage: "example:main", path: "prod2"}]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:constant", value: 143.221f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [{type: "minecraft:add", inputs: [4.0f, {type: "minecraft:mul", inputs: [7.0f, 2.0f]}]}, 2.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [{type: "minecraft:add", inputs: [1.0f, 1.0f]}, 1.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:sub", left: 21.0f, right: 78.0f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [21.0f, 78.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:constant", value: 1.25f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [1.25f, 1.25f]}
data modify storage example:main result_bolt set compute default float eee:aaaaaa
data modify storage example:main result_bolt set compute default float minecraft:0
data modify storage example:main result_bolt set compute default float minecraft:1
data modify storage example:main result_bolt set compute default float minecraft:2
data modify storage example:main result_bolt set compute default float minecraft:3
data modify storage example:main result_bolt set compute default float minecraft:4
data modify storage example:main result_bolt set compute default float minecraft:5
data modify storage example:main result_bolt set compute default float minecraft:6
data modify storage example:main result_bolt set compute default float minecraft:7
data modify storage example:main result_bolt set compute default float minecraft:8
data modify storage example:main result_bolt set compute default float minecraft:9
data modify storage example:main result_bolt set compute default float minecraft:10
data modify storage example:main result_bolt set compute default float minecraft:11
data modify storage example:main result_bolt set compute default float minecraft:12
data modify storage example:main result_bolt set compute default float minecraft:13
data modify storage example:main result_bolt set compute default float minecraft:14
data modify storage example:main result_bolt set compute default float {type: "minecraft:negate", input: {type: "minecraft:mul", inputs: [21.0f, 78.0f]}}
data modify storage example:main result_bolt set compute default float {type: "minecraft:sin", input: 1.0f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:sin", input: 1.0f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:max", inputs: [1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:max", inputs: [1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:max", inputs: [1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [1.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: ["1"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: ["1", "2", "3", "4", "5", "6"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:avg", inputs: ["1"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:avg", inputs: ["1", "2", "3", "4", "5", "6"]}
data modify storage example:main result_bolt set compute default integer {type: "minecraft:binomial", n: 5, p: 2.0f}
data modify storage example:main result_bolt set compute default integer {type: "minecraft:binomial", n: 5, p: 2.0f}
data modify storage example:main result_bolt set compute default integer {type: "minecraft:uniform", min: 5, max: 2}
data modify storage example:main result_bolt set compute default float aaa:bbb
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: ["aaa:bbb", "ccc:ddd"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: ["aaa:bbb", "ccc:ddd"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:storage", storage: "example:main", path: 'a."a:b"'}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [{type: "minecraft:storage", storage: "example:main", path: "prod1"}, {type: "minecraft:storage", storage: "example:main", path: "prod2"}]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:storage", storage: "example:main", path: "prod1"}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [25.0f, 85.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:storage", storage: "example:main", path: "prod1"}, {type: "minecraft:storage", storage: "example:main", path: "prod2"}]}, 2.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [{type: "minecraft:add", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:mul", inputs: [{type: "minecraft:storage", storage: "example:main", path: "prod1"}, {type: "minecraft:storage", storage: "example:main", path: "prod2"}]}, {type: "minecraft:storage", storage: "example:main", path: "prod3"}]}, 2.0f]}, 2485.0f]}, 52.0f]}, {type: "minecraft:max", inputs: [0.0f, 1.0f, {type: "minecraft:storage", storage: "example:main", path: "prod2"}, 1.0f]}]}, 143.0f]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:mul", inputs: [{type: "minecraft:storage", storage: "example:main", path: "prod1"}, 2.0f]}
data modify storage example:main result_bolt set compute default float aaa:bbb
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: ["aaa:bbb", "ccc:ddd"]}
data modify storage example:main result_bolt set compute default float {type: "minecraft:constant", value: 1.0f}
data modify storage example:main result_bolt set compute default float {type: "minecraft:add", inputs: [1.0f, 1.0f]}
compute default float {type: "minecraft:add", inputs: [1.0f, 1.0f]}
compute default float {type: "minecraft:conditional", condition: {type: "minecraft:float_value_check", value: {type: "minecraft:uniform", min: 0, max: 1}, test: {min: 0.5d}}, on_true: 1.0f, on_false: 0.0f}
compute default float {type: "minecraft:conditional", condition: {type: "minecraft:float_value_check", value: {type: "minecraft:uniform", min: 0, max: 1}, test: {min: 0.5d}}, on_true: 1.0f, on_false: 0.0f}
compute default float {type: "minecraft:conditional", condition: {type: "minecraft:random_chance", chance: 0.5d}, on_true: 220210.0f, on_false: 23.0f}
scoreboard players set @s dummy 1
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "context", target: "this"}, score: "minecraft.dummy"}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "fixed", name: "this"}, score: "minecraft.dummy"}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "context", target: "this"}, score: "minecraft.dummy"}}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "minecraft.dummy"}
compute default integer {type: "minecraft:score", target: {type: "fixed", name: "this"}, score: "minecraft.dummy"}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "minecraft.dummy"}
compute default integer {type: "minecraft:from_float", input: {type: "minecraft:div", left: 43.0f, right: 7.0f}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:div", left: 43, right: 7}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "fixed", name: "this"}, score: "this"}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}
compute default integer {type: "minecraft:score", target: {type: "fixed", name: "this"}, score: "this"}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}
compute default integer {type: "minecraft:score", target: {type: "context", target: "this"}, score: "this"}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "fixed", name: "this"}, score: "score"}}
compute default float {type: "minecraft:from_int", input: {type: "minecraft:score", target: {type: "fixed", name: "jeb_"}, score: "my_scoreeee"}}
compute default float 2

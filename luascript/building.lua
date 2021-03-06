-- this file is generated by program!
-- never modify it!!!
-- source file: building.csv

local building = {}

building.house = {
    use_money = 1000,
    use_food = 123,
    is_init = true,
    defense = 100,
}

building.house[1] = {
    use_money = 1000,
    use_food = 123,
    is_init = true,
    defense = 100,
}

building.house[2] = {
    use_money = 123,
    defense = 120,
}

building.house[3] = {
    use_money = 456,
    defense = 130,
}

building.farm = {
    use_money = 100,
    use_food = 234,
    is_init = false,
    defense = 200,
}

building.farm[1] = {
    use_money = 100,
    use_food = 234,
    is_init = false,
    defense = 200,
}

building.farm[2] = {
    use_money = 200,
}

building.farm[3] = {
    use_money = 200,
}

building.farm[4] = {
}

building.all_type = {}
local all_type = building.all_type
all_type[1] = house
all_type[2] = farm

for i = 1, #(building.all_type) do
    local item = building.all_type[i]
    for j = 1, #item do
        item[j].__index = item[j]
        if j < #item then
            setmetatable(item[j+1], item[j])
        end
    end
end


return building
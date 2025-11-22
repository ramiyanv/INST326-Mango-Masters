# Potion ingredient sets
polyjuice = {
    "lacewing flies", "leeches", "powdered bicorn horn",
    "knotgrass", "fluxweed", "boomslang skin", "ashwinder egg"
}

felix_felicis = {
    "ashwinder egg", "squill bulb", "mallowroot",
    "billywig sting slime", "occamy eggshell", "moonstone"
}

amortentia = {
    "rose thorns", "peppermint", "unicorn hair",
    "ashwinder egg", "moonstone", "pearlescent powder"
}

print("Polyjuice Potion:", sorted(polyjuice))
print("Felix Felicis:", sorted(felix_felicis))
print("Amortentia:", sorted(amortentia))

# Union of all ingredients
all_ingredients = polyjuice | felix_felicis | amortentia
print("\nAll unique ingredients:", sorted(all_ingredients))
print("Total unique ingredients:", len(all_ingredients))

print("\nShared by Polyjuice and Felix Felicis:", sorted(polyjuice & felix_felicis))
print("Shared by Polyjuice and Amortentia:", sorted(polyjuice & amortentia))
print("Shared by Felix Felicis and Amortentia:", sorted(felix_felicis & amortentia))
print("Shared by all three:", sorted(polyjuice & felix_felicis & amortentia))

print("\nUnique to Polyjuice:", sorted(polyjuice - (felix_felicis | amortentia)))
print("Unique to Felix Felicis:", sorted(felix_felicis - (polyjuice | amortentia)))
print("Unique to Amortentia:", sorted(amortentia - (polyjuice | felix_felicis)))

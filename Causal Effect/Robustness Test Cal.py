normal = 0.005316497001771836
random = 0.005137705532575421
placebo = -0.00020867160291763832
subset = 0.005381174247262295
difference_random = random - normal
difference_random = round(difference_random, 4)
percent_random = difference_random / normal
percent_random = round(percent_random * 100, 2)
str_print = ""
str_print += str(difference_random)
if percent_random > 0:
    str_print += str("(" + str(percent_random) + "%↑)")
else:
    str_print += str("(" + str(-percent_random) + "%↓)")
print(str_print)
placebo = round(placebo, 4)
print(placebo)

difference_subset = subset - normal
difference_subset = round(difference_subset, 4)
percent_subset = difference_subset / normal
percent_subset = round(percent_subset * 100, 2)
str_print = ""
str_print += str(difference_subset)
if percent_subset > 0:
    str_print += str("(" + str(percent_subset) + "%↑)")
else:
    str_print += str("(" + str(-percent_subset) + "%↓)")
print(str_print)
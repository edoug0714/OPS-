# OPS+

This repository contains a program to calculate OPS+ using raw statcast data. The actual data file cannot be included here because it is too large, but the program functions by compiling each player's OPS using each individual plate appearance, then finding each ballpark's 'park factor'.
MLB uses total runs scores for their park factor statistic, but I decided to use park OPS instead since it is more accurate. After calculating park factor, each player's OPS is multiplied by some factor depending on how many plate appearances they had in each stadium. Finally, the data is 
normalized where 100 is league average.

Note: This is a program I wrote while learning python and data analysis libraries, so it is not very efficient

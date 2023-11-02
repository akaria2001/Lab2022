#!/bin/bash

# Initialize an array and a sum variable
array=()
sum=0

# Read lines from stdin into array
while IFS= read -r line
do
    array+=("$line")
done

# Iterate over the array
for i in "${array[@]}"
do
    # Use regex to check if the array element is a number
    if [[ $i =~ ^[+-]?[0-9]+([.][0-9]+)?$ ]]
    then
        # If it is, add it to the sum
        sum=$(echo "$sum + $i" | bc)
    fi
done

# Print the sum
echo "The sum of the numeric values is: $sum"

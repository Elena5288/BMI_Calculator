# BMI_Calculator
# This is a BMI Calculator that calculates the BMI value, places the user in a category and shows a chart for the user to see to which category it belongs to.
The user can switch between imperial and metric units when entering the data.
The program returns an error if the height and weight are blanks or not numbers and prompts the user with an error message.
The inputs are stored in a csv file (BMI_records) if the user chooses to save them and prompts a message. After the save the data filled in (in the BMI Calculator frame) is deleted.
The text in the BMI results frame changes color according to the BMI category the user is placed on: underweight - blue, normal weight - green, overweight - yellow and obese - red.
In the BMI Chart frame we can see the BMI distribution chart, which is based on the historical data from the BMI_records file. 
If the user wants to see its placement then pressing the "See your chart placement" will update the chart while highlighing the placement category.

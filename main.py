import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Read the cleaned data
data = pd.read_csv("/Users/surajsatheesh/MCA/First Semester/Data Mining/Rainfall Predicition Project/austin_cleaned_dataset.csv")

X = data.drop(['PrecipitationSumInches'], axis=1)
Y = data['PrecipitationSumInches']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# Create and fit the linear regression model
clf = LinearRegression()
clf.fit(X_train, y_train)
# Lists to store predictions and day numbers
predictions = []
days = []

# Create a function to predict precipitation for the given day and display scatter plot
def predict_precipitation():
    try:
        day_value = int(day_input.get())
        if 0 <= day_value < len(X):
            input_values = X.iloc[[day_value]]
            precipitation_prediction = clf.predict(input_values)

            result_label.config(text=f'Predicted Precipitation for Day {day_value}: {precipitation_prediction[0]:.2f} inches')

            # Append predictions and day number to lists
            predictions.append(precipitation_prediction[0])
            days.append(day_value)

            # Display scatter plot for PrecipitationSumInches
            plt.scatter(range(len(Y)), Y, color='green', label='Actual Precipitation')
            plt.scatter(day_value, Y[day_value], color='red', label='Actual for Selected Day')
            plt.title('Precipitation level')
            plt.xlabel('Days')
            plt.ylabel('Precipitation in inches')
            plt.legend()
            plt.show()

            # Plot scatter graphs for selected attributes vs PrecipitationSumInches
            selected_attributes = ['TempAvgF', 'DewPointAvgF', 'HumidityAvgPercent',
                                    'SeaLevelPressureAvgInches', 'VisibilityAvgMiles',
                                    'WindAvgMPH']

            fig, axs = plt.subplots(3, 2, figsize=(10, 8))
            fig.suptitle('Precipitation Vs Selected Attributes Graph')

            for i, ax in enumerate(axs.flatten()):
                attribute_values = X[selected_attributes[i]]
                ax.scatter(attribute_values, Y, color='green', label='Actual Precipitation')
                ax.scatter(attribute_values[day_value], Y[day_value], color='red', label='Actual for Selected Day')
                ax.set_title(selected_attributes[i])
                ax.set_xlabel(selected_attributes[i])
                ax.set_ylabel('Precipitation in inches')
                ax.legend()

            plt.show()

        else:
            result_label.config(text=f'Invalid day value. Please enter a value between 0 and {len(X) - 1}.')
    except ValueError:
        result_label.config(text='Invalid input. Please enter a valid integer for the day.')

# Create the main window
root = tk.Tk()
root.title("Precipitation Prediction")

# Create input label and entry widget for day
label = ttk.Label(root, text="Enter Day for rainfall prediction")
label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
day_input = ttk.Entry(root)
day_input.grid(column=1, row=0, padx=10, pady=5)

# Create a button to trigger the prediction
predict_button = ttk.Button(root, text="Predict Precipitation", command=predict_precipitation)
predict_button.grid(column=0, row=1, columnspan=2, pady=10)

# Create a label to display the prediction result
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=2, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()

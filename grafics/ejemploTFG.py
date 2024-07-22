import pandas as pd
import numpy as np
import time

# Datos de consumo y generación dados
E = np.array([[1, 0.5, 0], [0, 0.5, 1]])
total_e = np.array([1, 1, 1])
consumption = np.array([1.5, 1.5])

def optimization_method2(E, total_e, consumption, max_iterations, p):
    n_rows, n_cols = E.shape
    nUser = n_rows

    # Initialize coefficients matrix
    coefficients_df = pd.DataFrame(np.zeros((nUser, n_cols)), columns=[f'c{j}' for j in range(1, n_cols + 1)])

    for j in range(n_cols):  # iterate over each column

        max_coef = E[:, j] / total_e[j]  # Calculate maximum coefficients
        max_coef[max_coef > 1] = 1  # Limit coefficients to 1 if they exceed 1

        sum = 0
        
        temporary_consumptions = np.sum((total_e * coefficients_df), axis=1)
        indices = np.argsort(temporary_consumptions)  # sort consumptions from lowest to highest
        for i in indices:
            if sum + max_coef[i] > 1:
                coefficients_df.iloc[i, j] = 1 - sum
                break
            else:
                coefficients_df.iloc[i, j] = max_coef[i]
                sum += max_coef[i]

    # Inicio del print
    print("------PRE-CORRECTION RESULTS------")
    for i in range(nUser):  
        current_sum = np.sum((total_e * coefficients_df.iloc[i, :]))
        deviation = abs(consumption[i] - current_sum)
        print(f"User {i}: generated {current_sum:.2f}, deviation {deviation:.2f} kWh, deviation {deviation/consumption[i]*100:.2f}%")

    # CORRECTION PHASE
    exceed = False
    l = 1
    for h in range(max_iterations):
        error = np.zeros(nUser)
        print(f"Iteration {h}")
        for i in range(nUser):
            error[i] = np.sum((total_e * coefficients_df.iloc[i, :])) - consumption[i]
        print("Error:", error)

        if np.all(error == 0) or np.all(error < 0) or np.all(error > 0):
            print("It is not possible to correct the coefficients")
            break

        indices = np.argsort(error)  # Sort errors from lowest to highest

        u2 = indices[0]
        u1 = indices[nUser - 1]

        diff = error[u2] - error[u1]
        print(f"User {u1} and User {u2} have the highest and lowest errors, respectively")
        print(f"Error difference: {diff:.2f}")

        if exceed:
            l += p  # correction rate

        if abs(diff) < 1e-4:  # If the difference is insignificant, correction can be omitted
            print("The difference is insignificant")
            break

        correction_amount = (diff / n_cols) * (1/l)  # Correction amount
        print(f"Correction amount: {correction_amount:.2f}")

        # Apply correction and avoid exceeding the limits [0, 1]
        coef_u1_new = coefficients_df.iloc[u1, :] + correction_amount
        coef_u2_new = coefficients_df.iloc[u2, :] - correction_amount

        # Check if the coefficients of u1 exceed the limits [0, 1], and if so, do not update them
        if (coef_u1_new > 1).any() or (coef_u1_new < 0).any():
            exceed = True
            # Identify the indices of the columns where coefficients exceed the limits
            invalid_indices = np.where((coef_u1_new > 1) | (coef_u1_new < 0))[0]

            # Maintain the original coefficients for those indices using .iloc
            coef_u1_new.iloc[invalid_indices] = coefficients_df.iloc[u1, :].iloc[invalid_indices]
            coef_u2_new.iloc[invalid_indices] = coefficients_df.iloc[u2, :].iloc[invalid_indices]
        else:
            exceed = False

        # Update the coefficients
        coefficients_df.iloc[u1, :] = coef_u1_new
        coefficients_df.iloc[u2, :] = coef_u2_new


        if (h == max_iterations-1):
            print("Maximum number of iterations reached", h)

    # Print post-correction results
    print("------POST-CORRECTION RESULTS------")
    for i in range(nUser):
        current_sum = np.sum((total_e * coefficients_df.iloc[i, :]))
        deviation = abs(consumption[i] - current_sum)
        print(f"User {i}: generated {current_sum:.2f}, deviation {deviation:.2f} kWh, deviation {deviation/consumption[i]*100:.2f}%")

    # Save to CSV file
    coefficients_df.to_csv('coefficients/optimization2_custom.csv', index=False)
    return coefficients_df

# Ejecutar el método de optimización si se desea
optimization2 = True
if optimization2:
    start_time = time.time()

    c = optimization_method2(E, total_e, consumption, max_iterations=10, p=1)
    print(c)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time: {:.2f} seconds".format(execution_time))
else:
    print("Optimization 2 with the custom method has not been performed")

import visualization as v


#v.plot_analyse('data/GandA.csv', 0.001, [1, 2, "ACCEL_X [g]", "ACCEL_Y [g]"])

#v.plot_analyse('data/GandA.csv', 0.01, [4, 5, "GYRO_X [deg/s]", "GYRO_Y [deg/s]"])



#v.plot_analyse('data/GandA.csv', 0.001, [1, 2, "ACCEL_X", "ACCEL_Y"])

#v.plot_analyse('data/GandA.csv', 0.01, [4, 5, "GYRO_X", "GYRO_Y"])

#v.normal_chart_2_time('data/test2.csv', 2, 5,"ROLL", "ROLL*", [0,0,90, 0, "DEG", "ROLL, ROLL*"])
    

#v.normal_chart_2_time('data/test2.csv', 2, 5,"ROLL", "ROLL*+ BW * 1000", [1000,0,90, 0, "DEG", "ROLL, ROLL* + BW * 1000"])

#v.normal_chart_2_time('data/test2.csv', 1 ,4, "PITCH", "PITCH*", [0,-0.1,0.1, 0, "DEG", "PITCH, PITCH*"])

#v.normal_chart_1_time('data/test2.csv', 8, "E_ROLL%", [100,-2,2, 0, "BŁĄD WZGĘDNY[%]", "E_ROLL%"])


#v.normal_chart_XY('data/testout.csv', 0, 1, "dt(time)", ["time [s]", "dt[s]", 0.06, 0.22, "Zmiana kroku czasowego w czasie dt(time)"])

#v.normal_chart_XY('data/testout.csv', 0, 3, "PITCH", ["time [s]", "PITCH[deg]", -90, 90, "PITCH (time)"])

v.normal_chart_XY('data/testout.csv', 0, 4, "ROLL", ["time [s]", "ROLL[s]", 0, 190, "ROLL(time)"])

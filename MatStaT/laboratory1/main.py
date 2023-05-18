from SampleClass import Sample

Sample1 = Sample("./data.xlsx")

Sample1.print_moments()                 # выводим все прощитанные моменты
Sample1.draw_frequency_histogram()      # выводим частотную диаграмму
Sample1.draw_possibility_histogram()    # показываем вероятностную диаграмму
Sample1.draw_dot_graph()                # показывем точечную диаграмму
Sample1.draw_empirical_fun()            # показываем эмпирическую диаграмму

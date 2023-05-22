from SampleClass import Sample

Sample1 = Sample("./dataYX.xlsx")

Sample1.print_momnets()
Sample1.print_correlation()
Sample1.print_equation()
Sample1.print_det()
Sample1.predict(x=80, p=95)
Sample1.draw_dot_graph()

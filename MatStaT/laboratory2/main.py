from SampleClass import Sample

Sample1 = Sample("./16variant.xlsx")

Sample1.print_momenets()
Sample1.print_correlation()
Sample1.print_equation()
Sample1.print_det()
Sample1.print_factf(p=95)
print("a: {}, b: {}".format(Sample1.a, Sample1.b))
Sample1.predictf(x=116, p=95)

Sample1.draw_dot_graph()

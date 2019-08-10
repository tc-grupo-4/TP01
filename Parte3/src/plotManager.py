from LTSpice_RawRead import RawRead

ltr = RawRead('Draft2.raw')
for name in ltr.get_trace_names():
    print(name)
    for step in ltr.get_steps():
        tr = ltr.get_trace(name)
        print(name)
        print('step {:d} {}'.format(step, tr.get_wave(step)))

from schemdraw import logic
import schemdraw
from schemdraw import elements as elm

d = schemdraw.Drawing()

kwargs = {}
kwargs['pins'] = []
num_output_lines = 4
for i in range(1, num_output_lines + 1):
    kwargs['pins'].append(sd_elem.IcPin(name=f'out{i}', anchorname=f'output line {i}', side='right'))
for i in range(1, 2 ** num_output_lines + 1):
    kwargs['pins'].append(sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}', side='left'))
JK = elm.Ic(pins=[elm.IcPin(name='>', side='left'),
                  elm.IcPin(name='K', side='left'),
                  elm.IcPin(name='J', side='left'),
                  elm.IcPin(name='$\overline{Q}$', side='right', anchorname='QBAR'),
                  elm.IcPin(name='Q', pin='15', side='right')])

d.add(JK)

d.draw()

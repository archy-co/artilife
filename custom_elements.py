"""Contains custom created elements"""

from schemdraw.segments import Segment, SegmentText
import schemdraw.elements as sd_elem


# JK = sd_elements.Ic(pins=[sd_elements.IcPin(name='>', pin='1', side='left'),
#                           sd_elements.IcPin(name='K', pin='16', side='left'),
#                           sd_elements.IcPin(name='J', pin='4', side='left'),
#                           sd_elements.IcPin(name='$\overline{Q}$', pin='14',
#                                             side='right', anchorname='QBAR'),
#                           sd_elements.IcPin(name='Q', pin='15', side='right')],
#                     edgepadW=.5,  # Make it a bit wider
#                     pinspacing=1).label('HC7476', 'bottom', fontsize=12)

class Constant(sd_elem.Element):
    def __init__(self, *d, constant_value: bool = True, **kwargs):
        super().__init__(*d, **kwargs)

        clen = 0.5
        cheight = 0.9

        self.segments.append(Segment([(-clen / 2, -cheight / 2),
                                      (-clen / 2, cheight / 2),
                                      (clen / 2, cheight / 2),
                                      (clen / 2, -cheight / 2),
                                      (-clen / 2, -cheight / 2)]))
        self.segments.append(Segment([(clen / 2, 0),
                                      (clen / 2 + 0.2, 0)]))
        self.segments.append(SegmentText((0, 0),
                                         str(int(constant_value))))

        self.anchors['out'] = (clen / 2 + 0.2, 0)

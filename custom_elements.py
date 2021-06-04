"""Custom visual elements for schemdraw library"""

from schemdraw.segments import Segment, SegmentText, SegmentCircle
import schemdraw.elements as sd_elem
import math


class Constant(sd_elem.Element):
    """Element that holds one value all time"""

    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10,
                 **kwargs):
        super().__init__(*d, **kwargs)

        self.clen = 0.5
        self.cheight = 0.9

        self.segments.append(Segment([(-self.clen / 2, -self.cheight / 2),
                                      (-self.clen / 2, self.cheight / 2),
                                      (self.clen / 2, self.cheight / 2),
                                      (self.clen / 2, -self.cheight / 2),
                                      (-self.clen / 2, -self.cheight / 2)]))

        self.segments.append(Segment([(self.clen / 2, 0),
                                      (self.clen / 2 + 0.2, 0)]))
        self.segments.append(SegmentText((0, 0),
                                         str(int(constant_value)),
                                         fontsize=lbl_size))

        self.anchors['out'] = (self.clen / 2 + 0.2, 0)
        self.anchors['center'] = (0, 0)


class Variable(Constant):
    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10,
                 **kwargs):
        super().__init__(*d, constant_value=constant_value, lbl_size=lbl_size,
                         **kwargs)

        self.segments.append(
            SegmentCircle((-self.clen / 6, self.cheight / 3), 0.01, fill=None))
        self.segments.append(
            SegmentCircle((self.clen / 6, self.cheight / 3), 0.01, fill=None))
        self.segments.append(Segment([(-self.clen / 6, self.cheight / 3),
                                      (self.clen / 6,
                                       self.cheight / 3 + self.cheight / 12)]))


class Not(sd_elem.Element):
    ''' Not gate/inverter

        Anchors:
            in
            out
    '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)

        gap = (math.nan, math.nan)
        leadlen = .35
        finlen = .15
        gateh = 1.
        gatel = .65
        notbubble = .12

        self.segments.append(Segment([(0, 0), (leadlen, 0), gap,
                                      (gatel+leadlen+notbubble*2, 0)]))
        self.segments.append(Segment([(gatel+leadlen+notbubble*2, 0),
                                      (gatel+leadlen*2, 0)]))
        self.segments.append(Segment([(leadlen, 0), (leadlen, -gateh/2),
                                      (gatel+leadlen, 0), (leadlen, gateh/2),
                                      (leadlen, 0)]))
        self.segments.append(SegmentCircle((gatel+leadlen+notbubble, 0), notbubble))
        self.anchors['out'] = (gatel+leadlen*2, 0)
        self.anchors['in'] = (0, 0)